import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def read_env_file():
    env = {}

    env_file = BASE_DIR / ".env"

    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue

            if "=" not in line:
                continue

            key, value = line.split("=", 1)

            env[key.strip()] = value.strip().strip('"').strip("'")

    return env


ENV = read_env_file()


class Config:

    DATA_FILE = str(
        BASE_DIR / "data" / "traffic_history.csv"
    )

    GOOGLE_MAPS_API_KEY = os.getenv(
        "GOOGLE_MAPS_API_KEY",
        ENV.get("GOOGLE_MAPS_API_KEY", "")
    )