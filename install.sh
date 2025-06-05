#!/bin/bash

# Set up python virtual environment
python3 -m venv .venv
source .venv/bin/activate.fish

# Install dependencies
apt install gdal-bin libgdal-dev
pip install numpy pillow pyvista GDAL elevation

mkdir images