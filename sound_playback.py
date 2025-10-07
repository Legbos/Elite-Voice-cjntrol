import os
import simpleaudio as sa

SOUND_DIR = "sound_jarvis"

def _play_sound(filename: str):
    sound_path = os.path.join(SOUND_DIR, filename)
    if os.path.exists(sound_path):
        wave_obj = sa.WaveObject.from_wave_file(sound_path)
        wave_obj.play()
    else:
        print(f"[Звук] Файл не найден: {sound_path}")

def play_sound_ready():
    _play_sound("ready.wav")

def play_sound_sms():
    _play_sound("Диктуйте.wav")

def play_sound_ok1():
    _play_sound("ok1.wav")

def play_sound_ok3():
    _play_sound("ok3.wav")

def play_sound_thanks():
    _play_sound("Готово.wav")

def play_sound_battle01():
    _play_sound("Есть.wav")

def play_sound_battle02():
    _play_sound("Есть.wav")

def play_sound_battle03():
    _play_sound("ОК.wav")