source /usr/share/cachyos-fish-config/cachyos-config.fish

starship init fish | source
zoxide init fish | source

alias cls="clear"
alias sudoe="sudo -E"

function fish_greeting
    fastfetch
end

function y
    set tmp (mktemp -t "yazi-cwd.XXXXXX")
    command yazi $argv --cwd-file="$tmp"
    if read -z cwd <"$tmp"; and [ "$cwd" != "$PWD" ]; and test -d "$cwd"
        builtin cd -- "$cwd"
    end
    rm -f -- "$tmp"
end
