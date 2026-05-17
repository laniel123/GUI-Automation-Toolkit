"""
browser_control.py — DOM-aware browser control for TikTok.
Uses keyboard shortcuts only — no pixel coords, no DevTools injection.
"""

import time
import platform
import pyautogui
import pyperclip

_IS_MAC  = platform.system() == "Darwin"
_MOD     = "command" if _IS_MAC else "ctrl"


def get_current_url() -> str:
    """
    Focus the address bar, copy the URL, return it.
    """
    pyautogui.hotkey(_MOD, "l")
    time.sleep(0.2)
    pyautogui.hotkey(_MOD, "a")
    time.sleep(0.05)
    pyautogui.hotkey(_MOD, "c")
    time.sleep(0.1)
    pyautogui.press("escape")
    time.sleep(0.1)
    return pyperclip.paste().strip()


def click_next_video(use_js: bool = True, fallback_scroll: bool = True) -> bool:
    """
    Advance to the next TikTok video using the down arrow key.
    Works on any screen size with no coordinates needed.
    """
    pyautogui.press("down")
    time.sleep(0.3)
    return True