#!/bin/bash

# 2. Randomize bold settings
# -n: No bold, -b: Random bold, -B: All bold
bold_options=("-n" "-b" "-B")
selected_bold=${bold_options[$RANDOM % ${#bold_options[@]}]}

# 3. Randomize scroll & special modes
# -a: Asynchronous (smooth)
# -o: Old-style scrolling
# -r: Rainbow mode
# -m: Lambda mode
special_flags=""
[[ $((RANDOM % 2)) -eq 0 ]] && special_flags+="-a "
[[ $((RANDOM % 3)) -eq 0 ]] && special_flags+="-o "
[[ $((RANDOM % 4)) -eq 0 ]] && special_flags+="-r "
[[ $((RANDOM % 5)) -eq 0 ]] && special_flags+="-m "

# 4. Randomize update delay (0 is fastest, 10 is slowest)
delay=$((RANDOM % 4 + 4))

# Build the command string
# We ignore -C if Rainbow mode (-r) is active as they conflict
if [[ $special_flags == *"-r"* ]]; then
  exec cmatrix -s $selected_bold $special_flags -u "$delay"
else
  exec cmatrix -s $selected_bold $special_flags -u "$delay"
fi
