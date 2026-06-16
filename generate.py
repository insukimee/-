# -*- coding: utf-8 -*-
"""Static site generator for MarketInsight (US-market focus, KO + JA)."""
import os

SITE = "https://insukimee.github.io/-"

# ---------------------------------------------------------------- AdSense config
# TODO(owner): replace with your real AdSense publisher ID (keep the "ca-" prefix).
ADSENSE_CLIENT = "ca-pub-4253549478648317"
# TODO(owner): after approval, create ad units and paste their slot IDs here.
AD_SLOT_DISPLAY = "1234567890"      # responsive display unit (lists, page bottom)
AD_SLOT_INARTICLE = "0987654321"    # in-article fluid unit (inside posts)
AD_LABEL = {"ko": "광고", "ja": "広告"}

# ---------------------------------------------------------------- nav config
NAV = {
    "ko": [
        ("index.html", "🏠", "홈"),
        ("stock-analysis.html", "📊", "종목분석"),
        ("economy-trends.html", "🌍", "미국경제"),
        ("__divider__", "", ""),
        ("about.html", "👤", "소개"),
        ("contact.html", "📧", "문의"),
    ],
    "ja": [
        ("index.html", "🏠", "ホーム"),
        ("stock-analysis.html", "📊", "銘柄分析"),
        ("economy-trends.html", "🌍", "米国経済"),
        ("__divider__", "", ""),
        ("about.html", "👤", "サイト紹介"),
        ("contact.html", "📧", "お問い合わせ"),
    ],
}
LOGO = {"ko": "마켓인사이트", "ja": "マーケットインサイト"}
LANG_SWITCH = {"ko": ("🌐 JP", "日本語に切り替え"), "ja": ("🌐 KR", "한국어로 전환")}
OTHER = {"ko": "ja", "ja": "ko"}
HAMBURGER_LABEL = {"ko": "메뉴 열기", "ja": "メニューを開く"}
BODY_CLASS = {"ko": "", "ja": " class=\"lang-ja\""}

FOOTER = {
    "ko": {
        "cat": "카테고리",
        "links1": [("stock-analysis.html", "종목분석"), ("economy-trends.html", "미국경제")],
        "info": "정보",
        "links2": [("about.html", "소개"), ("contact.html", "문의"),
                   ("privacy-policy.html", "개인정보처리방침"), ("terms.html", "이용약관")],
        "copy": "© 2026 마켓인사이트. All rights reserved.",
        "disc": "본 사이트의 정보는 투자 권유가 아니며, 투자 결정에 대한 책임은 투자자 본인에게 있습니다.",
    },
    "ja": {
        "cat": "カテゴリー",
        "links1": [("stock-analysis.html", "銘柄分析"), ("economy-trends.html", "米国経済")],
        "info": "情報",
        "links2": [("about.html", "サイト紹介"), ("contact.html", "お問い合わせ"),
                   ("privacy-policy.html", "プライバシーポリシー"), ("terms.html", "利用規約")],
        "copy": "© 2026 マーケットインサイト. All rights reserved.",
        "disc": "当サイトの情報は投資勧誘ではありません。投資判断の最終決定はご自身の責任で行ってください。",
    },
}
COOKIE = {
    "ko": ("이 사이트는 서비스 개선 및 맞춤형 광고 제공을 위해 쿠키를 사용합니다. 계속 이용하시면 쿠키 사용에 동의하는 것으로 간주됩니다.",
           "동의", "자세히"),
    "ja": ("当サイトでは、サービス向上とパーソナライズ広告のためにCookieを使用しています。ご利用を続けることで、Cookie使用に同意したとみなされます。",
           "同意する", "詳細"),
}
TAG = {"ko": "종목분석", "ja": "銘柄分析"}
BACK = {"ko": "← 종목분석 목록으로", "ja": "← 銘柄分析一覧へ"}
META_BY = {"ko": "작성자: 마켓인사이트 리서치팀", "ja": "作成者: マーケットインサイト・リサーチチーム"}
SECTION_TITLES = {
    "ko": ["사업 개요", "핵심 투자 포인트", "리스크 요인", "종합 평가"],
    "ja": ["事業概要", "主要な投資ポイント", "リスク要因", "総合評価"],
}
SECTORS = {
    "semi": ("반도체", "半導体"),
    "ai": ("AI·소프트웨어", "AI・ソフトウェア"),
    "infra": ("IT인프라·하드웨어", "ITインフラ・ハードウェア"),
    "cyber": ("사이버보안", "サイバーセキュリティ"),
    "space": ("우주·방산", "宇宙・防衛"),
    "energy": ("클린에너지·전력", "クリーンエネルギー・電力"),
    "ev": ("전기차", "EV"),
    "fintech": ("핀테크", "フィンテック"),
    "gaming": ("게임", "ゲーム"),
}
SECTOR_ORDER = ["semi", "ai", "infra", "cyber", "space", "energy", "ev", "fintech", "gaming"]

# TradingView symbols (exchange-qualified for reliable resolution).
TV_SYMBOL = {
    "NVDA": "NASDAQ:NVDA", "TSM": "NYSE:TSM", "GOOGL": "NASDAQ:GOOGL",
    "AAPL": "NASDAQ:AAPL", "AMZN": "NASDAQ:AMZN", "ORCL": "NYSE:ORCL",
    "PLTR": "NASDAQ:PLTR", "IONQ": "NYSE:IONQ", "IBM": "NYSE:IBM",
    "CSCO": "NASDAQ:CSCO", "DELL": "NYSE:DELL", "CIBR": "NASDAQ:CIBR",
    "SPCX": "SPCX", "RDW": "NYSE:RDW", "BWXT": "NYSE:BWXT", "TDY": "NYSE:TDY",
    "MOG.A": "NYSE:MOG.A", "FSLR": "NASDAQ:FSLR", "BE": "NYSE:BE",
    "VRT": "NYSE:VRT", "TSLA": "NASDAQ:TSLA", "HOOD": "NASDAQ:HOOD",
    "TTWO": "NASDAQ:TTWO",
}
TV_LOCALE = {"ko": "kr", "ja": "ja"}


def tv(sym):
    return TV_SYMBOL.get(sym, sym)


def tv_widgets(tvsym, locale):
    """Symbol info (price/change) + advanced chart for a ticker page."""
    return f"""        <div class="tv-block">
          <div class="tradingview-widget-container">
            <div class="tradingview-widget-container__widget"></div>
            <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-symbol-info.js" async>
            {{"symbol": "{tvsym}", "width": "100%", "locale": "{locale}", "colorTheme": "dark", "isTransparent": true}}
            </script>
          </div>
          <div class="tradingview-widget-container tv-chart">
            <div class="tradingview-widget-container__widget"></div>
            <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
            {{"symbol": "{tvsym}", "width": "100%", "height": 380, "locale": "{locale}", "colorTheme": "dark", "theme": "dark", "style": "1", "interval": "D", "hide_side_toolbar": true, "allow_symbol_change": false, "save_image": false}}
            </script>
          </div>
        </div>"""


def tv_tape(locale):
    """Scrolling live price strip with all tickers, for hub/home top."""
    syms = ", ".join(
        '{"proName": "%s", "title": "%s"}' % (tv(t["sym"]), t["sym"]) for t in TICKERS
    )
    return f"""    <div class="tradingview-widget-container tv-tape">
      <div class="tradingview-widget-container__widget"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
      {{"symbols": [{syms}], "showSymbolLogo": true, "colorTheme": "dark", "isTransparent": true, "displayMode": "adaptive", "locale": "{locale}"}}
      </script>
    </div>"""


def head(lang, title, desc, slug, other_slug):
    other = OTHER[lang]
    canonical = f"{SITE}/{lang}/{slug}"
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <meta name="google-adsense-account" content="{ADSENSE_CLIENT}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{LOGO[lang]}">
  <meta property="og:url" content="{canonical}">
  <link rel="canonical" href="{canonical}">
  <link rel="alternate" hreflang="{lang}" href="{slug}">
  <link rel="alternate" hreflang="{other}" href="../{other}/{other_slug}">
  <link rel="stylesheet" href="../css/style.css">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script>
</head>"""


def header_nav(lang, active, other_slug):
    sw_text, sw_aria = LANG_SWITCH[lang]
    other = OTHER[lang]
    items = ""
    for href, icon, label in NAV[lang]:
        if href == "__divider__":
            items += '    <div class="nav-divider"></div>\n'
            continue
        cls = ' class="active"' if href == active else ""
        items += f'    <a href="{href}"{cls}><span class="nav-icon">{icon}</span> {label}</a>\n'
    return f"""<body{BODY_CLASS[lang]}>
  <header class="header">
    <button class="hamburger" id="hamburger-btn" aria-label="{HAMBURGER_LABEL[lang]}">
      <span></span><span></span><span></span>
    </button>
    <a href="index.html" class="logo">{LOGO[lang]}</a>
    <a href="../{other}/{other_slug}" class="lang-switch" aria-label="{sw_aria}">{sw_text}</a>
  </header>
  <nav class="mobile-nav" id="mobile-nav">
{items}  </nav>
  <div class="nav-overlay" id="nav-overlay"></div>"""


def footer(lang):
    f = FOOTER[lang]
    l1 = "\n".join(f'        <a href="{h}">{t}</a>' for h, t in f["links1"])
    l2 = "\n".join(f'        <a href="{h}">{t}</a>' for h, t in f["links2"])
    ck_text, ck_accept, ck_learn = COOKIE[lang]
    return f"""  <footer class="footer">
    <div class="footer-links">
      <div class="footer-col">
        <h4>{f['cat']}</h4>
{l1}
      </div>
      <div class="footer-col">
        <h4>{f['info']}</h4>
{l2}
      </div>
    </div>
    <div class="footer-bottom">
      <p>{f['copy']}</p>
      <p class="disclaimer">{f['disc']}</p>
    </div>
  </footer>
  <div class="cookie-banner" id="cookie-banner">
    <p>{ck_text}</p>
    <div class="cookie-actions">
      <button class="cookie-btn accept" id="cookie-accept">{ck_accept}</button>
      <a href="privacy-policy.html" class="cookie-btn learn">{ck_learn}</a>
    </div>
  </div>
  <script src="../js/main.js"></script>
