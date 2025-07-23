#!/bin/env bash

# Generate the static site
python3 src/main.py

# Start the web server in the public directory
cd public && python3 -m http.server 8888