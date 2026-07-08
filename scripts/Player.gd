extends Node2D

## 랙돌 캐릭터 컨트롤러: 몸통에 힘을 가해 이동시키고, 점프/잡기/밀기를 처리한다.
## 정교한 조작감이 아니라 물리 반응 자체가 재미 요소이므로 로직은 최소한으로 유지한다.

@export var player_color: Color = Color.WHITE
@export var player_index: int = 0

const MOVE_FORCE := 900.0
const JUMP_IMPULSE := 380.0
const GRAB_RANGE := 42.0
const PUNCH_RANGE := 46.0
const PUNCH_IMPULSE := 420.0
const GROUND_CHECK_DISTANCE := 55.0

const INPUT_SCHEMES := [
	{"left": "p1_left", "right": "p1_right", "jump": "p1_jump", "grab": "p1_grab", "punch": "p1_punch"},
	{"left": "p2_left", "right": "p2_right", "jump": "p2_jump", "grab": "p2_grab", "punch": "p2_punch"},
]

@onready var torso: RigidBody2D = $Torso
@onready var head: RigidBody2D = $Head
@onready var arm_l: RigidBody2D = $ArmL
@onready var arm_r: RigidBody2D = $ArmR
@onready var leg_l: RigidBody2D = $LegL
@onready var leg_r: RigidBody2D = $LegR
@onready var ground_ray: RayCast2D = $Torso/GroundRayCast
@onready var hand: Marker2D = $ArmR/Hand

var _grab_joint: PinJoint2D = null

func _ready() -> void:
	ground_ray.target_position = Vector2(0, GROUND_CHECK_DISTANCE)
	_apply_color()
	_add_joint_collision_exceptions()

func _add_joint_collision_exceptions() -> void:
	for limb in [head, arm_l, arm_r, leg_l, leg_r]:
		torso.add_collision_exception_with(limb)
		limb.add_collision_exception_with(torso)

func _apply_color() -> void:
	for part in [torso, head, arm_l, arm_r, leg_l, leg_r]:
		var visual := part.get_node_or_null("Visual")
		if visual:
			visual.color = player_color

func _physics_process(_delta: float) -> void:
	var scheme: Dictionary = INPUT_SCHEMES[player_index % INPUT_SCHEMES.size()]

	var move := Input.get_action_strength(scheme["right"]) - Input.get_action_strength(scheme["left"])
	torso.apply_central_force(Vector2(move * MOVE_FORCE, 0))

	if Input.is_action_just_pressed(scheme["jump"]) and ground_ray.is_colliding():
		torso.apply_central_impulse(Vector2(0, -JUMP_IMPULSE))

	if Input.is_action_just_pressed(scheme["grab"]):
		_try_grab()
	elif Input.is_action_just_released(scheme["grab"]):
		_release_grab()

	if Input.is_action_just_pressed(scheme["punch"]):
		_try_punch()

func _try_grab() -> void:
	if _grab_joint:
		return
	for body in get_tree().get_nodes_in_group("ragdoll_part"):
		if body.get_parent() == self:
			continue
		if hand.global_position.distance_to(body.global_position) <= GRAB_RANGE:
			_grab_joint = PinJoint2D.new()
			add_child(_grab_joint)
			_grab_joint.global_position = hand.global_position
			_grab_joint.node_a = arm_r.get_path()
			_grab_joint.node_b = body.get_path()
			break

func _release_grab() -> void:
	if _grab_joint:
		_grab_joint.queue_free()
		_grab_joint = null

func _try_punch() -> void:
	for body in get_tree().get_nodes_in_group("ragdoll_part"):
		if body.get_parent() == self:
			continue
		var dist := hand.global_position.distance_to(body.global_position)
		if dist <= PUNCH_RANGE:
			var dir := (body.global_position - hand.global_position).normalized()
			body.apply_central_impulse(dir * PUNCH_IMPULSE)