</body>
</html>
"""


def ad(lang="ko"):
    """Responsive display ad unit (lists, page bottom)."""
    return f"""      <div class="ad-container">
        <div class="ad-label">{AD_LABEL[lang]}</div>
        <ins class="adsbygoogle"
             style="display:block"
             data-ad-client="{ADSENSE_CLIENT}"
             data-ad-slot="{AD_SLOT_DISPLAY}"
             data-ad-format="auto"
             data-full-width-responsive="true"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
      </div>"""


def ad_inarticle(lang="ko"):
    """In-article fluid ad unit (placed within post body)."""
    return f"""        <div class="ad-container ad-inarticle">
          <div class="ad-label">{AD_LABEL[lang]}</div>
          <ins class="adsbygoogle"
               style="display:block; text-align:center;"
               data-ad-layout="in-article"
               data-ad-format="fluid"
               data-ad-client="{ADSENSE_CLIENT}"
               data-ad-slot="{AD_SLOT_INARTICLE}"></ins>
          <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
        </div>"""


# ---------------------------------------------------------------- ticker data
# order: slug, symbol, sector, exchange, name_ko, name_ja, date
# content: lead_ko, lead_ja, then 4 (body_ko, body_ja) for the fixed sections
TICKERS = []


def add(slug, sym, sector, exch, nko, nja, date, lead_ko, lead_ja, bodies):
    TICKERS.append(dict(slug=slug, sym=sym, sector=sector, exch=exch,
                        nko=nko, nja=nja, date=date, lead_ko=lead_ko,
                        lead_ja=lead_ja, bodies=bodies))


add("nvda", "NVDA", "semi", "NASDAQ", "엔비디아", "エヌビディア", "2026.06.12",
    "AI 가속 컴퓨팅 시대의 핵심 기업인 엔비디아(NVDA)를 분석합니다. 데이터센터 GPU에서의 사실상 독점적 지위와 CUDA 소프트웨어 생태계가 해자의 근간입니다.",
    "AIアクセラレーテッド・コンピューティング時代の中核企業であるエヌビディア（NVDA）を分析します。データセンターGPUにおける事実上の独占的地位とCUDAソフトウェア・エコシステムが堀の根幹です。",
    [
     ("엔비디아는 AI 학습·추론용 GPU 시장의 80~90%를 점유하며, CUDA·쿠다 라이브러리·네트워킹(NVLink, 인피니밴드)을 묶은 풀스택 플랫폼으로 경쟁사를 따돌리고 있습니다. 데이터센터 부문이 매출의 대부분을 차지합니다.",
      "エヌビディアはAI学習・推論向けGPU市場の80〜90%を占有し、CUDA・ライブラリ・ネットワーキング（NVLink、InfiniBand）を束ねたフルスタック・プラットフォームで競合を引き離しています。データセンター部門が売上の大半を占めます。"),
     ("블랙웰(Blackwell) 및 차세대 아키텍처의 적기 양산, 하이퍼스케일러의 지속적인 AI 데이터센터 투자(CAPEX), 추론(inference) 수요 확대가 성장 동력입니다. 소버린 AI와 엔터프라이즈 채택도 신규 수요처입니다.",
      "Blackwell（ブラックウェル）および次世代アーキテクチャの適時量産、ハイパースケーラーの継続的なAIデータセンター投資（CAPEX）、推論（インファレンス）需要の拡大が成長ドライバーです。ソブリンAIやエンタープライズ採用も新たな需要源です。"),
     ("고객 집중도(소수 클라우드 기업 의존), AMD 및 자체 설계 ASIC(구글 TPU 등)와의 경쟁, 대중국 수출 규제, AI 투자 사이클 둔화 시 변동성 확대가 주요 리스크입니다.",
      "顧客集中度（少数のクラウド企業への依存）、AMDや自社設計ASIC（GoogleのTPU等）との競争、対中輸出規制、AI投資サイクル鈍化時のボラティリティ拡大が主なリスクです。"),
     ("AI 인프라의 핵심 공급자로서 구조적 성장의 중심에 있으나, 밸류에이션과 실적 기대치가 높아 분기 가이던스와 CAPEX 동향에 따른 변동성을 감안한 접근이 필요합니다.",
      "AIインフラの中核サプライヤーとして構造的成長の中心にありますが、バリュエーションと業績期待が高く、四半期ガイダンスやCAPEX動向によるボラティリティを踏まえたアプローチが必要です。"),
    ])

add("tsm", "TSM", "semi", "NYSE (ADR)", "TSMC", "TSMC", "2026.06.12",
    "세계 최대 파운드리이자 첨단 공정의 사실상 독점 사업자인 TSMC(TSM)를 분석합니다. AI 칩 수요의 최종 수혜자입니다.",
    "世界最大のファウンドリであり先端プロセスの事実上の独占事業者であるTSMC（TSM）を分析します。AIチップ需要の最終的な受益者です。",
    [
     ("TSMC는 3nm·2nm 등 최첨단 공정에서 압도적 점유율을 보유하며, 엔비디아·애플·AMD 등 핵심 팹리스 고객의 칩을 위탁 생산합니다. CoWoS 등 첨단 패키징 역량도 AI 칩 공급의 병목을 쥐고 있습니다.",
      "TSMCは3nm・2nmなど最先端プロセスで圧倒的なシェアを持ち、エヌビディア・アップル・AMDなど主要ファブレス顧客のチップを受託生産します。CoWoSなど先端パッケージング能力もAIチップ供給のボトルネックを握っています。"),
     ("AI·HPC 향 첨단 공정 수요 급증, 설계 경쟁과 무관하게 수혜를 보는 '곡괭이' 포지션, 가격 결정력과 높은 마진이 강점입니다. 미국·일본·독일 등 해외 팹 확장도 진행 중입니다.",
      "AI・HPC向け先端プロセス需要の急増、設計競争と無関係に恩恵を受ける『つるはし』ポジション、価格決定力と高いマージンが強みです。米国・日本・ドイツなど海外ファブ拡張も進行中です。"),
     ("대만 집중에 따른 지정학적 리스크(양안 관계), 막대한 설비투자 부담, 반도체 업황 사이클, 해외 팹의 비용·수율 안정화 과제가 리스크입니다.",
      "台湾集中による地政学的リスク（両岸関係）、巨額の設備投資負担、半導体市況サイクル、海外ファブのコスト・歩留まり安定化の課題がリスクです。"),
     ("AI 시대 반도체 공급망의 핵심 길목을 장악한 기업으로 중장기 성장성이 견조하나, 지정학 변수는 상시 점검이 필요합니다.",
      "AI時代の半導体サプライチェーンの要衝を押さえた企業として中長期の成長性は底堅いものの、地政学リスクは常時の点検が必要です。"),
    ])

add("googl", "GOOGL", "ai", "NASDAQ", "알파벳 (구글)", "アルファベット（Google）", "2026.06.11",
    "검색·광고의 지배자이자 AI 풀스택 역량을 갖춘 알파벳(GOOGL)을 분석합니다.",
    "検索・広告の支配者であり、AIフルスタック能力を備えたアルファベット（GOOGL）を分析します。",
    [
     ("알파벳은 구글 검색·유튜브 광고라는 막대한 현금창출원 위에, 구글 클라우드(GCP)와 제미나이(Gemini) AI 모델, 자체 TPU, 웨이모(자율주행)를 보유한 풀스택 기업입니다.",
      "アルファベットはGoogle検索・YouTube広告という巨大なキャッシュ創出源の上に、Google Cloud（GCP）やGemini AIモデル、自社TPU、Waymo（自動運転）を擁するフルスタック企業です。"),
     ("클라우드 부문의 고성장과 흑자 확대, 제미나이의 검색·워크스페이스 통합, 자체 TPU에 따른 비용 우위, 유튜브의 견조한 성장이 투자 포인트입니다.",
      "クラウド部門の高成長と黒字拡大、GeminiのSearch・Workspace統合、自社TPUによるコスト優位、YouTubeの堅調な成長が投資ポイントです。"),
     ("미 법무부 반독점 소송(검색 시장)에 따른 사업 구조 리스크, 생성형 AI가 기존 검색 광고 모델을 잠식할 가능성, 광고 경기 민감도가 리스크입니다.",
      "米司法省の反トラスト訴訟（検索市場）による事業構造リスク、生成AIが既存の検索広告モデルを侵食する可能性、広告景気への感応度がリスクです。"),
     ("AI 역량과 캐시카우를 겸비한 대형 플랫폼으로, 규제 불확실성을 감안하더라도 밸류에이션 매력이 부각되는 구간입니다.",
      "AI能力とキャッシュカウを兼ね備えた大型プラットフォームで、規制の不確実性を踏まえてもバリュエーションの魅力が際立つ局面です。"),
    ])

add("aapl", "AAPL", "ai", "NASDAQ", "애플", "アップル", "2026.06.11",
    "강력한 하드웨어·서비스 생태계를 보유한 애플(AAPL)을 분석합니다.",
    "強力なハードウェア・サービスのエコシステムを擁するアップル（AAPL）を分析します。",
    [
     ("애플은 아이폰을 중심으로 한 충성도 높은 사용자 기반과, 고마진의 서비스(앱스토어·구독) 부문으로 안정적 현금흐름을 창출합니다. 자체 실리콘(Apple Silicon)이 차별화 요소입니다.",
      "アップルはiPhoneを中心とする忠誠度の高いユーザー基盤と、高マージンのサービス（App Store・サブスク）部門で安定的なキャッシュフローを創出します。自社シリコン（Apple Silicon）が差別化要素です。"),
     ("서비스 매출의 구조적 성장, 거대한 설치 기반을 활용한 온디바이스 AI(Apple Intelligence) 확산, 적극적인 자사주 매입·배당이 주주환원 매력입니다.",
      "サービス売上の構造的成長、巨大なインストールベースを活用したオンデバイスAI（Apple Intelligence）の普及、積極的な自社株買い・配当が株主還元の魅力です。"),
     ("중국 시장의 수요·규제 리스크, AI 경쟁에서의 상대적 후발 인식, 하드웨어 교체 주기 의존, 규제 당국의 앱스토어 수수료 압박이 리스크입니다.",
      "中国市場の需要・規制リスク、AI競争における相対的な後発との見方、ハードウェア買い替えサイクルへの依存、規制当局によるApp Store手数料への圧力がリスクです。"),
     ("프리미엄 생태계와 서비스 성장에 기반한 방어적 우량주로, AI 기능의 실제 채택 속도가 향후 멀티플의 관건입니다.",
      "プレミアムなエコシステムとサービス成長に基づくディフェンシブな優良株で、AI機能の実際の採用ペースが今後のマルチプルの鍵となります。"),
    ])

add("amzn", "AMZN", "ai", "NASDAQ", "아마존", "アマゾン", "2026.06.11",
    "클라우드(AWS)와 이커머스·광고를 아우르는 아마존(AMZN)을 분석합니다.",
    "クラウド（AWS）とEコマース・広告を網羅するアマゾン（AMZN）を分析します。",
    [
     ("아마존은 세계 1위 클라우드 AWS, 거대한 이커머스 물류망, 빠르게 성장하는 광고 사업을 보유합니다. AWS가 영업이익의 핵심 동력입니다.",
      "アマゾンは世界首位のクラウドAWS、巨大なEコマース物流網、急成長する広告事業を擁します。AWSが営業利益の中核ドライバーです。"),
     ("AWS의 AI 워크로드 수요 회복과 자체 칩(Trainium/Inferentia), 리테일 마진 개선, 고마진 광고 성장, 물류 효율화가 투자 포인트입니다.",
      "AWSのAIワークロード需要の回復と自社チップ（Trainium/Inferentia）、リテールのマージン改善、高マージンの広告成長、物流効率化が投資ポイントです。"),
     ("AWS의 클라우드 경쟁 심화, 대규모 AI CAPEX 부담, 소비 경기 둔화 시 리테일 수익성 압박, 규제 리스크가 주요 변수입니다.",
      "AWSのクラウド競争激化、大規模なAI CAPEX負担、消費景気鈍化時のリテール収益性への圧迫、規制リスクが主な変数です。"),
     ("클라우드·광고의 고수익 구조와 리테일 레버리지가 결합된 성장주로, AWS 성장률 재가속 여부가 핵심 관전 포인트입니다.",
      "クラウド・広告の高収益構造とリテールのレバレッジが結合した成長株で、AWS成長率の再加速の可否が最大の注目点です。"),
    ])

add("orcl", "ORCL", "ai", "NYSE", "오라클", "オラクル", "2026.06.11",
    "데이터베이스 강자에서 AI 클라우드 인프라(OCI) 성장주로 변모한 오라클(ORCL)을 분석합니다.",
    "データベースの雄からAIクラウドインフラ（OCI）の成長株へと変貌したオラクル（ORCL）を分析します。",
    [
     ("오라클은 엔터프라이즈 데이터베이스의 전통 강자이며, 최근에는 OCI(오라클 클라우드 인프라)를 통해 AI 학습용 GPU 클러스터를 공급하며 가파른 수주잔고(RPO) 증가를 보이고 있습니다.",
      "オラクルはエンタープライズ・データベースの伝統的な雄であり、近年はOCI（オラクル・クラウド・インフラ）を通じてAI学習向けGPUクラスタを供給し、急激な受注残（RPO）の増加を見せています。"),
     ("AI 인프라 수요에 힘입은 OCI의 폭발적 성장, 대형 클라우드 계약 체결, 데이터베이스의 클라우드 전환, 멀티클라우드 제휴가 투자 포인트입니다.",
      "AIインフラ需要に支えられたOCIの急成長、大型クラウド契約の締結、データベースのクラウド移行、マルチクラウド提携が投資ポイントです。"),
     ("막대한 데이터센터 CAPEX와 부채 부담, 하이퍼스케일러 대비 후발 주자로서의 실행 리스크, 수주잔고의 매출 전환 속도가 변수입니다.",
      "巨額のデータセンターCAPEXと負債負担、ハイパースケーラーに対する後発としての実行リスク、受注残の売上転換ペースが変数です。"),
     ("AI 클라우드라는 새로운 성장축을 확보했으나, 높아진 기대치만큼 CAPEX 효율과 계약 이행 능력이 밸류에이션을 좌우합니다.",
      "AIクラウドという新たな成長軸を確保しましたが、高まった期待に見合うCAPEX効率と契約履行能力がバリュエーションを左右します。"),
    ])

add("pltr", "PLTR", "ai", "NASDAQ", "팔란티어", "パランティア", "2026.06.11",
    "정부·기업용 AI 운영 플랫폼을 제공하는 팔란티어(PLTR)를 분석합니다.",
    "政府・企業向けAI運用プラットフォームを提供するパランティア（PLTR）を分析します。",
    [
     ("팔란티어는 Gotham(정부)·Foundry(기업)·AIP(AI 플랫폼)를 통해 조직의 데이터를 실제 의사결정·운영에 연결합니다. 미 국방·정보기관과 상업 고객을 동시에 확보하고 있습니다.",
      "パランティアはGotham（政府）・Foundry（企業）・AIP（AIプラットフォーム）を通じて、組織のデータを実際の意思決定・運用に結び付けます。米国防・情報機関と商業顧客を同時に獲得しています。"),
     ("AIP를 앞세운 미국 상업 부문의 고성장, 흑자 전환 후 이익률 개선, 정부 계약의 안정적 기반, 높은 순매출 유지율이 투자 포인트입니다.",
      "AIPを前面に出した米国商業部門の高成長、黒字転換後の利益率改善、政府契約の安定的な基盤、高いネットリテンションが投資ポイントです。"),
     ("매우 높은 밸류에이션, 정부 매출 의존과 예산·정치 변수, 주식보상(SBC) 희석, 성장 둔화 시 멀티플 급락 가능성이 리스크입니다.",
      "非常に高いバリュエーション、政府売上への依存と予算・政治の変数、株式報酬（SBC）による希薄化、成長鈍化時のマルチプル急落の可能性がリスクです。"),
     ("AI 실전 적용(operational AI)의 대표주로 성장성은 뛰어나나, 가격 부담이 커 변동성을 견딜 수 있는 관점에서 접근해야 합니다.",
      "実戦適用AI（operational AI）の代表銘柄として成長性は際立ちますが、価格負担が大きく、ボラティリティに耐えられる視点でのアプローチが求められます。"),
    ])

add("ionq", "IONQ", "ai", "NYSE", "아이온큐", "IonQ", "2026.06.11",
    "트랩드 이온 방식 양자컴퓨팅 선도 기업 아이온큐(IONQ)를 분석합니다.",
    "トラップドイオン方式の量子コンピューティングをリードするIonQ（IONQ）を分析します。",
    [
     ("아이온큐는 이온 트랩 기반 양자컴퓨터를 개발하며, 클라우드(AWS·Azure·구글)를 통한 접근과 정부·연구기관 계약으로 초기 매출을 내고 있습니다.",
      "IonQはイオントラップ方式の量子コンピュータを開発し、クラウド（AWS・Azure・Google）経由のアクセスや政府・研究機関との契約で初期売上を計上しています。"),
     ("양자컴퓨팅의 장기 잠재력, 네트워킹·양자 인터넷으로의 확장, 정부·국방 수요, 기술 마일스톤 달성 시 모멘텀이 투자 포인트입니다.",
      "量子コンピューティングの長期的ポテンシャル、ネットワーキング・量子インターネットへの拡張、政府・防衛需要、技術マイルストーン達成時のモメンタムが投資ポイントです。"),
     ("아직 상업화 초기 단계로 적자·현금소진이 크고, 기술 경로의 불확실성, 대형 기술기업과의 경쟁, 높은 밸류에이션 변동성이 리스크입니다.",
      "まだ商業化の初期段階で赤字・キャッシュ消費が大きく、技術経路の不確実性、大手テック企業との競争、高いバリュエーション・ボラティリティがリスクです。"),
     ("고위험·고성장 테마주로, 포트폴리오 내 소액 분산 관점에서 접근하고 기술 진척과 자금 상황을 지속 점검해야 합니다.",
      "ハイリスク・ハイグロースのテーマ株であり、ポートフォリオ内での少額分散の観点でアプローチし、技術進捗と資金状況を継続的に点検すべきです。"),
    ])

add("ibm", "IBM", "infra", "NYSE", "IBM", "IBM", "2026.06.11",
    "하이브리드 클라우드와 엔터프라이즈 AI로 재편된 IBM을 분석합니다.",
    "ハイブリッドクラウドとエンタープライズAIへと再編されたIBMを分析します。",
    [
     ("IBM은 레드햇(하이브리드 클라우드), watsonx(엔터프라이즈 AI), 컨설팅, 메인프레임, 양자컴퓨팅을 축으로 사업을 재편했습니다. 안정적 현금흐름과 배당이 특징입니다.",
      "IBMはRed Hat（ハイブリッドクラウド）、watsonx（エンタープライズAI）、コンサルティング、メインフレーム、量子コンピューティングを軸に事業を再編しました。安定的なキャッシュフローと配当が特徴です。"),
     ("엔터프라이즈 AI·하이브리드 클라우드 수요, 소프트웨어 비중 확대에 따른 마진 개선, 견조한 배당, 양자컴퓨팅 리더십이 투자 포인트입니다.",
      "エンタープライズAI・ハイブリッドクラウド需要、ソフトウェア比率拡大によるマージン改善、堅調な配当、量子コンピューティングのリーダーシップが投資ポイントです。"),
     ("상대적으로 낮은 성장률, 컨설팅의 경기 민감도, 대형 클라우드 대비 경쟁 강도, 레거시 사업의 둔화가 리스크입니다.",
      "相対的に低い成長率、コンサルティングの景気感応度、大手クラウドに対する競争の強さ、レガシー事業の鈍化がリスクです。"),
     ("성장보다 안정적 현금흐름·배당과 AI/하이브리드 전환 스토리에 무게를 둔 종목으로, 방어적 보유에 적합합니다.",
      "成長よりも安定的なキャッシュフロー・配当とAI/ハイブリッド転換のストーリーに重きを置く銘柄で、ディフェンシブな保有に適します。"),
    ])

add("csco", "CSCO", "infra", "NASDAQ", "시스코", "シスコ", "2026.06.11",
    "네트워킹 강자이자 AI 데이터센터 인프라·보안으로 확장 중인 시스코(CSCO)를 분석합니다.",
    "ネットワーキングの雄であり、AIデータセンターインフラ・セキュリティへ拡張中のシスコ（CSCO）を分析します。",
    [
     ("시스코는 기업·통신 네트워크 장비의 선도 기업으로, 스플렁크 인수로 보안·관측성(observability)을 강화하고 AI 데이터센터용 이더넷·옵틱스로 영역을 넓히고 있습니다.",
      "シスコは企業・通信ネットワーク機器のリーディング企業で、Splunk買収によりセキュリティ・オブザーバビリティを強化し、AIデータセンター向けイーサネット・オプティクスへ領域を広げています。"),
     ("구독·소프트웨어 비중 확대에 따른 실적 안정성, AI 네트워킹 수주, 보안 사업 성장, 견조한 배당과 자사주 매입이 투자 포인트입니다.",
      "サブスク・ソフトウェア比率拡大による業績の安定性、AIネットワーキング受注、セキュリティ事業の成長、堅調な配当と自社株買いが投資ポイントです。"),
     ("성숙 시장에서의 낮은 성장, 화이트박스·경쟁사와의 가격 경쟁, 기업 IT 지출 사이클 의존이 리스크입니다.",
      "成熟市場での低成長、ホワイトボックス・競合との価格競争、企業IT支出サイクルへの依存がリスクです。"),
     ("배당과 안정성을 갖춘 인프라 우량주로, AI 네트워킹이 성장률을 끌어올릴 수 있을지가 관전 포인트입니다.",
      "配当と安定性を備えたインフラ優良株で、AIネットワーキングが成長率を押し上げられるかが注目点です。"),
    ])

add("dell", "DELL", "infra", "NYSE", "델 테크놀로지스", "デル・テクノロジーズ", "2026.06.11",
    "AI 서버 수요의 직접 수혜주인 델 테크놀로지스(DELL)를 분석합니다.",
    "AIサーバー需要の直接的な受益銘柄であるデル・テクノロジーズ（DELL）を分析します。",
    [
     ("델은 서버·스토리지(ISG)와 PC(CSG) 사업을 보유하며, 최근 AI 최적화 서버 수요 급증으로 ISG 부문 수주잔고가 크게 늘었습니다.",
      "デルはサーバー・ストレージ（ISG）とPC（CSG）事業を擁し、近年はAI最適化サーバー需要の急増によりISG部門の受注残が大きく増加しています。"),
     ("AI 서버 수주잔고 확대, 엔터프라이즈 스토리지 회복, PC 교체 사이클(AI PC) 기대, 주주환원이 투자 포인트입니다.",
      "AIサーバー受注残の拡大、エンタープライズ・ストレージの回復、PC買い替えサイクル（AI PC）への期待、株主還元が投資ポイントです。"),
     ("AI 서버의 낮은 마진, PC 시장의 경기 민감성, 부품가 변동, 부채 부담이 리스크입니다.",
      "AIサーバーの低マージン、PC市場の景気感応性、部品価格の変動、負債負担がリスクです。"),
     ("AI 인프라 투자의 직접 수혜주이나, 수익성(특히 AI 서버 마진) 개선이 주가 재평가의 관건입니다.",
      "AIインフラ投資の直接的な受益銘柄ですが、収益性（特にAIサーバーのマージン）改善が株価再評価の鍵です。"),
    ])

add("cibr", "CIBR", "cyber", "NASDAQ", "퍼스트트러스트 나스닥 사이버보안 ETF", "ファースト・トラスト ナスダック サイバーセキュリティETF", "2026.06.10",
    "사이버보안 섹터에 분산 투자하는 ETF인 CIBR을 분석합니다. 개별 종목이 아닌 테마 분산 수단입니다.",
    "サイバーセキュリティ・セクターへ分散投資するETFであるCIBRを分析します。個別銘柄ではなくテーマ分散の手段です。",
    [
     ("CIBR은 크라우드스트라이크·팔로알토네트웍스 등 글로벌 사이버보안 기업에 분산 투자하는 First Trust의 테마 ETF입니다. 개별 종목 리스크를 낮추면서 섹터에 베팅하는 수단입니다.",
      "CIBRはクラウドストライク・パロアルトネットワークスなどグローバルなサイバーセキュリティ企業へ分散投資するFirst TrustのテーマETFです。個別銘柄リスクを抑えつつセクターにベットする手段です。"),
     ("랜섬웨어·국가 배후 공격 증가에 따른 보안 지출의 구조적 성장, 클라우드·AI 보안 수요, 분산을 통한 개별 기업 리스크 완화가 투자 포인트입니다.",
      "ランサムウェア・国家背景の攻撃の増加によるセキュリティ支出の構造的成長、クラウド・AIセキュリティ需要、分散による個別企業リスクの緩和が投資ポイントです。"),
     ("상위 편입 종목 집중도, 섹터 전반의 높은 밸류에이션과 금리 민감도, ETF 운용보수, 테마 변동성이 리스크입니다.",
      "上位組入銘柄への集中度、セクター全体の高いバリュエーションと金利感応度、ETFの運用報酬、テーマのボラティリティがリスクです。"),
     ("개별 종목 선별이 부담스러운 투자자에게 사이버보안 성장 테마를 분산으로 담는 합리적 수단입니다.",
      "個別銘柄の選別が負担な投資家にとって、サイバーセキュリティの成長テーマを分散で取り込む合理的な手段です。"),
    ])

add("spcx", "SPCX", "space", "신규 상장 (2026.06.12 IPO)", "스페이스X", "スペースX", "2026.06.12",
    "민간 우주 산업의 압도적 1위 기업 스페이스X(SPCX)를 분석합니다. 2026년 6월 12일 신규 상장(IPO)되어 이제 공개 시장에서 거래되는 종목입니다.",
    "民間宇宙産業の圧倒的首位企業であるスペースX（SPCX）を分析します。2026年6月12日に新規上場（IPO）し、現在は公開市場で取引される銘柄です。",
    [
     ("스페이스X는 재사용 로켓(팰컨9), 위성 인터넷(스타링크), 차세대 스타십을 보유한 우주 기업으로, 2026년 6월 12일 상장했습니다. 발사 시장을 사실상 장악했으며, 스타링크 가입자 확대로 매출이 빠르게 성장하고 있습니다.",
      "スペースXは再使用ロケット（ファルコン9）、衛星インターネット（スターリンク）、次世代スターシップを擁する宇宙企業で、2026年6月12日に上場しました。打ち上げ市場を事実上掌握し、スターリンク加入者の拡大で売上が急成長しています。"),
     ("스타링크의 가입자·매출 급증, 발사 시장 독점적 지위, 스타십 상용화 시 비용 혁신 잠재력, 정부·국방 계약, 그리고 상장으로 확보한 유동성과 자금 조달력이 핵심 가치 동인입니다.",
      "スターリンクの加入者・売上の急増、打ち上げ市場での独占的地位、スターシップ商用化時のコスト革新ポテンシャル、政府・防衛契約、そして上場により確保した流動性と資金調達力が中核的な価値ドライバーです。"),
     ("상장 초기 특유의 높은 변동성, 향후 보호예수(락업) 해제에 따른 물량 부담, 높은 기대가 반영된 밸류에이션, 막대한 자본 소요와 스타십 개발·인증 리스크, 수익성 안정화 과제가 리스크입니다.",
      "上場初期特有の高いボラティリティ、今後のロックアップ解除に伴う需給負担、高い期待が織り込まれたバリュエーション、巨額の資本需要とスターシップ開発・認証リスク、収益性の安定化という課題がリスクです。"),
     ("우주 경제의 핵심 기업이 공개 시장에 진입해 이제 직접 투자가 가능해졌습니다. 다만 상장 직후에는 가격 변동성과 락업 일정이 크게 작용하므로, 분할 매수와 실적·가이던스 확인을 병행하는 신중한 접근이 바람직합니다.",
      "宇宙経済の中核企業が公開市場に登場し、これにより直接投資が可能になりました。ただし上場直後は価格変動とロックアップの日程が大きく作用するため、分割購入と業績・ガイダンスの確認を併用する慎重なアプローチが望ましいです。"),
    ])

add("rdw", "RDW", "space", "NYSE", "레드와이어", "レッドワイヤー", "2026.06.10",
    "우주 인프라 부품과 우주 제조를 다루는 레드와이어(RDW)를 분석합니다.",
    "宇宙インフラ部品と宇宙製造を手掛けるレッドワイヤー（RDW）を分析します。",
    [
     ("레드와이어는 태양광 패널·구조물 등 우주선 부품과 미세중력 제조, 최근 무인기(드론) 사업 확장까지 아우르는 우주·방산 기업입니다.",
      "レッドワイヤーは太陽光パネル・構造物などの宇宙機部品や微小重力製造、近年は無人機（ドローン）事業の拡張まで網羅する宇宙・防衛企業です。"),
     ("우주·방산 예산 확대 수혜, 핵심 부품 공급 지위, 무인 시스템으로의 사업 다각화, 수주 증가가 투자 포인트입니다.",
      "宇宙・防衛予算拡大の恩恵、主要部品の供給地位、無人システムへの事業多角化、受注の増加が投資ポイントです。"),
     ("소형주 특유의 높은 변동성, 흑자 안정화 과제, 계약의 불규칙성(lumpiness), 자금 조달·희석 가능성이 리스크입니다.",
      "小型株特有の高いボラティリティ、黒字安定化の課題、契約の不規則性（lumpiness）、資金調達・希薄化の可能性がリスクです。"),
     ("우주 인프라 성장 테마의 고변동 소형주로, 수주·수익성 추세를 확인하며 소액 분산 관점이 적합합니다.",
      "宇宙インフラ成長テーマの高ボラティリティ小型株で、受注・収益性のトレンドを確認しつつ少額分散の観点が適します。"),
    ])

add("bwxt", "BWXT", "space", "NYSE", "BWX 테크놀로지스", "BWXテクノロジーズ", "2026.06.10",
    "미 해군 원자로와 원자력·핵의학을 다루는 BWX 테크놀로지스(BWXT)를 분석합니다.",
    "米海軍の原子炉や原子力・核医学を手掛けるBWXテクノロジーズ（BWXT）を分析します。",
    [
     ("BWXT는 미 해군 항공모함·잠수함용 원자로를 사실상 독점 공급하며, 원전 부품, 핵의학용 의료 동위원소, 소형모듈원자로(SMR)·마이크로원자로로 사업을 확장하고 있습니다.",
      "BWXTは米海軍の空母・潜水艦向け原子炉を事実上独占供給し、原発部品、核医学用の医療同位体、小型モジュール炉（SMR）・マイクロ炉へ事業を拡張しています。"),
     ("장기 방산 계약에 따른 안정적 매출, 원자력 르네상스·SMR 성장 옵션, 의료 동위원소 사업, 높은 진입장벽이 투자 포인트입니다.",
      "長期の防衛契約による安定的な売上、原子力ルネサンス・SMRの成長オプション、医療同位体事業、高い参入障壁が投資ポイントです。"),
     ("미 정부 예산 의존, 대형 프로젝트의 실행·원가 리스크, 신사업(SMR) 상용화 시점의 불확실성이 리스크입니다.",
      "米政府予算への依存、大型プロジェクトの実行・原価リスク、新事業（SMR）商用化時期の不確実性がリスクです。"),
     ("안정적 방산 캐시플로에 원자력 성장 옵션이 더해진 종목으로, 방어와 성장 테마를 겸비합니다.",
      "安定的な防衛キャッシュフローに原子力の成長オプションが加わった銘柄で、ディフェンスと成長テーマを兼ね備えます。"),
    ])

add("tdy", "TDY", "space", "NYSE", "텔레다인 테크놀로지스", "テレダイン・テクノロジーズ", "2026.06.10",
    "정밀 계측·이미징·항공우주 전자장비의 강자 텔레다인(TDY)을 분석합니다.",
    "精密計測・イメージング・航空宇宙エレクトロニクスの雄であるテレダイン（TDY）を分析します。",
    [
     ("텔레다인은 디지털 이미징, 계측·시험장비, 항공우주·방산 전자장비, 해양 기기 등 고부가가치 산업 전반에 분산된 포트폴리오를 보유합니다.",
      "テレダインはデジタルイメージング、計測・試験装置、航空宇宙・防衛エレクトロニクス、海洋機器など高付加価値の産業全般に分散したポートフォリオを擁します。"),
     ("다각화된 사업 구조의 안정성, 방산·우주 수요, 규율 있는 M&A를 통한 성장, 견조한 현금흐름이 투자 포인트입니다.",
      "多角化された事業構造の安定性、防衛・宇宙需要、規律あるM&Aを通じた成長、堅調なキャッシュフローが投資ポイントです。"),
     ("산업·계측 수요의 경기 민감도, M&A 통합 리스크, 일부 상업 시장의 변동성이 리스크입니다.",
      "産業・計測需要の景気感応度、M&A統合リスク、一部の商業市場のボラティリティがリスクです。"),
     ("다양한 고품질 사업의 결합으로 변동성을 낮춘 우량 산업주로, 꾸준한 복리 성장형 종목입니다.",
      "多様な高品質事業の結合でボラティリティを抑えた優良産業株で、着実な複利成長型の銘柄です。"),
    ])

add("mog-a", "MOG.A", "space", "NYSE", "무그", "ムーグ", "2026.06.10",
    "정밀 모션 컨트롤·항공우주 작동기의 무그(MOG.A)를 분석합니다.",
    "精密モーションコントロール・航空宇宙アクチュエーターのムーグ（MOG.A）を分析します。",
    [
     ("무그는 항공기·미사일·우주발사체·산업장비의 정밀 작동(액추에이션)·모션 컨트롤 시스템을 공급하는 기업입니다. A주는 의결권이 있는 클래스입니다.",
      "ムーグは航空機・ミサイル・宇宙ロケット・産業機器の精密アクチュエーション・モーションコントロールシステムを供給する企業です。A株は議決権のあるクラスです。"),
     ("방산·항공우주 사이클 수혜, 정밀 부품의 높은 기술 장벽과 교체·애프터마켓 수요, 안정적 수주가 투자 포인트입니다.",
      "防衛・航空宇宙サイクルの恩恵、精密部品の高い技術障壁と交換・アフターマーケット需要、安定的な受注が投資ポイントです。"),
     ("방산 예산·프로그램 사이클 의존, 산업 부문의 경기 민감도, 마진 변동, 공급망 리스크가 변수입니다.",
      "防衛予算・プログラムサイクルへの依存、産業部門の景気感応度、マージン変動、サプライチェーンリスクが変数です。"),
     ("항공우주·방산의 핵심 부품 공급사로, 견조한 수주잔고와 애프터마켓이 안정성을 뒷받침합니다.",
      "航空宇宙・防衛の中核部品サプライヤーで、堅調な受注残とアフターマーケットが安定性を支えます。"),
    ])

add("fslr", "FSLR", "energy", "NASDAQ", "퍼스트솔라", "ファーストソーラー", "2026.06.10",
    "미국산 박막 태양광 모듈의 선두 기업 퍼스트솔라(FSLR)를 분석합니다.",
    "米国産薄膜太陽光モジュールのリーディング企業ファーストソーラー（FSLR）を分析します。",
    [
     ("퍼스트솔라는 카드뮴-텔루라이드(CdTe) 박막 기술로 차별화된 미국 중심 태양광 모듈 제조사입니다. 장기 계약 기반의 대규모 수주잔고를 확보하고 있습니다.",
      "ファーストソーラーはカドミウムテルル（CdTe）薄膜技術で差別化した、米国中心の太陽光モジュール製造企業です。長期契約に基づく大規模な受注残を確保しています。"),
     ("미국 내 생산 기반과 정책(세액공제) 수혜, 장기 계약에 따른 매출 가시성, 데이터센터·전력 수요 증가, 견조한 재무구조가 투자 포인트입니다.",
      "米国内の生産基盤と政策（税額控除）の恩恵、長期契約による売上の可視性、データセンター・電力需要の増加、堅調な財務構造が投資ポイントです。"),
     ("정책 변화(세액공제 축소) 리스크, 모듈 가격 경쟁과 중국 공급과잉, 수요·금리 민감도가 리스크입니다.",
      "政策変更（税額控除縮小）リスク、モジュール価格競争と中国の供給過剰、需要・金利感応度がリスクです。"),
     ("미국 정책·전력 수요의 수혜를 받는 태양광 대표주로, 정책 방향성이 실적·주가의 핵심 변수입니다.",
      "米国の政策・電力需要の恩恵を受ける太陽光の代表銘柄で、政策の方向性が業績・株価の最大の変数です。"),
    ])

add("be", "BE", "energy", "NYSE", "블룸에너지", "ブルームエナジー", "2026.06.10",
    "고체산화물 연료전지 기반 온사이트 발전 기업 블룸에너지(BE)를 분석합니다.",
    "固体酸化物形燃料電池ベースのオンサイト発電企業ブルームエナジー（BE）を分析します。",
    [
     ("블룸에너지는 고체산화물 연료전지(SOFC) '에너지 서버'로 현장 분산 발전을 제공합니다. 전력망 부담이 큰 데이터센터의 즉시 전력 수요가 새로운 성장 동력입니다.",
      "ブルームエナジーは固体酸化物形燃料電池（SOFC）『エナジーサーバー』でオンサイトの分散発電を提供します。電力網への負担が大きいデータセンターの即時電力需要が新たな成長ドライバーです。"),
     ("AI 데이터센터의 전력 수요 급증 수혜, 빠른 설치가 가능한 분산 발전, 수소 연계 잠재력, 대형 수주가 투자 포인트입니다.",
      "AIデータセンターの電力需要急増の恩恵、迅速に設置可能な分散発電、水素連携のポテンシャル、大型受注が投資ポイントです。"),
     ("수익성·현금흐름 개선 과제, 정책·보조금 의존, 연료(가스) 가격, 경쟁 기술과의 비교 열위 가능성이 리스크입니다.",
      "収益性・キャッシュフロー改善の課題、政策・補助金への依存、燃料（ガス）価格、競合技術に対する劣位の可能性がリスクです。"),
     ("데이터센터 전력난이라는 강한 수요 테마를 가진 성장주이나, 흑자 전환의 지속성이 재평가의 관건입니다.",
      "データセンターの電力不足という強い需要テーマを持つ成長株ですが、黒字転換の持続性が再評価の鍵です。"),
    ])

add("vrt", "VRT", "energy", "NYSE", "버티브", "ヴァーティブ", "2026.06.10",
    "데이터센터 전력·냉각 인프라의 핵심 공급사 버티브(VRT)를 분석합니다.",
    "データセンターの電力・冷却インフラの中核サプライヤーであるヴァーティブ（VRT）を分析します。",
    [
     ("버티브는 데이터센터의 전력 관리, 냉각(액침·수냉 포함), 모니터링 인프라를 공급합니다. AI 서버의 고밀도 발열을 처리하는 열관리 수요의 직접 수혜주입니다.",
      "ヴァーティブはデータセンターの電力管理、冷却（液浸・水冷含む）、モニタリングインフラを供給します。AIサーバーの高密度発熱を処理する熱管理需要の直接的な受益銘柄です。"),
     ("AI 데이터센터 구축 붐에 따른 수주 급증, 액체냉각 등 고부가 솔루션 성장, 견조한 수주잔고와 마진 개선이 투자 포인트입니다.",
      "AIデータセンター構築ブームによる受注急増、液冷など高付加価値ソリューションの成長、堅調な受注残とマージン改善が投資ポイントです。"),
     ("하이퍼스케일러 고객 집중도, 데이터센터 투자 사이클 둔화 시 변동성, 높은 밸류에이션, 공급망 리스크가 변수입니다.",
      "ハイパースケーラー顧客への集中度、データセンター投資サイクル鈍化時のボラティリティ、高いバリュエーション、サプライチェーンリスクが変数です。"),
     ("AI 인프라 '곡괭이' 성격의 핵심 수혜주로, 데이터센터 CAPEX 사이클과 동행하는 고성장·고변동 종목입니다.",
      "AIインフラの『つるはし』的な中核受益銘柄で、データセンターCAPEXサイクルと連動する高成長・高ボラティリティ銘柄です。"),
    ])

add("tsla", "TSLA", "ev", "NASDAQ", "테슬라", "テスラ", "2026.06.10",
    "전기차를 넘어 자율주행·로봇·에너지로 확장하는 테슬라(TSLA)를 분석합니다.",
    "EVを超えて自動運転・ロボット・エネルギーへ拡張するテスラ（TSLA）を分析します。",
    [
     ("테슬라는 글로벌 전기차 선두 기업이자, FSD(자율주행)·로보택시, 에너지 저장(ESS), 휴머노이드 로봇(옵티머스)으로 사업을 확장하는 기업입니다.",
      "テスラはグローバルEVのリーディング企業であり、FSD（自動運転）・ロボタクシー、エネルギー貯蔵（ESS）、ヒューマノイドロボット（オプティマス）へ事業を拡張する企業です。"),
     ("FSD·로보택시의 상용화 옵션, 고성장 에너지 저장 사업, 옵티머스의 장기 잠재력, 제조 원가 혁신이 투자 포인트입니다.",
      "FSD・ロボタクシーの商用化オプション、高成長のエネルギー貯蔵事業、オプティマスの長期ポテンシャル、製造原価の革新が投資ポイントです。"),
     ("EV 수요 둔화와 가격 경쟁에 따른 마진 압박, 자율주행/로봇 내러티브에 의존한 높은 밸류에이션, 경영진 리스크가 변수입니다.",
      "EV需要の鈍化と価格競争によるマージン圧迫、自動運転/ロボットのナラティブに依存した高いバリュエーション、経営陣リスクが変数です。"),
     ("자동차 실적과 AI/로봇 미래가치가 혼재된 종목으로, 로보택시·옵티머스의 실제 진척이 주가의 핵심 동인입니다.",
      "自動車業績とAI/ロボットの将来価値が混在する銘柄で、ロボタクシー・オプティマスの実際の進捗が株価の最大のドライバーです。"),
    ])

add("hood", "HOOD", "fintech", "NASDAQ", "로빈후드", "ロビンフッド", "2026.06.10",
    "리테일 투자·암호화폐 플랫폼으로 확장 중인 로빈후드(HOOD)를 분석합니다.",
    "リテール投資・暗号資産プラットフォームへ拡張中のロビンフッド（HOOD）を分析します。",
    [
     ("로빈후드는 수수료 무료 주식·옵션·암호화폐 거래 앱으로 시작해, 선물·예측시장·은퇴계좌·구독(Gold) 등으로 제품군을 빠르게 확장하고 있습니다.",
      "ロビンフッドは手数料無料の株式・オプション・暗号資産取引アプリとして始まり、先物・予測市場・退職口座・サブスク（Gold）などへ製品群を急速に拡張しています。"),
     ("신규 제품을 통한 ARPU 상승, 암호화폐·옵션 거래 활성화, 예치금 기반 순이자수익, 젊은 사용자층 확보가 투자 포인트입니다.",
      "新規プロダクトによるARPU上昇、暗号資産・オプション取引の活発化、預り金ベースの純金利収益、若年ユーザー層の獲得が投資ポイントです。"),
     ("리테일 거래·암호화폐 시황에 대한 높은 민감도, 규제 리스크, 금리 하락 시 순이자수익 감소, 경쟁 심화가 변수입니다.",
      "リテール取引・暗号資産市況への高い感応度、規制リスク、金利低下時の純金利収益の減少、競争激化が変数です。"),
     ("리테일 강세장과 암호화폐 사이클의 레버리지가 큰 핀테크 성장주로, 시황에 따른 변동성이 큽니다.",
      "リテールの強気相場と暗号資産サイクルのレバレッジが大きいフィンテック成長株で、市況によるボラティリティが大きいです。"),
    ])

add("ttwo", "TTWO", "gaming", "NASDAQ", "테이크투 인터랙티브", "テイクツー・インタラクティブ", "2026.06.10",
    "GTA 시리즈를 보유한 글로벌 게임 퍼블리셔 테이크투(TTWO)를 분석합니다.",
    "GTAシリーズを擁するグローバルなゲームパブリッシャー、テイクツー（TTWO）を分析します。",
    [
     ("테이크투는 Rockstar(GTA·레드 데드)와 2K, 모바일(징가)을 보유한 대형 게임사입니다. 차기 'GTA VI' 출시가 향후 실적의 최대 촉매로 주목받습니다.",
      "テイクツーはRockstar（GTA・レッド・デッド）と2K、モバイル（Zynga）を擁する大手ゲーム会社です。次回作『GTA VI』のリリースが今後の業績の最大の触媒として注目されています。"),
     ("GTA VI라는 초대형 흥행 카탈리스트, 강력한 IP 라인업, 라이브 서비스·인앱 결제의 반복 매출, 모바일 포트폴리오가 투자 포인트입니다.",
      "GTA VIという超大型ヒットの触媒、強力なIPラインアップ、ライブサービス・アプリ内課金による反復売上、モバイルポートフォリオが投資ポイントです。"),
     ("GTA VI 출시 일정 지연·기대치 미달 리스크, 모바일 부문 부진, 막대한 개발비, 출시 전후 변동성이 변수입니다.",
      "GTA VIのリリース時期の遅延・期待値未達リスク、モバイル部門の不振、巨額の開発費、リリース前後のボラティリティが変数です。"),
     ("GTA VI 모멘텀이 지배하는 이벤트형 종목으로, 출시 일정과 초기 판매가 주가의 방향을 결정합니다.",
      "GTA VIのモメンタムが支配するイベント型銘柄で、リリース時期と初動の販売が株価の方向を決定します。"),
    ])


# ---------------------------------------------------------------- renderers
def render_post(t, lang):
    name = t["nko"] if lang == "ko" else t["nja"]
    sector = SECTORS[t["sector"]][0 if lang == "ko" else 1]
    other_slug = f"post-{t['slug']}.html"
    title_word = "심층 분석" if lang == "ko" else "詳細分析"
    title = f"{name} ({t['sym']}) {title_word} - {LOGO[lang]}"
    desc = (t["lead_ko"] if lang == "ko" else t["lead_ja"])[:110]
    titles = SECTION_TITLES[lang]
    lead = t["lead_ko"] if lang == "ko" else t["lead_ja"]
    body_parts = []
    for i, (bko, bja) in enumerate(t["bodies"]):
        body = bko if lang == "ko" else bja
        body_parts.append(f"        <h2>{i+1}. {titles[i]}</h2>\n        <p>{body}</p>")
        if i == 1:  # in-article ad after the 2nd section
            body_parts.append(ad_inarticle(lang))
    body_html = "\n".join(body_parts)
    exch_lbl = "거래소" if lang == "ko" else "取引所"
    sector_lbl = "섹터" if lang == "ko" else "セクター"
    meta = f"{exch_lbl}: {t['exch']} · {sector_lbl}: {sector} · {META_BY[lang]}"
    h = head(lang, title, desc, f"post-{t['slug']}.html", other_slug)
    hn = header_nav(lang, "stock-analysis.html", other_slug)
    return f"""{h}
{hn}
  <main>
    <article class="post-content">
      <div class="post-header">
        <span class="post-tag">{TAG[lang]} · {t['sym']}</span>
        <h1>{name} ({t['sym']}) {title_word}</h1>
        <div class="post-meta">{('작성일' if lang=='ko' else '作成日')}: {t['date']} · {meta}</div>
      </div>
{tv_widgets(tv(t['sym']), TV_LOCALE[lang])}
      <div class="quote-note">{('실시간 시세·차트는 TradingView 제공이며 지연될 수 있습니다.' if lang=='ko' else 'リアルタイム株価・チャートはTradingView提供で、遅延する場合があります。')}</div>
      <div class="post-body">
        <p>{lead}</p>
{body_html}
      </div>
{ad(lang)}
      <a href="stock-analysis.html" class="back-btn">{BACK[lang]}</a>
    </article>
  </main>
{footer(lang)}"""


def ticker_card(t, lang):
    name = t["nko"] if lang == "ko" else t["nja"]
    sector = SECTORS[t["sector"]][0 if lang == "ko" else 1]
    lead = (t["lead_ko"] if lang == "ko" else t["lead_ja"])
    short = lead.split(".")[0] + "." if lang == "ko" else lead.split("。")[0] + "。"
    return f"""        <a href="post-{t['slug']}.html" class="article-card stock-bg">
          <div class="article-card-content">
            <span class="article-tag">{sector} · {t['sym']}</span>
            <h3>{name} ({t['sym']})</h3>
            <p>{short}</p>
            <div class="article-meta">{t['date']}</div>
          </div>
        </a>"""


def render_hub(lang):
    title = ("미국 주식 종목분석 - " if lang == "ko" else "米国株 銘柄分析 - ") + LOGO[lang]
    desc = ("미국 증시 핵심 종목의 사업 모델·투자 포인트·리스크를 분석하는 종목 리서치 모음"
            if lang == "ko" else
            "米国市場の主要銘柄のビジネスモデル・投資ポイント・リスクを分析する銘柄リサーチ集")
    banner_h = "📊 종목분석" if lang == "ko" else "📊 銘柄分析"
    banner_p = ("미국 증시 핵심 종목의 사업·경쟁력·리스크 심층 분석"
                if lang == "ko" else "米国市場の主要銘柄の事業・競争力・リスクの詳細分析")
    h = head(lang, title, desc, "stock-analysis.html", "stock-analysis.html")
    hn = header_nav(lang, "stock-analysis.html", "stock-analysis.html")
    groups = ""
    for sk in SECTOR_ORDER:
        ts = [t for t in TICKERS if t["sector"] == sk]
        if not ts:
            continue
        sname = SECTORS[sk][0 if lang == "ko" else 1]
        cards = "\n".join(ticker_card(t, lang) for t in ts)
        groups += f"""      <h2 class="sector-title">{sname}</h2>
      <div class="article-list stagger-children">
{cards}
      </div>
