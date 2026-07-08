extends Node2D
class_name Player

## 랙돌 캐릭터 컨트롤러
## 몸통(Torso)을 중심으로 머리/팔/다리를 PinJoint2D로 연결한 물리 기반 캐릭터
## 1P: 이동(WASD/방향키) + 점프(Space) + 잡기(Shift) + 밀기(마우스 좌클릭)

const RAGDOLL_VISUAL_SCRIPT := preload("res://scripts/RagdollVisual.gd")

@export var move_force: float = 900.0
@export var jump_impulse: float = 350.0
@export var push_impulse: float = 400.0
@export var player_color: Color = Color(0.9, 0.3, 0.3)
@export var device_id: int = 0  # 로컬 멀티용: 0=키보드, 1=패드1 등

var torso: RigidBody2D
var head: RigidBody2D
var arm_l: RigidBody2D
var arm_r: RigidBody2D
var leg_l: RigidBody2D
var leg_r: RigidBody2D

var is_grounded: bool = false
var grabbed_body: RigidBody2D = null
var grab_joint: PinJoint2D = null

func _ready() -> void:
	_build_ragdoll()

func _build_ragdoll() -> void:
	# 몸통
	torso = _make_limb(Vector2(0, 0), Vector2(20, 30), 1.0)
	# 머리
	head = _make_limb(Vector2(0, -45), Vector2(16, 16), 0.6, true)
	# 팔
	arm_l = _make_limb(Vector2(-25, -10), Vector2(8, 25), 0.4)
	arm_r = _make_limb(Vector2(25, -10), Vector2(8, 25), 0.4)
	# 다리
	leg_l = _make_limb(Vector2(-10, 40), Vector2(9, 28), 0.5)
	leg_r = _make_limb(Vector2(10, 40), Vector2(9, 28), 0.5)

	_connect_joint(torso, head, Vector2(0, -25))
	_connect_joint(torso, arm_l, Vector2(-15, -15))
	_connect_joint(torso, arm_r, Vector2(15, -15))
	_connect_joint(torso, leg_l, Vector2(-10, 20))
	_connect_joint(torso, leg_r, Vector2(10, 20))

func _make_limb(local_pos: Vector2, size: Vector2, mass: float, is_circle: bool = false) -> RigidBody2D:
	var body := RigidBody2D.new()
	body.position = local_pos
	body.mass = mass
	body.gravity_scale = 1.0
	body.linear_damp = 0.5
	body.angular_damp = 2.0
	body.contact_monitor = true
	body.max_contacts_reported = 4
	body.add_to_group("ragdoll_part")

	var shape := CollisionShape2D.new()
	if is_circle:
		var c := CircleShape2D.new()
		c.radius = size.x
		shape.shape = c
	else:
		var cap := CapsuleShape2D.new()
		cap.radius = size.x / 2.0
		cap.height = size.y
		shape.shape = cap
	body.add_child(shape)

	var visual := RAGDOLL_VISUAL_SCRIPT.new()
	visual.fill_color = player_color
	visual.shape_size = size
	visual.is_circle = is_circle
	body.add_child(visual)

	add_child(body)
	return body

func _connect_joint(body_a: RigidBody2D, body_b: RigidBody2D, world_offset: Vector2) -> void:
	var joint := PinJoint2D.new()
	joint.position = body_a.position + world_offset
	joint.node_a = body_a.get_path()
	joint.node_b = body_b.get_path()
	joint.softness = 0.05
	add_child(joint)

func _physics_process(_delta: float) -> void:
	if not torso:
		return
	_handle_movement()
	_check_grounded()

func _action(action_name: String) -> String:
	# device_id 0 = 1P 입력 스킴, 1 = 2P 입력 스킴 (project.godot의 p1_*/p2_* 액션)
	return "p%d_%s" % [device_id + 1, action_name]

func _handle_movement() -> void:
	var dir := Vector2.ZERO
	if Input.is_action_pressed(_action("move_left")):
		dir.x -= 1
	if Input.is_action_pressed(_action("move_right")):
		dir.x += 1

	if dir.length() > 0:
		torso.apply_central_force(dir.normalized() * move_force)
		# 다리도 같이 밀어줘서 걷는 느낌
		leg_l.apply_central_force(dir.normalized() * move_force * 0.3)
		leg_r.apply_central_force(dir.normalized() * move_force * 0.3)

	if Input.is_action_just_pressed(_action("jump")) and is_grounded:
		torso.apply_central_impulse(Vector2(0, -jump_impulse))

	if Input.is_action_just_pressed(_action("push")):
		_push_nearby()

	if Input.is_action_pressed(_action("grab")):
		_try_grab()
	else:
		_release_grab()

func _check_grounded() -> void:
	# 간단한 접지 판정: 다리의 수직 속도가 낮으면 접지로 간주 (1차 버전, 추후 Raycast로 개선 권장)
	is_grounded = abs(leg_l.linear_velocity.y) < 50 or abs(leg_r.linear_velocity.y) < 50

func _push_nearby() -> void:
	# 팔 위치 기준으로 근처 다른 플레이어 몸통에 임펄스 적용
	var space_state := get_world_2d().direct_space_state
	var query := PhysicsShapeQueryParameters2D.new()
	var shape := CircleShape2D.new()
	shape.radius = 40
	query.shape = shape
	query.transform = Transform2D(0, arm_r.global_position)
	query.exclude = [self]
	var results := space_state.intersect_shape(query)
	for r in results:
		var col = r["collider"]
		if col is RigidBody2D and col.get_parent() != self:
			var push_dir = (col.global_position - arm_r.global_position).normalized()
			col.apply_central_impulse(push_dir * push_impulse)

func _try_grab() -> void:
	if grabbed_body:
		return
	var space_state := get_world_2d().direct_space_state
	var query := PhysicsShapeQueryParameters2D.new()
	var shape := CircleShape2D.new()
	shape.radius = 30
	query.shape = shape
	query.transform = Transform2D(0, arm_r.global_position)
	query.exclude = [self]
	var results := space_state.intersect_shape(query)
	for r in results:
		var col = r["collider"]
		if col is RigidBody2D and col.get_parent() != self:
			grabbed_body = col
			grab_joint = PinJoint2D.new()
			get_tree().current_scene.add_child(grab_joint)
			grab_joint.global_position = arm_r.global_position
			grab_joint.node_a = arm_r.get_path()
			grab_joint.node_b = col.get_path()
			break

func _release_grab() -> void:
	if grab_joint:
		grab_joint.queue_free()
		grab_joint = null
		grabbed_body = null

func eliminate() -> void:
	# 낙사존 진입 시 Stage.gd에서 호출됨. 1차 버전은 리스폰만 처리.
	print(name, " 탈락!")
	_respawn(Vector2(0, -100))

func _respawn(new_pos: Vector2) -> void:
	position = new_pos
	for limb in [torso, head, arm_l, arm_r, leg_l, leg_r]:
		if limb:
			limb.linear_velocity = Vector2.ZERO
			limb.angular_velocity = 0.0
