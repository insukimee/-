extends Node3D
class_name Stage3D

## 공사장 컨셉의 첫 3D 스테이지: 콘크리트 바닥 + 비계 기둥 + 굴러다니는 드럼통 + 경고 펜스
## 여러 컨셉 맵을 만들 때는 이 스크립트를 복제해 Stage3D_Rooftop.gd 등으로 확장한다.

var _stripe_texture: ImageTexture

func _ready() -> void:
	_stripe_texture = _make_stripe_texture()
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
	mat.roughness = 0.9
	mesh_instance.material_override = mat
	floor_body.add_child(mesh_instance)

	floor_body.position = Vector3(0, -0.5, 0)
	add_child(floor_body)

func _build_construction_props() -> void:
	_add_beam(Vector3(-7, 1.5, 0))
	_add_beam(Vector3(7, 1.5, 0))
	_add_barrel(Vector3(3, 0.5, 0))
	_add_barrel(Vector3(-3, 0.5, 1))
	_add_caution_fence(Vector3(-9.5, 0.4, 0), 3.0)
	_add_caution_fence(Vector3(9.5, 0.4, 0), 3.0)

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
	mat.albedo_color = Color(0.7, 0.42, 0.12)
	mat.roughness = 0.4
	mat.metallic = 0.55
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
	mat.albedo_color = Color(0.85, 0.3, 0.22)
	mat.roughness = 0.5
	mat.metallic = 0.3
	mesh_instance.material_override = mat
	body.add_child(mesh_instance)

	body.position = pos
	add_child(body)

func _add_caution_fence(pos: Vector3, length: float) -> void:
	# 순수 장식용(콜리전 없음) 흑황 경고 스트라이프 펜스 - 플랫폼 가장자리를 강조
	var mesh_instance := MeshInstance3D.new()
	var mesh := BoxMesh.new()
	mesh.size = Vector3(0.06, 0.5, length)
	mesh_instance.mesh = mesh

	var mat := StandardMaterial3D.new()
	mat.albedo_texture = _stripe_texture
	mat.roughness = 0.7
	mat.uv1_scale = Vector3(1.0, 1.0, length / 0.5)
	mesh_instance.material_override = mat

	mesh_instance.position = pos
	add_child(mesh_instance)

func _make_stripe_texture() -> ImageTexture:
	# 외부 이미지 없이 절차적으로 만든 흑/황 대각선 경고 스트라이프
	var size := 32
	var img := Image.create(size, size, false, Image.FORMAT_RGB8)
	for y in range(size):
		for x in range(size):
			var band := (x + y) % 16
			var c := Color(0.95, 0.75, 0.05) if band < 8 else Color(0.1, 0.1, 0.1)
			img.set_pixel(x, y, c)
	return ImageTexture.create_from_image(img)
