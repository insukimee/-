extends Node3D

## 3D 프로토타입 진입 씬: 조명/환경 설정 + 스테이지/플레이어 스폰
## 아직 1인용 로컬 테스트 수준 (p1_* 입력만 사용, 목숨/승리 조건 없음)

const PLAYER_SCENE := preload("res://scenes3d/Player3D.tscn")
const STAGE_SCENE := preload("res://scenes3d/Stage3D.tscn")

func _ready() -> void:
	_build_lighting()

	var stage := STAGE_SCENE.instantiate()
	add_child(stage)

	var p := PLAYER_SCENE.instantiate()
	p.position = Vector3(0, 1.5, 0)
	add_child(p)

func _build_lighting() -> void:
	var sun := DirectionalLight3D.new()
	sun.rotation_degrees = Vector3(-50, -30, 0)
	sun.light_energy = 1.1
	add_child(sun)

	var env_node := WorldEnvironment.new()
	var env := Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color(0.55, 0.62, 0.68)
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color(0.5, 0.5, 0.55)
	env_node.environment = env
	add_child(env_node)
