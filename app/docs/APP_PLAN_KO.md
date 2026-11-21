# US Market Insight Android 앱 계획

확인 날짜: 2026-11-03. 정책 문서는 그날 연 페이지 기준이며, 제출 전에 같은 URL을 다시 열어야 합니다. 열지 못한 항목은 "확인 필요"로 적었습니다.

앱 표시 이름과 한국어·일본어 스토어 표시명은 **US Market Insight**로 확정입니다(17자, Play 제목 한도 30). "US 마켓인사이트" 등 한글 표기는 앱 이름·스토어 이름에 쓰지 않습니다. 한글 "마켓인사이트" 단독·유사 표기는 한국경제신문 자본시장 서비스와 혼동될 수 있어 사용하지 않습니다. 근거(2026-11-03): [marketinsight.hankyung.com](https://marketinsight.hankyung.com/), App Store 앱 이름 "마켓인사이트"(The Korea Economic Daily, <https://apps.apple.com/kr/app/id802681902>). Google Play의 동일 이름 상세 URL은 이번 검색에서 특정하지 못했습니다. `applicationId`는 확정이 아닙니다.

## 1. 방식을 고른 이유

| 방식 | 판단 |
| --- | --- |
| 기존 Bubblewrap TWA (`STORE_PUBLISHING.md`, `twa-manifest.json`) | 사이트를 Chrome Custom Tab/TWA로 여는 래퍼에 가깝다. 관심 목록·AdMob·FCM·최초 고지를 앱 기능으로 넣기 어렵다. Digital Asset Links가 호스트 루트에 있어야 주소창이 사라진다. |
| PWABuilder iOS 패키지 | 이번 범위가 아니다. 단순 웹 래퍼로 보이기 쉽다. |
| React Native / 완전 네이티브 | 이미 있는 HTML 분석을 다시 짜야 한다. 1차 범위에 비해 크다. |
| Capacitor 8 | 번들 HTML 위에 셸을 얹고, 네이티브 플러그인만 붙인다. 웹 자산을 로컬에 두므로 원격 URL만 여는 래퍼와 구분된다. |

**선택: Capacitor. TWA는 대체합니다.** 웹사이트용 PWA(홈 화면 추가)는 그대로 둬도 됩니다. Play에 TWA 앱과 Capacitor 앱을 둘 다 올리면 사용자가 갈라지므로, 스토어 앱은 Capacitor 하나만 두는 쪽을 제안합니다. `twa-manifest.json`과 `STORE_PUBLISHING.md`는 이번 PR에서 지우지 않습니다. 스토어 경로의 본선은 `app/`입니다.

Android를 먼저 올리고, iOS는 TestFlight로 시험을 앞당깁니다. `ios/`는 Capacitor 8의 Swift Package Manager 프로젝트입니다. 빌드와 업로드는 맥에서만 됩니다. 절차는 `IOS_TESTFLIGHT_KO.md`입니다.

## 2. 아키텍처

```
app/
  app.config.json          사이트 주소, 가칭 applicationId, 광고·푸시 설정
  capacitor.config.json    appName = US Market Insight, webDir = www
  shell/src                셸 원본 (탭, 관심 목록, 동의, AdMob, FCM)
  scripts/build-www.mjs    ko/ ja/ css/ js/ icons 를 www 로 복사하고 셸을 주입
  www/                     빌드 산출물. gitignore
  android/                 커밋. 키스토어와 google-services.json 은 제외
  native-extras/           패치 원본 (토픽 플러그인, 서명 예시, Firebase 예시)
```

셸은 프레임워크 없이 기존 HTML 위에 붙입니다. 이유는 분석 글을 다시 컴포넌트로 옮기지 않아도 되고, 오프라인 번들이 사이트와 같은 파일이기 때문입니다. 번들러는 esbuild 하나이고, 산출물은 `www/shell/app.js`입니다.

Capacitor `server.url`은 비워 둡니다. 앱이 켜지면 `https://localhost`의 로컬 파일을 읽습니다. 원격 사이트는 공유 URL, 약관 링크, `feed.json` 확인에만 씁니다.

복사본에서 하는 일 (사이트 원본은 수정하지 않음):

- AdSense 스크립트와 `.ad-container` 제거
- 서비스 워커 등록을 앱에서만 끔 (`window.__MI_APP__`)
- 셸 CSS/JS 주입

관심 목록은 `@capacitor/preferences`에만 저장합니다. 웹 미리보기에서 이 플러그인은 localStorage를 백엔드로 쓰지만, 앱 코드는 localStorage를 직접 부르지 않습니다. Android에서는 SharedPreferences입니다. 계정과 당사 서버는 없습니다.

## 3. 패키지명 후보

Play에 한 번 게시되면 `applicationId`는 바꿀 수 없습니다. 코드의 현재 값은 **1순위이며 확정 전**입니다.

| 순위 | applicationId | 메모 |
| --- | --- | --- |
| 1 (코드에 넣음) | `com.usmarketinsight.app` | `usmarketinsight.com`의 역도메인 + `app` |
| 2 | `com.usmarketinsight.android` | 플랫폼이 이름에 들어 있어 iOS 번들 ID와 역할을 나누기 쉽다 |
| 3 | `com.usmarketinsight.reader` | 읽기 전용 정보 앱이라는 점을 이름에 담음 |

기존 TWA 초안의 `io.github.insukimee.marketinsight` (`twa-manifest.json`)는 GitHub 계정 기준이라 도메인 이전과 무관합니다. Play가 그 ID를 이미 쓰는지 이 저장소만으로는 알 수 없습니다. 게시된 적이 없다면 버려도 됩니다. 게시된 적이 있으면 그 앱을 업데이트하는 쪽과 새 ID로 내는 쪽을 사장님이 정해야 합니다.

도메인 이전 전에 `com.usmarketinsight.*`를 써도 되는지에 대해, Play의 applicationId는 TWA의 Digital Asset Links와 다릅니다. 이번 조사에서 Play가 applicationId에 대해 DNS 소유권을 검사한다는 도움말은 찾지 못했습니다. 그래서 기술적으로는 이전 전에도 그 문자열을 쓸 수 있습니다. 위험은 따로 있습니다. 게시 후 변경이 불가하고, 다른 개발자가 같은 ID를 먼저 올리면 그 ID는 쓸 수 없으며, 도메인을 아직 보유하지 않은 채 그 브랜드의 역도메인을 쓰면 나중에 브랜드 분쟁이 생길 수 있습니다. 확정 전에 Play Console에서 ID를 점유하는 업로드를 하지 않는 편이 안전합니다.

## 4. 도메인 이전

`app.config.json`의 `siteBaseUrl` 기본값은 `https://insukimee.github.io/-`입니다. `usmarketinsight.com`으로 바꿀 때는 이 한 줄과, 사이트가 생기게 될 `feed.json`의 `url` 필드를 맞춥니다. 앱 안에 복사된 HTML은 다시 `npm run build:www`를 해야 최신 글이 바뀝니다. 공유 시트에 나가는 링크는 설정값을 바로 탑니다.

## 5. 기능 상태

| 기능 | 상태 | 근거 |
| --- | --- | --- |
| 로컬 번들 (`ko/`, `ja/`, css, js, icons) | 구현됨 | `npm test`가 광고 제거와 23개 종목 목록을 확인 |
| 하단 탭, 다크 셸, 고지 바, 세이프 에어리어 CSS | 구현됨 | Chrome 390×844에서 동의·홈·종목·관심·설정·일본어 화면을 확인 |
| Android 뒤로 가기, 상태바 색 | 코드 있음 | `@capacitor/app`, `@capacitor/status-bar`. 실기기에서 누르는 동작은 미확인 |
| 관심 종목 추가/삭제 | 구현됨 | Preferences API. 브라우저에서 별표 후 관심 탭에 NVDA가 보임. 기기 SharedPreferences는 미확인 |
| 오프라인 배너 + 번들 열람 | 구현됨 | 브라우저 `offline` 이벤트로 배너 표시를 확인. 비행기 모드 기기는 미확인 |
| 원격 `feed.json` 갱신 | 목업 | 원격이 없거나 실패하면 `shell/feed.sample.json`. 사이트에 피드 파일이 아직 없음 |
| 네이티브 공유 | 코드 있음 | `@capacitor/share`. 공유 시트는 기기에서 미확인. 실패 시 클립보드 |
| AdMob 배너 + UMP | 코드 있음 | 샘플 광고 단위만 커밋. 브라우저에서는 "테스트 광고 슬롯" 목업. **테스트 광고가 기기에 뜨는 것은 미확인** |
| FCM 등록, Android 13+ 권한, 토픽 구독 | 코드 있음 | `google-services.json`이 없으면 토큰이 나오지 않고 나머지 기능은 동작. **수신 미확인** |
| 로컬 알림 | 없음 | 푸시가 본선. 사용자별 시각 알림은 토픽으로 불가해 넣지 않음 |
| 최초 실행 고지, 정보 화면, 버전 | 구현됨 | 고지 버전 `2026-11-03`. 거부 대신 "확인하고 계속" |
| ko/ja, 기기 언어로 시작 | 구현됨 | 저장값이 없으면 `ja`로 시작하는 언어만 일본어, 그 외 한국어 |
| 아이콘·피처 그래픽 | 가안 | `scripts/gen-icons.py`. 사장님 확정 전 |
| iOS 프로젝트, 샘플 AdMob, ATT 문구, 푸시 엔타이틀먼트 | 코드 있음. Linux에서 컴파일하지 못함. 아이폰 실행은 미확인 |

## 6. 광고

앱 안 AdSense(웹 태그)는 쓰지 않습니다. AdSense 정책은 앱 WebView의 웹 광고를 일반 앱 광고 경로로 보지 않고, 잘못된 게재는 계정 정지로 이어질 수 있습니다. 사이트 페이지를 복사할 때 광고 태그를 제거하는 이유가 이것입니다.

플러그인 비교:

| 플러그인 | 판단 |
| --- | --- |
| `@capacitor-community/admob` 8.3.0 | 채택. Capacitor 8.5+용. 배너 API와 UMP(`requestConsentInfo`, `showConsentForm`)가 있음 |
| Cordova AdMob 브리지 | Capacitor 프로젝트에 Cordova를 한 겹 더 얹음 |
| 네이티브 SDK를 직접 호출 | 가능하지만 셸이 JavaScript라 브리지를 또 만들어야 함 |

형식은 **하단 적응형 배너만** 1차에 넣습니다.

- 전면 광고는 글을 읽다 가리고, 실수로 누르기 쉬워 무효 트래픽과 심사 거절 위험이 큽니다.
- 네이티브 광고는 분석 문단과 섞이면 투자 권유로 오해됩니다.
- 배너는 탭 바로 위에 두고, 동의 화면이 떠 있는 동안에는 요청하지 않습니다.
- 광고 문구로 클릭을 유도하지 않습니다.
- `tagForChildDirectedTreatment: false`, `tagForUnderAgeOfConsent: false`, `maxAdContentRating: Teen`.
- `useTestAds: true`인 동안 샘플 단위만 요청합니다. 운영 ID가 `REPLACE_`로 남아 있으면 요청 자체를 막습니다.

커밋된 샘플 값 (Google이 공개한 테스트 ID, 비밀 아님):

- 앱 ID `ca-app-pub-3940256099942544~3347511713` (`strings.xml`의 `admob_app_id`)
- 배너 `ca-app-pub-3940256099942544/6300978111`

운영 앱 ID와 광고 단위는 `app.config.json`에 자리만 있습니다. AdMob 계정은 사장님이 만듭니다. 우리는 만들지 않습니다.

UMP: EEA/영국 등에서 Google이 요구하는 동의는 플러그인의 UMP 호출로 연결해 두었습니다. 동의 폼 문구·게시 여부는 AdMob 콘솔 설정입니다. 한국 개인정보보호법과 일본 개인정보보호법에서 맞춤 광고·국외 이전에 어떤 고지가 더 필요한지는 법률 자문이 필요하며, 여기서 단정하지 않습니다.

어린이 대상이 아닙니다. Play의 "아동용으로 설계"와 Families 프로그램에 넣지 않는 쪽을 제안합니다.

AdMob 콘솔에서 도박 등 민감 카테고리를 막는 설정이 있습니다. 금융 상품 광고를 막을지는 사장님 판단입니다. 분석 글 옆에 다른 투자 상품 광고가 붙으면 권유로 보일 수 있습니다. 정확한 차단 카테고리 이름은 콘솔에서 확인이 필요합니다.

`AD_ID` 권한은 매니페스트에 선언했습니다. 이 권한이 없으면 Android 13 이상에서 광고 ID가 0으로 바뀝니다.

`app-ads.txt`: AdMob은 스토어에 적은 개발자 웹사이트의 **루트**에 `app-ads.txt`를 둡니다. 지금 저장소의 `ads.txt`는 웹 AdSense용이고 `app-ads.txt`를 대신하지 않습니다. `insukimee.github.io/-/ads.txt`는 호스트 루트가 아닙니다. 도메인이 `usmarketinsight.com`으로 옮겨진 뒤, 그 루트에 `app-ads.txt`를 두고 Play의 개발자 웹사이트를 그 도메인으로 맞추는 구성을 제안합니다. 파일 형식의 최신 예시는 제출 전 AdMob 도움말에서 다시 확인이 필요합니다. <https://support.google.com/admob/answer/9363762>

## 7. 푸시

안드로이드는 FCM이 본선입니다. iOS도 같은 토픽 이름을 쓰도록 JS를 맞춰 두었으나, Firebase iOS SDK는 아직 링크하지 않아 토픽 구독은 거절됩니다. 실수신은 APNs 키와 `GoogleService-Info.plist` 이후입니다. 자세한 표는 `IOS_TESTFLIGHT_KO.md`입니다.

로컬 알림으로 "요일·시각"을 받지 않는 이유: 토픽 메시지는 구독자 전원에게 같은 시각에 나갑니다. 기기마다 다른 시각은 토큰을 서버에 저장하거나 로컬 알람이 필요합니다. 1차는 토큰 서버를 두지 않습니다.

토픽 이름:

- 관심 종목 `ticker-{slug}` (`MOG.A`는 `ticker-mog-a`)
- 오늘의 분석 `digest-ko`, `digest-ja`

권한은 설정의 알림 스위치를 켤 때만 요청합니다. 거부되면 스위치가 꺼지고, 글과 관심 목록은 그대로입니다.

`google-services.json`이 없으면 FirebaseInit이 되지 않아 토픽 호출이 실패합니다. 그 실패는 설정 화면에 문장으로 남고 앱은 계속됩니다. 파일 예시는 `native-extras/google-services.json.example`이고, 실제 파일은 gitignore입니다.

### 서버 비교

| | (a) GitHub Actions + FCM HTTP v1 | (b) Cloud Functions / Cloud Run | (c) VPS |
| --- | --- | --- | --- |
| 비용 | FCM은 Firebase 요금표에서 No-cost. Actions 분 과금은 저장소가 공개인지에 따라 달라질 수 있어 확인 필요 | Functions는 Spark에 없고 Blaze가 필요. 요금표의 무료 구간 초과분과 빌드 이미지 저장 소액이 생길 수 있음 | 상시 요금, OS 패치 |
| 운영 | 배포 워크플로 뒤에 붙임. 상시 프로세스 없음 | 함수 배포·요금 알림 | 서버 점검, 장애 |
| 키 | 서비스 계정 JSON은 GitHub Secret. 저장소에 두지 않음 | 함수 런타임 서비스 계정. 키 파일을 레포에 두지 않음 | 디스크에 키를 두면 유출 면이 큼 |
| 난이도 | 피드 diff와 curl. 낮음 | 중간 | 높음 |
| 관심 종목별 알림 | 가능. 앱이 `ticker-nvda`를 구독하고 워크플로가 그 토픽으로 보냄. 사용자 명단이 필요 없음 | 가능. 토큰 DB까지 가면 개인별 시각도 가능 | 가능 |
| 한계 | 토픽은 개인 타깃이 아님. 구독 속도 제한, 다운스트림 기본 분당 60만 메시지, 토픽 페이로드 2048바이트. 인스턴스당 토픽 2000개(종목 23개면 충분). 워크플로 시간 제한과 재시도는 YAML에서 10분과 429 재시도를 제안 | Blaze 결제 수단이 필요 | 운영 부담 |

출처 (2026-11-03에 연 페이지의 요약):

- FCM No-cost, Functions는 Blaze 전용: <https://firebase.google.com/pricing>
- 토픽은 클라이언트 `subscribeToTopic`으로 생성·구독, 인스턴스당 2000, 구독 429: <https://firebase.google.com/docs/cloud-messaging/android/topic-messaging>
- 분당 한도와 429: <https://firebase.google.com/docs/cloud-messaging/throttling-and-quotas>
- 토픽 메시지 2048바이트: <https://firebase.google.com/docs/reference/fcm/rest/v1/ErrorCode>

**권장: (a).** 사이트가 정적이고 종목 수가 적어, 관심 종목 알림은 서버 없이 토픽 구독으로 됩니다. 사용자별 시각이 필요해지면 그때 (b)를 검토합니다. (c)는 권하지 않습니다.

제안 YAML은 `docs/proposals/fcm-dispatch.workflow.yml`에만 있습니다. `.github/workflows`에는 넣지 않았습니다. 서비스 계정과 Firebase 프로젝트는 사장님이 만듭니다.

사이트에 제안하는 `feed.json` 스키마는 `docs/proposals/feed.schema.json`입니다. `generate.py`가 티커 루프의 제목·날짜·언어로 `items`를 만들고 `sitemap` 옆에 쓰면 됩니다. 이번 PR은 `generate.py`를 수정하지 않습니다. 앱은 파일이 없으면 샘플로 떨어집니다.

## 8. 개인정보 흐름

| 데이터 | 기기 밖 | 받는 쪽 |
| --- | --- | --- |
| 관심 종목, 언어, 고지 동의, 본 피드 id | 나가지 않음 | 없음 |
| FCM 등록 토큰 | 알림을 켜면 Google로 감 | Firebase. 우리 서버에는 저장하지 않음 |
| 광고 ID, 앱 세트 ID, IP로 추정한 대략 위치, 광고 상호작용, 진단 | AdMob SDK가 수집·공유 | Google. [AdMob Play 데이터 공개](https://developers.google.com/admob/android/privacy/play-data-disclosure) |
| 온라인일 때 TradingView 위젯 | 위젯이 제3자 요청 | TradingView. Data safety에 넣을지는 확인 필요 |

Play의 "수집"은 기기 밖으로 나가는 데이터입니다. 관심 목록만 놓고 보면 개발자 수집이 아닙니다. 광고 SDK와 FCM은 수집·공유에 넣어야 합니다. 판매하지 않습니다. 맞춤 광고를 켜면 Play의 "추적" 정의에 들어갈 수 있습니다. UMP에서 비맞춤만 허용하면 답이 달라질 수 있어, 추적 예/아니오의 최종 칸은 확인 필요로 남깁니다.

### 개인정보처리방침에 넣을 문장 초안 (사이트 PR에서 사용)

한국어:

> US Market Insight 앱은 웹사이트와 별도로 다음을 처리합니다. 관심 종목, 표시 언어, 고지 동의 여부는 이용자 기기에만 저장하며 당사 서버로 전송하지 않습니다. 알림을 켜면 Firebase Cloud Messaging이 푸시 토큰(기기 식별자)을 만들고, Google이 알림 전달을 위해 이를 처리합니다. 당사는 그 토큰을 자체 서버에 저장하지 않습니다. 앱 광고는 Google AdMob으로 게재합니다. Google은 광고 ID, 앱 세트 ID, IP 주소에서 추정한 대략적인 위치, 광고와의 상호작용, 진단 정보를 수집하고 광고·분석·부정 이용 방지 목적으로 처리할 수 있습니다. 이 앱은 아동을 대상으로 하지 않습니다. 유럽경제지역과 영국 등에서는 Google의 광고 동의 창이 추가로 표시될 수 있습니다. 웹사이트의 Google AdSense는 앱 안에서 사용하지 않습니다.

日本語:

> US Market Insight アプリは、ウェブサイトとは別に次を扱います。関心銘柄、表示言語、注意事項への同意は利用者の端末だけに保存し、当社のサーバーへは送りません。通知をオンにすると Firebase Cloud Messaging がプッシュトークン（端末の識別子）を作り、Google が通知の配信のために処理します。当社はそのトークンを自社サーバーに保存しません。アプリ内広告は Google AdMob で表示します。Google は広告 ID、アプリセット ID、IP アドレスから推定したおおまかな位置情報、広告との相互作用、診断情報を、広告・分析・不正防止のために収集し共有することがあります。このアプリは子どもを対象にしません。欧州経済領域や英国などでは Google の広告同意フォームが追加で表示されることがあります。ウェブサイトの Google AdSense はアプリ内では使いません。

이 문장을 사이트 `privacy-policy.html`에 반영하는 변경은 이번 PR에 없습니다.

## 9. 아이콘

`scripts/gen-icons.py`가 사이트와 같은 상승 막대 도안으로 다음을 만듭니다.

- 1024 마스터, Play 아이콘 512, 피처 그래픽 1024×500 (`resources/play/`)
- Android 레거시 mipmap, adaptive foreground, 배경색 `#0D0D0D`

Play 아이콘 요건(2026-11-03, [미리보기 애셋](https://support.google.com/googleplay/android-developer/answer/9866151)): 512×512, 32비트 PNG(알파), 1024KB 이하. 피처 그래픽은 1024×500, JPEG 또는 알파 없는 24비트 PNG.

adaptive icon은 API 26+에서 원형·스퀴클 마스크에 잘립니다. 막대는 중앙 안전 영역 안에 두었습니다.

1024 마케팅 아이콘은 알파 없는 RGB PNG로 `resources/ios/AppIcon-1024.png`에 두었습니다. 도안은 가안입니다.

도안은 가안입니다. 사장님 확정 전에는 스토어에 최종 자산으로 올리지 않습니다.

## 10. 사이트 쪽 필요 변경 제안 (이번 PR에서는 안 함)

- `generate.py`가 `feed.json`을 루트에 생성
- 개인정보처리방침·이용약관에 위 앱 문단 추가 (ko/ja)
- 도메인 루트에 `app-ads.txt`
- 공개 웹사이트 원본의 헤더·저작권은 아직 "마켓인사이트"입니다. 앱 번들은 로고, 홈 화면 제목, 저작권 줄만 "US Market Insight"로 바꿉니다. 사이트 원본을 같은 영문으로 바꿀지는 별도 결정이며, 앱 이름을 한글로 맞추지는 않습니다.
- 선택: 종목 페이지에 `data-ticker` 속성. 지금은 파일명으로 티커를 읽음

## 11. 위험

- 심사자가 웹뷰 래퍼로 볼 수 있음. 대응 문안은 체크리스트의 심사 노트. 로컬 번들, 기기 관심 목록, 공유, FCM 토픽, AdMob, 고지 게이트가 그 근거입니다. 기기 미검증 항목은 심사 전에 실기기에서 확인해야 합니다.
- 분석 글의 목표주가 서술이 투자자문·금융 기능 선언으로 읽힐 수 있음. 법률 자문 전제.
- 샘플 광고 ID로 프로덕션에 올리면 정책 위반이거나 광고가 나가지 않음. `npm run check:release`가 이를 막도록 실패하게 해 두었습니다.
- 패키지명을 확정 전에 Play에 올리면 그 ID가 고정됨.
- TradingView 위젯은 온라인이면 제3자 콘텐츠라, 시세처럼 보일 수 있음. 고지 문단에 "실시간 시세 기능이 없고 위젯은 지연될 수 있음"을 넣었습니다.
- 서명 키와 `google-services.json`을 커밋하면 안 됨. `.gitignore`에 넣어 두었습니다.

## 12. iOS

TestFlight 절차, 맥 명령, 심사 주의는 `IOS_TESTFLIGHT_KO.md`입니다. Linux에서는 프로젝트를 생성한 것까지이고, Xcode 빌드는 하지 못했습니다.
