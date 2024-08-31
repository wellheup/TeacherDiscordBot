#!/bin/bash

echo "Checking and installing required tools..."

# Check if a command exists and install it if it does not
ensure_installed() {
  local pkg_name=$1
  local check_cmd=$2
  local install_cmd=$3

  if ! command -v $check_cmd &> /dev/null; then
    echo "$pkg_name not found. Installing..."
    eval $install_cmd
  else
    echo "$pkg_name is already installed."
  fi
}

# Check and install Python packages
ensure_installed "black" "black" "pip install black"
ensure_installed "isort" "isort" "pip install isort"
ensure_installed "flake8" "flake8" "pip install flake8"

# Check and install Prettier
ensure_installed "prettier" "prettier" "npm install --global prettier"

echo "Formatting project files while excluding specific directories..."

# Directories to exclude
EXCLUDE_DIRS="venv,node_modules,__pycache__,*.egg-info,dist,.pythonlibs,.upm,.__pycache__,.git,.pytest_cache,.local"

# Convert excluded directories into -prune patterns for find command
EXCLUDE_FIND_PATTERNS=$(echo $EXCLUDE_DIRS | tr ',' ' ' | sed 's|\([^ ]*\)|-path ./\1 -o|g' | sed 's/ -o$//')

# Function to run formatting commands with appropriate exclusions
run_format() {
  local file_pattern=$1
  local format_cmd=$2

  find . \( $EXCLUDE_FIND_PATTERNS \) -prune -false -o -name "$file_pattern" -print0 | xargs -0 $format_cmd
}

# Format Python files
echo "Formatting Python files with black..."
run_format "*.py" "black"

echo "Sorting imports with isort..."
run_format "*.py" "isort"

echo "Checking code with flake8..."
run_format "*.py" "flake8 --config .flake8"

# Format HTML and CSS files
echo "Formatting HTML files with prettier..."
prettier --write "**/*.html" --ignore-path ".prettierignore"

echo "Formatting CSS files with prettier..."
prettier --write "**/*.css" --ignore-path ".prettierignore"

echo "Formatting complete!"