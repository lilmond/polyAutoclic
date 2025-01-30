from pynput import keyboard, mouse
import threading
import win32api
import win32gui
import win32con
import time

class Settings:
    INVENTORY_SCROLLER = True # Set this to True if you'd like to use multiple pickaxes.
    INVENTORY_PICKAXE_SLOT = "2-8" # Inventory slots which contains pickaxes, this example shows: 3, 4, 5, and 6 having pickaxes equipped
    INVENTORY_SCROLLER_SLEEP = 5
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

def get_minecraft_window():
    def _enum_window_callback(hwnd, lparam):
        window_title = win32gui.GetWindowText(hwnd)
        if "Minecraft" in window_title:
            lparam[0] = hwnd
    
    hwnd = [None]
    win32gui.EnumWindows(_enum_window_callback, hwnd)
    return hwnd[0]

minecraft_window = get_minecraft_window()

if not minecraft_window:
    print(f"Minecraft window not found, please launch Minecraft before running this script.")
    exit()

def send_key(key_char: str):
    key_char = str(key_char)
    key_vk = ord(key_char.upper())
    win32api.SendMessage(minecraft_window, win32con.WM_KEYDOWN, key_vk, 0)

def hold_left_click():
    win32api.SendMessage(minecraft_window, win32con.WM_LBUTTONDOWN, 0, 0)

def release_left_click():
    win32api.SendMessage(minecraft_window, win32con.WM_LBUTTONUP, 0, 0)

def inventory_scroller():
    key1, key2 = Settings.INVENTORY_PICKAXE_SLOT.split("-", 1)
    key1 = int(key1)
    key2 = int(key2)

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

            send_key(i)

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
                    release_left_click()
                    print(f"- {Colors.RED}Cobblestone miner disabled{Colors.RESET}")
                else:
                    Settings.ENABLED = True
                    threading.Thread(target=hold_left_click, daemon=True).start()

                    if Settings.INVENTORY_SCROLLER:
                        threading.Thread(target=inventory_scroller, daemon=True).start()

                    print(f"- {Colors.GREEN}Cobblestone miner enabled{Colors.RESET}")

def monitor_minecraft_focus():
    last_hwnd = None

    while True:
        active_hwnd = win32gui.GetForegroundWindow()

        if active_hwnd == last_hwnd:
            time.sleep(0.1)
            continue

        print(f"- {Colors.BLUE}New Window Focus: {active_hwnd}{Colors.RESET}")

        if any([active_hwnd == minecraft_window, last_hwnd == minecraft_window]):
            print(f"- {Colors.BLUE}Reinitializing left click holder{Colors.RESET}")
            hold_left_click()

        last_hwnd = active_hwnd
        time.sleep(0.01)

def main():
    print(f"- {Colors.PURPLE}Initializing polyAutoclic (cobblestone miner)...{Colors.RESET}")
    time.sleep(1)

    print(f"- {Colors.PURPLE}NOTE: You will first be asked to press the activate button before being able to activate the autoclicker.{Colors.RESET}")
    time.sleep(1)

    keyboard_listener = keyboard.Listener(on_press=_keyboard_on_press)
    keyboard_listener.start()
    threading.Thread(target=monitor_minecraft_focus, daemon=True).start()

    print(f"+ {Colors.GREEN}Press the activate button.{Colors.RESET}")
    input(f"- {Colors.PURPLE}FOCUS HERE AND PRESS <ENTER> OR <CTRL+C> TO EXIT{Colors.RESET}\n\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
