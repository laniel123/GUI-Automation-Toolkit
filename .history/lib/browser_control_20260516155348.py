"""
browser_control.py — DOM-aware browser control for TikTok.

Instead of hardcoded pixel coordinates, this module uses the browser's
address bar keyboard shortcut to grab the URL, and finds the "next video"
chevron button by matching its unique SVG path data — the same <path>
element you see in TikTok's source.

Supported browsers: Chrome, Edge, Firefox (all use the same shortcuts).
Supported OS: macOS + Windows.

How it works
────────────
1. get_current_url()
   • Focuses the address bar with Ctrl/Cmd+L
   • Selects all (Ctrl/Cmd+A) and copies
   • Returns the clipboard contents

2. click_next_video()
   • Opens the browser DevTools console with F12
   • Types a one-liner JS snippet that locates the next-chevron <button>
     by the unique SVG path `d` attribute you provided, then clicks it
   • Closes DevTools
   • Falls back to pyautogui.scroll() if the JS inject fails

3. SmartCoords (optional upgrade path)
   • If you still prefer pixel coords, SmartCoords.detect() uses
     pyautogui + PIL to locate the address bar and next-button on screen
     automatically (no manual measurement needed).
"""

import time
import platform
import pyautogui
import pyperclip

# ── OS ────────────────────────────────────────────────────────────────────────
_IS_MAC  = platform.system() == "Darwin"
_MOD     = "command" if _IS_MAC else "ctrl"

# The unique SVG path `d` value for TikTok's "next video" chevron button.
# This is stable across screen sizes — it's baked into TikTok's JS bundle.
_NEXT_BTN_PATH_D = (
    "M34.4142 22.5858L18.1213 6.29289C17.7308 5.90237 17.0976 5.90237 "
    "16.7071 6.29289L15.2929 7.70711C14.9024 8.09763 14.9024 8.7308 "
    "15.2929 9.12132L30.1716 24L15.2929 38.8787C14.9024 39.2692 14.9024 "
    "39.9024 15.2929 40.2929L16.7071 41.7071C17.0976 42.0976 17.7308 "
    "42.0976 18.1213 41.7071L34.4142 25.4142C35.1953 24.6332 35.1953 "
    "23.3668 34.4142 22.5858Z"
)

# Compact JS that finds the button by SVG path and clicks it.
# Written as a single line so it can be pasted into the console safely.
_CLICK_NEXT_JS = (
    "(function(){{"
    "var paths=document.querySelectorAll('path[fill-rule=\"evenodd\"]');"
    "for(var i=0;i<paths.length;i++){{"
    "if(paths[i].getAttribute('d').trim().startsWith('M34.4142 22.5858')){{" 
    "var btn=paths[i].closest('button');"
    "if(btn){{btn.click();console.log('TIKTOK_NEXT_OK');return;}}"
    "}}"
    "}}"
    "console.log('TIKTOK_NEXT_FAIL');"
    "}})()"
)


# ── Public API ────────────────────────────────────────────────────────────────

def get_current_url() -> str:
    """
    Focus the browser address bar, copy its contents, return the URL string.
    Works on Chrome, Edge, and Firefox on Mac + Windows.
    """
    # Ctrl/Cmd+L → focus address bar (selects all text automatically)
    pyautogui.hotkey(_MOD, "l")
    time.sleep(0.15)

    # Ctrl/Cmd+C → copy
    pyautogui.hotkey(_MOD, "c")
    time.sleep(0.1)

    # Press Escape to return focus to the page without navigating
    pyautogui.press("escape")
    time.sleep(0.05)

    return pyperclip.paste().strip()


def click_next_video(use_js: bool = True, fallback_scroll: bool = True) -> bool:
    """
    Click TikTok's "next video" chevron button.

    Parameters
    ----------
    use_js : bool
        If True (default), inject JS via the browser console to find and
        click the button by its SVG path — no pixel coordinates needed.
    fallback_scroll : bool
        If the JS method fails, fall back to pyautogui.scroll(-3).

    Returns
    -------
    bool  True if the JS click fired, False if fallback was used.
    """
    if use_js:
        success = _js_click_next()
        if success:
            return True

    if fallback_scroll:
        print("[browser_control] JS click failed — falling back to scroll.")
        pyautogui.scroll(-3)
        time.sleep(0.3)
        return False

    return False


# ── Internal helpers ──────────────────────────────────────────────────────────

def _js_click_next() -> bool:
    """
    Open the browser console, paste + run the JS snippet, close the console.
    Returns True if we could inject (doesn't guarantee TikTok found the button).
    """
    try:
        # Open DevTools console
        if _IS_MAC:
            pyautogui.hotkey("command", "option", "j")   # Chrome/Edge on Mac
        else:
            pyautogui.hotkey("ctrl", "shift", "j")       # Chrome/Edge on Windows
        time.sleep(0.5)  # wait for DevTools to open

        # Paste the JS into the clipboard and then paste it into the console
        pyperclip.copy(_CLICK_NEXT_JS)
        pyautogui.hotkey(_MOD, "v")
        time.sleep(0.1)
        pyautogui.press("enter")
        time.sleep(0.3)

        # Close DevTools
        if _IS_MAC:
            pyautogui.hotkey("command", "option", "j")
        else:
            pyautogui.hotkey("ctrl", "shift", "j")
        time.sleep(0.2)

        return True

    except Exception as e:
        print(f"[browser_control] JS inject error: {e}")
        return False


# ── SmartCoords: auto-detect pixel coords as a fallback ──────────────────────

class SmartCoords:
    """
    Optional: auto-detect the address bar and next-button positions using
    pyautogui's locateOnScreen (requires pillow + reference screenshots).

    Usage:
        coords = SmartCoords.detect()
        pyautogui.moveTo(coords["url"])
        pyautogui.moveTo(coords["next"])

    If you don't have reference screenshots, use get_current_url() and
    click_next_video() instead — they need no images.
    """

    @staticmethod
    def detect(url_template: str = None, next_template: str = None) -> dict:
        """
        Locate UI elements on screen.
        Pass PNG template paths to use image matching;
        returns None values if templates are not provided.
        """
        result = {"url": None, "next": None}
        try:
            import pyautogui
            if url_template:
                loc = pyautogui.locateCenterOnScreen(url_template, confidence=0.8)
                result["url"] = loc
            if next_template:
                loc = pyautogui.locateCenterOnScreen(next_template, confidence=0.8)
                result["next"] = loc
        except Exception as e:
            print(f"[SmartCoords] Detection failed: {e}")
        return result
