# Dark Modern Soft Powerline theme for Oh My Zsh
# Powerline layout from the Starship Catppuccin Powerline preset,
# with the Dark Modern Soft colors (VS Code theme, extras/palette.json).
#
# Requires a Nerd Font.

# Dark Modern Soft palette (matches the VS Code theme)
typeset -g SP_TEAL="#4fb0a6"
typeset -g SP_BLUE="#4690d2"
typeset -g SP_YELLOW="#e8bd5f"
typeset -g SP_CYAN="#68cbe6"
typeset -g SP_GRAY="#3b3c3e"
typeset -g SP_GREEN="#6ac483"
typeset -g SP_RED="#e4506f"
typeset -g SP_WHITE="#eef0f4"
typeset -g SP_TEXT="#d4d6dd"
typeset -g SP_CRUST="#1d1e22"

typeset -g SP_CURRENT_BG=""

# Powerline symbols
typeset -g SP_LEFT_ROUND=$'\ue0b6'
typeset -g SP_RIGHT_ROUND=$'\ue0b4'
typeset -g SP_ARROW=$'\ue0b0'

# Escape prompt text safely.
sp_escape() {
    print -nr -- "${1//\%/%%}"
}

# Start a Powerline segment.
# The first segment starts with the rounded Powerline cap.
sp_segment() {
    local background="$1"
    local foreground="$2"
    local text="$3"

    if [[ -z "$SP_CURRENT_BG" ]]; then
        print -nr -- "%F{$background}$SP_LEFT_ROUND%f"
    else
        print -nr -- "%F{$SP_CURRENT_BG}%K{$background}$SP_ARROW%f"
    fi

    print -nr -- "%K{$background}%F{$foreground} $text %f"
    SP_CURRENT_BG="$background"
}

# Close the current Powerline segment.
sp_end_segment() {
    if [[ -n "$SP_CURRENT_BG" ]]; then
        print -nr -- "%F{$SP_CURRENT_BG}%k$SP_RIGHT_ROUND%f"
    fi

    SP_CURRENT_BG=""
}

# Detect the operating system symbol used by the Starship preset.
sp_os_symbol() {
    case "$(uname -s 2>/dev/null)" in
        Linux)
            if [[ -f /etc/os-release ]]; then
                local distribution
                distribution="$(. /etc/os-release && print -r -- "$ID")"

                case "$distribution" in
                    ubuntu) print -nr -- "󰕈" ;;
                    arch) print -nr -- "󰣇" ;;
                    debian) print -nr -- "󰣚" ;;
                    fedora) print -nr -- "󰣛" ;;
                    alpine) print -nr -- "" ;;
                    *) print -nr -- "󰌽" ;;
                esac
            else
                print -nr -- "󰌽"
            fi
            ;;
        Darwin)
            print -nr -- "󰀵"
            ;;
        MINGW*|MSYS*|CYGWIN*)
            print -nr -- ""
            ;;
        *)
            print -nr -- "󰌽"
            ;;
    esac
}

# OS + username.
prompt_sp_identity() {
    local os_symbol
    os_symbol="$(sp_os_symbol)"

    sp_segment "$SP_TEAL" "$SP_CRUST" " $os_symbol"
    print -nr -- "%K{$SP_TEAL}%F{$SP_CRUST} %n %f"
}

# Current directory.
# Keep the same compact behavior as the original Agnoster:
# show only the current folder name instead of the complete path.
prompt_sp_directory() {
    local directory_name="${PWD##*/}"

    if [[ "$PWD" == "$HOME" ]]; then
        directory_name="~"
    elif [[ -z "$directory_name" ]]; then
        directory_name="/"
    fi

    sp_segment "$SP_BLUE" "$SP_WHITE" " $directory_name "
}

# Git branch and status.
prompt_sp_git() {
    (( $+commands[git] )) || return

    local inside_git
    inside_git="$(git rev-parse --is-inside-work-tree 2>/dev/null)" || return
    [[ "$inside_git" == "true" ]] || return

    local branch
    branch="$(git symbolic-ref --short HEAD 2>/dev/null)"
    if [[ -z "$branch" ]]; then
        branch="$(git rev-parse --short HEAD 2>/dev/null)"
    fi

    local git_status=""
    local staged=""
    local unstaged=""
    local untracked=""
    local ahead_behind=""

    staged="$(git diff --cached --name-only 2>/dev/null)"
    unstaged="$(git diff --name-only 2>/dev/null)"
    untracked="$(git ls-files --others --exclude-standard 2>/dev/null)"

    [[ -n "$staged" ]] && git_status+="✚"
    [[ -n "$unstaged" ]] && git_status+="±"
    [[ -n "$untracked" ]] && git_status+="?"

    local upstream
    upstream="$(git rev-parse --abbrev-ref '@{upstream}' 2>/dev/null)"
    if [[ -n "$upstream" ]]; then
        local ahead_count
        local behind_count

        ahead_count="$(git rev-list --count "${upstream}..HEAD" 2>/dev/null)"
        behind_count="$(git rev-list --count "HEAD..${upstream}" 2>/dev/null)"

        if (( ahead_count > 0 && behind_count > 0 )); then
            ahead_behind="⇅"
        elif (( ahead_count > 0 )); then
            ahead_behind="⇡"
        elif (( behind_count > 0 )); then
            ahead_behind="⇣"
        fi
    fi

    local text=" $branch"
    [[ -n "$git_status" || -n "$ahead_behind" ]] && text+=" (${git_status}${ahead_behind})"

    sp_segment "$SP_YELLOW" "$SP_CRUST" " $text "
}

# Conda environment.
prompt_sp_conda() {
    [[ -z "$CONDA_DEFAULT_ENV" ]] && return

    sp_segment "$SP_CYAN" "$SP_CRUST" "  $CONDA_DEFAULT_ENV "
}

# Current time.
prompt_sp_time() {
    sp_segment "$SP_GRAY" "$SP_TEXT" "  $(date '+%H:%M') "
}

# Command duration, displayed when the previous command took at least one second.
prompt_sp_duration() {
    [[ -z "$SP_COMMAND_START" ]] && return

    local elapsed=$(( EPOCHSECONDS - SP_COMMAND_START ))
    SP_COMMAND_START=""

    (( elapsed < 1 )) && return

    sp_segment "$SP_GRAY" "$SP_TEXT" " in ${elapsed}s "
}

# Final prompt character.
prompt_sp_character() {
    local exit_code="$1"
    sp_end_segment

    if (( exit_code == 0 )); then
        print -nr -- " %F{$SP_GREEN}❯%f "
    else
        print -nr -- " %F{$SP_RED}❯%f "
    fi
}

# Record command start time.
sp_preexec() {
    SP_COMMAND_START=$EPOCHSECONDS
}

# Build the prompt.
prompt_sp() {
    local exit_code="$?"

    SP_CURRENT_BG=""

    prompt_sp_identity
    prompt_sp_directory
    prompt_sp_git
    prompt_sp_conda
    prompt_sp_time
    prompt_sp_duration
    prompt_sp_character "$exit_code"
}

autoload -Uz add-zsh-hook
add-zsh-hook preexec sp_preexec

PROMPT='$(prompt_sp)'
