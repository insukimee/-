# Google Play 등록 체크리스트

US Market Insight Android 앱용입니다. 확인 날짜는 **2026-11-03**입니다. 각 링크는 그날 연 공식 페이지입니다. 숫자가 바뀌므로 제출 직전에 같은 URL을 다시 여세요. 페이지를 열지 못했거나 콘솔 화면의 칸 이름까지는 보지 못한 것은 **확인 필요**입니다.

이 문서의 본문은 Google Play입니다. iOS TestFlight와 App Store 문구는 `IOS_TESTFLIGHT_KO.md`, `store-listing/ios-ko.md`, `store-listing/ios-ja.md`입니다.

담당: **사장님**은 계정·결제·법적 명의·최종 문구 승인·키 보관. **우리**는 초안, 빌드, 문서. 계정 생성·결제·제출·키 생성은 하지 않습니다.

## 1. 개발자 계정

| 항목 | 2026-11-03에 확인한 내용 | 담당 |
| --- | --- | --- |
| 등록비 | 1회 25달러. 신용/직불 카드. 선불 카드는 안 된다고 안내. 신원 정보가 무효면 환불되지 않을 수 있다고 적혀 있음 | 사장님 |
| 계정 유형 | 개인 또는 조직. 조직은 D-U-N-S가 필수(정부 기관 등 예외는 도움말). D-U-N-S 신청은 Dun & Bradstreet 경유가 무료라고 안내. 발급 일수는 그 페이지에서 확인하지 못함 | 사장님 |
| 금융 앱과 계정 유형 | 도움말은 은행·대출·주식 거래·펀드·암호자산 지갑/거래소를 제공하는 경우 조직 계정을 고르라고 함. 이 앱은 그 기능을 넣지 않음. 그래도 조직이 필수인지는 단정하지 않음. **확인 필요** | 사장님 + 법률 |
| 신원 | 개인: 정부 신분증. 조직: D-U-N-S, 신분증, 조직 서류. 결제 프로필의 이름과 맞아야 함 | 사장님 |
| 전화번호 | 조직은 Play에 표시되는 전화번호를 인증. 개인은 신원·기기 인증이 끝난 뒤 전화 인증으로 안내됨 | 사장님 |
| 기기 인증 | 개인 계정 소유자는 Play Console 모바일 앱으로 Android 기기를 인증해야 게시할 수 있다고 시작 가이드에 있음 | 사장님 |
| 소요 일수 | 신원 확인이 며칠인지는 연 도움말에 없었음. **확인 필요**. 일정 문서에서도 단정하지 않음 | — |

링크:

- 시작하기 (요금, 신원, 개인 계정의 테스트·기기 인증): <https://support.google.com/googleplay/android-developer/answer/6112435>
- 계정 유형: <https://support.google.com/googleplay/android-developer/answer/13634885>
- 신원 확인: <https://support.google.com/googleplay/android-developer/answer/10841920>

## 2. 비공개 테스트 (개인 계정)

출처: <https://support.google.com/googleplay/android-developer/answer/14151465> (2026-11-03).

그 페이지는 **2023-11-13 이후에 만든 개인 개발자 계정**에 다음을 요구합니다.

- 비공개 테스트에 옵트인한 테스터가 **최소 12명**
- 프로덕션 액세스를 신청하는 시점에, 그 사람들이 **직전 14일 연속** 옵트인 상태
- 프로덕션과 사전 등록은 이 요건 전에 잠김
- 내부 테스트는 선택이며, 앱 설정을 마치기 전에도 가능하다고 안내
- 신청 질문은 비공개 테스트 / 앱 / 출시 준비의 세 묶음
- 검토가 끝나면 계정 소유자에게 이메일이 간다고 함. **며칠인지는 페이지에서 확인하지 못함**

12와 14는 그날의 공식 문장입니다. 예전에 20명이던 적이 있어 정책은 바뀝니다. 제출 전에 같은 문서를 다시 여세요. 조직 계정에 같은 숫자가 적용된다고 그 페이지가 쓰지는 않았습니다. **조직 계정의 테스트 요건은 확인 필요.**

담당: 테스터 모집은 사장님. 테스트 트랙용 AAB는 우리.

## 3. 앱 서명과 AAB

출처: <https://support.google.com/googleplay/android-developer/answer/9842756> (2026-11-03).

