source /usr/share/cachyos-fish-config/cachyos-config.fish

starship init fish | source
zoxide init fish | source

alias cls="clear"

function fish_greeting
    set -l roll (random 1 100)

    if test $roll -le 40
        set -l fonts /usr/share/figlet/*.flf
        set -l random_font (basename (random choice $fonts) .flf)
        toilet -f $random_font Hello -F rainbow
    else if test $roll -le 80
        fortune -s | cowsay | lolcat -p 10
    else
        fastfetch
    end
end

function y
    set tmp (mktemp -t "yazi-cwd.XXXXXX")
    command yazi $argv --cwd-file="$tmp"
    if read -z cwd <"$tmp"; and [ "$cwd" != "$PWD" ]; and test -d "$cwd"
        builtin cd -- "$cwd"
    end
    rm -f -- "$tmp"
end
