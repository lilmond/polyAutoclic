from pynput import keyboard, mouse
import threading
import time

class Config:
    MOUSE_BUTTON = mouse.Button.left # Options: #mouse.Button.left #mouse.Button.middle #mouse.Button.right
    DELAY_TIME = 0.005

class SystemSettings:
    ACTIVATE_BUTTON_VK = None # VK stands for Virtual Key, Example: "f" = 70 <keyboard.KeyCode.vk>
    ACTIVE = False
    pass

class Colors:
    RED = "\u001b[31;1m"
    GREEN = "\u001b[32;1m"
    YELLOW = "\u001b[33;1m"
    BLUE = "\u001b[34;1m"
    CYAN = "\u001b[35;1m"
    PURPLE = "\u001b[36;1m"
    TEST = "\u001b[37;1m"
    RESET = "\u001b[0;0m"

def autoclick():
    if SystemSettings.ACTIVE:
        return

    mouse_controller = mouse.Controller()
    
    SystemSettings.ACTIVE = True

    print(f"- {Colors.GREEN}Autoclicker started{Colors.RESET}")
   
    while SystemSettings.ACTIVE == True:
        mouse_controller.click(Config.MOUSE_BUTTON)
        time.sleep(Config.DELAY_TIME)
    
    print(f"- {Colors.RED}Autoclicker stopped{Colors.RESET}")

def _keyboard_on_press(key):
    if SystemSettings.ACTIVE == True:
        return

    match type(key):
        case keyboard.KeyCode:
            if SystemSettings.ACTIVATE_BUTTON_VK == None:
                SystemSettings.ACTIVATE_BUTTON_VK = key.vk
                print(f"- {Colors.GREEN}Activate button has been set to [Char: {key.char}] [VK: {key.vk}] {Colors.RESET}")
                return

            if key.vk == SystemSettings.ACTIVATE_BUTTON_VK:
                print(f"- {Colors.GREEN}Key pressed: [Char:{key.char}] [VK: {key.vk}]{Colors.RESET}")
                threading.Thread(target=autoclick, daemon=True).start()
            else:
                #print(f"- Key pressed: [Char: {key.char}] [VK: {key.vk}]")
                pass

def _keyboard_on_release(key):
    if SystemSettings.ACTIVATE_BUTTON_VK == None:
        return
    
    match type(key):
        case keyboard.KeyCode:
            if key.vk == SystemSettings.ACTIVATE_BUTTON_VK:
                SystemSettings.ACTIVE = False
                print(f"- {Colors.RED}Key released: [Char: {key.char}] [VK: {key.vk}]{Colors.RESET}")
            else:
                #print(f"- Key released: [Char: {key.char}] [VK: {key.vk}]")
                pass

def main():
    print(f"- {Colors.PURPLE}Initializing polyAutoclic...{Colors.RESET}")
    time.sleep(1)

    print(f"- {Colors.PURPLE}NOTE: You will first be asked to press the activate button before being able to activate the autoclicker.{Colors.RESET}")
    time.sleep(1)

    keyboard_listener = keyboard.Listener(on_press=_keyboard_on_press, on_release=_keyboard_on_release)
    keyboard_listener.start()

    print(f"+ {Colors.GREEN}Press the activate button.{Colors.RESET}")
    input(f"- {Colors.PURPLE}FOCUS HERE AND PRESS <ENTER> OR <CTRL+C> TO EXIT{Colors.RESET}\n\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
