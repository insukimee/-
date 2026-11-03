# iOS TestFlight 안내

확인 날짜: 2026-11-03. 사장님은 아이폰에서 TestFlight로 시험합니다. Android 출시를 멈추는 것이 아니라, iOS 시험용 빌드를 앞으로 당긴 것입니다.

계정 만들기, 결제, 스토어 제출, 인증서·프로비저닝 프로필·`.p8` 키 생성은 하지 않습니다. 그 파일은 저장소에 넣지 않습니다.

번들 ID `com.usmarketinsight.app`는 Android와 같은 **1순위 후보**이며, App Store에 앱을 만들기 전에는 바꿀 수 있습니다. 한 번 등록하면 그 앱의 번들 ID는 바꾸기 어렵습니다.

## 1. 이 저장소에서 Linux로 한 일

| 한 일 | 결과 |
| --- | --- |
| `@capacitor/ios@8.6.0` 설치, `npx cap add ios` | 성공. CocoaPods가 아니라 **Swift Package Manager** 프로젝트로 생성됨. `ios/App/CapApp-SPM/Package.swift`가 있음. Podfile은 없음 |
| 최소 iOS | 프로젝트와 Package.swift 모두 **iOS 15.0**. Capacitor 8 안내와 같음. 출처: https://capacitorjs.com/docs/updating/8-0 |
| 표시 이름 | `US Market Insight`. 한국어·일본어 InfoPlist.strings도 같은 영문 |
| 샘플 AdMob iOS 앱 ID, SKAdNetwork 목록, ATT 문구 | Info.plist에 넣음. 운영 ID는 없음 |
| 푸시 엔타이틀먼트 `aps-environment` = development | 넣음. TestFlight 전에 production으로 바꾸는 절차는 아래 |
| `xcodebuild` | 이 Linux에는 없음. 명령이 없다는 오류. **맥에서만 빌드 가능** |
| 시뮬레이터 실행, 서명, 업로드 | 하지 않음. 못 함 |

Capacitor 8 문서: 새 iOS 프로젝트는 SPM이 기본입니다. CocoaPods로 만들려면 `npx cap add ios --packagemanager CocoaPods`입니다. 우리는 기본값(SPM)을 썼습니다. 같은 문서가 Xcode 26.0 이상을 요구합니다.

Apple 업로드 요건(2026-11-03에 연 페이지): 2026-04-28부터 App Store Connect에 올리는 앱은 Xcode 26 이상과 iOS 26 SDK 이상으로 빌드해야 합니다. https://developer.apple.com/news/upcoming-requirements/  
Xcode 26이 요구하는 macOS 버전은 이번 조사에서 확인하지 못했습니다. **확인 필요.**

## 2. 맥에서 그대로 실행할 명령

맥에 Xcode 26 이상이 설치된 뒤, 저장소를 받고:

```bash
cd app
npm install
npm run build
npx cap sync ios
open ios/App/App.xcodeproj
```

SPM 프로젝트라 `.xcworkspace`가 없습니다. `App.xcodeproj`를 엽니다.

Xcode에서:

1. 왼쪽에서 App 타깃 → Signing & Capabilities.
2. Team에 사장님의 Apple Developer 팀을 고릅니다. Automatically manage signing이 켜져 있어야 합니다.
3. Push Notifications 능력을 추가합니다. 지금 파일의 `aps-environment`는 `development`입니다. TestFlight용 아카이브 전에는 그 값을 `production`으로 바꿉니다.

```bash
# TestFlight 올리기 직전에만. 개발용 실행으로 되돌릴 때는 development 로 다시 바꿉니다.
sed -i '' 's/>development</>production</' ios/App/App/App.entitlements
```

4. 메뉴 Product → Archive. 끝나면 Organizer에서 Distribute App → App Store Connect → Upload.

터미널로 아카이브할 때(서명 팀이 이미 Xcode에 로그인되어 있을 때):

```bash
cd app/ios/App
xcodebuild -project App.xcodeproj -scheme App -configuration Release \
  -destination 'generic/platform=iOS' \
  -archivePath "$HOME/US-Market-Insight.xcarchive" \
  archive
```

업로드는 Xcode Organizer 또는 Transporter 앱이 더 안전합니다. `xcodebuild -exportArchive`는 내보내기 옵션 plist와 서명 팀이 있어야 해서, 그 plist를 저장소에 넣지 않았습니다. Organizer에서 Upload를 누르면 됩니다.

Transporter: Mac App Store에서 Apple Transporter를 설치하고, Organizer에서 받은 `.ipa`를 넣습니다. ipa를 만드는 화면은 Organizer의 Distribute App입니다.

## 3. 누가 무엇을 하나

| 우리 | 사장님 |
| --- | --- |
| iOS 프로젝트, 샘플 광고 ID, 고지, ko/ja 문구, 이 문서 | Apple ID와 2단계 인증 |
| 맥에서 빌드하는 명령 | Apple Developer Program 가입과 연회비 결제. 우리는 대신하지 않음 |
| 번들 ID 후보를 코드에 넣어둠 | App Store Connect에서 앱 생성, 번들 ID 등록 |
| | TestFlight 내부 테스터 초대 |
| | APNs 인증키(.p8)를 Firebase에 등록 |
| | `GoogleService-Info.plist`를 맥의 `ios/App/App/`에만 두고 커밋하지 않음 |

