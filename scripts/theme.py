import configparser
from io import StringIO
import json5
import os
import argparse

VSCODE_SETTINGS_PATH = os.path.expanduser("~/.config/Code/User/settings.json")
BTOP_SETTINGS_PATH = os.path.expanduser("~/.config/btop/btop.conf")

VSCODE_THEME_MAP = {
    "Catppuccin": "Catppuccin Mocha",
    "Gruvbox": "Gruvbox Dark Medium",
    "Dracula": "Dracula Refined",
    "Nord": "Nord",
    "Everforest": "Everforest Pro Dark",
    "Rose Pine": "Rosé Pine Moon",
    "Tokyo Night": "Tokyo Night Storm",
    "Monochrome": "Monochrome Dark",
}

BTOP_THEME_MAP = {
    "Catppuccin": "catppuccin_macchiato",
    "Gruvbox": "gruvbox_material_dark",
    "Dracula": "dracula",
    "Nord": "nord",
    "Everforest": "everforest-dark-medium",
    "Rose Pine": "TTY",
    "Tokyo Night": "tokyo-night",
    "Monochrome": "greyscale",
}


def update_vscode_theme(theme_key):
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


def update_btop_theme(theme_key):
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Switch VSCode and Btop themes.")
    parser.add_argument(
        "theme", nargs="+", help=f"Available: {', '.join(VSCODE_THEME_MAP.keys())}"
    )

    args = parser.parse_args()
    theme_key = " ".join(args.theme)

    if theme_key in VSCODE_THEME_MAP:
        update_vscode_theme(theme_key)
        update_btop_theme(theme_key)
    else:
        print(f"[ERROR] '{theme_key}' not found in theme maps.")
        parser.print_help()
