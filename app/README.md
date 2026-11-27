# US Market Insight (Android)

미국 증시 분석 정적 사이트를 기기에 담고, 관심 종목·공유·AdMob·FCM을 얹은 Capacitor Android 앱입니다. 앱 표시 이름과 한국어·일본어 스토어 표시명은 **US Market Insight**입니다. 한글 "마켓인사이트"는 앱 이름에 쓰지 않습니다.

이 디렉터리는 사이트(`generate.py`, `ko/`, `ja/` 등)와 분리되어 있습니다. 사이트 원본은 빌드할 때 `www/`로 복사만 합니다.

`appId` `com.usmarketinsight.app`는 **1순위 후보**이며 Play에 게시하기 전에는 바꿀 수 있습니다. 게시 후에는 바꿀 수 없습니다. 확정 여부는 `app.config.json`의 `appIdConfirmed: false`를 보세요.

iOS 프로젝트는 `ios/`에 있습니다. Capacitor 8은 Swift Package Manager를 기본으로 씁니다. 이 환경(Linux)에는 Xcode가 없어 빌드하지 못했습니다. 맥에서 열 명령과 TestFlight 절차는 `docs/IOS_TESTFLIGHT_KO.md`입니다.

## 요구 도구

- Node.js 20 이상 (이 환경: 22)
- JDK 21 (Android Gradle Plugin 8.13이 클래스 파일 21을 사용)
- Android SDK 36, build-tools 36

SDK 경로는 저장소에 넣지 않습니다. 빌드 전에 환경 변수만 지정합니다.

```bash
export ANDROID_HOME="$HOME/android-sdk"
export ANDROID_SDK_ROOT="$ANDROID_HOME"
```

## 설치와 웹 번들

```bash
cd app
npm install
npm test
```

`npm test`는 순수 함수 테스트, `www/` 생성, 번들에 AdSense가 없는지를 확인합니다.

`www/`는 빌드 산출물이라 git에 없습니다. 다시 만들려면:

```bash
npm run build
```

`npm run build:www`는 같은 명령입니다.

`app.config.json`의 `siteBaseUrl`이 공유 링크·약관 링크·피드 주소의 기준입니다. 도메인이 `usmarketinsight.com`으로 바뀌면 이 값만 바꾸고 `npm run build`를 다시 실행합니다.

## Android

네이티브 프로젝트는 `android/`에 있고, 서명 파일과 `google-services.json`은 빠져 있습니다. 처음 클론한 뒤:

```bash
npm run build
npx cap sync android
```

`android/`를 지우고 다시 만들었다면 아이콘과 권한 패치를 다시 적용합니다.

```bash
python3 scripts/gen-icons.py
node scripts/apply-native-extras.mjs
npx cap sync android
```

디버그 APK:

```bash
cd android
./gradlew assembleDebug --no-daemon
```

산출물: `android/app/build/outputs/apk/debug/app-debug.apk`  
디버그 인증서로만 서명됩니다. Play에 올리는 파일이 아닙니다. APK는 git에 넣지 않습니다.

폰에 직접 설치할 때:

1. 위 순서(`npm run build`, `npx cap sync android`, `./gradlew assembleDebug`)로 APK를 만듭니다.
2. Android 설정에서 이 출처의 앱 설치를 허용합니다.
3. 파일을 폰으로 옮겨 열거나, USB 디버깅 후 `adb install -r app-debug.apk`를 실행합니다.

이 디버그 APK는 Google 샘플 광고 ID를 쓰고, `google-services.json`이 없어 푸시 토큰이 나오지 않습니다. 알림을 켜면 등록이 실패하고, 글 읽기와 관심 목록은 동작합니다. Play에 올리면 안 됩니다.

서명 없는 릴리스 AAB:

```bash
cd android
./gradlew bundleRelease --no-daemon
```

`android/keystore.properties`가 없으면 서명이 붙지 않습니다. 템플릿은 `native-extras/keystore.properties.example`입니다. 키스토어는 저장소 밖에서 만들고, 파일과 비밀번호는 커밋하지 않습니다.

```bash
keytool -genkeypair -v \
  -keystore "$HOME/us-market-insight-upload.keystore" \
  -alias upload \
  -keyalg RSA -keysize 2048 -validity 10000
```

예시를 `android/keystore.properties`로 복사한 뒤 `storeFile`을 그 키스토어로 지정하고 다시 `bundleRelease`를 실행합니다. Play App Signing을 쓰면 이 키는 업로드 키입니다. 앱 서명 키는 Play가 보관합니다. 자세한 구분과 분실 시 재설정은 `docs/STORE_CHECKLIST_KO.md`를 보세요.

프로덕션 업로드 전에 아래가 실패하는 것이 정상입니다. 샘플 광고 ID와 미확정 패키지명이 아직이기 때문입니다.

```bash
npm run check:release
```

## 이번 환경에서 확인한 빌드

2026-11-03, Linux, JDK 21, `compileSdk`/`targetSdk` 36, `minSdk` 24.

- `./gradlew assembleDebug bundleRelease` 성공.
- 디버그 APK는 Android 디버그 인증서로 서명됨.
- `app-release.aab`는 업로드 키가 없어 **서명되지 않음**. Play 업로드용으로 쓰지 말 것.
- AAB에 `arm64-v8a`와 `armeabi-v7a` 네이티브 라이브러리가 함께 들어 있음 (AndroidX DataStore `.so`).
- 에뮬레이터와 실기기에는 설치하지 않음. AdMob 테스트 배너와 FCM 수신은 기기에서 아직 확인하지 않음.
- 브라우저에서 번들 셸(동의, 탭, 관심 종목, 설정, 일본어, 오프라인 배너)은 확인함.

## 광고와 푸시

- 웹 AdSense는 복사본에서 제거합니다. 앱 광고는 AdMob이고, 저장소의 ID는 Google 샘플 ID입니다.
- `google-services.json`이 없으면 앱은 실행되지만 푸시 토큰은 나오지 않습니다. 예시는 `native-extras/google-services.json.example`입니다. 실제 파일은 커밋하지 않습니다.

## 문서

| 파일 | 내용 |
| --- | --- |
| `docs/APP_PLAN_KO.md` | 구조, 기능 상태, 광고, 푸시, 개인정보 |
| `docs/SCHEDULE_ESTIMATE_KO.md` | Android 기준 일정 범위 |
| `docs/STORE_CHECKLIST_KO.md` | Play 등록 목록 |
| `docs/OPEN_QUESTIONS_KO.md` | 사장님 결정이 남은 항목 |
| `docs/store-listing/` | 스토어 문구 초안 (ko, ja) |

## 하지 않는 일

개발자 계정 생성, 결제, 스토어 제출, 키스토어 생성, Firebase/AdMob 계정 생성은 이 저장소에서 하지 않습니다.
