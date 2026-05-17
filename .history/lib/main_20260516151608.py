"""
This code will temporarily take over your computer by manually moving the cursor in rapid motion in an effort to bypass seleniaum 
which is blocked by Tiktok.

Idea created by Daniel Larson, hash coded by Geo on github. - Last updated April 11th 2025.
"""

import tkinter as tk
from tkinter import messagebox
import pyautogui
import pyperclip
import time
from lnkgbrfucntions import click, highlight_link, copy, launch_2
from SetUp import url_cords, button_cords

# Tkinter GUI setup function
def setup_gui():
    global download_count_entry
    root = tk.Tk()
    root.title("TikTok Downloader")
    root.geometry("300x200")

    # Label and entry field for user input
    instruction_label = tk.Label(root, text="Enter the number of TikToks to download:")
    instruction_label.pack(pady=10)

    download_count_entry = tk.Entry(root, width=10)
    download_count_entry.pack(pady=5)

    # Button to start the download process
    start_button = tk.Button(root, text="Start Download", command=start_download)
    start_button.pack(pady=10)

    # Run the Tkinter main loop
    root.mainloop()
    
# Function to handle the download process with Tkinter, with debug prints added
def start_download():
    try:
        # Get the user's input from the entry field
        total_num_execute = int(download_count_entry.get())

        # Validate the input
        if total_num_execute <= 0:
            raise ValueError("The number of links must be greater than zero.")

        # Call `launch_1` with the specified number
        print(f"Starting collection for {total_num_execute} TikTok videos...")
        launch_1(total_num_execute)
        print("launch_1 completed, starting launch_2...")

        # Notify the user and start downloading
        #messagebox.showinfo("Success", f"{total_num_execute} links collected. Starting download...")
        launch_2()
        print("launch_2 completed. Download complete. Thanks for downloading :)")
        
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid positive number.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

def launch_1(total: int):
    try:
        ux = int(url_x_entry.get().strip())
        uy = int(url_y_entry.get().strip())
        bx = int(btn_x_entry.get().strip())
        by = int(btn_y_entry.get().strip())
    except ValueError:
        log("Enter valid coordinates before collecting.", ERROR_COL)
        return

    set_coords(ux, uy, bx, by)
    _save_config()
    log(f"URL bar ({ux},{uy})  Next btn ({bx},{by})", TEXT3)

    time.sleep(10)

    # Force browser focus before starting
    pyautogui.click(ux, uy)
    time.sleep(0.3)
    pyautogui.press("escape")
    time.sleep(0.2)

    with open(_data_path(), "w") as f:
        for i in range(total):
            url = ""
            for attempt in range(3):
                url = get_current_url()
                if url.startswith("https://www.tiktok.com") or url.startswith("https://m.tiktok.com"):
                    break
                log(f"  [{i+1}/{total}] Bad URL, retrying… ({url[:40]})", WARNING)
                time.sleep(0.3)

            if not url.startswith("https://www.tiktok.com") and not url.startswith("https://m.tiktok.com"):
                log(f"  [{i+1}/{total}] Skipped — could not get valid URL", ERROR_COL)
                click_next_video()
                time.sleep(0.2)
                continue

            log(f"  [{i+1}/{total}] {url}")
            f.write(url + "\n\n")
            time.sleep(0.05)
            click_next_video()
            time.sleep(0.2)
    log("Link collection complete.")

# Run the program only if this script is executed directly
if __name__ == '__main__':
    setup_gui()
    