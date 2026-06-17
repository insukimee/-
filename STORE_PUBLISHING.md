# 앱스토어 등록 가이드 (마켓인사이트 PWA → 스토어 앱)

이 사이트는 설치형 PWA이므로, 그대로 감싸서 **Google Play / Apple App Store** 에 올릴 수 있습니다.
아래 단계는 **본인 컴퓨터·개발자 계정으로 직접** 수행해야 합니다(서명·결제·콘솔 업로드는 대행 불가).

라이브 URL: `https://insukimee.github.io/-/`
웹 매니페스트: `https://insukimee.github.io/-/manifest.webmanifest`

---

## 💸 비용 진실표 (먼저 확인)

| 배포처 | 비용 | 무료 가능? |
|--------|------|-----------|
| **PWA (홈 화면 설치)** | 무료 | ✅ 지금 바로 |
| **APK 직접 배포 (사이드로드)** | 무료 | ✅ |
| **Amazon Appstore** | 무료(개발자 계정 무료) | ✅ |
| **Google Play** | $25 (1회·평생) | ❌ |
| **Apple App Store** | $99/년 + Mac | ❌ |

> 공식 Play/App Store는 **등록비가 반드시 듭니다.** 완전 무료로 "스토어 앱" 느낌을 내려면 아래 0번 경로를 쓰세요.

---

## 0) 완전 무료 경로 (추천 순서)

### 0-A. 그냥 PWA로 쓰기 (0원, 빌드 0, 지금 끝)
- 휴대폰에서 `https://insukimee.github.io/-/` 접속 → "홈 화면에 추가/앱 설치"
- 전체화면 앱처럼 실행 + 오프라인 동작. **이미 완성되어 있음.**

### 0-B. APK 만들어 직접 배포 (0원, 본인 PC에서 빌드)
- 아래 1번의 Bubblewrap으로 `app-release-signed.apk` 생성(빌드 자체는 무료).
- 그 APK 파일을 사이트나 클라우드에 올려 **다운로드 링크/QR로 배포** → 사용자가 설치.
- 스토어 등록비 0원. 단, 사용자가 "출처를 알 수 없는 앱 설치"를 허용해야 함.

### 0-C. Amazon Appstore에 무료 등록 (0원, 진짜 스토어)
- developer.amazon.com 개발자 계정 **무료**.
- 0-B에서 만든 APK를 업로드 → 심사 후 Amazon Appstore에 게재(안드로이드용).
- Google Play는 아니지만, **무료로 "스토어에 올라간" 앱**이 됩니다.

### 무료 경로의 TWA 검증 (도메인 없이)
0-B/0-C에서 주소창 없는 전체화면으로 만들려면 `assetlinks.json` 이 호스트 루트에 있어야 합니다.
**무료 방법**: `insukimee/insukimee.github.io` 저장소(사용자 페이지, 무료)를 만들고
그 루트에 `.well-known/assetlinks.json` 을 두면 `https://insukimee.github.io/.well-known/assetlinks.json` 으로 서빙됩니다.
(검증이 안 돼도 앱은 동작하며, 상단에 주소 바가 잠깐 보이는 정도 차이)

---

## ⚠️ (유료 경로) 도메인 — Play/Apple 정식 등록 시 권장


TWA(안드로이드)는 앱과 사이트의 소유권을 연결하기 위해
`https://<호스트>/.well-known/assetlinks.json` 을 **호스트 루트**에서 읽습니다.

현재 호스트는 `insukimee.github.io` 이고 사이트는 하위 경로(`/-/`)라서,
검증 파일은 `https://insukimee.github.io/.well-known/assetlinks.json` 에 있어야 합니다
(= 우리 저장소가 아니라 `insukimee.github.io` 사용자 페이지 루트).

**두 가지 방법 중 하나를 고르세요:**

- **(A·권장) 커스텀 도메인 연결** — 예: `marketinsight.app`
  - `assetlinks.json`, `ads.txt`가 모두 도메인 루트에서 정상 동작.
  - 연결법: 도메인 구입 → DNS에 GitHub Pages IP/CNAME 설정 → 저장소 Settings → Pages → Custom domain 입력 → 저장소 루트에 `CNAME` 파일 생성.
  - 이후 TWA `host`를 그 도메인으로 바꾸면 됩니다.

