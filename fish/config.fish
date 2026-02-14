source /usr/share/cachyos-fish-config/cachyos-config.fish

alias cls="clear"
alias sude="sudo -E"

starship init fish | source
zoxide init fish | source

function fish_greeting
    catnap
end

function y
    set tmp (mktemp -t "yazi-cwd.XXXXXX")
    command yazi $argv --cwd-file="$tmp"
    if read -z cwd <"$tmp"; and [ "$cwd" != "$PWD" ]; and test -d "$cwd"
        builtin cd -- "$cwd"
    end
    rm -f -- "$tmp"
end