가입 안내(2026-11-03): 프로그램은 멤버십 1년에 99달러입니다. 지역에 따라 현지 통화로 표시됩니다. 개인은 본인 법적 이름, 조직은 D-U-N-S와 법적 권한이 필요합니다. 승인에 걸리는 일수는 그 페이지에 없어서 단정하지 않습니다. https://developer.apple.com/programs/enroll/

무료 Apple ID만으로 Xcode Personal Team에 로그인하면, 본인 기기에 개발용으로 설치할 수 있습니다. 그 경로는 App ID 10개·기기 3대·앱 3개·프로비저닝 7일 제한이 있습니다. TestFlight와 푸시에는 유료 프로그램이 필요합니다. https://developer.apple.com/help/account/basics/about-your-developer-account/

## 4. 사장님이 할 일 (순서)

1. Apple ID에 2단계 인증을 켭니다.
2. https://developer.apple.com/programs/enroll/ 에서 본인 명의로 가입합니다. 개인 또는 조직. 조직은 D-U-N-S가 필요합니다. 결제는 사장님만 합니다.
3. 맥에 Xcode 26 이상을 설치하고, Xcode → Settings → Accounts에 그 Apple ID를 넣습니다.
4. App Store Connect에서 앱을 만듭니다. 이름 **US Market Insight**, 번들 ID는 코드와 같은 `com.usmarketinsight.app`(확정 전). SKU는 사장님이 정합니다.
5. 위 명령으로 아카이브를 만들고 Organizer에서 업로드합니다. 암호화 질문에는 표준 HTTPS만 쓴다고 답하면 됩니다. Info.plist의 `ITSAppUsesNonExemptEncryption`은 false로 넣어 두었습니다.
6. TestFlight에서 내부 테스터를 초대합니다. 아이폰에 TestFlight 앱을 설치하고, 메일 초대를 수락합니다.

