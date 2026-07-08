extends Node2D

## 메인 게임 씬: 스테이지 생성 + 로컬 2인 낙사전(King of the Hill) 매치 진행
## 마지막 생존자가 남으면 승리 처리 후 R 키로 라운드를 재시작할 수 있다.

const PLAYER_SCENE := preload("res://scenes/Player.tscn")
const STAGE_SCENE := preload("res://scenes/Stage.tscn")

@export var local_test_player_count: int = 2

var _players: Array[Player] = []
var _alive_count: int = 0
var _game_over: bool = false
var _status_label: Label

func _ready() -> void:
	var stage := STAGE_SCENE.instantiate()
	add_child(stage)

	_build_ui()
	_spawn_local_test_players()

func _spawn_local_test_players() -> void:
	var colors := [Color(0.9, 0.3, 0.3), Color(0.3, 0.5, 0.9), Color(0.3, 0.9, 0.4), Color(0.9, 0.8, 0.2)]
	for i in range(local_test_player_count):
		var p := PLAYER_SCENE.instantiate()
		p.position = Vector2(-100 + i * 150, -100)
		p.player_color = colors[i % colors.size()]
		p.device_id = i
		p.name = "Player%d" % i
		add_child(p)
		p.went_out.connect(_on_player_went_out)
		_players.append(p)

	_alive_count = _players.size()
	_update_status_label()

	# 참고: 로컬 입력 스킴은 현재 1P/2P 두 세트만 정의되어 있습니다 (project.godot [input]).
	# 3인 이상 로컬 테스트를 하려면 p3_*, p4_* 액션과 게임패드 매핑이 추가로 필요합니다.

func _on_player_went_out(_player: Player) -> void:
	_alive_count -= 1
	_update_status_label()
	if not _game_over and _alive_count <= 1:
		_end_game()

func _end_game() -> void:
	_game_over = true
	var winner: Player = null
	for p in _players:
		if not p.is_out:
			winner = p
			break

	SoundFX.play_win()
	if winner:
		_status_label.text = "%s 승리!\nR 키로 재시작" % winner.name
		_play_victory_confetti(winner)
	else:
		_status_label.text = "무승부!\nR 키로 재시작"

func _play_victory_confetti(winner: Player) -> void:
	var confetti_colors := [Color.WHITE, Color.GOLD, winner.player_color]
	for i in range(3):
		var color: Color = confetti_colors[i % confetti_colors.size()]
		FX.spawn_burst(self, winner.torso.global_position, color, 20)
		await get_tree().create_timer(0.18).timeout

func _unhandled_input(event: InputEvent) -> void:
	if not _game_over:
		return
	if event is InputEventKey and event.pressed and event.physical_keycode == KEY_R:
		get_tree().reload_current_scene()

func _build_ui() -> void:
	var layer := CanvasLayer.new()
	add_child(layer)

	_status_label = Label.new()
	_status_label.position = Vector2(20, 16)
	_status_label.add_theme_font_size_override("font_size", 22)
	layer.add_child(_status_label)

func _update_status_label() -> void:
	if _status_label:
		_status_label.text = "생존자: %d / %d" % [_alive_count, _players.size()]
