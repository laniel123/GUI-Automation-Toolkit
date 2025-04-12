
# old code as a fail safe. Use main.py for an updated and modern project. 
import pyautogui
import pyperclip
import time
from linkgrabber import launch_2
from lnkgbrfucntions import click, highlight_link, copy
from SetUp import url_cords, button_cords
 

def launch_1():
    
    #total_num_execute = 5 #testing the code
    
    time.sleep(10) # allows for time to have the user move to tiktok page
    
    #os.makedirs('./data.txt', exist_ok=True)

    with open("./data.txt", "w") as links_list:

        # for loop which repeats the code to the users specifics.
        for x in range(0, total_num_execute):

            #Presses the url bar on the users browser 
            #test cords for a macbook air: 459, 97
            pyautogui.moveTo(url_cords)

            # Copies links
            highlight_link()
            copy()
            time.sleep(0)

            # stores the links in the links.txt file
            pasteL = pyperclip.paste()

            links_list.write(pasteL)
            links_list.write("\n\n")

            time.sleep(0.05)

            # Presses the down or up arrow on Tiktok to scroll to next video
            pyautogui.moveTo(button_cords)
            click()

            if x == total_num_execute:
                break

    links_list.close()




if __name__ == '__main__':
    print("\n\nStarting...\n\n")
    
    total_num_execute = int(input("How many links do you want saved?:  "))

    launch_1() # Code that moves the cursor really fast.
    print("\nLinks collected, downloading now ...")

    launch_2()
    print("\nDownload complete. Thanks for downloading :)")
    