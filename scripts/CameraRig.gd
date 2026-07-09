extends Camera2D

## "player_torso" 그룹(생존한 플레이어의 몸통)을 모두 화면에 담기게 따라가며 줌을 조절하고,
## shake()로 순간적인 화면 흔들림을 낸다.

@export var follow_speed: float = 4.0
@export var zoom_speed: float = 4.0
@export var min_zoom: float = 0.85  # 더 작을수록 확대(줌인)
@export var max_zoom: float = 1.9   # 더 클수록 축소(줌아웃)
@export var padding: Vector2 = Vector2(220, 170)

var _shake_time: float = 0.0
var _shake_strength: float = 0.0

func _ready() -> void:
	add_to_group("camera_rig")
	position_smoothing_enabled = false
	enabled = true

func _process(delta: float) -> void:
	_follow_players(delta)
	_update_shake()

func _follow_players(delta: float) -> void:
	var torsos := get_tree().get_nodes_in_group("player_torso")
	if torsos.is_empty():
		return

	var min_pos: Vector2 = torsos[0].global_position
	var max_pos: Vector2 = torsos[0].global_position
	for t in torsos:
		var p: Vector2 = t.global_position
		min_pos.x = min(min_pos.x, p.x)
		min_pos.y = min(min_pos.y, p.y)
		max_pos.x = max(max_pos.x, p.x)
		max_pos.y = max(max_pos.y, p.y)

	var center := (min_pos + max_pos) / 2.0
	var span := (max_pos - min_pos) + padding * 2.0
	var viewport_size := get_viewport_rect().size

	var zoom_x := span.x / viewport_size.x
	var zoom_y := span.y / viewport_size.y
	var target_zoom: float = clamp(max(zoom_x, zoom_y), min_zoom, max_zoom)

	global_position = global_position.lerp(center, clamp(follow_speed * delta, 0.0, 1.0))
	zoom = zoom.lerp(Vector2.ONE * target_zoom, clamp(zoom_speed * delta, 0.0, 1.0))

func shake(strength: float, duration: float) -> void:
	_shake_strength = max(_shake_strength, strength)
	_shake_time = max(_shake_time, duration)

func _update_shake() -> void:
	if _shake_time <= 0.0:
		offset = Vector2.ZERO
		return
	_shake_time = max(_shake_time - get_process_delta_time(), 0.0)
	offset = Vector2(randf_range(-1.0, 1.0), randf_range(-1.0, 1.0)) * _shake_strength
