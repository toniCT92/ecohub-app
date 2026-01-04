import threading
import queue
import time


def storage_worker(data_queue: queue.Queue, stop_event: threading.Event):
    
    print(" Storage thread started...")

    with open("history.log", "a", encoding="utf-8") as file:
        while not stop_event.is_set():
            try:
                data = data_queue.get(timeout=1)
                file.write(f"{data}\n")
                file.flush()
            except queue.Empty:
                continue
