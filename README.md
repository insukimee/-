# 마켓인사이트 (MarketInsight)

주식·기업·경제 흐름을 분석하는 한국어/일본어 금융 인사이트 정적 웹사이트입니다.

## 구성

```
.
├── index.html              # 루트 → ko/index.html 리다이렉트
├── sitemap.xml             # hreflang alternate 포함 사이트맵
├── css/style.css           # 다크 테마 반응형 디자인 시스템
├── js/main.js              # 햄버거 내비, 쿠키 배너, 스크롤 애니메이션
├── ko/                     # 한국어 버전
│   ├── index.html
│   ├── stock-analysis.html / company-analysis.html / economy-trends.html
│   ├── post-samsung-electronics.html / post-ai-semiconductor.html
│   ├── post-kospi-scenario.html / post-dividend-portfolio.html
│   ├── about.html / contact.html / privacy-policy.html / terms.html
└── ja/                     # 일본어 버전 (동일 구조)
    ├── post-toyota-motor.html / post-ai-semiconductor.html
    └── post-nikkei-scenario.html / post-dividend-portfolio.html
```

각 글은 헤더의 `🌐 KR/JP` 버튼과 `hreflang` 메타로 다른 언어 버전과 상호 링크됩니다.

## 로컬 실행

정적 사이트라 빌드가 필요 없습니다. 아무 정적 서버로 열면 됩니다.

```bash
python3 -m http.server 8000
# http://localhost:8000/ 접속 (→ ko/index.html 로 이동)
```

## 배포 (GitHub Pages)

`main` 브랜치에 푸시하면 `.github/workflows/deploy.yml` 워크플로가 자동으로
GitHub Pages에 배포합니다.

### ⚠️ 배포 전 필수 단계 (한 번만)

GitHub Pages는 **public 저장소**에서만 무료로 동작합니다. 현재 저장소가
**private** 이면 배포가 `Resource not accessible by integration` 오류로 실패합니다.

다음 중 하나를 진행하세요.

1. **저장소를 public 으로 전환 (권장·무료)**
   - `Settings → General → Danger Zone → Change repository visibility → Public`
   - 전환 후 다음 푸시(또는 `Actions` 탭에서 Re-run)부터 워크플로가
     Pages 사이트를 **자동 생성·배포**합니다. (추가 수동 설정 불필요)

2. **private 유지 + GitHub Pro/Team 플랜**
   - Pro/Team 이상이면 private 저장소에서도 Pages 사용 가능
   - 이후 동일하게 푸시/재실행하면 배포됩니다.

### 배포 후 주소

```
https://insukimee.github.io/-/
```

(루트 접속 시 `ko/index.html` 로 자동 이동)

## 면책

본 사이트의 콘텐츠는 정보 제공 목적이며 투자 권유가 아닙니다.
