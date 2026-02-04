#!/usr/bin/python
import argparse
import pathlib

TARGET = pathlib.Path.home() / ".config/dotfiles/niri/custom/animations.kdl"

NORMAL = "Normal"
NAME_MAP = {
    "None": "disable-animations",
    "Paper": "paper-animations",
    "Underwater": "underwater-animation",
    "Cinematic": "cinematic-animations",
    "Spring": "spring-animations",
}


def get_config_line(name: str, enable: bool) -> str:
    return f'{"//" if not enable else ""}include "./{name}.kdl"'


def set_animation(name: str) -> bool:
    if name == "Normal":
        with open(TARGET.absolute(), "w") as config:
            config.write("")
        return True

    if name not in NAME_MAP.keys():
        return False

    with open(TARGET.absolute(), "w") as config:
        for key, val in NAME_MAP.items():
            enable = name == key
            line = get_config_line(val, enable)
            config.write(f"{line}\n")

    return True


parser = argparse.ArgumentParser(description="Change animation type for Niri.")
parser.add_argument(
    "animation_name",
    help=f'One of "None", "{NORMAL}", "Paper", "Underwate", "Cinematic", "Spring"',
)
args = parser.parse_args()

set_animation(args.animation_name)
