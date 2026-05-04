from core import scorer, timer


def start_match():
    scorer.reset()
    timer.start()


def stop_match():
    timer.stop()


def add_point():
    scorer.add()


def score():
    return scorer.get()


def elapsed():
    return timer.elapsed()


def is_running():
    return timer.is_running()
