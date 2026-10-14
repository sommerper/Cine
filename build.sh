#!/bin/sh
# Builds Cine and installs it to ~/.local (launcher ends up at ~/.local/bin/cine).
set -e
cd "$(dirname "$0")"
[ -d _build ] || meson setup _build --prefix="$HOME/.local"
meson install -C _build
