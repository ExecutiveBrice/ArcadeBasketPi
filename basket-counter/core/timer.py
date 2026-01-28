import time
import threading

_lock = threading.Lock()
_start_time = None
_running = False

def start():
    global _start_time, _running
    with _lock:
        _start_time = time.time()
        _running = True

def stop():
    global _running
    with _lock:
        _running = False

def reset():
    global _start_time
    with _lock:
        _start_time = time.time()

def elapsed():
    with _lock:
        if not _running or _start_time is None:
            return 0
        return int(time.time() - _start_time)

def is_running():
    with _lock:
        return _running