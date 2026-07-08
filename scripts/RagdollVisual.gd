extends Node2D

## 랙돌 파츠 시각화: ColorRect 대신 캡슐/원형 + 테두리를 직접 그린다.
## is_circle이면 머리로 간주해 간단한 눈 디테일도 함께 그린다.

@export var fill_color: Color = Color.WHITE
@export var outline_color: Color = Color(0, 0, 0, 0.55)
@export var outline_width: float = 3.0
@export var shape_size: Vector2 = Vector2(20, 30)
@export var is_circle: bool = false

func _draw() -> void:
	if is_circle:
		var radius: float = shape_size.x
		draw_circle(Vector2.ZERO, radius + outline_width, outline_color)
		draw_circle(Vector2.ZERO, radius, fill_color)
		_draw_face(radius)
	else:
		var radius: float = shape_size.x / 2.0
		var half_h: float = max(shape_size.y / 2.0 - radius, 0.0)
		_draw_capsule(radius + outline_width, half_h, outline_color)
		_draw_capsule(radius, half_h, fill_color)

func _draw_capsule(radius: float, half_h: float, color: Color) -> void:
	draw_circle(Vector2(0, -half_h), radius, color)
	draw_circle(Vector2(0, half_h), radius, color)
	if half_h > 0.0:
		draw_rect(Rect2(Vector2(-radius, -half_h), Vector2(radius * 2.0, half_h * 2.0)), color)

func _draw_face(radius: float) -> void:
	var eye_offset := radius * 0.4
	var eye_y := -radius * 0.05
	var eye_radius := radius * 0.14
	draw_circle(Vector2(-eye_offset, eye_y), eye_radius, Color.BLACK)
	draw_circle(Vector2(eye_offset, eye_y), eye_radius, Color.BLACK)
