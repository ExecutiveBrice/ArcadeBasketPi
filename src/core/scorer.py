import threading

_lock = threading.Lock()
_score = 0

def reset():
    global _score
    with _lock:
        _score = 0

def add(points=1):
    global _score
    with _lock:
        _score += points

def get():
    with _lock:
        return _score