"""
    return f"""{h}
{hn}
  <main>
    <div class="page-banner">
      <h1>{banner_h}</h1>
      <p>{banner_p}</p>
    </div>
{tv_tape(TV_LOCALE[lang])}
    <div class="container">
{groups}
{ad(lang)}
    </div>
  </main>
{footer(lang)}"""


def render_index(lang):
    title = (LOGO[lang] + " - 미국 시장을 읽는 투자 인사이트") if lang == "ko" else (LOGO[lang] + " - 米国市場を読む投資インサイト")
    desc = ("미국 증시 핵심 종목 분석과 미국 경제 흐름을 다루는 투자 인사이트 플랫폼"
            if lang == "ko" else "米国市場の主要銘柄分析と米国経済の動向を扱う投資インサイト・プラットフォーム")
    hero_h = "미국 시장을 읽는<br>투자 인사이트" if lang == "ko" else "米国市場を読む<br>投資インサイト"
    hero_p = ("미국 증시 핵심 종목과 매크로 경제 분석을 통해 더 나은 투자 판단을 돕는 콘텐츠 플랫폼입니다."
              if lang == "ko" else "米国市場の主要銘柄とマクロ経済の分析を通じて、より良い投資判断をサポートするコンテンツ・プラットフォームです。")
    sec_h = "📊 종목분석" if lang == "ko" else "📊 銘柄分析"
    eco_h = "🌍 미국경제" if lang == "ko" else "🌍 米国経済"
    more = "전체보기" if lang == "ko" else "すべて見る"
    featured = [t for t in TICKERS if t["sym"] in ("NVDA", "GOOGL", "TSLA", "PLTR")]
    cards = "\n".join(ticker_card(t, lang) for t in featured)
    eco_card = render_eco_card(lang)
    h = head(lang, title, desc, "index.html", "index.html")
    hn = header_nav(lang, "index.html", "index.html")
    return f"""{h}
{hn}
  <main>
    <section class="hero">
      <div class="hero-label">Market Insight</div>
      <h1>{hero_h}</h1>
      <p>{hero_p}</p>
    </section>
{tv_tape(TV_LOCALE[lang])}
    <div class="section-divider"></div>
    <div class="section-header">
      <h2>{sec_h}</h2>
      <a href="stock-analysis.html">{more}</a>
    </div>
    <div class="container">
      <div class="article-list stagger-children">
{cards}
      </div>
    </div>
    <div class="section-divider"></div>
    <div class="section-header">
      <h2>{eco_h}</h2>
      <a href="economy-trends.html">{more}</a>
    </div>
    <div class="container">
      <div class="article-list stagger-children">
{eco_card}
      </div>
    </div>
    <div class="section-divider"></div>
    <div class="container">
{ad(lang)}
    </div>
  </main>
{footer(lang)}"""


def render_eco_card(lang):
    if lang == "ko":
        return """        <a href="economy-trends.html" class="article-card stock-bg">
          <div class="article-card-content">
            <span class="article-tag">미국경제</span>
            <h3>2026년 미국 경제·증시 전망</h3>
            <p>연준 통화정책, 금리 경로, AI 투자 사이클이 미국 증시에 미치는 영향을 점검합니다.</p>
            <div class="article-meta">2026.06.12</div>
          </div>
        </a>"""
    return """        <a href="economy-trends.html" class="article-card stock-bg">
          <div class="article-card-content">
            <span class="article-tag">米国経済</span>
            <h3>2026年 米国経済・株式市場の展望</h3>
            <p>FRBの金融政策、金利の経路、AI投資サイクルが米国市場に与える影響を点検します。</p>
            <div class="article-meta">2026.06.12</div>
          </div>
        </a>"""


def render_economy(lang):
    title = ("2026년 미국 경제·증시 전망 - " if lang == "ko" else "2026年 米国経済・株式市場の展望 - ") + LOGO[lang]
    if lang == "ko":
        desc = "연준 통화정책, 금리 경로, AI 투자 사이클을 토대로 한 미국 경제·증시 전망"
        banner_h, banner_p = "🌍 미국경제", "연준·금리·고용·AI 투자 등 미국 매크로 분석"
        h1 = "2026년 미국 경제·증시 전망"
        body = """        <p>미국 증시의 방향을 좌우하는 핵심 변수는 연방준비제도(Fed)의 통화정책, 금리 경로, 그리고 AI 주도의 설비투자 사이클입니다. 본 페이지에서는 미국 매크로 환경의 주요 축을 정리합니다.</p>
        <h2>1. 연준 통화정책과 금리 경로</h2>
        <p>인플레이션의 둔화 속도와 고용 시장의 균형에 따라 연준의 금리 인하 시점·폭이 결정됩니다. 금리 경로는 성장주·기술주의 밸류에이션에 직접적인 영향을 미치므로, FOMC의 점도표와 물가 지표(CPI·PCE)가 핵심 관전 포인트입니다.</p>
        <h2>2. AI 설비투자(CAPEX) 사이클</h2>
        <p>대형 클라우드 기업들의 AI 데이터센터 투자는 반도체·전력·냉각·네트워킹 등 광범위한 밸류체인의 수요를 견인하고 있습니다. 이 CAPEX 사이클의 지속성과 투자 대비 수익화(ROI) 검증이 시장의 핵심 화두입니다.</p>
        <h2>3. 고용·소비와 경기 연착륙</h2>
        <p>견조한 고용과 소비가 유지되는 한 미국 경제의 연착륙 시나리오가 우세합니다. 다만 고금리의 지연 효과, 신용 사이클, 상업용 부동산 등 잠재 리스크는 지속 점검이 필요합니다.</p>
        <h2>4. 투자 시사점</h2>
        <p>구조적 성장 테마(AI·반도체·전력 인프라)에 대한 핵심 보유를 유지하되, 금리·실적 변동성에 대비해 현금흐름이 견조한 우량주와 방어적 섹터로 균형을 맞추는 전략이 유효합니다.</p>"""
    else:
        desc = "FRBの金融政策、金利の経路、AI投資サイクルを踏まえた米国経済・株式市場の展望"
        banner_h, banner_p = "🌍 米国経済", "FRB・金利・雇用・AI投資など米国マクロ分析"
        h1 = "2026年 米国経済・株式市場の展望"
        body = """        <p>米国市場の方向を左右する主要変数は、連邦準備制度（FRB）の金融政策、金利の経路、そしてAI主導の設備投資サイクルです。本ページでは米国マクロ環境の主要な軸を整理します。</p>
        <h2>1. FRBの金融政策と金利の経路</h2>
        <p>インフレの鈍化ペースと雇用市場の均衡により、FRBの利下げ時期・幅が決まります。金利の経路は成長株・ハイテク株のバリュエーションに直接影響するため、FOMCのドットチャートと物価指標（CPI・PCE）が重要な注目点です。</p>
        <h2>2. AI設備投資（CAPEX）サイクル</h2>
        <p>大手クラウド企業のAIデータセンター投資は、半導体・電力・冷却・ネットワーキングなど広範なバリューチェーンの需要を牽引しています。このCAPEXサイクルの持続性と投資対効果（ROI）の検証が市場の中心的なテーマです。</p>
        <h2>3. 雇用・消費と景気のソフトランディング</h2>
        <p>堅調な雇用と消費が維持される限り、米国経済のソフトランディング・シナリオが優勢です。ただし高金利の遅効性、信用サイクル、商業用不動産などの潜在リスクは継続的な点検が必要です。</p>
        <h2>4. 投資への示唆</h2>
        <p>構造的な成長テーマ（AI・半導体・電力インフラ）のコア保有を維持しつつ、金利・業績のボラティリティに備えて、キャッシュフローが堅調な優良株とディフェンシブ・セクターでバランスを取る戦略が有効です。</p>"""
    h = head(lang, title, desc, "economy-trends.html", "economy-trends.html")
    hn = header_nav(lang, "economy-trends.html", "economy-trends.html")
    return f"""{h}
{hn}
  <main>
    <div class="page-banner">
      <h1>{banner_h}</h1>
      <p>{banner_p}</p>
    </div>
    <article class="post-content">
      <div class="post-header">
        <span class="post-tag">{'미국경제' if lang=='ko' else '米国経済'}</span>
        <h1>{h1}</h1>
        <div class="post-meta">{('작성일' if lang=='ko' else '作成日')}: 2026.06.12 · {META_BY[lang]}</div>
      </div>
      <div class="post-body">
{body}
      </div>
{ad(lang)}
      <a href="index.html" class="back-btn">{('← 홈으로' if lang=='ko' else '← ホームへ')}</a>
    </article>
  </main>
{footer(lang)}"""


def render_about(lang):
    title = ("소개 - " if lang == "ko" else "サイト紹介 - ") + LOGO[lang]
    if lang == "ko":
        desc = "마켓인사이트는 미국 증시 종목과 미국 경제 흐름을 분석하는 금융 인사이트 플랫폼입니다."
        body = """      <h1>마켓인사이트 소개</h1>
      <p>마켓인사이트(MarketInsight)는 미국 증시의 핵심 종목과 미국 경제 흐름을 분석하는 금융 인사이트 플랫폼입니다. 개인 투자자가 보다 합리적인 투자 판단을 내릴 수 있도록, 전문적이고 심층적인 미국 시장 분석 콘텐츠를 제공합니다.</p>
      <h2>우리의 목표</h2>
      <p>복잡한 미국 시장 데이터와 기업 펀더멘털을 누구나 이해하기 쉽게 정리해 전달합니다. 단순한 정보 전달을 넘어, 독자가 스스로 종목과 시장을 읽고 판단할 수 있는 능력을 기를 수 있도록 돕습니다.</p>
      <h2>다루는 콘텐츠</h2>
      <ul>
        <li>미국 증시 핵심 종목의 사업 모델·경쟁력·리스크 분석</li>
        <li>AI·반도체·우주·클린에너지 등 성장 테마 분석</li>
        <li>연준 통화정책, 금리, 고용 등 미국 매크로 경제 해설</li>
        <li>종목별 투자 포인트 정리</li>
      </ul>
      <h2>면책 조항</h2>
      <p>본 사이트의 모든 정보는 일반적인 투자 참고 목적으로만 제공되며, 특정 금융 상품의 매수·매도를 권유하는 투자 권유가 아닙니다. 페이지에 표시되는 시세는 외부 데이터를 기반으로 하며 지연될 수 있는 참고용 수치이고, 분석은 정성적 견해입니다. 투자 결정의 최종 책임은 투자자 본인에게 있습니다.</p>"""
    else:
        desc = "マーケットインサイトは米国市場の銘柄と米国経済の動向を分析する金融インサイト・プラットフォームです。"
        body = """      <h1>マーケットインサイトについて</h1>
      <p>マーケットインサイト（MarketInsight）は、米国市場の主要銘柄と米国経済の動向を分析する金融インサイト・プラットフォームです。個人投資家がより合理的な投資判断を下せるよう、専門的で深掘りした米国市場の分析コンテンツを提供します。</p>
      <h2>私たちの目標</h2>
      <p>複雑な米国市場のデータや企業ファンダメンタルズを、誰でも理解しやすい形で整理してお届けします。単なる情報提供にとどまらず、読者が自ら銘柄と市場を読み解く力を養えるようサポートします。</p>
      <h2>取り扱うコンテンツ</h2>
      <ul>
        <li>米国市場の主要銘柄のビジネスモデル・競争力・リスク分析</li>
        <li>AI・半導体・宇宙・クリーンエネルギーなど成長テーマの分析</li>
        <li>FRBの金融政策、金利、雇用など米国マクロ経済の解説</li>
        <li>銘柄ごとの投資ポイントの整理</li>
      </ul>
      <h2>免責事項</h2>
      <p>本サイトのすべての情報は一般的な投資参考目的のみで提供されており、特定の金融商品の売買を勧誘する投資勧誘ではありません。ページに表示される株価は外部データに基づき遅延する場合がある参考値であり、分析は定性的な見解です。投資決定の最終的な責任は投資家ご自身にあります。</p>"""
    return static_page(lang, "about.html", title, desc, body)


def render_contact(lang):
    title = ("문의 - " if lang == "ko" else "お問い合わせ - ") + LOGO[lang]
    if lang == "ko":
        desc = "마켓인사이트에 문의사항이나 제안 사항을 보내주세요."
        body = """      <h1>문의하기</h1>
      <p>콘텐츠 관련 의견, 광고 문의, 제보 등 어떤 내용이든 편하게 보내주세요. 최대한 빠르게 답변 드리겠습니다.</p>
      <form class="contact-form" id="contact-form">
        <div class="form-group">
          <label for="name">이름</label>
          <input type="text" id="name" name="name" placeholder="홍길동" required>
        </div>
        <div class="form-group">
          <label for="email">이메일</label>
          <input type="email" id="email" name="email" placeholder="example@email.com" required>
        </div>
        <div class="form-group">
          <label for="subject">문의 유형</label>
          <select id="subject" name="subject">
            <option value="general">일반 문의</option>
            <option value="content">콘텐츠 제보/제안</option>
            <option value="ad">광고 문의</option>
            <option value="error">오류 신고</option>
          </select>
        </div>
        <div class="form-group">
          <label for="message">내용</label>
          <textarea id="message" name="message" placeholder="문의 내용을 입력해 주세요." required></textarea>
        </div>
        <button type="submit" class="submit-btn" data-success="전송 완료">전송하기</button>
      </form>"""
    else:
        desc = "マーケットインサイトへのお問い合わせはこちらから。"
        body = """      <h1>お問い合わせ</h1>
      <p>コンテンツに関するご意見、広告のお問い合わせ、情報提供など、お気軽にお送りください。できる限り早くご返答いたします。</p>
      <form class="contact-form" id="contact-form">
        <div class="form-group">
          <label for="name">お名前</label>
          <input type="text" id="name" name="name" placeholder="山田太郎" required>
        </div>
        <div class="form-group">
          <label for="email">メールアドレス</label>
          <input type="email" id="email" name="email" placeholder="example@email.com" required>
        </div>
        <div class="form-group">
          <label for="subject">お問い合わせの種類</label>
          <select id="subject" name="subject">
            <option value="general">一般的なお問い合わせ</option>
            <option value="content">コンテンツの提案・情報提供</option>
            <option value="ad">広告のお問い合わせ</option>
            <option value="error">エラーの報告</option>
          </select>
        </div>
        <div class="form-group">
          <label for="message">メッセージ</label>
          <textarea id="message" name="message" placeholder="お問い合わせ内容をご入力ください。" required></textarea>
        </div>
        <button type="submit" class="submit-btn" data-success="送信完了">送信する</button>
      </form>"""
    return static_page(lang, "contact.html", title, desc, body)


def render_privacy(lang):
    title = ("개인정보처리방침 - " if lang == "ko" else "プライバシーポリシー - ") + LOGO[lang]
    if lang == "ko":
        desc = "마켓인사이트 개인정보처리방침"
        body = """      <h1>개인정보처리방침</h1>
      <p>마켓인사이트(이하 "사이트")는 이용자의 개인정보를 중요하게 생각하며, 관련 법령을 준수합니다.</p>
      <h2>1. 수집하는 개인정보 항목</h2>
      <ul>
        <li>방문 기록 및 쿠키 정보 (서비스 개선·광고 최적화 목적)</li>
        <li>문의 양식 이용 시 입력한 이름, 이메일 주소, 문의 내용</li>
      </ul>
      <h2>2. 개인정보의 이용 목적</h2>
      <ul>
        <li>서비스 이용 분석 및 품질 개선</li>
        <li>맞춤형 광고 제공 (Google AdSense 등 제3자 광고 네트워크)</li>
        <li>문의 사항 응대</li>
      </ul>
      <h2>3. 쿠키 사용</h2>
      <p>사이트는 쿠키를 사용해 이용자의 방문 기록 및 선호도를 저장합니다. 브라우저 설정에서 쿠키를 거부할 수 있으나, 일부 기능 이용이 제한될 수 있습니다.</p>
      <h2>4. 제3자 제공</h2>
      <p>사이트는 이용자의 동의 없이 개인정보를 제3자에게 제공하지 않습니다. 단, 법령에 따른 요구가 있는 경우는 예외입니다.</p>
      <h2>5. Google AdSense 및 광고 쿠키</h2>
      <p>당 사이트는 Google AdSense를 통해 광고를 게재합니다. Google을 포함한 제3자 광고 사업자는 쿠키를 사용하여 이용자의 이전 방문 기록을 바탕으로 맞춤형 광고를 제공합니다. Google이 광고 쿠키(DoubleClick 쿠키 포함)를 사용함에 따라, 이용자의 당 사이트 및 다른 웹사이트 방문 정보에 기반한 광고가 표시될 수 있습니다.</p>
      <p>이용자는 <a href="https://www.google.com/settings/ads" rel="noopener" target="_blank" style="color: var(--color-up);">Google 광고 설정</a>에서 맞춤형 광고를 비활성화할 수 있습니다. 또한 <a href="https://www.aboutads.info/choices/" rel="noopener" target="_blank" style="color: var(--color-up);">www.aboutads.info</a>에서 제3자 업체의 맞춤형 광고 쿠키 사용을 거부할 수 있습니다. Google의 광고 관련 데이터 처리에 대한 자세한 내용은 <a href="https://policies.google.com/technologies/partner-sites" rel="noopener" target="_blank" style="color: var(--color-up);">Google 정책</a>을 참고하세요.</p>
      <h2>6. 문의</h2>
      <p>개인정보 관련 문의는 <a href="contact.html" style="color: var(--color-up);">문의하기</a> 페이지를 통해 접수해 주세요.</p>
      <p style="margin-top: 32px; font-size: 12px; color: var(--text-muted);">최종 업데이트: 2026년 6월 16일</p>"""
    else:
        desc = "マーケットインサイトのプライバシーポリシー"
        body = """      <h1>プライバシーポリシー</h1>
      <p>マーケットインサイト（以下「当サイト」）は、ユーザーの個人情報を重要視し、関連法令を遵守します。</p>
      <h2>1. 収集する個人情報の項目</h2>
      <ul>
        <li>訪問記録およびCookie情報（サービス改善・広告最適化の目的）</li>
        <li>お問い合わせフォームご利用の際に入力されたお名前、メールアドレス、お問い合わせ内容</li>
      </ul>
      <h2>2. 個人情報の利用目的</h2>
      <ul>
        <li>サービス利用の分析および品質改善</li>
        <li>パーソナライズ広告の提供（Google AdSenseなどの第三者広告ネットワーク）</li>
        <li>お問い合わせへの対応</li>
      </ul>
      <h2>3. Cookieの使用について</h2>
      <p>当サイトはCookieを使用して、ユーザーの訪問記録や嗜好を保存します。ブラウザの設定でCookieを拒否できますが、一部の機能がご利用いただけなくなることがあります。</p>
      <h2>4. 第三者への提供</h2>
      <p>当サイトは、ユーザーの同意なく個人情報を第三者に提供しません。ただし、法令による要求がある場合は例外とします。</p>
      <h2>5. Google AdSenseおよび広告Cookie</h2>
      <p>当サイトはGoogle AdSenseを通じて広告を配信しています。Googleを含む第三者の広告事業者は、Cookieを使用してユーザーの過去の訪問履歴に基づくパーソナライズ広告を提供します。Googleが広告Cookie（DoubleClick Cookieを含む）を使用することにより、ユーザーの当サイトおよび他のウェブサイトへのアクセス情報に基づいた広告が表示される場合があります。</p>
      <p>ユーザーは <a href="https://www.google.com/settings/ads" rel="noopener" target="_blank" style="color: var(--color-up);">Google広告設定</a> でパーソナライズ広告を無効にできます。また <a href="https://www.aboutads.info/choices/" rel="noopener" target="_blank" style="color: var(--color-up);">www.aboutads.info</a> で第三者によるパーソナライズ広告Cookieの使用を拒否できます。Googleの広告に関するデータ処理の詳細は <a href="https://policies.google.com/technologies/partner-sites" rel="noopener" target="_blank" style="color: var(--color-up);">Googleのポリシー</a> をご覧ください。</p>
      <h2>6. お問い合わせ</h2>
      <p>個人情報に関するお問い合わせは <a href="contact.html" style="color: var(--color-up);">お問い合わせ</a> ページよりご連絡ください。</p>
      <p style="margin-top: 32px; font-size: 12px; color: var(--text-muted);">最終更新日: 2026年6月16日</p>"""
    return static_page(lang, "privacy-policy.html", title, desc, body)


def render_terms(lang):
    title = ("이용약관 - " if lang == "ko" else "利用規約 - ") + LOGO[lang]
    if lang == "ko":
        desc = "마켓인사이트 이용약관"
        body = """      <h1>이용약관</h1>
      <p>마켓인사이트(이하 "사이트")를 이용하시기 전에 본 약관을 주의 깊게 읽어 주세요. 사이트를 이용하시면 본 약관에 동의하는 것으로 간주됩니다.</p>
      <h2>제1조 (목적)</h2>
      <p>본 약관은 사이트가 제공하는 미국 시장 금융 정보 서비스의 이용 조건 및 절차, 이용자와 사이트 간의 권리·의무를 규정함을 목적으로 합니다.</p>
      <h2>제2조 (서비스 내용)</h2>
      <p>사이트는 미국 증시 종목 및 경제 관련 분석 콘텐츠를 제공합니다. 모든 콘텐츠는 정보 제공 목적이며 투자 권유가 아닙니다.</p>
      <h2>제3조 (면책 조항)</h2>
      <ul>
        <li>사이트의 정보는 정확성·완전성을 보증하지 않으며, 표시되는 시세는 외부 데이터로 지연될 수 있는 참고용입니다.</li>
        <li>투자 결정으로 인한 손해에 대해 사이트는 책임을 지지 않습니다.</li>
        <li>외부 링크(제3자 사이트) 콘텐츠에 대해 사이트는 책임을 지지 않습니다.</li>
      </ul>
      <h2>제4조 (지식재산권)</h2>
      <p>사이트에 게재된 모든 콘텐츠의 저작권은 마켓인사이트에 있으며, 무단 복제·배포를 금합니다.</p>
      <p style="margin-top: 32px; font-size: 12px; color: var(--text-muted);">최종 업데이트: 2026년 6월 16일</p>"""
    else:
        desc = "マーケットインサイトの利用規約"
        body = """      <h1>利用規約</h1>
      <p>マーケットインサイト（以下「当サイト」）をご利用になる前に、本規約をよくお読みください。当サイトをご利用いただくことで、本規約に同意したものとみなされます。</p>
      <h2>第1条（目的）</h2>
      <p>本規約は、当サイトが提供する米国市場の金融情報サービスの利用条件・手続き、ユーザーと当サイト間の権利・義務を定めることを目的とします。</p>
      <h2>第2条（サービス内容）</h2>
      <p>当サイトは、米国市場の銘柄および経済に関する分析コンテンツを提供します。すべてのコンテンツは情報提供目的であり、投資勧誘ではありません。</p>
      <h2>第3条（免責事項）</h2>
      <ul>
        <li>当サイトの情報は正確性・完全性を保証せず、表示される株価は外部データに基づき遅延する場合がある参考値です。</li>
        <li>投資判断による損害について、当サイトは一切責任を負いません。</li>
        <li>外部リンク（第三者サイト）のコンテンツについて、当サイトは責任を負いません。</li>
      </ul>
      <h2>第4条（知的財産権）</h2>
      <p>当サイトに掲載されているすべてのコンテンツの著作権はマーケットインサイトに帰属し、無断複製・転載を禁じます。</p>
      <p style="margin-top: 32px; font-size: 12px; color: var(--text-muted);">最終更新日: 2026年6月16日</p>"""
    return static_page(lang, "terms.html", title, desc, body)


def static_page(lang, slug, title, desc, body):
    active = slug if slug in ("about.html", "contact.html") else ""
    h = head(lang, title, desc, slug, slug)
    hn = header_nav(lang, active, slug)
    return f"""{h}
{hn}
  <main>
    <div class="static-page">
{body}
    </div>
  </main>
{footer(lang)}"""


def render_root_index():
    return """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="0; url=ko/index.html">
  <title>MarketInsight</title>
  <link rel="canonical" href="ko/index.html">
