#!/bin/bash

MSG="Cachy!"
FONT_DIR="/usr/share/figlet/"

for font in "$FONT_DIR"*.flf; do
  font_name=$(basename "$font" .flf)
  echo "$font_name"
  toilet -f "$font_name" "$MSG" -F rainbow
  echo ""
done
