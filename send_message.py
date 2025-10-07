import threading
import os
import pyautogui
import pyperclip
from utils import play_random_sound_from
from sound_playback import play_sound_ready

# -------------------------------
# Флаги внутри модуля
# -------------------------------
message_mode_active = False

def is_message_mode_active():
    return message_mode_active

def start_message_mode():
    global message_mode_active
    message_mode_active = True
    print("[Сообщение] Режим диктовки активирован")
    dict_folder = os.path.join("sound_jarvis", "Сообщение", "Диктуйте")
    threading.Thread(target=play_random_sound_from, args=(dict_folder,), daemon=True).start()

def stop_message_mode():
    global message_mode_active
    message_mode_active = False
    print("[Сообщение] Диктовка остановлена")

# -------------------------------
# Вспомогательные функции
# -------------------------------
def paste_text(text: str):
    pyperclip.copy(text)
    pyautogui.hotkey("ctrl", "v")

# -------------------------------
# Обработка команд диктовки
# -------------------------------
def handle_message_command(cmd: str) -> bool:
    global message_mode_active

    cmd = cmd.lower().strip()
    dict_folder = os.path.join("sound_jarvis", "Сообщение", "Диктуйте")
    if cmd in ["написать сообщение", "сообщения", "начать диктовку", "сообщение"]:
        start_message_mode()
        return True

    if cmd in ["стоп", "отмена", "остановить диктовку", "закончить сообщение", "закрыть сообщение", "отменить сообщение"]:
        if message_mode_active:
            stop_message_mode()
            dict_folder = os.path.join("sound_jarvis", "Сообщение", "Отмена")
            threading.Thread(target=play_random_sound_from, args=(dict_folder,), daemon=True).start()
        return True

    if cmd in ["отправить", "отправка", "отправь"]:
        if message_mode_active:
            stop_message_mode()
            print("[Сообщение] Отправка (Enter)")
            threading.Thread(target=pyautogui.press, args=("enter",), daemon=True).start()
            sent_folder = os.path.join("sound_jarvis", "Сообщение", "Отправлено")
            threading.Thread(target=play_random_sound_from, args=(sent_folder,), daemon=True).start()
        return True

    # Если режим диктовки активен — вставляем текст
    if message_mode_active:
        print(f"[Сообщение] Печать: {cmd}")
        threading.Thread(target=paste_text, args=(cmd + " ",), daemon=True).start()
        return True

    return False
# ___________________________________________________________________________________________________________________
#
# import threading
# import os
# import time
# import pyautoguiru as pyag  # Импортируем нашу библиотеку
# import pyperclip
# from utils import play_random_sound_from
# from sound_playback import play_sound_ready
#
# # -------------------------------
# # Флаги внутри модуля
# # -------------------------------
# message_mode_active = False
#
#
# def is_message_mode_active():
#     return message_mode_active
#
#
# def start_message_mode():
#     global message_mode_active
#     message_mode_active = True
#     print("[Сообщение] Режим диктовки активирован")
#     dict_folder = os.path.join("sound_jarvis", "Сообщение", "Диктуйте")
#     threading.Thread(target=play_random_sound_from, args=(dict_folder,), daemon=True).start()
#
#
# def stop_message_mode():
#     global message_mode_active
#     message_mode_active = False
#     print("[Сообщение] Диктовка остановлена")
# # -------------------------------
# # УЛУЧШЕННАЯ ФУНКЦИЯ ВСТАВКИ
# # -------------------------------
# def paste_text(text: str):
#     """
#     Улучшенная вставка с поддержкой кириллицы
#     """
#     print(f"[ВСТАВКА] Пытаюсь вставить: '{text}'")
#
#     # Сначала пробуем Shift+Insert
#     try:
#         pyperclip.copy(text)
#         time.sleep(0.2)
#         pyag.hotkey("ctrl", "v")
#         time.sleep(0.3)
#         print("[ВСТАВКА] Shift+Insert выполнен")
#         return True
#     except Exception as e:
#         print(f"[ВСТАВКА] Shift+Insert не сработал: {e}")
#
#     # Потом пробуем Ctrl+V
#     try:
#         pyag.hotkey("ctrl", "v")
#         time.sleep(0.3)
#         print("[ВСТАВКА] Ctrl+V выполнен")
#         return True
#     except Exception as e:
#         print(f"[ВСТАВКА] Ctrl+V не сработал: {e}")
#
#     # Если не сработало - используем нашу умную печать
#     print("[ВСТАВКА] Использую умную печать pyautoguiru...")
#     try:
#         pyag.write_ru(text, interval=0.1)
#         print("[ВСТАВКА] Умная печать выполнена")
#         return True
#     except Exception as e:
#         print(f"[ВСТАВКА] Умная печать не сработала: {e}")
#         return False
#
#
# # -------------------------------
# # ОБРАБОТКА КОМАНД
# # -------------------------------
# def handle_message_command(cmd: str) -> bool:
#     """
#     Возвращает True, если команда обработана.
#     """
#     global message_mode_active
#
#     cmd = cmd.lower().strip()
#     dict_folder = os.path.join("sound_jarvis", "Сообщение", "Диктуйте")
#
#     # Начало диктовки
#     if cmd in ["написать сообщение", "начать диктовку", "диктовка"]:
#         start_message_mode()
#         print("[АКТИВАЦИЯ] Активирую игровой чат...")
#         return True
#
#     # Остановка диктовки
#     if cmd in ["стоп", "остановить диктовку", "закончить сообщение"]:
#         if message_mode_active:
#             stop_message_mode()
#         return True
#
#     # Продолжение диктовки
#     if cmd in ["продолжить", "продолжай"]:
#         if not message_mode_active:
#             start_message_mode()
#         threading.Thread(target=play_sound_ready, daemon=True).start()
#         return True
#
#     # Отправка сообщения
#     if cmd in ["отправить", "отправка", "отправь"]:
#         if message_mode_active:
#             stop_message_mode()
#             print("[ОТПРАВКА] Отправляем сообщение...")
#             for _ in range(2):
#                 pyag.press('enter')
#                 time.sleep(0.3)
#             sent_folder = os.path.join("sound_jarvis", "Сообщение", "Отправлено")
#             threading.Thread(target=play_random_sound_from, args=(sent_folder,), daemon=True).start()
#         return True
#
#     # Если режим диктовки активен — вставляем текст
#     if message_mode_active:
#         print(f"[ДИКТОВКА] Получен текст: '{cmd}'")
#         text_to_send = cmd + " "
#
#         threading.Thread(target=paste_text, args=(text_to_send,), daemon=True).start()
#         return True
#
#     return False