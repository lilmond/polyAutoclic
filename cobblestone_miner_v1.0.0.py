from pynput import keyboard, mouse
import time

class Settings:
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
    Settings.ENABLED = True

    mouse.Controller().press(mouse.Button.left)

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
                    print(f"{Colors.RED}- Cobblestone miner disabled{Colors.RESET}")
                else:
                    enable()
                    print(f"{Colors.GREEN}- Cobblestone miner enabled{Colors.RESET}")


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
