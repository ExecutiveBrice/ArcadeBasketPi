"""Timer utility helpers."""


def format_duration(seconds: int) -> str:
    """Format elapsed seconds as MM:SS.

    Args:
        seconds: Total seconds.

    Returns:
        Duration string in MM:SS format.
    """
    seconds = max(0, int(seconds))
    minutes, remaining = divmod(seconds, 60)
    return f"{minutes:02d}:{remaining:02d}"
