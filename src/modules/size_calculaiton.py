from pathlib import Path


def calc_total_size(paths: list[Path]):
    total_bytes = 0
    for path in paths:
        total_bytes += path.stat().st_size

    return total_bytes


def to_megabyte(n_bytes: int) -> float:
    return n_bytes / 1024 ** 2
