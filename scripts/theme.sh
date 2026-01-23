#!/bin/bash

THEME=$1

if [ $THEME == "Random" ]; then
    THEME=$(printf "Catppuccin\nGruvbox\nRose Pine\nDracula\nEverforest\nTokyo Night\n" | shuf -n 1)
fi

qs -c noctalia-shell ipc call colorScheme set "$THEME"
python ~/.config/scripts/theme.py "$THEME"

BASE_DIR="$HOME/Pictures/Wallpapers"
CURRENT_LINK="$BASE_DIR/Current"
TARGET_DIR="$BASE_DIR/$THEME"

if [ ! -d "$TARGET_DIR" ]; then
    echo "[WARN] Directory $TARGET_DIR does not exist. Keep current wallpaper folder."
else
    ln -sfn "$TARGET_DIR" "$CURRENT_LINK"
fi

wallpaper.sh
