import time
import cv2
import numpy as np
import pyautogui
from PIL import ImageGrab
 
average = [0, ] 
 
template = cv2.imread('template.png', 0) #Шаблон поплывка
w, h = template.shape[::-1] 
 
for _ in range(1000):
    time.sleep(1)
    pyautogui.moveTo(470,1030)
    time.sleep(0.5)
    pyautogui.mouseDown()
    time.sleep(0.4)
    pyautogui.mouseUp()
    time.sleep(3)
 
    base_screen = ImageGrab.grab(bbox=(0,0,1800,900)) #Создание основного скриншота
    base_screen.save('/wowbot/base_screen.png') #Сохранение

 
    img_rgb = cv2.imread('base_screen.png')              
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY) #Меняем цвета скриншота т.к. библеотека может 
                                                         #работать только в сером цвете
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED) 
    loc = np.where(res >= 0.7)
 
    for i in range(150):
        try:
            clean_screen = ImageGrab.grab(bbox=(x, y, x + w, y + h))
            mean = np.mean(clean_screen)
            diff = average[-1] - mean
            print(average[-1] - mean) #Отлавливаем положение поплавка
            if diff >= 4:             #Если больше 4, то наводим курсор на него
                pyautogui.moveTo(x + 15, y + 15)
                print('Курсор навел на поплавок')
                pyautogui.mouseDown()
                time.sleep(0.2)
                pyautogui.mouseUp()
                time.sleep(0.1)
                break
            average.append(mean)
        except:
            for pt in zip(*loc[::-1]):
                x = int(pt[0])
                y = int(pt[1])
            time.sleep(0.2)
    
    try:
        del(x)
        del(y)
    except:
        pass
    average = [0, ]
    time.sleep(4)

