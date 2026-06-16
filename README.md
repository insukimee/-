# 마켓인사이트 (MarketInsight)

미국 증시 핵심 종목과 미국 경제 흐름을 분석하는 한국어/일본어 금융 인사이트 정적 웹사이트입니다.

## 구성

```
.
├── index.html              # 루트 → ko/index.html 리다이렉트
├── sitemap.xml             # hreflang alternate 포함 사이트맵 (생성됨)
├── generate.py             # 전체 페이지 생성 스크립트 (티커 데이터 + 템플릿)
├── css/style.css           # 다크 테마 반응형 디자인 시스템
├── js/main.js              # 햄버거 내비, 쿠키 배너, 스크롤 애니메이션
├── ko/                     # 한국어 버전 (생성됨)
│   ├── index.html / stock-analysis.html / economy-trends.html
│   ├── post-<ticker>.html  # 종목별 분석 페이지 23개
│   └── about.html / contact.html / privacy-policy.html / terms.html
└── ja/                     # 일본어 버전 (동일 구조, 생성됨)
```

각 페이지는 헤더의 `🌐 KR/JP` 버튼과 `hreflang` 메타로 다른 언어 버전과 상호 링크됩니다.

## 다루는 종목 (23종)

`stock-analysis.html` 허브에서 섹터별로 묶어 보여줍니다.

| 섹터 | 티커 |
|------|------|
| 반도체 | NVDA, TSM |
| AI·소프트웨어 | GOOGL, AAPL, AMZN, ORCL, PLTR, IONQ |
| IT인프라·하드웨어 | IBM, CSCO, DELL |
| 사이버보안 | CIBR (ETF) |
| 우주·방산 | SPCX(SpaceX, 비상장), RDW, BWXT, TDY, MOG.A |
| 클린에너지·전력 | FSLR, BE, VRT |
| 전기차 | TSLA |
| 핀테크 | HOOD |
| 게임 | TTWO |

> SPCX(스페이스X)는 비상장 기업이라 일반 주식으로 거래되지 않으며, 비상장/프리IPO 관점으로 분석합니다.

## 페이지 생성

콘텐츠/티커를 수정하려면 `generate.py`의 데이터를 고친 뒤 다시 실행합니다.

```bash
python3 generate.py   # ko/ ja/ 의 모든 HTML과 sitemap.xml 재생성
```

## 로컬 실행

```bash
python3 -m http.server 8000
# http://localhost:8000/ 접속 (→ ko/index.html 로 이동)
```

## 배포

`main` 브랜치에 푸시하면 `.github/workflows/deploy.yml` 이 GitHub Pages로 자동 배포합니다.
(저장소 Settings → Pages → Source: GitHub Actions 가 설정되어 있어야 함)

라이브 주소: `https://insukimee.github.io/-/`

## 면책

본 사이트의 콘텐츠는 정보 제공 목적이며 투자 권유가 아닙니다. 실시간 시세가 아닌 정성적 분석이며,
투자 판단의 최종 책임은 투자자 본인에게 있습니다.
