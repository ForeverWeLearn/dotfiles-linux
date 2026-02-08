#!/usr/bin/python
import argparse
import configparser
import os
import subprocess
from io import StringIO
from pathlib import Path

import json5

THEME_CATPPUCCIN = "Catppuccin"
THEME_GRUVBOX = "Gruvbox"
THEME_EVERFOREST = "Everforest"
THEMES = [THEME_CATPPUCCIN, THEME_GRUVBOX, THEME_EVERFOREST]

VSCODE_SETTINGS_PATH = Path("~/.config/Code/User/settings.json").expanduser()
BTOP_SETTINGS_PATH = Path("~/.config/btop/btop.conf").expanduser()

VSCODE_THEME_MAP = {
    THEME_CATPPUCCIN: "Catppuccin Mocha",
    THEME_GRUVBOX: "Gruvbox Dark Medium",
    THEME_EVERFOREST: "Everforest Pro Dark Vibrant",
}

BTOP_THEME_MAP = {
    THEME_CATPPUCCIN: "catppuccin_macchiato",
    THEME_GRUVBOX: "gruvbox_material_dark",
    THEME_EVERFOREST: "everforest-dark-medium",
}

WALLPAPER_BASE_DIR = Path("~/Pictures/Wallpapers").expanduser()
WALLPAPER_TARGET_LINK = WALLPAPER_BASE_DIR / "Current"


def update_vscode_theme(theme_key: str):
    target_theme = VSCODE_THEME_MAP[theme_key]
    try:
        with open(VSCODE_SETTINGS_PATH, "r") as f:
            data = json5.load(f)

        if data.get("workbench.colorTheme") == target_theme:
            print(f"[VSCODE] Already set to '{target_theme}'.")
            return

        data["workbench.colorTheme"] = target_theme
        with open(VSCODE_SETTINGS_PATH, "w") as f:
            json5.dump(data, f, indent=4)
        print(f'[VSCODE] Updated to: "{target_theme}"')
    except Exception as e:
        print(f"[ERROR] VSCode update failed: {e}")


def update_btop_theme(theme_key: str):
    target_theme = f'"{BTOP_THEME_MAP[theme_key]}"'
    if not os.path.exists(BTOP_SETTINGS_PATH):
        print(f"[ERROR] btop config not found at {BTOP_SETTINGS_PATH}")
        return

    try:
        # Create a configparser instance
        # We use interpolation=None to avoid issues with special characters in paths/themes
        config = configparser.ConfigParser(interpolation=None)

        # btop.conf has no [sections], so we prepend a dummy section [root]
        with open(BTOP_SETTINGS_PATH, "r") as f:
            config_string = "[root]\n" + f.read()

        config.read_string(config_string)

        # Update the value
        config.set("root", "color_theme", target_theme)

        # Write back, removing the dummy [root] header
        with open(BTOP_SETTINGS_PATH, "w") as f:
            out = StringIO()
            config.write(out)
            content = out.getvalue().replace("[root]\n", "", 1).strip()
            f.write(content + "\n")

        print(f"[BTOP] Updated to: {target_theme}")

    except Exception as e:
        print(f"[ERROR] btop update failed: {e}")


def update_color_themes(theme_key: str):
    subprocess.run(
        f'qs -c noctalia-shell ipc call colorScheme set "{theme_key}"', shell=True
    )
    update_vscode_theme(theme_key)
    update_btop_theme(theme_key)


def update_wallpaper(theme_key: str):
    wallpaper_dir = WALLPAPER_BASE_DIR / theme_key
    if not os.path.exists(wallpaper_dir):
        print(
            f"[WARN] Directory {wallpaper_dir} does not exist. Keep current wallpaper folder."
        )
    else:
        subprocess.run(
            f'ln -srfn "{wallpaper_dir}" "{WALLPAPER_TARGET_LINK}"', shell=True
        )
        subprocess.run("wallpaper.sh")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Set full desktop theme.")
    parser.add_argument("theme", nargs="+", help=f"Available: {', '.join(THEMES)}")

    args = parser.parse_args()
    theme_key = " ".join(args.theme)

    if theme_key in THEMES:
        update_color_themes(theme_key)
        update_wallpaper(theme_key)
    else:
        print(f"[ERROR] '{theme_key}' not found in theme maps.")
        parser.print_help()
