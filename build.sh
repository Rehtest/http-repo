#!/bin/bash

# Build script for GitHub Pages deployment
# This builds the site with the GitHub Pages basepath

echo "Building site for GitHub Pages..."
python3 src/main.py "/http-repo/"
echo "Build completed! Site is ready in the docs directory."