- 신규 앱은 Play App Signing에 들어가고, 도움말은 업로드 시 양자 대응 하이브리드 서명(Google이 키를 생성)에 자동 등록된다고 설명합니다.
- **업로드 키**는 사장님이 가진 keystore(RSA 2048 이상)로 App Bundle에 서명하는 키입니다. 잃어도 Play에서 재설정을 요청할 수 있습니다.
- **앱 서명 키**는 사용자 기기에 설치되는 APK에 Google이 서명하는 키입니다. Google이 생성한 키를 쓰는 구성이 기본 안내입니다. 직접 관리하는 키를 잃으면 재설정이 안 될 수 있다고 구분되어 있습니다.
- 업로드 키와 앱 서명 키는 다르게 두는 것이 안내입니다.
- API 제공자(광고 등)에 지문을 등록할 때는 로컬 업로드 키만이 아니라 Play가 보여주는 앱 서명 키 지문을 등록합니다. 하이브리드 서명이면 지문이 여러 개입니다.

keystore, `keystore.properties`, 비밀번호는 커밋하지 않습니다. 생성 명령과 예시 파일은 `app/README.md`, `native-extras/keystore.properties.example`.

이번 빌드 (2026-11-03, JDK 21, AGP 8.13):

- `./gradlew assembleDebug` 성공. APK는 **Android 디버그 인증서**로만 서명됨. Play 업로드 불가.
- `./gradlew bundleRelease` 성공. `keystore.properties`가 없어 **AAB는 서명되지 않음** (`jarsigner` 기준 unsigned). 업로드 전에 사장님 키로 다시 빌드해야 합니다.
- `compileSdk` / `targetSdk` = 36, `minSdk` = 24. 타깃 요건은 아래.
- AAB의 `lib/`에 `arm64-v8a`, `armeabi-v7a`, `x86`, `x86_64`가 있고, 네이티브 파일은 `libdatastore_shared_counter.so`입니다. 64비트 라이브러리를 빼지 않았습니다.
- 64비트 요건 도움말 본문은 이번에 열지 못했습니다. 링크만 남깁니다. **문장 확인 필요:** <https://developer.android.com/google/play/requirements/64-bit>
- 신규 앱이 AAB만 받는다는 도움말 본문도 이번에 열지 못했습니다. 빌드 산출물은 AAB로 맞춰 두었습니다. **확인 필요:** <https://developer.android.com/guide/app-bundle>

타깃 API (연 페이지): <https://support.google.com/googleplay/android-developer/answer/11926878>  
2026-08-31부터 신규 앱과 업데이트는 Android 16 (API 36) 이상을 타깃해야 합니다. 연장 신청 기한으로 적힌 날은 2026-11-01입니다. 오늘(2026-11-03) 이후 제출은 API 36이 맞습니다. 같은 내용: <https://developer.android.com/google/play/requirements/target-sdk>

## 4. 스토어 등록정보 그래픽

출처: <https://support.google.com/googleplay/android-developer/answer/9866151> (2026-11-03).

| 자산 | 요건 (그 페이지) | 담당 |
| --- | --- | --- |
| 앱 아이콘 | 512×512, 32비트 PNG(알파), 최대 1024KB. 순위·가격을 암시하는 배지 금지 | 사장님이 도안 확정, 우리가 파일로 맞춤. 현재 가안 `resources/play/icon-512.png` |
| 피처 그래픽 | 1024×500. JPEG 또는 알파 없는 24비트 PNG. 게시 필수 | 가안 `resources/play/feature-graphic-1024x500.png`. 글자 없음. 확정 필요 |
| 스크린샷 | 게시에 기기 유형을 합쳐 **최소 2장**. JPEG 또는 알파 없는 24비트 PNG. 짧은 변 320–긴 변 3840, 긴 변이 짧은 변의 2배 이하. 유형별 최대 8장 | 우리 캡처 + 사장님 승인 |
| 추천 구좌용 | 앱은 1080px 이상 4장, 세로 9:16이면 최소 1080×1920을 권장(필수 게시는 2장) | 우리 |
| 태블릿·Chromebook | 대형 화면 안내로 4장 이상, 1080–7680, 16:9 또는 9:16을 적을 수 있다고 함. 태블릿 배포를 켰을 때 콘솔이 필수로 막는지는 그 문장만으로 단정하지 않음. **확인 필요** | 우리 |
| 미리보기 영상 | 선택. YouTube URL 하나. 공개 또는 일부 공개, 광고 끄기, 연령 제한 영상 아님 | 사장님이 원하면 |

