#!/bin/bash

TERM_WIDTH=$(tput cols)
TERM_HEIGHT=$(tput lines)

NUM=$((RANDOM % 100))
FRONT=$(toilet -f future "$NUM" -F rainbow)

gum style \
  --align center \
  --margin "2 1 0 1" \
  --padding "5 0" \
  --width $((TERM_WIDTH - 2)) \
  --height 12 \
  "$FRONT"

tput civis
