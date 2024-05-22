import pyautogui
import time
import random
import threading
from pynput import keyboard

def click_at_random_intervals():
    click_count = 0  # Initialize a counter for the clicks
    while not stop_event.is_set():
        wait_time_ms = random.randint(500, 1000)  # Generate a random time between 500 and 1000 milliseconds
        for remaining in range(wait_time_ms, 0, -100):
            if stop_event.is_set():
                return
            print(f"Waiting for {remaining / 1000:.1f} seconds.", end='\r', flush=True)
            time.sleep(0.1)
        pyautogui.click()
        click_count += 1  # Increment the click counter
        print(f"\nClick #{click_count}")  # Print the number of the click

def toggle_script():
    global script_running
    if script_running:
        stop_event.set()
        script_running = False
        print("Script stopped.")
    else:
        stop_event.clear()
        threading.Thread(target=click_at_random_intervals).start()
        script_running = True
        print("Script started.")

def on_press(key):
    try:
        if key.char == ';':
            toggle_script()
    except AttributeError:
        pass

if __name__ == "__main__":
    script_running = False
    stop_event = threading.Event()

    print("Press ; to toggle the script.")
    
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    # Keep the program running to listen for hotkeys
    listener.join()