</head>
<body>
  <p>Redirecting… <a href="ko/index.html">Click here if not redirected</a></p>
</body>
</html>
"""


def render_ads_txt():
    # ads.txt authorizes Google to sell ad inventory for this domain.
    pub = ADSENSE_CLIENT.replace("ca-", "")  # ads.txt uses pub-XXXX (no "ca-")
    return f"google.com, {pub}, DIRECT, f08c47fec0942fa0\n"


def render_robots():
    return f"""User-agent: *
Allow: /

Sitemap: {SITE}/sitemap.xml
"""


def render_sitemap():
    pages = ["index.html", "stock-analysis.html", "economy-trends.html",
             "about.html", "contact.html", "privacy-policy.html", "terms.html"]
    pages += [f"post-{t['slug']}.html" for t in TICKERS]
    urls = []
    for p in pages:
        prio = "1.0" if p == "index.html" else ("0.8" if p in ("stock-analysis.html", "economy-trends.html") else "0.7")
        freq = "daily" if p == "index.html" else "weekly"
        for lang in ("ko", "ja"):
            urls.append(f"""  <url>
    <loc>{SITE}/{lang}/{p}</loc>
    <lastmod>2026-06-16</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{prio}</priority>
    <xhtml:link rel="alternate" hreflang="ko" href="{SITE}/ko/{p}"/>
    <xhtml:link rel="alternate" hreflang="ja" href="{SITE}/ja/{p}"/>
  </url>""")
    body = "\n".join(urls)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
{body}
</urlset>
"""


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True) if os.path.dirname(path) else None
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    for lang in ("ko", "ja"):
        write(f"{lang}/index.html", render_index(lang))
        write(f"{lang}/stock-analysis.html", render_hub(lang))
        write(f"{lang}/economy-trends.html", render_economy(lang))
        write(f"{lang}/about.html", render_about(lang))
        write(f"{lang}/contact.html", render_contact(lang))
        write(f"{lang}/privacy-policy.html", render_privacy(lang))
        write(f"{lang}/terms.html", render_terms(lang))
        for t in TICKERS:
            write(f"{lang}/post-{t['slug']}.html", render_post(t, lang))
    write("index.html", render_root_index())
    write("sitemap.xml", render_sitemap())
    write("ads.txt", render_ads_txt())
    write("robots.txt", render_robots())
    print(f"Generated {len(TICKERS)} tickers x2 langs + structural pages + ads.txt/robots.txt.")


if __name__ == "__main__":
    main()