iPhone 6.9"/6.5" 같은 크기는 Apple 쪽 이름입니다. Play 도움말은 픽셀과 비율로 안내합니다.

초안 문구: `docs/store-listing/ko.md`, `ja.md`.  
Play 등록정보에 Apple식 100자 키워드 칸은 이 도움말에서 보이지 않았습니다. 제목·짧은 설명·긴 설명에 넣습니다. 콘솔에 키워드 칸이 있으면 **확인 필요**.

앱 이름 확정값: **US Market Insight** (17자, 한도 30). 한국어 스토어 표시명도 이 영문입니다. "US 마켓인사이트"와 한글 "마켓인사이트" 단독·유사 표기는 쓰지 않습니다. 한국경제신문 자본시장 서비스와 혼동될 수 있습니다. 근거(2026-11-03): <https://marketinsight.hankyung.com/>, App Store <https://apps.apple.com/kr/app/id802681902> (앱 이름 "마켓인사이트", 제공자 The Korea Economic Daily). Google Play의 동일 이름 상세 URL은 이번 검색에서 특정하지 못했습니다.

## 5. URL

| URL | 지금 | 담당 |
| --- | --- | --- |
| 개인정보처리방침 | `https://insukimee.github.io/-/ko/privacy-policy.html` 가 사이트에 있음. 앱의 관심 목록(기기 내), FCM 토큰, AdMob을 반영해야 함. 초안 문장은 `APP_PLAN_KO.md` | 사장님 승인, 우리 문안, 사이트 반영은 별도 PR |
| 이용약관 | `…/ko/terms.html`, 일본어는 `…/ja/…`. 도메인은 `siteBaseUrl` | 같은 방식 |
| 지원 URL | 사이트의 contact 페이지를 쓸 수 있음. 콘솔이 요구하는 정확한 필드명은 **확인 필요** | 사장님 |
| 마케팅/개발자 웹사이트 | `app-ads.txt`는 이 웹사이트 **루트**에 있어야 AdMob이 읽음. github.io 하위 경로는 루트가 아님. 도메인 이전 후 `https://usmarketinsight.com/app-ads.txt`를 제안 | 사장님 |

사용자 데이터 정책(개인정보처리방침이 필요한 경우의 근거로 연 페이지): <https://support.google.com/googleplay/android-developer/answer/10144311>

## 6. 카테고리, 액세스, 연령, 광고 선언

- **카테고리:** 금융, 뉴스 및 잡지, 비즈니스 중 사장님 결정. 미확정.
- 뉴스 및 잡지로 가면 선언이 있습니다. 연락처·모기업 유형, 금융 콘텐츠는 초점 예시로 "Finance"가 적혀 있습니다. 현재 사건 뉴스는 30일 이내 갱신, 그 외 뉴스/잡지는 3개월 이내를 그 페이지가 말합니다.  
  <https://support.google.com/googleplay/android-developer/answer/16189314>  
  <https://support.google.com/googleplay/android-developer/answer/10523915>
- **앱 액세스:** 로그인이 없습니다. 데모 계정이 필요 없습니다. 콘솔의 "모든 기능을 제한 없이 사용할 수 있음"에 해당하는지는 화면을 보지 못해 **확인 필요**.
- **대상 연령:** 아동용으로 설계하지 않음. `tagForChildDirectedTreatment`은 false. 정확한 연령 등급은 IARC 설문 결과입니다.
- **광고 포함:** 예. AdMob을 붙이기로 했으므로 광고 포함으로 선언해야 합니다. 콘솔 칸의 정확한 라벨은 화면 미확인. **확인 필요.** 광고 정책 링크는 이번에 본문을 열지 못했습니다: <https://support.google.com/googleplay/android-developer/answer/9857753>
- **광고 ID:** 매니페스트에 `com.google.android.gms.permission.AD_ID`. Data safety의 기기 또는 기타 ID에 포함.

## 7. 콘텐츠 등급 (IARC)

설문 절차 페이지 본문은 이번에 열지 못했습니다. **확인 필요:** <https://support.google.com/googleplay/android-developer/answer/9859655>

