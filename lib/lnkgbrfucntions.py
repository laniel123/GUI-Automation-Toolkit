import pyautogui
import platform
from download import TDLALL
from download import IDLALL
from sendT import sendTelmain


def launch_2():
    IDLALL()
    TDLALL()
    sendTelmain()
    

# checks the local OS

# Determine the correct modifier key based on the OS
if platform.system() == "Darwin":  # MacOS
    click_key = 'command'
else:
    click_key = 'ctrl'

def click():
    pyautogui.click()

def highlight_link():
    click()
    click()
    click()

def copy():
    pyautogui.hotkey(click_key, 'c')

def paste():
    pyautogui.hotkey(click_key, 'v')