extends Node2D
class_name Stage

## 기본 스테이지: 좁아지는 발판 + 낙사존
## 추후 컨베이어 벨트, 회전 장애물 등 기믹은 이 스크립트에 노드 추가로 확장

@export var floor_width: float = 800.0
@export var floor_height: float = 40.0

## 좁아지는 발판 기믹 (GDD 5번 1순위)
@export var narrowing_enabled: bool = true
@export var narrow_delay: float = 5.0  # 좁아지기 시작까지 대기 시간(초)
@export var narrow_speed: float = 10.0  # 초당 줄어드는 폭(px)
@export var narrow_min_width: float = 160.0  # 최소 폭

var _floor_shape: RectangleShape2D
var _floor_visual: ColorRect
var _narrow_elapsed: float = 0.0

func _ready() -> void:
	_build_floor()
	_build_death_zone()

func _process(delta: float) -> void:
	if not narrowing_enabled or _floor_shape.size.x <= narrow_min_width:
		return
	_narrow_elapsed += delta
	if _narrow_elapsed < narrow_delay:
		return
	var new_width: float = max(_floor_shape.size.x - narrow_speed * delta, narrow_min_width)
	_floor_shape.size.x = new_width
	_floor_visual.size.x = new_width
	_floor_visual.position.x = -new_width / 2.0

func _build_floor() -> void:
	var floor_body := StaticBody2D.new()
	floor_body.position = Vector2(0, 300)
	var shape := CollisionShape2D.new()
	var rect := RectangleShape2D.new()
	rect.size = Vector2(floor_width, floor_height)
	shape.shape = rect
	floor_body.add_child(shape)

	var visual := ColorRect.new()
	visual.color = Color(0.35, 0.35, 0.4)
	visual.size = rect.size
	visual.position = -rect.size / 2.0
	floor_body.add_child(visual)

	add_child(floor_body)

	_floor_shape = rect
	_floor_visual = visual

func _build_death_zone() -> void:
	# 스테이지 하단에 닿으면 탈락 처리하는 Area2D
	var zone := Area2D.new()
	zone.position = Vector2(0, 600)
	var shape := CollisionShape2D.new()
	var rect := RectangleShape2D.new()
	rect.size = Vector2(2000, 50)
	shape.shape = rect
	zone.add_child(shape)
	zone.body_entered.connect(_on_death_zone_entered)
	add_child(zone)

func _on_death_zone_entered(body: Node) -> void:
	# body는 랙돌의 개별 파츠(RigidBody2D)이므로 부모(Player)를 찾아 탈락 처리
	var player := body.get_parent()
	if player and player.has_method("eliminate"):
		player.eliminate()
	else:
		print("낙사 감지: ", body.get_path())
