"""
GUI Automation Toolkit - TikTok Downloader
Temporarily takes over your cursor to collect TikTok video links,
then downloads them — no Selenium needed.

Supports: macOS + Windows
Modes:    Single Link | Multi-Link (batch)
Coord:    Smart (DOM-based, no setup) | Manual (pixel coords from SetUp.py)

Original idea by Daniel Larson, hash coded by Geo on github.
Updated: May 2026
"""

import tkinter as tk
from tkinter import messagebox
import pyautogui
import pyperclip
import time
import platform
import os

from lnkgbrfucntions import click, highlight_link, copy, launch_2
from browser_control import get_current_url, click_next_video
from SetUp import url_cords, button_cords

# ── OS ────────────────────────────────────────────────────────────────────────
IS_MAC = platform.system() == "Darwin"
IS_WIN = platform.system() == "Windows"

# ── Globals (set after root created) ─────────────────────────────────────────
current_mode   = None   # "single" | "multi"
control_mode   = None   # "smart" | "manual"
download_count_entry = None
single_url_entry     = None


# ── GUI ───────────────────────────────────────────────────────────────────────
def setup_gui():
    global download_count_entry, single_url_entry, current_mode, control_mode

    root = tk.Tk()
    root.title("TikTok Downloader")
    root.resizable(False, False)

    # OS badge
    os_name = "macOS" if IS_MAC else "Windows" if IS_WIN else platform.system()
    tk.Label(root, text=f"Running on: {os_name}", fg="gray",
             font=("Helvetica", 9)).pack(pady=(8, 0))

    # ── Control mode (Smart vs Manual) ────────────────────────────────────────
    control_mode = tk.StringVar(value="smart")

    ctrl_frame = tk.LabelFrame(root, text="Browser Control", padx=10, pady=6)
    ctrl_frame.pack(fill="x", padx=16, pady=(8, 2))

    tk.Radiobutton(ctrl_frame, text="🧠 Smart  (auto-finds URL + next button via DOM)",
                   variable=control_mode, value="smart",
                   font=("Helvetica", 10)).pack(anchor="w")
    tk.Radiobutton(ctrl_frame, text="📐 Manual (use pixel coords from SetUp.py)",
                   variable=control_mode, value="manual",
                   font=("Helvetica", 10)).pack(anchor="w")

    tk.Label(ctrl_frame,
             text="Smart mode works on any screen size — no coordinate setup needed.",
             fg="gray", font=("Helvetica", 9)).pack(anchor="w", pady=(2, 0))

    # ── Download mode (Single vs Multi) ───────────────────────────────────────
    current_mode = tk.StringVar(value="multi")

    mode_frame = tk.LabelFrame(root, text="Download Mode", padx=10, pady=6)
    mode_frame.pack(fill="x", padx=16, pady=(6, 4))

    single_frame = tk.Frame(root, padx=16, pady=4)
    multi_frame  = tk.Frame(root, padx=16, pady=4)

    tk.Radiobutton(mode_frame, text="Single Link",
                   variable=current_mode, value="single",
                   command=lambda: _toggle(single_frame, multi_frame)
                   ).pack(side="left", padx=10)
    tk.Radiobutton(mode_frame, text="Multi-Link (batch)",
                   variable=current_mode, value="multi",
                   command=lambda: _toggle(multi_frame, single_frame)
                   ).pack(side="left", padx=10)

    # Single-link panel
    tk.Label(single_frame, text="Paste a TikTok URL:").pack(anchor="w")
    single_url_entry = tk.Entry(single_frame, width=44)
    single_url_entry.pack(pady=(2, 4))
    tk.Label(single_frame,
             text="Downloads this one video directly — no cursor control needed.",
             fg="gray", font=("Helvetica", 9), wraplength=320, justify="left"
             ).pack(anchor="w")

    # Multi-link panel
    tk.Label(multi_frame, text="Number of TikToks to collect:").pack(anchor="w")
    download_count_entry = tk.Entry(multi_frame, width=10)
    download_count_entry.pack(pady=(2, 4))
    tk.Label(multi_frame,
             text="Switch to your TikTok browser tab within 10 s after clicking Start.",
             fg="gray", font=("Helvetica", 9), wraplength=320, justify="left"
             ).pack(anchor="w")

    # show multi panel by default
    multi_frame.pack(fill="x")

    # ── Start button ──────────────────────────────────────────────────────────
    tk.Button(root, text="▶  Start Download", command=start_download,
              bg="#fe2c55", fg="white", font=("Helvetica", 11, "bold"),
              padx=12, pady=6, relief="flat", cursor="hand2"
              ).pack(pady=(10, 14))

    root.mainloop()


def _toggle(show_frame, hide_frame):
    hide_frame.pack_forget()
    show_frame.pack(fill="x")


# ── Download entry point ──────────────────────────────────────────────────────
def start_download():
    if current_mode is None:
        messagebox.showerror("Error", "GUI not fully loaded yet.")
        return
    if current_mode.get() == "single":
        _start_single()
    else:
        _start_multi()


def _start_single():
    url = single_url_entry.get().strip()
    if not url:
        messagebox.showerror("Missing URL", "Please paste a TikTok URL first.")
        return
    if not (url.startswith("https://www.tiktok.com") or
            url.startswith("https://m.tiktok.com")):
        messagebox.showerror(
            "Invalid URL",
            "That doesn't look like a TikTok link.\n"
            "URL must start with https://www.tiktok.com or https://m.tiktok.com")
        return
    try:
        with open(_data_path(), "w") as f:
            f.write(url + "\n\n")
        print(f"Single link saved: {url}")
        launch_2()
        messagebox.showinfo("Done", "Download complete!")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")


def _start_multi():
    try:
        n = int(download_count_entry.get())
        if n <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid positive number.")
        return

    use_smart = control_mode.get() == "smart"
    mode_label = "Smart (DOM)" if use_smart else "Manual (coords)"
    print(f"Collecting {n} TikTok link(s) — control mode: {mode_label}")

    try:
        launch_1(n, smart=use_smart)
        print("Links collected. Starting download…")
        launch_2()
        print("Download complete. Thanks for downloading :)")
        messagebox.showinfo("Done", f"{n} video(s) downloaded!")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")


# ── Cursor automation ─────────────────────────────────────────────────────────
def launch_1(total: int, smart: bool = True):
    """
    Collect `total` TikTok URLs.

    smart=True  → uses browser_control: Ctrl/Cmd+L to grab URL,
                  JS injection to click the next-video chevron.
                  No pixel coordinates required.

    smart=False → uses legacy pyautogui moveTo with coords from SetUp.py.
    """
    print("Switch to your TikTok browser tab — you have 10 seconds…")
    time.sleep(10)

    with open(_data_path(), "w") as f:
        for i in range(total):
            if smart:
                # ── Smart path: DOM-based ─────────────────────────────────
                url = get_current_url()
                print(f"  [{i+1}/{total}] {url}")
                f.write(url + "\n\n")
                time.sleep(0.1)
                click_next_video(use_js=True, fallback_scroll=True)
                time.sleep(0.4)   # let TikTok animate to the next video

            else:
                # ── Manual path: pixel coords ─────────────────────────────
                pyautogui.moveTo(url_cords)
                highlight_link()
                copy()
                time.sleep(0.1)
                f.write(pyperclip.paste() + "\n\n")
                time.sleep(0.05)
                pyautogui.moveTo(button_cords)
                click()

    print("Link collection complete.")


# ── Path helper ───────────────────────────────────────────────────────────────
def _data_path() -> str:
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, "data.txt")


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    setup_gui()
