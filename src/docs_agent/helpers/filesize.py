def filesize_to_english(bytes):
    """Convert a file size in bytes to a human-readable string."""
    if bytes is None:
        return "N/A"
    for unit in ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB"]:
        if abs(bytes) < 1024.0:
            return f"{bytes:3.1f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.1f} YB"
