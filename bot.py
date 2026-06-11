import os
import sys
import time
import asyncio
import logging

import requests
import yfinance as yf
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get('TELEGRAM_TOKEN')

PORTFOLIO = ['GOOGL', 'META', 'CIBR', 'JEPI', 'ANET', 'IRM', 'ORCL', 'IONQ', 'IBM']
WATCHLIST = ['RKLB', 'ASTS', 'LUNR', 'TDY', 'BWXT', 'VRT', 'BE', 'FSLR']

# 아래 일정 데이터는 수동 관리 — 주기적으로 갱신 필요
EARNINGS = {
    'GOOGL': '2025-07-29', 'META': '2025-07-30',
    'ORCL': '2025-06-10', 'IBM': '2025-07-23',
    'ANET': '2025-07-29', 'IONQ': '2025-08-06',
}
MACRO_EVENTS = [
    ('FOMC', '2025-06-18'),
    ('CPI', '2025-06-11'),
    ('PCE', '2025-06-27'),
    ('고용지표', '2025-07-04'),
]
FED_RATE = '4.25~4.50%'

CRYPTO_API_URL = ('https://api.coingecko.com/api/v3/simple/price'
                  '?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true')
CRYPTO_CACHE_TTL = 60  # CoinGecko 무료 API rate limit 보호용 캐시 (초)
REQUEST_TIMEOUT = 10

_crypto_cache = {'ts': 0.0, 'msg': None}


def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📈 포트폴리오", callback_data='portfolio'),
         InlineKeyboardButton("👀 관심종목", callback_data='watchlist')],
        [InlineKeyboardButton("🚀 SPCX", callback_data='spcx'),
         InlineKeyboardButton("🪙 비트코인", callback_data='bitcoin')],
        [InlineKeyboardButton("🏦 경제지표", callback_data='macro'),
         InlineKeyboardButton("📊 어닝일정", callback_data='earnings')],
    ])


def back_keyboard():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 메뉴로", callback_data='menu')]])


MENU_TEXT = '📊 투자 모니터링 봇\n\n원하는 항목을 선택하세요:'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(MENU_TEXT, reply_markup=main_menu_keyboard())


def _fetch_price(ticker):
    info = yf.Ticker(ticker).fast_info
    return info.last_price, info.previous_close


async def get_price(ticker):
    """yfinance는 동기 라이브러리이므로 스레드로 빼서 이벤트 루프 블로킹을 방지한다."""
    try:
        price, prev = await asyncio.to_thread(_fetch_price, ticker)
        if price is None or not prev:
            return None, None
        return price, ((price - prev) / prev) * 100
    except Exception:
        logger.exception("가격 조회 실패: %s", ticker)
        return None, None


async def get_prices(tickers):
    results = await asyncio.gather(*(get_price(t) for t in tickers))
    return list(zip(tickers, results))


def format_price_lines(prices):
    lines = []
    for ticker, (price, change) in prices:
        if price is None:
            lines.append(f"⚪ *{ticker}*: 데이터 없음")
        else:
            emoji = "🟢" if change >= 0 else "🔴"
            lines.append(f"{emoji} *{ticker}*: ${price:,.2f} ({change:+.2f}%)")
    return "\n".join(lines)


def _fetch_crypto():
    res = requests.get(CRYPTO_API_URL, timeout=REQUEST_TIMEOUT)
    res.raise_for_status()
    return res.json()


async def get_crypto_message():
    now = time.monotonic()
    if _crypto_cache['msg'] and now - _crypto_cache['ts'] < CRYPTO_CACHE_TTL:
        return _crypto_cache['msg']

    data = await asyncio.to_thread(_fetch_crypto)
    lines = ["🪙 *크립토 현황*", ""]
    for name, label in (('bitcoin', 'BTC'), ('ethereum', 'ETH')):
        coin = data[name]
        change = coin.get('usd_24h_change') or 0
        emoji = "🟢" if change >= 0 else "🔴"
        lines.append(f"{emoji} *{label}*: ${coin['usd']:,.0f} ({change:+.2f}%)")
    msg = "\n".join(lines)

    _crypto_cache['ts'] = now
    _crypto_cache['msg'] = msg
    return msg


async def safe_edit(query, text, reply_markup=None):
    try:
        await query.edit_message_text(text, parse_mode='Markdown', reply_markup=reply_markup)
    except BadRequest as e:
        # 같은 내용으로 다시 편집하면 텔레그램이 에러를 던지므로 무시
        if 'not modified' not in str(e).lower():
            raise


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == 'menu':
        await safe_edit(query, MENU_TEXT, reply_markup=main_menu_keyboard())
        return

    if data == 'portfolio':
        await safe_edit(query, "⏳ 조회 중...")
        prices = await get_prices(PORTFOLIO)
        msg = "💼 *포트폴리오 현황*\n\n" + format_price_lines(prices)

    elif data == 'watchlist':
        await safe_edit(query, "⏳ 조회 중...")
        prices = await get_prices(WATCHLIST)
        msg = "👀 *관심종목*\n\n" + format_price_lines(prices)

    elif data == 'spcx':
        await safe_edit(query, "⏳ 조회 중...")
        msg = "🚀 *SPCX 모니터링*\n\n"
        msg += "🎯 전략: 3분봉 FVG 스캘핑\n"
        msg += "📌 초기 1/3 하락 후 U자형 회복 예상\n\n"
        price, change = await get_price('SPCX')
        if price is not None:
            emoji = "🟢" if change >= 0 else "🔴"
            msg += f"{emoji} 현재가: ${price:,.2f} ({change:+.2f}%)"
        else:
            msg += "⏳ 데이터 없음"

    elif data == 'bitcoin':
        await safe_edit(query, "⏳ 조회 중...")
        try:
            msg = await get_crypto_message()
        except Exception:
            logger.exception("크립토 데이터 조회 실패")
            msg = "❌ 데이터를 불러올 수 없습니다"

    elif data == 'macro':
        msg = "🏦 *주요 경제지표 일정*\n\n"
        for name, date in MACRO_EVENTS:
            msg += f"📌 {name}: {date}\n"
        msg += f"\n💡 연준 금리 현황: {FED_RATE}"

    elif data == 'earnings':
        msg = "📊 *어닝 일정*\n\n"
        for ticker, date in EARNINGS.items():
            msg += f"📅 *{ticker}*: {date}\n"

    else:
        return

    await safe_edit(query, msg, reply_markup=back_keyboard())


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("업데이트 처리 중 예외 발생", exc_info=context.error)


def main():
    if not TOKEN:
        sys.exit("TELEGRAM_TOKEN 환경변수가 설정되지 않았습니다.")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_error_handler(error_handler)

    # run_polling은 내부에서 이벤트 루프를 직접 관리하는 블로킹 호출
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
