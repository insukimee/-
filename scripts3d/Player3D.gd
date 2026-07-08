extends Node3D
class_name Player3D

## 3D 랙돌 프로토타입 (2D Player.gd의 3D 이식 1단계)
## 몸통을 중심으로 머리/팔/다리를 캡슐 RigidBody3D + PinJoint3D로 연결한다.
## 아직 1P 입력(p1_*)만 사용하고, 목숨/탈락/이펙트/사운드는 붙이지 않은 최소 프로토타입.

@export var move_force: float = 9.0
@export var jump_impulse: float = 5.5
@export var push_impulse: float = 7.0
@export var player_color: Color = Color(0.9, 0.3, 0.3)

var torso: RigidBody3D
var head: RigidBody3D
var arm_l: RigidBody3D
var arm_r: RigidBody3D
var leg_l: RigidBody3D
var leg_r: RigidBody3D

var is_grounded: bool = false
var _ground_ray: RayCast3D

func _ready() -> void:
	_build_ragdoll()

func _build_ragdoll() -> void:
	torso = _make_limb(Vector3(0, 0, 0), 0.32, 0.85, 6.0)
	head = _make_limb(Vector3(0, 1.05, 0), 0.26, 0.0, 3.0, true)
	arm_l = _make_limb(Vector3(-0.5, 0.3, 0), 0.13, 0.65, 2.0)
	arm_r = _make_limb(Vector3(0.5, 0.3, 0), 0.13, 0.65, 2.0)
	leg_l = _make_limb(Vector3(-0.2, -0.95, 0), 0.15, 0.8, 3.0)
	leg_r = _make_limb(Vector3(0.2, -0.95, 0), 0.15, 0.8, 3.0)

	_connect_joint(torso, head, Vector3(0, 0.55, 0))
	_connect_joint(torso, arm_l, Vector3(-0.35, 0.3, 0))
	_connect_joint(torso, arm_r, Vector3(0.35, 0.3, 0))
	_connect_joint(torso, leg_l, Vector3(-0.2, -0.45, 0))
	_connect_joint(torso, leg_r, Vector3(0.2, -0.45, 0))

	_setup_ground_ray()

func _make_limb(local_pos: Vector3, radius: float, height: float, mass: float, is_sphere: bool = false) -> RigidBody3D:
	var body := RigidBody3D.new()
	body.position = local_pos
	body.mass = mass
	body.linear_damp = 0.4
	body.angular_damp = 1.5
	body.add_to_group("ragdoll_part")

	var shape := CollisionShape3D.new()
	var mesh_instance := MeshInstance3D.new()
	if is_sphere:
		var sphere := SphereShape3D.new()
		sphere.radius = radius
		shape.shape = sphere
		var mesh := SphereMesh.new()
		mesh.radius = radius
		mesh.height = radius * 2.0
		mesh_instance.mesh = mesh
	else:
		var cap := CapsuleShape3D.new()
		cap.radius = radius
		cap.height = height
		shape.shape = cap
		var mesh := CapsuleMesh.new()
		mesh.radius = radius
		mesh.height = height
		mesh_instance.mesh = mesh
	body.add_child(shape)

	var mat := StandardMaterial3D.new()
	mat.albedo_color = player_color
	mesh_instance.material_override = mat
	body.add_child(mesh_instance)

	add_child(body)
	return body

func _connect_joint(a: RigidBody3D, b: RigidBody3D, world_offset: Vector3) -> void:
	var joint := PinJoint3D.new()
	joint.position = a.position + world_offset
	joint.node_a = a.get_path()
	joint.node_b = b.get_path()
	add_child(joint)

func _setup_ground_ray() -> void:
	_ground_ray = RayCast3D.new()
	_ground_ray.target_position = Vector3(0, -0.35, 0)
	leg_l.add_child(_ground_ray)
	for limb in [torso, head, arm_l, arm_r, leg_l, leg_r]:
		_ground_ray.add_exception(limb)

func _physics_process(_delta: float) -> void:
	if not torso:
		return

	is_grounded = _ground_ray.is_colliding()

	var dir := 0.0
	if Input.is_action_pressed("p1_move_left"):
		dir -= 1.0
	if Input.is_action_pressed("p1_move_right"):
		dir += 1.0
	if dir != 0.0:
		torso.apply_central_force(Vector3(dir * move_force, 0, 0))
		leg_l.apply_central_force(Vector3(dir * move_force * 0.3, 0, 0))
		leg_r.apply_central_force(Vector3(dir * move_force * 0.3, 0, 0))

	if Input.is_action_just_pressed("p1_jump") and is_grounded:
		torso.apply_central_impulse(Vector3(0, jump_impulse, 0))

	if Input.is_action_just_pressed("p1_push"):
		_push_nearby()

func _push_nearby() -> void:
	var space_state := get_world_3d().direct_space_state
	var query := PhysicsShapeQueryParameters3D.new()
	var shape := SphereShape3D.new()
	shape.radius = 0.9
	query.shape = shape
	query.transform = Transform3D(Basis(), arm_r.global_position)
	query.exclude = [self]
	var results := space_state.intersect_shape(query)
	for r in results:
		var col = r["collider"]
		if col is RigidBody3D and col.get_parent() != self:
			var push_dir: Vector3 = (col.global_position - arm_r.global_position).normalized()
			col.apply_central_impulse(push_dir * push_impulse)
