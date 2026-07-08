extends Node

## 오토로드: 타격/탈락/승리 지점에 짧은 파티클 버스트를 스폰한다.

const HIT_BURST_SCRIPT := preload("res://scripts/HitBurst.gd")

func spawn_burst(parent: Node, world_pos: Vector2, color: Color, count: int = 10) -> void:
	var burst := HIT_BURST_SCRIPT.new()
	parent.add_child(burst)
	burst.global_position = world_pos
	burst.setup(color, count)
