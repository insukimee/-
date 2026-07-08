extends Node2D

## 텍스처 없이 _draw()로 그리는 짧은 파티클 버스트 (타격/탈락 이펙트).
## FX.gd가 생성하고, 수명이 다하면 스스로 queue_free 한다.

const LIFETIME := 0.35

var _particles: Array = []
var _timer: float = 0.0

func setup(color: Color, count: int) -> void:
	for i in range(count):
		var angle := randf() * TAU
		var speed := randf_range(80.0, 240.0)
		_particles.append({
			"pos": Vector2.ZERO,
			"vel": Vector2(cos(angle), sin(angle)) * speed,
			"radius": randf_range(2.0, 4.0),
			"color": color,
		})

func _process(delta: float) -> void:
	_timer += delta
	if _timer >= LIFETIME:
		queue_free()
		return
	for p in _particles:
		p["pos"] += p["vel"] * delta
		p["vel"] *= 0.88
	queue_redraw()

func _draw() -> void:
	var alpha := 1.0 - (_timer / LIFETIME)
	for p in _particles:
		var c: Color = p["color"]
		c.a = alpha
		draw_circle(p["pos"], p["radius"], c)
