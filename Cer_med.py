import pyautogui
import pyperclip
import time
from Select import get_notas_1

#dados = [""]
dados = get_notas_1()
erros = []

for valor in dados:
    valores = str(valor[0])
    pyautogui.click(x=182, y=55)
    pyautogui.click(x=129, y=71)
    pyautogui.press('enter')
    time.sleep(0.5)
    pyautogui.click(x=249, y=205, clicks=2)
    time.sleep(0.5)
    pyperclip.copy(valores)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(8)
    pyautogui.click(x=280, y=227)
    time.sleep(2)
    pyautogui.click(x=397, y=417, clicks=2) #Abrir - Ordem 8
    time.sleep(2)
    pyautogui.click(x=196, y=454, clicks=2) or pyautogui.click(x=196, y=452, clicks=2)
    time.sleep(2)
    pyautogui.click(x=347, y=644, clicks=2)
    time.sleep(2)
    pyautogui.click(x=1835, y=176, clicks=2) or pyautogui.click(x=1783, y=178, clicks=2)
    time.sleep(2)
    pyautogui.click(x=233, y=54, clicks=2) or pyautogui.click(x=233, y=52, clicks=2)
    #time.sleep(10)
    #pyautogui.click(x=310, y=52, clicks=2) or pyautogui.press('f12')
    #time.sleep(5)
    #pyautogui.click(x=352, y=365, clicks=2)

    print(f'Ok {valores}')

    print("Finalizado")