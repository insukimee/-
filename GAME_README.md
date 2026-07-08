# Ragdoll Party (임시명) - Godot 프로젝트 뼈대

갱비스트 스타일 2D 랙돌 물리 파티 격투 게임의 초기 프로토타입 뼈대입니다.
GDD.md에 기획 문서가 함께 들어있습니다.

## 실행 방법

1. [Godot 4.3+](https://godotengine.org/download) 설치 (엔진 다운로드, 별도 설치 불필요한 zip 버전 추천)
2. Godot 실행 → "Import" → 이 폴더의 `project.godot` 선택
3. 우측 상단 재생 버튼(▶) 또는 F5로 실행
4. 조작 (로컬 2인, `Main.gd`가 device_id 0/1로 두 캐릭터 스폰):
   - 1P: A/D 이동, Space 점프, 마우스 좌클릭 밀기, 왼쪽 Shift 잡기
   - 2P: 방향키 이동, Enter 점프, `/` 밀기, 오른쪽 Shift 잡기

## 폴더 구조

```
./
├── GDD.md                # 게임 기획서
├── project.godot          # 프로젝트 설정 (입력맵 포함)
├── scenes/
│   ├── Main.tscn           # 메인 씬 (스테이지+플레이어 스폰)
│   ├── Player.tscn          # 랙돌 캐릭터
│   └── Stage.tscn            # 스테이지(바닥+낙사존)
└── scripts/
    ├── Main.gd
    ├── Player.gd            # 랙돌 물리 + 이동/점프/잡기/밀기 로직
    └── Stage.gd             # 바닥, 낙사존
```

> 참고: 이 저장소 루트에는 게임과 무관한 기존 정적 웹사이트(마켓인사이트) 파일들도 함께
> 들어있습니다. 루트 `README.md`는 그 웹사이트 문서이므로, 게임 관련 안내는 이 파일
> (`GAME_README.md`)에 정리합니다.

## 현재 상태 (M1 단계)

- [x] 랙돌 캐릭터 물리 뼈대 (몸통-머리-팔-다리, PinJoint2D 연결)
- [x] 이동/점프/밀기/잡기 기본 로직
- [x] 낙사존 판정 → 리스폰 처리
- [x] 캡슐/원형 + 테두리 비주얼 (RagdollVisual.gd)
- [x] 로컬 2인 별도 입력 분리 (device_id 0/1 → p1_*/p2_* 액션, project.godot [input] 참고)
- [ ] 스테이지 기믹 (좁아지는 발판/컨베이어 벨트/회전 장애물) — 현재는 낙사존뿐
- [ ] 네트워크 멀티플레이 (M4 단계에서 진행 예정)

## 다음 단계 (Claude Code로 이어서 작업 시 프롬프트 예시)

이 프로젝트 폴더를 열고 Claude Code(`claude` 명령)를 실행한 뒤 아래처럼 요청하면 이어서 개발할 수 있습니다:

1. "Stage.gd에 컨베이어 벨트 기믹을 추가해줘"
2. "Stage.gd에 좁아지는 발판 기믹을 추가해줘"
3. "Godot MultiplayerSynchronizer를 이용해서 호스트 권위 방식 네트워크 동기화를 붙여줘"

## 알아두어야 할 것

- `project.godot`의 `[input]` 섹션은 최소 형태로 작성되어 있습니다. Godot 에디터에서 Project > Project Settings > Input Map에서 정상 인식되는지 확인하고, 필요하면 GUI에서 다시 매핑해 주세요.
- 랙돌 관절 값(softness, damp 등)은 초기값이라 캐릭터가 뻣뻣하거나 흐물거릴 수 있습니다. Player.gd 상단의 @export 변수와 `_connect_joint`의 `softness` 값을 조정하며 튜닝하세요.
- 밀기(`_push_nearby`)와 잡기(`_try_grab`)는 오른팔(arm_r) 위치 기준으로 근접 판정합니다. 좌우 반전 시 로직 보강이 필요합니다.
