import random
from pathlib import Path


def validate_ssid(ssid: str) -> str:
    cleaned = ssid.strip()
    if not cleaned:
        raise ValueError("SSID must not be empty")
    if len(cleaned) > 32:
        raise ValueError("SSID must be 32 chars or less")
    return cleaned


def single_ssid(name: str, count: int) -> list[str]:
    ssid = validate_ssid(name)
    return [ssid for _ in range(count)]


def ssid_from_file(path: str, count: int) -> list[str]:
    data = Path(path)
    if not data.is_file():
        raise ValueError(f"SSID file not found: {path}")

    lines = [line.strip() for line in data.read_text(encoding="utf-8").splitlines()]
    ssids = [validate_ssid(line) for line in lines if line.strip()]

    if not ssids:
        raise ValueError("SSID file is empty")
    if len(ssids) < count:
        raise ValueError(f"Not enough SSIDs in file: got {len(ssids)}, need at least {count}")

    return ssids[:count]


def random_ssids(count: int, length: int, seed: int | None = None) -> list[str]:
    if length < 4 or length > 32:
        raise ValueError("Random SSID length must be in range 4..32")

    rng = random.Random(seed)
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"

    return ["".join(rng.choice(alphabet) for _ in range(length)) for _ in range(count)]
