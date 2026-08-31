# -*- coding: utf-8 -*-
"""YouTube Shorts 대본 초안 생성기.

generate.py의 티커 데이터(TICKERS)를 'YouTube Shorts 보이스 가이드' 템플릿
(0-3초 훅 / 3-15초 상황설명 / 15-40초 인사이트 / 40-55초 결론 / 55-60초 클로징)에
채워 넣어 shorts/<slug>.md 초안을 만든다.

주의: 여기서 뽑아내는 본문은 generate.py의 정식 분석 문구(문어체)를 그대로
가져온 것이라 가이드의 4대 원칙(번역체·확률적 표현·구어체 등)이 아직 반영되지
않은 '재료' 상태다. 실제 촬영 전에는 가이드 3장 규칙에 맞춰 사람이 다듬거나
LLM으로 한 번 더 구어체 변환을 거쳐야 한다. 체크리스트 항목도 그 다듬기 여부를
사람이 직접 표시하도록 비워 둔다.
"""
import argparse
import os
import re

from generate import TICKERS

OUT_DIR = "shorts"

HOOK_BANK = [
    "{name}, 이거 모르면 이번 주 손해봅니다",
    "다들 {name} 이거 놓쳤어요",
    "{name}, 차트 하나로 설명할게요",
]

TRANSITIONS = ["쉽게 말하면", "결론부터 말하면", "여기서 포인트는"]

CLOSERS = [
    "판단은 각자의 몫이지만, 저는 이렇게 보고 있어요",
    "투자는 결국 본인 책임, 그래도 감은 잡고 가야죠",
]

DISCLAIMER = (
    "⚠️ 이 대본은 초안이에요. \"무조건\", \"확정 수익\", \"지금이 마지막 기회\" 같은 "
    "표현은 오해 소지가 있으니 최종 대본에서는 피해주세요. 투자 판단의 책임은 "
    "시청자 본인에게 있다는 점도 클로징에서 짚어주세요."
)

CHARS_PER_SEC = 6.5  # 한국어 내레이션 속도 추정치(자/초) — 길이 자가 점검용


def estimate_seconds(text):
    return len(re.sub(r"\s+", "", text)) / CHARS_PER_SEC


def build_sections(t, index):
    name, sym = t["nko"], t["sym"]
    overview, points, risk, verdict = (b[0] for b in t["bodies"])
    hook = HOOK_BANK[index % len(HOOK_BANK)].format(name=name)
    insight = f"{TRANSITIONS[0]}, {overview}\n\n{TRANSITIONS[2]}: {points}\n\n{risk}"
    conclusion = f"{verdict}\n\n{CLOSERS[index % len(CLOSERS)]}"
    closing = f"다음 영상에서는 다른 종목 얘기해볼게요."
    return [
        ("0-3초 · 훅", hook),
        ("3-15초 · 상황 설명", t["lead_ko"]),
        ("15-40초 · 핵심 인사이트", insight),
        ("40-55초 · 그래서 어떻게?", conclusion),
        ("55-60초 · 클로징 훅", closing),
    ]


def build_markdown(t, index):
    sections = build_sections(t, index)
    total = sum(estimate_seconds(text) for _, text in sections)
    fit = "45~60초 목표 범위 내" if 45 <= total <= 60 else "범위 밖 — 길이 조정 필요"
    body = "\n\n".join(f"## [{label}]\n{text}" for label, text in sections)
    checklist = "\n".join([
        "- [ ] 3초 안에 궁금증을 유발했는가?",
        "- [ ] 전문 용어를 한 번이라도 \"번역\"했는가?",
        "- [ ] 숫자 뒤에 \"그래서 어떻다\"는 해석이 붙었는가?",
        "- [ ] 확정적 투자 권유 표현이 없는가?",
        "- [ ] 소리 내어 읽었을 때 자연스러운가? (문어체 X)",
        "- [ ] 마지막에 다음 콘텐츠로 이어지는 훅이 있는가?",
    ])
    return f"""# {t['nko']} ({t['sym']}) — Shorts 대본 초안

> 자동 생성: `generate.py` 티커 데이터 + YouTube Shorts 보이스 가이드 템플릿
> 예상 길이: 약 {total:.0f}초 ({fit})

{body}

---

## 체크리스트
{checklist}

---

{DISCLAIMER}
"""


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ticker", help="특정 심볼만 생성 (예: NVDA)")
    parser.add_argument("--out", default=OUT_DIR, help="출력 디렉터리 (기본: shorts)")
    args = parser.parse_args()

    tickers = TICKERS
    if args.ticker:
        sym = args.ticker.upper()
        tickers = [t for t in TICKERS if t["sym"] == sym]
        if not tickers:
            parser.error(f"티커를 찾을 수 없음: {args.ticker}")

    for i, t in enumerate(tickers):
        write(f"{args.out}/{t['slug']}.md", build_markdown(t, i))

    print(f"Generated {len(tickers)} Shorts 대본 초안 → {args.out}/")


if __name__ == "__main__":
    main()