- **(B) 별도 사용자 페이지 저장소 사용**
  - `insukimee/insukimee.github.io` 저장소를 만들고 그 루트에 `.well-known/assetlinks.json` 을 둡니다.
  - 그러면 `https://insukimee.github.io/.well-known/assetlinks.json` 으로 서빙됩니다.

> 참고: 이 저장소에도 `.well-known/assetlinks.json` 템플릿을 넣어뒀지만,
> 그건 `https://insukimee.github.io/-/.well-known/assetlinks.json` 경로라
> TWA 검증 경로(`/.well-known/...`)와 다릅니다. 위 A 또는 B로 호스트 루트에 두세요.

---

## 1) Google Play (Android) — Bubblewrap으로 TWA 빌드

### 사전 준비
- Node.js 18+ , JDK 17
- Google Play 개발자 계정 (1회 $25): https://play.google.com/console

### 단계
```bash
# 1. Bubblewrap 설치
npm install -g @bubblewrap/cli

# 2. 프로젝트 초기화 (웹 매니페스트에서 자동 구성)
bubblewrap init --manifest https://insukimee.github.io/-/manifest.webmanifest
#   - 패키지명: io.github.insukimee.marketinsight (예시)
#   - 키스토어 생성 여부: Yes → 비밀번호/별칭 메모해 두기 (분실 시 업데이트 불가!)

# 3. 서명 키의 SHA-256 지문 확인
bubblewrap fingerprint
#   또는: keytool -list -v -keystore android.keystore -alias android
#   출력의 SHA256 값을 복사

# 4. assetlinks.json 에 SHA-256 넣고 "호스트 루트"에 배포 (위 A 또는 B)
#    .well-known/assetlinks.json 의 REPLACE_WITH_YOUR_SHA256_FINGERPRINT 를 교체

# 5. 빌드 → AAB/APK 생성
bubblewrap build
#   결과물: app-release-bundle.aab (스토어 업로드용), app-release-signed.apk (테스트용)
```

### Play Console 업로드
1. https://play.google.com/console → **앱 만들기**
2. **프로덕션 → 새 버전 만들기** → `app-release-bundle.aab` 업로드
3. 스토어 등록정보 작성:
   - 앱 이름 / 짧은 설명 / 전체 설명
   - 아이콘(512), 그래픽 이미지(1024×500), 스크린샷(폰 2장 이상)
   - **개인정보처리방침 URL**: `https://insukimee.github.io/-/ko/privacy-policy.html` ✅ (이미 있음)
4. **콘텐츠 등급 설문**, **데이터 보안(Data safety)** 작성
   - 광고 사용(AdSense): "광고 표시함" 체크
5. 국가/가격(무료) 설정 → **검토 제출** (보통 며칠 소요)

---

## 2) Apple App Store (iOS) — PWABuilder

iOS는 **Mac + Xcode** 와 **Apple 개발자 프로그램(연 $99)** 이 필요합니다.

1. https://www.pwabuilder.com 접속 → URL 입력: `https://insukimee.github.io/-/`
2. **iOS 패키지 다운로드** → 압축 해제
3. Mac의 **Xcode** 로 프로젝트 열기 → 서명 팀(Apple Developer) 지정
4. **App Store Connect** (https://appstoreconnect.apple.com) 에서 앱 생성
5. Xcode에서 Archive → Upload → App Store Connect에서 심사 제출
   - 개인정보처리방침 URL 입력(위 동일)
   - Apple은 "단순 웹 래퍼"를 거부할 수 있으니, 앱다운 기능/가치를 설명 권장

---

## 업데이트 방법
사이트 내용은 푸시하면 자동 반영(앱도 최신 웹을 로드).
앱 자체 버전(아이콘·이름·권한)만 바꿀 때 `appVersionCode`를 올려 다시 `bubblewrap build` → 재업로드.

---

## 요약 체크리스트
- [ ] 도메인 결정 (A 커스텀 도메인 / B 사용자 페이지 저장소)
- [ ] `assetlinks.json` 호스트 루트 배포 + SHA-256 기입
- [ ] (Android) Play 개발자 계정 $25 → Bubblewrap 빌드 → AAB 업로드
- [ ] (iOS) Apple 개발자 $99 + Mac/Xcode → PWABuilder → 업로드
- [ ] 스토어 등록정보(아이콘/스크린샷/설명/개인정보 URL) 작성 → 제출
