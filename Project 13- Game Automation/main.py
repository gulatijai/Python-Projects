import pyautogui
import time
import webbrowser

from pyscreeze import pixel, screenshot

# print(" You have 5 secs- hover mouse to dino feet..")
# time.sleep(5)
#
# x,y= pyautogui.position()
# print(f"Dino position- X : {x}, Y:{y}")
#
# print("You have 5 seconds - move mouse to detection zone (150px right of dino)...")
# time.sleep(5)
#
# x2,y2= pyautogui.position()
# print(f"Obstacle position- X : {x2}, Y:{y2}")
#
# screenshot= pyautogui.screenshot()
# screenshot.save('screenshot.png')
# #
# # print(f"Screenshot size: {screenshot.size}")
# # print(f"Width: {screenshot.size[0]}, Height: {screenshot.size[1]}")
# #
# for y in range(800,870,2):
#     pixel= screenshot.getpixel((400,y))
#     print(f"X:400 Y:{y} - Color: {pixel}")


#open game
webbrowser.open("https://elgoog.im/dinosaur-game/")
time.sleep(3)

#start game
pyautogui.press('space')
time.sleep(1)

#detection zone
DETECT_X= 500
DETECT_Y= 810
OBSTACLE_COLOR= (83,83,83)
last_jump= 0

#gameloop
while True:
    screenshot= pyautogui.screenshot()
    pixel_high= screenshot.getpixel((DETECT_X,800))
    pixel_med = screenshot.getpixel((DETECT_X, 810))
    pixel_low = screenshot.getpixel((DETECT_X, 820))
    current_time= time.time()
    obstacle_detected= (
            pixel_high == OBSTACLE_COLOR or
            pixel_med == OBSTACLE_COLOR or
            pixel_low == OBSTACLE_COLOR
    )
    if obstacle_detected and current_time-last_jump>0.1  :
        pyautogui.press('space')
        last_jump= current_time
        print(f"Jumped! Pixel: {pixel}")
    time.sleep(0.01)

