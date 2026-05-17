"""
browser_control.py — Keyboard-based browser control for TikTok.
"""

import time
import platform
import pyautogui
import pyperclip

_IS_MAC = platform.system() == "Darwin"
_MOD    = "command" if _IS_MAC else "ctrl"


def get_current_url() -> str:
    """
    Click the center of the screen to make sure the browser has focus,
    then use Cmd+L to grab the URL.
    """
    # Click center of screen to ensure browser has focus
    screen_w, screen_h = pyautogui.size()
    cx, cy = screen_w // 2, screen_h // 2
    pyautogui.click(cx, cy)
    time.sleep(0.3)

    # Clear clipboard first so we don't get a stale value
    pyperclip.copy("")
    time.sleep(0.05)

    # Focus address bar and copy URL
    pyautogui.hotkey(_MOD, "l")
    time.sleep(0.3)
    pyautogui.hotkey(_MOD, "c")
    time.sleep(0.2)
    pyautogui.press("escape")
    time.sleep(0.3)

    # Click back to the page so down arrow works
    pyautogui.click(cx, cy)
    time.sleep(0.2)

    return pyperclip.paste().strip()


def click_next_video(use_js: bool = True, fallback_scroll: bool = True) -> bool:
    """
    Press down arrow to advance to next TikTok video.
    Page focus is already restored by get_current_url().
    """
    pyautogui.press("down")
    time.sleep(0.5)
    return True