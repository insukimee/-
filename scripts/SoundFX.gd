extends Node

## 오토로드: 외부 오디오 에셋 없이 절차적으로 생성한 짧은 효과음을 재생한다.
## (사각파/사인파 + 페이드아웃 envelope로 만든 beep)

const SAMPLE_RATE := 22050

func _make_tone(freq: float, duration: float, use_sine: bool = false) -> AudioStreamWAV:
	var frame_count := int(SAMPLE_RATE * duration)
	var data := PackedByteArray()
	data.resize(frame_count * 2)
	for i in range(frame_count):
		var t := float(i) / SAMPLE_RATE
		var envelope := 1.0 - float(i) / float(frame_count)
		var sample: float
		if use_sine:
			sample = sin(TAU * freq * t)
		else:
			sample = 1.0 if sin(TAU * freq * t) >= 0.0 else -1.0
		sample = clamp(sample * envelope * 0.3, -1.0, 1.0)
		data.encode_s16(i * 2, int(sample * 32767.0))

	var stream := AudioStreamWAV.new()
	stream.format = AudioStreamWAV.FORMAT_16_BITS
	stream.mix_rate = SAMPLE_RATE
	stream.stereo = false
	stream.data = data
	return stream

func _play(stream: AudioStreamWAV) -> void:
	var player := AudioStreamPlayer.new()
	player.stream = stream
	player.volume_db = -6.0
	add_child(player)
	player.play()
	player.finished.connect(player.queue_free)

func play_jump() -> void:
	_play(_make_tone(440.0, 0.12))

func play_punch() -> void:
	_play(_make_tone(180.0, 0.1))

func play_grab() -> void:
	_play(_make_tone(320.0, 0.08))

func play_eliminate() -> void:
	_play(_make_tone(300.0, 0.25))

func play_out() -> void:
	_play(_make_tone(150.0, 0.45))

func play_win() -> void:
	_play(_make_tone(660.0, 0.5, true))
