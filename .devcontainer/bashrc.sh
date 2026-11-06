parse_git_branch() {
    git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/(\1)/'
}
export PS1="\u@\h \[\e[32m\]\w \[\e[91m\]\$(parse_git_branch)\[\e[00m\]$ "
source /usr/app/venv/bin/activate

if [ -f "/workspaces/template-python-devcontainer/.devcontainer/load_mcp_config_tokens.sh" ]; then
    source "/workspaces/template-python-devcontainer/.devcontainer/load_mcp_config_tokens.sh"
fi
