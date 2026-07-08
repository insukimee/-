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
	sun.rotation_degrees = Vector3(-48, -35, 0)
	sun.light_energy = 1.15
	sun.light_color = Color(1.0, 0.96, 0.9)
	sun.shadow_enabled = true
	sun.directional_shadow_max_distance = 40.0
	add_child(sun)

	# 반대쪽에서 은은하게 채워주는 보조광 (그림자 진 면이 완전히 새까맣지 않도록)
	var fill := DirectionalLight3D.new()
	fill.rotation_degrees = Vector3(-20, 140, 0)
	fill.light_energy = 0.35
	fill.light_color = Color(0.75, 0.82, 1.0)
	add_child(fill)

	var env_node := WorldEnvironment.new()
	var env := Environment.new()

	env.background_mode = Environment.BG_SKY
	var sky_material := ProceduralSkyMaterial.new()
	sky_material.sky_top_color = Color(0.35, 0.5, 0.75)
	sky_material.sky_horizon_color = Color(0.75, 0.8, 0.85)
	sky_material.ground_bottom_color = Color(0.3, 0.28, 0.25)
	sky_material.ground_horizon_color = Color(0.55, 0.5, 0.45)
	var sky := Sky.new()
	sky.sky_material = sky_material
	env.sky = sky

	env.ambient_light_source = Environment.AMBIENT_SOURCE_SKY
	env.ambient_light_energy = 0.9

	env.fog_enabled = true
	env.fog_light_color = Color(0.75, 0.8, 0.85)
	env.fog_density = 0.012

	env.ssao_enabled = true
	env.ssao_intensity = 1.5

	env.glow_enabled = true
	env.glow_intensity = 0.5
	env.glow_bloom = 0.05

	env.tonemap_mode = Environment.TONE_MAPPER_FILMIC

	env_node.environment = env
	add_child(env_node)
