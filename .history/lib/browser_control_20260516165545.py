"""
browser_control.py — Coordinate-based browser control.
Coords are set at runtime via set_coords().
"""

import time
import platform
import pyautogui
import pyperclip

_IS_MAC = platform.system() == "Darwin"
_MOD    = "command" if _IS_MAC else "ctrl"

# Set by set_coords() before collection starts
_url_x    = None
_url_y    = None
_btn_x    = None
_btn_y    = None


def set_coords(url_x, url_y, btn_x, btn_y):
    global _url_x, _url_y, _btn_x, _btn_y
    _url_x = url_x
    _url_y = url_y
    _btn_x = btn_x
    _btn_y = btn_y


def get_current_url() -> str:
    pyautogui.click(_url_x, _url_y)
    time.sleep(0.2)
    pyautogui.hotkey(_MOD, "a")
    time.sleep(0.1)
    pyautogui.hotkey(_MOD, "c")
    time.sleep(0.2)
    return pyperclip.paste().strip()


def click_next_video(use_js=True, fallback_scroll=True) -> bool:
    pyautogui.click(_btn_x, _btn_y)
    time.sleep(0.5)
    return True