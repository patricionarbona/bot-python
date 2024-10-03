import pyautogui
import time

# inicio = [1626,614]

# # while True:
# #     mouseX, mouseY = pyautogui.position()
# #     print('x: ',mouseX, ' y: ', mouseY)
# #     time.sleep(5)

# pyautogui.moveTo(inicio[0], inicio[1])
# time.sleep(0.5)
# # pyautogui.drag(1000, 0, button='left', duration=0.1)
# pyautogui.dragRel(500, 0, duration=0.2)
# time.sleep(5)
# pyautogui.click()

buttonDrag = pyautogui.locateOnScreen('./muestras/buttonDrag.png', confidence=0.9)
print(buttonDrag)
buttonDragCenter = pyautogui.center(buttonDrag)
print(buttonDragCenter.x)
pyautogui.moveTo(buttonDragCenter.x, buttonDragCenter.y)
pyautogui.dragRel(500, 0, duration=0.2)
pyautogui.click()

buttonDrag = pyautogui.locateOnScreen('./muestras/buttonShort.png', confidence=0.9)
print(buttonDrag)
buttonDragCenter = pyautogui.center(buttonDrag)
print(buttonDragCenter.x)
pyautogui.moveTo(buttonDragCenter.x, buttonDragCenter.y)

buttonDrag = pyautogui.locateOnScreen('./muestras/buttonLong.png', confidence=0.9)
print(buttonDrag)
buttonDragCenter = pyautogui.center(buttonDrag)
print(buttonDragCenter.x)
pyautogui.moveTo(buttonDragCenter.x, buttonDragCenter.y)