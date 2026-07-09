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
@export var lives: int = 1  # 낙사존에 이 횟수만큼 떨어지면 완전 탈락 (기본 1: 즉시 탈락)

## 몸통/다리를 세워두는 복원력(PD 제어). 값을 키우면 더 꼿꼿하게 서고,
## 줄이면 더 흐물흐물해진다. 팔은 일부러 제외해서 랙돌 느낌은 유지.
@export var torso_balance_stiffness: float = 26000.0
@export var torso_balance_damping: float = 1600.0
@export var leg_balance_stiffness: float = 9000.0
@export var leg_balance_damping: float = 700.0

signal went_out(player: Player)

var torso: RigidBody2D
var head: RigidBody2D
var arm_l: RigidBody2D
var arm_r: RigidBody2D
var leg_l: RigidBody2D
var leg_r: RigidBody2D

const COYOTE_TIME := 0.15  # 발이 막 떨어져도 잠깐은 점프를 허용
const JUMP_BUFFER_TIME := 0.15  # 착지 살짝 전에 눌러도 점프가 예약되도록

var is_grounded: bool = false
var is_out: bool = false
var grabbed_body: RigidBody2D = null
var grab_joint: PinJoint2D = null
var _ground_ray_l: RayCast2D
var _ground_ray_r: RayCast2D
var _coyote_timer: float = 0.0
var _jump_buffer_timer: float = 0.0

func _ready() -> void:
	_build_ragdoll()

func _build_ragdoll() -> void:
	# 몸통
	torso = _make_limb(Vector2(0, 0), Vector2(20, 30), 1.0)
	torso.add_to_group("player_torso")
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

	_setup_ground_rays()

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

func _setup_ground_rays() -> void:
	# 다리 밑으로 짧은 레이캐스트를 쏴서 접지를 판정한다.
	# Player 루트(회전하지 않음)에 붙이고 매 프레임 다리 위치로 옮겨서 사용한다.
	# 다리 자체의 자식으로 붙이면 다리가 넘어질 때(랙돌 특성상 거의 항상 그럼)
	# "아래" 방향 레이가 다리 회전을 따라 같이 돌아가서 땅을 못 가리키는 문제가 있었다.
	_ground_ray_l = _make_ground_ray()
	_ground_ray_r = _make_ground_ray()
	for limb in [torso, head, arm_l, arm_r, leg_l, leg_r]:
		_ground_ray_l.add_exception(limb)
		_ground_ray_r.add_exception(limb)

func _make_ground_ray() -> RayCast2D:
	var ray := RayCast2D.new()
	ray.target_position = Vector2(0, 20)
	ray.collision_mask = 1
	add_child(ray)
	return ray

func _physics_process(delta: float) -> void:
	if not torso or is_out:
		return
	_apply_balance()
	_check_grounded()
	_update_jump_timers(delta)
	_handle_movement()

func _apply_balance() -> void:
	# 몸통과 다리에 "똑바로 서려는" 토크를 걸어준다. 액티브 랙돌 없이 PinJoint2D만
	# 쓰면 자유롭게 회전하는 관절 특성상 스폰하자마자 힘없이 주저앉아버리고,
	# 다리도 몸통 아래가 아니라 아무 데나 널브러져서 접지 판정 자체가 불가능해진다.
	_balance_body(torso, torso_balance_stiffness, torso_balance_damping)
	_balance_body(leg_l, leg_balance_stiffness, leg_balance_damping)
	_balance_body(leg_r, leg_balance_stiffness, leg_balance_damping)

func _balance_body(body: RigidBody2D, stiffness: float, damping: float) -> void:
	var rotation_error := wrapf(-body.rotation, -PI, PI)
	var torque := rotation_error * stiffness - body.angular_velocity * damping
	body.apply_torque(torque)

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

	if Input.is_action_just_pressed(_action("jump")):
		_jump_buffer_timer = JUMP_BUFFER_TIME

	if _jump_buffer_timer > 0.0 and _coyote_timer > 0.0:
		torso.apply_central_impulse(Vector2(0, -jump_impulse))
		SoundFX.play_jump()
		_jump_buffer_timer = 0.0
		_coyote_timer = 0.0

	if Input.is_action_just_pressed(_action("push")):
		_push_nearby()

	if Input.is_action_pressed(_action("grab")):
		_try_grab()
	else:
		_release_grab()

func _check_grounded() -> void:
	_ground_ray_l.global_position = leg_l.global_position
	_ground_ray_r.global_position = leg_r.global_position
	_ground_ray_l.force_raycast_update()
	_ground_ray_r.force_raycast_update()
	is_grounded = _ground_ray_l.is_colliding() or _ground_ray_r.is_colliding()

func _update_jump_timers(delta: float) -> void:
	if is_grounded:
		_coyote_timer = COYOTE_TIME
	else:
		_coyote_timer = max(_coyote_timer - delta, 0.0)
	_jump_buffer_timer = max(_jump_buffer_timer - delta, 0.0)

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
	var hit_something := false
	var hit_pos := Vector2.ZERO
	for r in results:
		var col = r["collider"]
		if col is RigidBody2D and col.get_parent() != self:
			var push_dir = (col.global_position - arm_r.global_position).normalized()
			col.apply_central_impulse(push_dir * push_impulse)
			hit_something = true
			hit_pos = col.global_position
	if hit_something:
		SoundFX.play_punch()
		FX.spawn_burst(get_tree().current_scene, hit_pos, player_color, 10)
		get_tree().call_group("camera_rig", "shake", 5.0, 0.12)

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
			SoundFX.play_grab()
			break

func _release_grab() -> void:
	if grab_joint:
		grab_joint.queue_free()
		grab_joint = null
		grabbed_body = null

func eliminate() -> void:
	# 낙사존 진입 시 Stage.gd에서 호출됨.
	if is_out:
		return
	lives -= 1
	if lives <= 0:
		_go_out()
	else:
		print(name, " 탈락! (남은 목숨 ", lives, ")")
		SoundFX.play_eliminate()
		_respawn(Vector2(0, -100))

func _respawn(new_pos: Vector2) -> void:
	position = new_pos
	for limb in [torso, head, arm_l, arm_r, leg_l, leg_r]:
		if limb:
			limb.linear_velocity = Vector2.ZERO
			limb.angular_velocity = 0.0

func _go_out() -> void:
	# 목숨을 모두 소진하면 완전히 게임에서 빠진다 (콜리전 제거 + 숨김).
	is_out = true
	print(name, " 완전 탈락!")
	SoundFX.play_out()
	FX.spawn_burst(get_tree().current_scene, torso.global_position, player_color, 18)
	get_tree().call_group("camera_rig", "shake", 10.0, 0.25)
	_release_grab()
	torso.remove_from_group("player_torso")
	for limb in [torso, head, arm_l, arm_r, leg_l, leg_r]:
		if limb:
			limb.freeze = true
			limb.visible = false
			limb.collision_layer = 0
			limb.collision_mask = 0
	went_out.emit(self)
