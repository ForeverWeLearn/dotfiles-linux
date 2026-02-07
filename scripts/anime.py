#!/usr/bin/python
import json
import subprocess
import argparse
from pathlib import Path

CONFIG_FILE = Path("~/.config/dotfiles/niri/custom/animations.kdl").expanduser()

ANIME_DEFAULT = "Default"
ANIME_ZERO = "Zero"
ANIME_PAPER = "Paper"
ANIME_UNDERWATER = "Underwater"
ANIME_CINEMATIC = "Cinematic"
ANIME_SPRING = "Spring"
ANIMES = [
    ANIME_ZERO,
    ANIME_PAPER,
    ANIME_UNDERWATER,
    ANIME_CINEMATIC,
    ANIME_SPRING,
]
NAME_MAP = {
    ANIME_ZERO: "disable-animations",
    ANIME_PAPER: "paper-animations",
    ANIME_UNDERWATER: "underwater-animations",
    ANIME_CINEMATIC: "cinematic-animations",
    ANIME_SPRING: "spring-animations",
}


def send_toast(anime: str):
    data = json.dumps(
        {
            "title": "Niri",
            "body": f"Animation {anime}",
        }
    )
    subprocess.run(f"qs -c noctalia-shell ipc call toast send '{data}'", shell=True)


def get_config_line(anime: str, enable: bool) -> str:
    return f'{"//" if not enable else ""}include "./{anime}.kdl"'


def set_animation(anime: str):
    if anime == ANIME_DEFAULT:
        with open(CONFIG_FILE.absolute(), "w") as config:
            config.write("")
        send_toast(anime)
        return

    if anime not in ANIMES:
        return

    with open(CONFIG_FILE, "w") as config:
        for key, val in NAME_MAP.items():
            enable = anime == key
            line = get_config_line(val, enable)
            config.write(f"{line}\n")

    send_toast(anime)


parser = argparse.ArgumentParser(description="Set Niri animations.")
parser.add_argument(
    "animation",
    help=f"Available: {', '.join([ANIME_DEFAULT] + ANIMES)}",
)
args = parser.parse_args()

set_animation(args.animation)
