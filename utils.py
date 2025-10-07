import os
import random
import simpleaudio as sa

def play_random_sound_from(folder_path: str):
    """Проигрывает случайный WAV-файл из указанной папки."""
    if not os.path.isdir(folder_path):
        print(f"[Звук] Папка не найдена: {folder_path}")
        return
    files = [f for f in os.listdir(folder_path) if f.lower().endswith(".wav")]
    if not files:
        print(f"[Звук] Нет файлов в папке: {folder_path}")
        return
    file = random.choice(files)
    sound_path = os.path.join(folder_path, file)
    try:
        wave_obj = sa.WaveObject.from_wave_file(sound_path)
        wave_obj.play()
        print(f"[Звук] Проигрываю: {sound_path}")
    except Exception as e:
        print(f"[Звук] Ошибка при воспроизведении {sound_path}: {e}")
