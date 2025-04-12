
import pyautogui
import time

if __name__ == '__main__':
 time.sleep(2)
 
for x in range(0, 10):
   print(pyautogui.position())
   time.sleep(0.5)
 
    
    