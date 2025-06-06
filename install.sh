#!/usr/bin/env bash

# Create virtual environment if it doesn't exist
if [ ! -d .venv ]; then
    python3 -m venv .venv
fi

# Detect shell
shell_name=$(basename "$SHELL")

# Activate virtual environment
case "$shell_name" in
    bash|zsh)
        source .venv/bin/activate
        ;;
    fish)
        source .venv/bin/activate.fish
        ;;
    csh|tcsh)
        source .venv/bin/activate.csh
        ;;
    *)
        echo "Unsupported shell: $shell_name"
        echo "Please activate the virtual environment manually."
        exit 1
        ;;
esac

# Install dependencies
pip install numpy pillow pyvista

mkdir model
