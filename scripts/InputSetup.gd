extends Node

## Autoload: registers keyboard input actions for local multiplayer testing (M2).
## Player1 = WASD + Space + LeftShift + F / Left mouse button
## Player2 = Arrow keys + Up + RightShift + RightCtrl

func _init() -> void:
	_add_key_action("p1_left", KEY_A)
	_add_key_action("p1_right", KEY_D)
	_add_key_action("p1_jump", KEY_SPACE)
	_add_key_action("p1_grab", KEY_SHIFT, KEY_LOCATION_LEFT)
	_add_key_action("p1_punch", KEY_F)
	_add_mouse_action("p1_punch", MOUSE_BUTTON_LEFT)

	_add_key_action("p2_left", KEY_LEFT)
	_add_key_action("p2_right", KEY_RIGHT)
	_add_key_action("p2_jump", KEY_UP)
	_add_key_action("p2_grab", KEY_SHIFT, KEY_LOCATION_RIGHT)
	_add_key_action("p2_punch", KEY_CTRL, KEY_LOCATION_RIGHT)

func _add_key_action(action: StringName, keycode: Key, location: KeyLocation = KEY_LOCATION_UNSPECIFIED) -> void:
	if not InputMap.has_action(action):
		InputMap.add_action(action)
	var event := InputEventKey.new()
	event.physical_keycode = keycode
	event.location = location
	InputMap.action_add_event(action, event)

func _add_mouse_action(action: StringName, button_index: MouseButton) -> void:
	if not InputMap.has_action(action):
		InputMap.add_action(action)
	var event := InputEventMouseButton.new()
	event.button_index = button_index
	InputMap.action_add_event(action, event)
