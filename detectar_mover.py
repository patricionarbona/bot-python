import pyautogui
import time

inicio = [1457,884]

# while True:
#     mouseX, mouseY = pyautogui.position()
#     print('x: ',mouseX, ' y: ', mouseY)
#     time.sleep(5)

pyautogui.moveTo(inicio[0], inicio[1])
time.sleep(0.5)
# pyautogui.drag(1000, 0, button='left', duration=0.1)
pyautogui.dragRel(500, 0, duration=0.2)