초안(설문의 보기가 다르면 무시하고 콘솔 문장에 맞출 것):

- 폭력, 성적 콘텐츠, 욕설, 규제 약물, 도박 콘텐츠: 앱이 제공하는 글에는 해당 목적으로 넣지 않음
- 사용자 간 상호작용, 사용자 생성 콘텐츠, 위치 공유를 앱 기능으로 제공하지 않음
- 광고 SDK가 IP로 대략 위치를 추정하는 것은 등급 설문이 아니라 Data safety 쪽. 설문에 "이용자 정보를 공유하는가"가 있으면 AdMob/FCM을 숨기지 말 것
- 결과 등급(예: 3세, 12세)은 설문 전에 단정하지 않음

## 8. Data safety 초안

양식 설명: <https://support.google.com/googleplay/android-developer/answer/10787469>  
AdMob이 밝힌 SDK 수집: <https://developers.google.com/admob/android/privacy/play-data-disclosure>  
대략적 위치의 정의(IP 추정 포함)와 기기 ID 예시(광고 ID): <https://developer.android.com/privacy-and-security/declare-data-use>

개발자가 직접 수집한다고 적지 말 것과, SDK가 수집하는 것을 빠뜨리지 말 것을 구분합니다. 아래는 초안이며 콘솔 보기와 다르면 콘솔이 우선입니다. **최종 제출 값은 확인 필요.**

| 질문 | 초안 |
| --- | --- |
| 데이터를 수집하거나 공유하는가 | 예. AdMob과, 알림을 켠 경우 FCM |
| 데이터를 판매하는가 | 아니요 |
| 추적에 쓰는가 | 맞춤 광고를 켜면 해당할 수 있음. UMP에서 비맞춤만 받으면 달라질 수 있음. **확인 필요** |
| 암호화 전송 | 예. HTTPS, Play 경유. 앱이 자체 서버를 두지 않음 |
| 삭제 요청 | 계정이 없음. 관심 목록은 앱 삭제 또는 앱 안에서 삭제로 지워짐. FCM 토큰과 광고 ID의 삭제 경로는 Google 계정/광고 설정. 양식의 "사용자가 삭제를 요청할 수 있는가"는 계정 없는 앱의 보기에 맞춰 **확인 필요** |
| 대략적 위치 | AdMob이 IP로 추정. 수집됨, 공유됨(Google). 목적: 광고, 부정 이용 방지. 앱은 `ACCESS_COARSE_LOCATION`을 선언하지 않음 |
| 정확한 위치 | 초안은 아니요. 위젯이 다르게 동작하면 **확인 필요** |
| 앱 활동(상호작용) | AdMob 공개 표에 있음. 수집·공유, 목적 광고/분석 |
| 진단 | AdMob 공개 표에 있음 |
| 기기 또는 기타 ID | 광고 ID, 앱 세트 ID (AdMob). FCM 등록 토큰(알림을 켠 경우, 앱 기능). 공유 대상 Google |
| 이름, 이메일, 금융 정보, 연락처 | 앱이 수집하지 않음. 문의는 사이트의 웹 양식이며 앱의 필수 흐름이 아님 |
| 관심 종목 | 기기에만 있음. Play 정의상 기기 밖으로 나가지 않으면 수집이 아님 |

## 9. 금융 기능 선언과 투자 정보

선언 양식: <https://support.google.com/googleplay/android-developer/answer/13849271> (2026-11-03).

모든 게시 앱이 작성합니다. 금융 기능이 없어도 "My app doesn’t provide any financial features"를 고르고 인증합니다. 보기로 적힌 것에는 주식 거래·포트폴리오, 그리고 Support services의 **Financial advice**가 있습니다.

금융 서비스 정책 문장(연 정책 페이지): 금융 상품은 돈과 암호자산의 관리·투자를 포함하고 맞춤 조언을 포함한다고 되어 있습니다. 지역 규정을 따르고, 금융 기능이 있으면 선언 양식을 내야 합니다. <https://support.google.com/googleplay/android-developer/answer/18258653>

이 앱의 사실:

- 주문, 계좌, 입출금, 포트폴리오 관리 기능이 없음
- 불특정 다수에게 올리는 분석 글이며, 앱이 "사라"고 하지 않음
- 고지: 투자 권유 아님, 수익 보장 아님, 증권사 아님, 실시간 시세 기능 아님

