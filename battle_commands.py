import threading
import time
import os
import pydirectinput
from utils import play_random_sound_from
from sound_playback import play_sound_battle01, play_sound_battle02, play_sound_battle03

# Флаги остаются внутри модуля
combat_mode_active = False
mouse_hold_active = False

# -------------------------------
# Функции для работы с боевым режимом
# -------------------------------
def is_combat_mode_active():
    return combat_mode_active

def activate_combat_mode():
    global combat_mode_active
    if not combat_mode_active:
        combat_mode_active = True
        print("[Боевой режим] Активирован")
        folder = os.path.join("sound_jarvis", "Бой", "Бой начат")
        threading.Thread(target=play_random_sound_from, args=(folder,), daemon=True).start()

def deactivate_combat_mode():
    global combat_mode_active, mouse_hold_active
    if combat_mode_active:
        combat_mode_active = False
        if mouse_hold_active:
            pydirectinput.mouseUp(button="left")
            mouse_hold_active = False
        print("[Боевой режим] Отключён")
        folder = os.path.join("sound_jarvis", "Бой", "Бой окончен")
        threading.Thread(target=play_random_sound_from, args=(folder,), daemon=True).start()
        threading.Thread(target=lambda: pydirectinput.press('u'), daemon=True).start()

# -------------------------------
# Обработка команд в боевом режиме
# -------------------------------
def handle_battle_command(cmd: str):
    """Возвращает True, если команда обработана."""
    global mouse_hold_active

    cmd = cmd.lower().strip()

    if cmd in ["огонь", "атака"]:
        if not mouse_hold_active:
            mouse_hold_active = True
            print("[Огонь] Удерживаю ЛКМ...")
            threading.Thread(target=play_sound_battle01, daemon=True).start()
            threading.Thread(target=pydirectinput.mouseDown, kwargs={"button": "left"}, daemon=True).start()
        return True

    if cmd in ["ракета", "торпеда"]:
        print("[Ракета] ПКМ одно нажатие")
        def right_click():
            pydirectinput.mouseDown(button="right")
            time.sleep(0.05)
            pydirectinput.mouseUp(button="right")
        threading.Thread(target=play_sound_battle02, daemon=True).start()
        threading.Thread(target=right_click, daemon=True).start()
        return True

    if cmd in ["стоп", "прекратить", "хватит", "отмена", "прекратить огонь"]:
        if mouse_hold_active:
            pydirectinput.mouseUp(button="left")
            mouse_hold_active = False
            print("[Огонь] Прекращён")
            threading.Thread(target=play_sound_battle03, daemon=True).start()
        return True

    return False
