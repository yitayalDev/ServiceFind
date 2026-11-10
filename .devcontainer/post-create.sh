#!/usr/bin/env bash
#
# ServiceFind post-create script.
# Runs after the devcontainer is created. Verifies that Flutter, Dart, and
# Python are available and prints their versions.
set -euo pipefail

echo "============================================================"
echo " ServiceFind post-create verification"
echo "============================================================"

echo ""
echo "--- Flutter ---"
flutter --version

echo ""
echo "--- Dart ---"
dart --version

echo ""
echo "--- Python ---"
python3 --version

echo ""
echo "--- Pip (in venv) ---"
python3 -m pip --version

echo ""
echo "--- Flutter doctor (summary) ---"
flutter doctor || true

echo ""
echo "============================================================"
echo " ServiceFind environment is ready."
echo "============================================================"
