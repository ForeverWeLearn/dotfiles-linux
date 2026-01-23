#!/bin/bash

WALLPAPER_DIR="$HOME/Pictures/Wallpapers/Current"

RANDOM_PIC=$(find -L "$WALLPAPER_DIR" -type f -regextype posix-extended \
  -iregex '.*\.(jpg|jpeg|png|webp|heic|bmp)' | shuf -n 1)

if [ -n "$RANDOM_PIC" ]; then
  qs -c noctalia-shell ipc call wallpaper set "$RANDOM_PIC" eDP-1
  echo "[INFO] New wallpaper: $RANDOM_PIC"
else
  echo "[WARN] No images found in $WALLPAPER_DIR"
  exit 1
fi
