#!/bin/bash

# Set up python virtual environment
python3 -m venv .venv
source .venv/bin/activate.fish

# Install dependencies
pip install numpy pillow pyvista