TestFlight 공식 문장(2026-11-03, https://developer.apple.com/help/app-store-connect/test-a-beta-version/testflight-overview/ ):

- 빌드는 올린 뒤 최대 90일 동안 시험할 수 있고, 그 뒤 테스터가 쓸 수 없게 됩니다.
- 내부 테스터는 콘텐츠 접근 권한이 있는 App Store Connect 사용자이며, 추가 페이지는 최대 100명이라고 합니다. https://developer.apple.com/help/app-store-connect/test-a-beta-version/add-internal-testers/
- 외부 테스터는 최대 10,000명이고, 초대하면 베타 빌드 심사가 필요할 수 있다고 적혀 있습니다.
- 같은 개요는 "앱의 첫 빌드를 그룹에 넣으면 App Review로 간다"고도 합니다. 내부 그룹만 쓸 때 심사가 면제되는지는 그 두 문장만으로 단정하지 않습니다. **확인 필요.** Xcode 배포 문서에는 "TestFlight (Internal Testing Only)"와 "TestFlight and App Store"가 나뉘어 있습니다. https://developer.apple.com/documentation/xcode/distributing-your-app-for-beta-testing-and-releases

아이폰에 Xcode로 개발 서명 앱을 직접 설치할 때는 개발자 모드가 필요할 수 있습니다. TestFlight로 받는 빌드는 그 경로와 다릅니다. 개발자 모드 문서 본문은 이번에 열지 못했습니다. **확인 필요:** https://developer.apple.com/documentation/xcode/enabling-developer-mode-on-a-device

## 5. 광고와 푸시

### 광고

`@capacitor-community/admob` 8.3.0은 iOS 배너와 UMP, ATT(`requestTrackingAuthorization`)를 지원합니다. 셸은 iOS에서 동의 정보(UMP) 다음에 ATT를 요청하고, ATT를 거부해도 배너 요청은 계속합니다. 맞춤 광고만 제한됩니다.

Info.plist:

- `GADApplicationIdentifier`: Google 샘플 `ca-app-pub-3940256099942544~1458002511`. Ad Manager iOS 빠른 시작 주석과 Google 샘플 프로젝트에서 확인. AdMob iOS 빠른 시작 렌더본은 자리표시로만 보여, 출시 전 같은 페이지와 다시 대조합니다. **확인 필요(샘플 문자열의 페이지 위치).**
- 배너 테스트 단위: `ca-app-pub-3940256099942544/2934735716` (고정 배너 데모). https://developers.google.com/admob/ios/test-ads (2026-11-03)
- `SKAdNetworkItems`: 2026-11-02자 빠른 시작 예시에 나온 식별자. 페이지가 더 길 수 있어 출시 전 전체 목록과 비교합니다. **확인 필요.** https://developers.google.com/admob/ios/quick-start
- `NSUserTrackingUsageDescription`: 영어 기본, 한국어·일본어 `InfoPlist.strings`

이 Linux 빌드에서는 광고가 실제로 뜨는지 확인하지 못했습니다. **목업이 아니라 네이티브 설정과 JS 호출은 연결되어 있고, 실행 확인은 맥/아이폰에서 해야 합니다.**

### 푸시

| 시험 단계에서 | 됨 | 안 됨 |
| --- | --- | --- |
| 알림 권한을 켤 때만 요청 | 코드 있음 | 아이폰에서 팝업이 뜨는지는 미확인 |
| 토픽 이름 (`ticker-nvda`, `digest-ko`) | JS는 Android와 같은 함수 | iOS 플러그인은 Firebase가 없어 구독을 거절함. 앱은 죽지 않음 |
| APNs 수신 | | 유료 개발자 계정, Push 능력, `.p8` 키, `GoogleService-Info.plist`, 실기기 필요 |
| `aps-environment` | development로 넣어둠 | TestFlight는 production. 위 sed 참고 |
| Background Modes | 넣지 않음 | 알림 배너만이면 필수로 보지 않음. 무음 데이터 푸시를 쓸 때만 remote-notification. **확인 필요** |

`.p8` 절차(사장님): Apple Developer → Keys → Apple Push Notifications service (APNs) 키를 만들고 `.p8`을 받습니다. 한 번만 내려받을 수 있는 경우가 많습니다. Firebase 콘솔 → 프로젝트 설정 → Cloud Messaging → Apple 앱 구성에 Key ID, Team ID, `.p8`을 올립니다. 그 파일은 채팅이나 git에 올리지 않습니다. 인증서(`.p12`) 대신 `.p8` 키를 권합니다. 인증서는 만료되고 키는 계정의 여러 앱에 쓸 수 있습니다. 키와 인증서의 최신 화면 이름은 **확인 필요.**

`GoogleService-Info.plist` 예시는 `ios/App/App/GoogleService-Info.plist.example`입니다. 실제 파일은 gitignore입니다.

App Privacy(영양성분표)에는 Android Data safety와 같이, 광고 식별자·대략적 위치(AdMob), 푸시를 켤 경우 기기 토큰을 적어야 합니다. 관심 목록은 기기에만 있습니다. 추적(ATT)을 쓰면 그 사실을 표에 밝힙니다. 칸의 정확한 보기는 제출 화면에서 **확인 필요.**

## 6. 일정

영업일 범위입니다. 심사 일수는 단정하지 않습니다.

| 단계 | 범위 | 막히는 곳 |
| --- | --- | --- |
| 맥에서 아카이브까지 | 계정과 Xcode가 있으면 1–2일 | Xcode 26, 맥, 서명 팀 |
| 개발자 프로그램 승인 | 일수 단정 안 함 | 사장님 명의, 결제, 조직이면 D-U-N-S |
| TestFlight 처리 | 공식 SLA를 확인하지 못함 | 업로드 후 Processing. 24시간이 넘으면 문제가 있을 수 있다는 식의 안내만 봤고, 그 문장도 2차 자료라 **확인 필요** |
| 외부 테스터 베타 심사 | 일수 단정 안 함 | 첫 외부 공개. 내부만 쓰면 다를 수 있음 |
| 스토어 정식 심사 | 일수 단정 안 함 | 4.2, 금융·광고 질문 |

## 7. 심사에서 볼 점

- Guideline 4.2 최소 기능: 원격 주소만 여는 웹 래퍼로 보이면 거절됩니다. 이 앱은 로컬 번들, 기기 관심 목록, 공유, 고지, 광고 SDK, 푸시 권한(설정 시)을 넣었습니다. 푸시와 광고는 아이폰에서 아직 확인하지 못했습니다.
- 투자 정보: 매매·계좌가 없음을 첫 화면과 설명에 적습니다. 목표주가 문장이 투자자문으로 보이면 추가 자료가 필요할 수 있습니다. 법률 자문이 필요하고, 단정하지 않습니다.
- 광고: ATT 문구, 샘플 ID를 운영 ID로 바꾸기 전 출시 금지, 클릭 유도 금지.
- 개인정보: 추적과 광고 데이터.

스토어 문구 초안: `store-listing/ios-ko.md`, `store-listing/ios-ja.md`.

스크린샷(2026-11-03, https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications/ ):

- 기기 크기마다 최소 1장, 최대 10장. JPEG 또는 PNG. 알파 채널 없음.
- 아이폰은 Dynamic Island 중간 화면 스크린샷이 필요합니다. 받은 크기 예: 1179×2556, 1206×2622(세로).
- 이 프로젝트는 아이패드도 타깃(`TARGETED_DEVICE_FAMILY` 1,2)이라, 도움말은 아이패드 13인치 스크린샷을 요구합니다. 그 픽셀 숫자는 이번 페이지 수신분에서 끝까지 확인하지 못했습니다. **확인 필요.** 아이패드를 빼려면 Xcode에서 기기 패밀리를 iPhone만으로 줄이는 결정이 필요합니다.

1024 마케팅 아이콘은 알파가 없어야 합니다. `resources/ios/AppIcon-1024.png`와 앱 아이콘 세트는 색 유형 RGB(알파 없음)로 만들었습니다. 도안은 아직 가안입니다.
