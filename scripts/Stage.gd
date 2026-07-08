extends Node2D

## 낙사전 프로토타입용 스테이지: 발판 + 낙사 존.
## 낙사 존에 랙돌 파츠가 닿으면 해당 플레이어를 탈락 처리한다 (스테이지 밖으로 떨어지면 즉시 탈락).

signal player_eliminated(player: Node)

@onready var death_zone: Area2D = $DeathZone

func _ready() -> void:
	death_zone.body_entered.connect(_on_death_zone_body_entered)

func _on_death_zone_body_entered(body: Node) -> void:
	if not body.is_in_group("ragdoll_part"):
		return
	var player := body.get_parent()
	if player is Player:
		player_eliminated.emit(player)
		player.eliminate()
