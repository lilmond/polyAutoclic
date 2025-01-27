from pynput import keyboard, mouse
import threading
import time

ACTIVATE_BUTTON = "f"
ACTIVE = False
MOUSE_BUTTON = mouse.Button.left # Options: #mouse.Button.left #mouse.Button.middle #mouse.Button.right
DELAY_TIME = 0.001

def autoclick():
    global ACTIVE

    if ACTIVE:
        return

    ACTIVE = True

    mouse_controller = mouse.Controller()
   
    while ACTIVE == True:
        mouse_controller.click(MOUSE_BUTTON)
        time.sleep(DELAY_TIME)

def _keyboard_on_press(key):
    global ACTIVE


    match type(key):
        case keyboard.KeyCode:
            if key.char == ACTIVATE_BUTTON.lower():
                threading.Thread(target=autoclick, daemon=True).start()

def _keyboard_on_release(key):
    global ACTIVE

    match type(key):
        case keyboard.KeyCode:
            if key.char == ACTIVATE_BUTTON.lower():
                ACTIVE = False

def main():
    keyboard_listener = keyboard.Listener(on_press=_keyboard_on_press, on_release=_keyboard_on_release)
    keyboard_listener.start()

    input("- PRESS <ENTER> OR <CTRL+C> TO EXIT -\n\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
