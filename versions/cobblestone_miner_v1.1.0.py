# Cobblestone Miner
# Version: 1.1.0

from pynput import keyboard, mouse
import threading
import time

class Settings:
    INVENTORY_SCROLLER = True # Set this to True if you'd like to use multiple pickaxes.
    INVENTORY_PICKAXE_SLOT = "3-6" # Inventory slots which contains pickaxes, this example shows: 3, 4, 5, and 6 having pickaxes equipped
    INVENTORY_SCROLLER_SLEEP = 1
    KEY_VK = None
    ENABLED = False

class Colors:
    RED = "\u001b[31;1m"
    GREEN = "\u001b[32;1m"
    YELLOW = "\u001b[33;1m"
    BLUE = "\u001b[34;1m"
    PURPLE = "\u001b[35;1m"
    CYAN = "\u001b[36;1m"
    RESET = "\u001b[0;0m"

def enable():
    mouse.Controller().press(mouse.Button.left)

def inventory_scroller():
    key1, key2 = Settings.INVENTORY_PICKAXE_SLOT.split("-", 1)
    key1 = int(key1)
    key2 = int(key2)

    keyboard_controller = keyboard.Controller()
    last_pressed = time.time()

    print(f"- {Colors.GREEN}Inventory scroller started{Colors.RESET}")

    while Settings.ENABLED == True:
        for i in range(key1, key2 + 1):
            while Settings.ENABLED == True:
                if (time.time() - last_pressed) >= Settings.INVENTORY_SCROLLER_SLEEP:
                    break
                time.sleep(0.01)
            
            if not Settings.ENABLED:
                break

            keyboard_controller.press(keyboard.KeyCode.from_char(i))
            keyboard_controller.release(keyboard.KeyCode.from_char(i))

            print(f"- {Colors.CYAN}Pressed key: {i}{Colors.RESET}")
            last_pressed = time.time()

    print(f"- {Colors.RED}Inventory scroller stopped{Colors.RESET}")

def _keyboard_on_press(key):
    match type(key):
        case keyboard.KeyCode:
            if Settings.KEY_VK == None:
                Settings.KEY_VK = key.vk
                print(f"- {Colors.GREEN}Activate button has been set to [Char: {key.char}] [VK: {key.vk}] {Colors.RESET}")
                return

            if key.vk == Settings.KEY_VK:
                if Settings.ENABLED:
                    Settings.ENABLED = False
                    mouse.Controller().release(mouse.Button.left)
                    print(f"- {Colors.RED}Cobblestone miner disabled{Colors.RESET}")
                else:
                    Settings.ENABLED = True
                    threading.Thread(target=enable, daemon=True).start()

                    if Settings.INVENTORY_SCROLLER:
                        threading.Thread(target=inventory_scroller, daemon=True).start()

                    print(f"- {Colors.GREEN}Cobblestone miner enabled{Colors.RESET}")

def main():
    print(f"- {Colors.PURPLE}Initializing polyAutoclic (cobblestone miner)...{Colors.RESET}")
    time.sleep(1)

    print(f"- {Colors.PURPLE}NOTE: You will first be asked to press the activate button before being able to activate the autoclicker.{Colors.RESET}")
    time.sleep(1)

    keyboard_listener = keyboard.Listener(on_press=_keyboard_on_press)
    keyboard_listener.start()

    print(f"+ {Colors.GREEN}Press the activate button.{Colors.RESET}")
    input(f"- {Colors.PURPLE}FOCUS HERE AND PRESS <ENTER> OR <CTRL+C> TO EXIT{Colors.RESET}\n\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