초안 답: **금융 기능 없음.** 다만 목표주가와 종합 평가 문장을 자문으로 보면 `Financial advice`에 들어갈 수 있고, 그 경우 라이선스 서류로 이어질 수 있습니다. 어느 칸인지는 법률 자문과 콘솔 도움말을 제출 전에 다시 봐야 합니다. **확인 필요. 단정하지 않음.**

한국에서 불특정 다수 대상 투자 판단 조언이 유사투자자문업 신고 대상인 경우가 있으나, 이 앱이 그 요건에 해당하는지는 법률 자문이 필요합니다. 일본의 금융상품거래법상 투자조언·대리업도 같습니다. 고지 문장만으로 규제 밖이라고 쓰지 않습니다.

고지 위치: 최초 실행 전체 화면, 탭 아래 상단 바, 설정·정보 화면, 스토어 설명 첫머리, 공유 문구.

사용자 생성 콘텐츠 없음. 댓글(Disqus)은 웹 정책에 있으나 앱 필수 기능이 아닙니다. 앱 안에서 Disqus가 보이는지는 페이지에 스크립트가 있을 때만입니다. 사이트 생성물 기준으로 댓글 위젯이 모든 글에 있는지는 이 체크리스트에서 재확인하지 않았습니다. **확인 필요.**

## 10. 수출·암호화

Apple의 수출 규정 질문과 같은 칸이 Play에 있는지는 이번에 확인하지 못했습니다. **확인 필요.** 앱은 표준 HTTPS 외에 자체 암호 기능을 넣지 않습니다.

## 11. 심사 노트 초안 (영문)

Play Console의 심사 메모에 붙여 넣을 초안입니다.

```
US Market Insight is an information app. It is not a broker, not an exchange,
and it does not place orders, hold accounts, or provide a real-time quote service.

No login or demo account is required. All screens are available immediately
after the first-run notice.

The app is not a remote website wrapper:
- Analysis pages are bundled inside the app and open offline.
- A watchlist is stored on device with Capacitor Preferences (no account).
- The Android share sheet shares a public article link.
- Optional FCM topic notifications (permission is requested only when the user
  opts in; the app works if permission is denied).
- A bottom tab bar, back handling, and a persistent "not investment advice" notice.
- Ads, when enabled, use the AdMob SDK. The website's AdSense tags are stripped
  from the bundled pages.

Please review in Korean or Japanese. The first screen is the disclaimer.
```

기기에서 푸시와 테스트 광고를 확인하기 전에는 이 문단의 FCM·AdMob 문장이 코드 기준이라는 점을 제출 담당자가 알고 있어야 합니다.

래퍼가 아닌 이유(심사 대응용, 한국어): 로컬 번들, 기기 관심 목록, 시스템 공유, 사용자가 켠 경우에만 FCM 토픽, 하단 탭과 뒤로 가기, 투자 비권유 고지, AdMob(웹 광고 태그 제거).

## 12. 출시 전 우리 쪽 기술 체크

- [ ] `appIdConfirmed`를 true로 바꾸기 전에 사장님 확정
- [ ] `npm run check:release`가 통과 (지금은 실패하는 것이 맞음)
- [ ] 샘플 AdMob ID를 운영 ID로 교체하고 `useTestAds`를 false로
- [ ] `google-services.json`을 빌드 머신에만 두고 토픽 수신을 기기에서 확인
- [ ] 업로드 키로 서명한 AAB
- [ ] 실기기에서 뒤로 가기, 오프라인, 관심 목록, 공유, 고지
- [ ] 개인정보처리방침 URL이 앱 설명을 포함해 열려 있음
- [ ] 512 아이콘, 1024×500 피처 그래픽, 스크린샷 최소 2장(권장 4장, 1080×1920)
- [ ] 광고 포함 = 예, Data safety, IARC, 금융 기능 선언

## 13. iOS

Android와 병행해 TestFlight 시험을 진행합니다. 계정·결제·제출은 사장님이 합니다. 체크리스트와 맥 명령은 `IOS_TESTFLIGHT_KO.md`에 있습니다. 앱 이름·부제는 각 30자입니다(2026-11-03, https://developer.apple.com/app-store/product-page/). 초안 이름은 US Market Insight(17자)입니다.
