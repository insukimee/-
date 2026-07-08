extends Node3D
class_name Stage3D

## 공사장 컨셉의 첫 3D 스테이지: 콘크리트 바닥 + 비계 기둥 + 굴러다니는 드럼통
## 여러 컨셉 맵을 만들 때는 이 스크립트를 복제해 Stage3D_Rooftop.gd 등으로 확장한다.

func _ready() -> void:
	_build_floor()
	_build_construction_props()

func _build_floor() -> void:
	var floor_body := StaticBody3D.new()
	var shape := CollisionShape3D.new()
	var box := BoxShape3D.new()
	box.size = Vector3(20, 1, 8)
	shape.shape = box
	floor_body.add_child(shape)

	var mesh_instance := MeshInstance3D.new()
	var mesh := BoxMesh.new()
	mesh.size = box.size
	mesh_instance.mesh = mesh
	var mat := StandardMaterial3D.new()
	mat.albedo_color = Color(0.45, 0.42, 0.4)
	mesh_instance.material_override = mat
	floor_body.add_child(mesh_instance)

	floor_body.position = Vector3(0, -0.5, 0)
	add_child(floor_body)

func _build_construction_props() -> void:
	_add_beam(Vector3(-7, 1.5, 0))
	_add_beam(Vector3(7, 1.5, 0))
	_add_barrel(Vector3(3, 0.5, 0))
	_add_barrel(Vector3(-3, 0.5, 1))

func _add_beam(pos: Vector3) -> void:
	var body := StaticBody3D.new()
	var shape := CollisionShape3D.new()
	var box := BoxShape3D.new()
	box.size = Vector3(0.4, 3.0, 0.4)
	shape.shape = box
	body.add_child(shape)

	var mesh_instance := MeshInstance3D.new()
	var mesh := BoxMesh.new()
	mesh.size = box.size
	mesh_instance.mesh = mesh
	var mat := StandardMaterial3D.new()
	mat.albedo_color = Color(0.75, 0.5, 0.15)
	mesh_instance.material_override = mat
	body.add_child(mesh_instance)

	body.position = pos
	add_child(body)

func _add_barrel(pos: Vector3) -> void:
	# 물리적으로 굴러다니는 장애물 (RigidBody3D)
	var body := RigidBody3D.new()
	body.mass = 4.0
	var shape := CollisionShape3D.new()
	var cyl := CylinderShape3D.new()
	cyl.radius = 0.4
	cyl.height = 1.0
	shape.shape = cyl
	body.add_child(shape)

	var mesh_instance := MeshInstance3D.new()
	var mesh := CylinderMesh.new()
	mesh.top_radius = 0.4
	mesh.bottom_radius = 0.4
	mesh.height = 1.0
	mesh_instance.mesh = mesh
	var mat := StandardMaterial3D.new()
	mat.albedo_color = Color(0.8, 0.25, 0.2)
	mesh_instance.material_override = mat
	body.add_child(mesh_instance)

	body.position = pos
	add_child(body)
