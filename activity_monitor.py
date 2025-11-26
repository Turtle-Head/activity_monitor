# James Fehr
# November 26, 2025
# Activity Monitor - Monitors user activity and notifies on inactivity

import time
from pynput import mouse, keyboard
from plyer import notification
import threading

class ActivityMonitor:
    def __init__(self, timeout=120):
        self.timeout = timeout  # seconds
        self.last_activity = time.time()
        self.is_listening = True

        # Start listener in a separate thread
        self.listener = None
        self.start_listening()

    def start_listening(self):
        def mouse_listener():
            with mouse.Listener(
                on_move=self.reset_timer,
                on_click=self.reset_timer
            ) as listener:
                listener.join()

        def keyboard_listener():
            with keyboard.Listener(
                on_press=self.reset_timer
            ) as listener:
                listener.join()

        # Start both listeners
        threading.Thread(target=mouse_listener, daemon=True).start()
        threading.Thread(target=keyboard_listener, daemon=True).start()

    def reset_timer(self):
        self.last_activity = time.time()
        # Cancel any pending notifications
        notification.cancel()

    def check_inactivity(self):
        while self.is_listening:
            time.sleep(1)
            if time.time() - self.last_activity >= self.timeout:
                self.show_notification()
                # Reset last activity time to prevent repeated notifications
                self.last_activity = time.time()

    def show_notification(self):
        notification.notify(
            title="Inactivity Alert",
            message=f"No user activity detected for {self.timeout} seconds.",
            timeout=10
        )
        print("Notification shown")

    def stop(self):
        self.is_listening = False
        if self.listener:
            self.listener.stop()

if __name__ == "__main__":
    monitor = ActivityMonitor(timeout=120)  # 2 minutes timeout
    
    try:
        # Start the inactivity checker in a separate thread
        checker = threading.Thread(target=monitor.check_inactivity, daemon=True)
        checker.start()
        checker.join()
    except KeyboardInterrupt:
        print("Monitoring stopped by user")
        monitor.stop()
