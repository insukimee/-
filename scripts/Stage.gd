extends Node2D
class_name Stage

## 기본 스테이지: 바닥 + 낙사존
## 추후 컨베이어 벨트, 회전 장애물 등 기믹은 이 스크립트에 노드 추가로 확장

@export var floor_width: float = 800.0
@export var floor_height: float = 40.0

func _ready() -> void:
	_build_floor()
	_build_death_zone()

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
