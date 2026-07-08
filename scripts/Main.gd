extends Node2D

## 메인 게임 씬: 스테이지 생성 + 로컬 테스트용 플레이어 스폰
## 네트워크 붙이기 전 단계이므로 우선 로컬 1~2인 테스트용으로 구성

const PLAYER_SCENE := preload("res://scenes/Player.tscn")
const STAGE_SCENE := preload("res://scenes/Stage.tscn")

@export var local_test_player_count: int = 2

func _ready() -> void:
	var stage := STAGE_SCENE.instantiate()
	add_child(stage)

	_spawn_local_test_players()

func _spawn_local_test_players() -> void:
	var colors := [Color(0.9, 0.3, 0.3), Color(0.3, 0.5, 0.9), Color(0.3, 0.9, 0.4), Color(0.9, 0.8, 0.2)]
	for i in range(local_test_player_count):
		var p := PLAYER_SCENE.instantiate()
		p.position = Vector2(-100 + i * 150, -100)
		p.player_color = colors[i % colors.size()]
		p.player_index = i
		p.name = "Player%d" % i
		add_child(p)

	# 2인 로컬 테스트: Player.gd가 player_index에 따라 p1_*/p2_* 입력 액션을
	# 분기해서 사용합니다 (InputSetup.gd 오토로드에서 키 매핑 정의).
