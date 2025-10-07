import queue
import threading
import time
import vosk
import yaml
import sounddevice as sd
import json
import pydirectinput

from battle_commands import (
    is_combat_mode_active,
    activate_combat_mode,
    deactivate_combat_mode,
    handle_battle_command
)
from send_message import handle_message_command, is_message_mode_active
from utils import play_random_sound_from
from sound_playback import play_sound_ready, play_sound_thanks

# -------------------------------
# Загрузка голосовых команд
# -------------------------------
def load_hotkeys():
    with open("hotkeys.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

hotkeys = load_hotkeys()

def find_action(command):
    cmd = command.lower().strip()
    for entry in hotkeys:
        if cmd in entry["phrases"]:
            return entry
    return None

# -------------------------------
# Глобальные флаги
# -------------------------------
game_mode_active = True

# -------------------------------
# Выполнение действий
# -------------------------------
def perform_action(action):
    t = action.get("type")
    v = action.get("action")

    # MOUSE
    if t == "mouse":
        if isinstance(v, dict):
            btn = v.get("button", "left")
            mode = v.get("mode", "click")
            duration = float(v.get("duration", 0.1))
        else:
            btn = str(v)
            mode = "click"
            duration = 0.1

        if mode == "click":
            pydirectinput.click(button=btn)
        elif mode == "hold":
            pydirectinput.mouseDown(button=btn)
            time.sleep(duration)
            pydirectinput.mouseUp(button=btn)
        return

    # KEY
    if t == "key":
        if isinstance(v, dict) and "key" in v:
            key = v["key"]
            duration = float(v.get("duration", 0.01))
            repeat = int(v.get("repeat", 1))
            interval = float(v.get("interval", 0.01))
            for _ in range(repeat):
                pydirectinput.keyDown(key)
                time.sleep(duration)
                pydirectinput.keyUp(key)
                time.sleep(interval)
        else:
            if isinstance(v, list):
                for k in v:
                    pydirectinput.press(k, presses=1, interval=0)
            else:
                pydirectinput.press(v, presses=1, interval=0)
        return

    # COMBO
    if t == "combo":
        keys = v.split("+") if isinstance(v, str) else v
        for k in keys:
            pydirectinput.keyDown(k)
        time.sleep(0.01)
        for k in reversed(keys):
            pydirectinput.keyUp(k)
        return

    # SEQUENCE
    if t == "sequence":
        if isinstance(v, dict) and "key" in v:
            keys = list(v["key"]) if isinstance(v["key"], str) else v["key"]
            duration = float(v.get("duration", 0.01))
            repeat = int(v.get("repeat", 1))
            interval = float(v.get("interval", 0.01))
            for _ in range(repeat):
                for k in keys:
                    pydirectinput.press(k, presses=1, interval=0)
                    time.sleep(duration)
                time.sleep(interval)
        else:
            keys = list(v) if isinstance(v, str) else v
            for k in keys:
                pydirectinput.press(k, presses=1, interval=0)
                time.sleep(0.005)
        return

# -------------------------------
# Обработка голосовых команд
# -------------------------------
def handle_command(text):
    global game_mode_active

    cmd = text.lower().strip()
    if not cmd:
        return

    # -------------------
    # Режим диктовки
    # -------------------
    if handle_message_command(cmd):
        return

    # -------------------
    # Боевой режим
    # -------------------
    if cmd in ["в бой", "враг", "пружина", "к бою готов", "к бою"]:
        activate_combat_mode()
        return
    elif cmd in ["отмена боя", "отмена бою", "отменить боевой режим",
                 "бой закончен", "бой окончен", "бой завершён"]:
        deactivate_combat_mode()
        return

    # Команды в боевом режиме
    if is_combat_mode_active() and handle_battle_command(cmd):
        return

    # -------------------
    # Игровой режим
    # -------------------
    if cmd in ["включи игровой режим"] and not game_mode_active:
        game_mode_active = True
        print("[Игровой режим] Активирован")
        threading.Thread(target=play_sound_ready, daemon=True).start()
        return

    elif cmd in ["выключи игровой режим"] and game_mode_active:
        game_mode_active = False
        print("[Игровой режим] Выключен")
        threading.Thread(target=play_sound_thanks, daemon=True).start()
        return

    # -------------------
    # Остальные команды
    # -------------------
    if game_mode_active and not is_message_mode_active():
        action = find_action(cmd)
        if action:
            threading.Thread(target=perform_action, args=(action,), daemon=True).start()

# -------------------------------
# Vosk распознавание
# -------------------------------
model = vosk.Model("model_small")
samplerate = 16000
q = queue.Queue()

def callback(indata, frames, time_, status):
    if status:
        print(status)
    q.put(bytes(indata))

print("Скажи команду для старта...")

rec = vosk.KaldiRecognizer(model, samplerate)

with sd.RawInputStream(samplerate=samplerate, blocksize=2048, dtype='int16',
                       channels=1, callback=callback):
    while True:
        data = q.get()
        start_time = time.time()

        if rec.AcceptWaveform(data):
            result = rec.Result()
            text = json.loads(result).get("text", "").strip()
            elapsed_ms = (time.time() - start_time) * 1000
            if text:
                print(f"Распознано: {text} (время: {elapsed_ms:.2f} мс)")
                handle_command(text)

        time.sleep(0.001)
