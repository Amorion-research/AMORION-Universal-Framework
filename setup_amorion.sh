#!/usr/bin/env bash
set -e

# Define variables
TEMPLATE_REPO="https://github.com/philip/amorion-templates.git"
TEMPLATE_DIR=".amorion-templates"
EXPERIMENT_SCRIPT="experiments/exp1_ss1_tensor.sh"
MUTUAL_INFO_FILE="modules/SS1_tensor/mutual_information.txt"
PYTHON_REQUIREMENTS="requirements.txt"

# Function to check if a command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Function to install Python dependencies
install_python_dependencies() {
  if command_exists pip3; then
    if [ -f "$PYTHON_REQUIREMENTS" ]; then
      echo "Installing Python dependencies from $PYTHON_REQUIREMENTS..."
      pip3 install -r "$PYTHON_REQUIREMENTS"
    else
      echo "Error: $PYTHON_REQUIREMENTS not found.  Please create this file with your dependencies."
      exit 1
    fi
  else
    echo "Error: pip3 not found. Please install pip3."
    exit 1
  fi
}

# Function to clone or update the template repository
clone_or_update_template() {
  if [ ! -d "$TEMPLATE_DIR" ]; then
    echo "Cloning template repository from $TEMPLATE_REPO..."
    git clone "$TEMPLATE_REPO" "$TEMPLATE_DIR" || {
      echo "Error: Failed to clone template repository."
      exit 1
    }
  else
    echo "Updating template repository..."
    (cd "$TEMPLATE_DIR" && git pull) || {
      echo "Error: Failed to update template repository."
      exit 1
    }
  fi
}

# Function to synchronize templates
sync_templates() {
  echo "Synchronizing templates..."
  rsync -avr "$TEMPLATE_DIR/" ./ || {
    echo "Error: Failed to synchronize templates."
    exit 1
  }
}

# Function to set execute permissions
set_execute_permissions() {
  echo "Setting execute permissions..."
  chmod +x setup_amorion.sh "$EXPERIMENT_SCRIPT"
}

# Function to run the experiment
run_experiment() {
  echo "Running experiment: $EXPERIMENT_SCRIPT..."
  bash "$EXPERIMENT_SCRIPT" || {
    echo "Error: Experiment failed."
    exit 1
  }
}

# Function to display results
display_results() {
  echo "--- Files in SS1_tensor ---"
  ls modules/SS1_tensor

  echo "--- Mutual Information ---"
  if [ -f "$MUTUAL_INFO_FILE" ]; then
    cat "$MUTUAL_INFO_FILE"
  else
    echo "Error: $MUTUAL_INFO_FILE not found."
  fi
}

# Main script execution
echo "Starting Amorion setup..."

# Check for git and rsync
if ! command_exists git; then
  echo "Error: git is not installed. Please install git."
  exit 1
fi

if ! command_exists rsync; then
  echo "Error: rsync is not installed. Please install rsync."
  exit 1
fi

clone_or_update_template
sync_templates
install_python_dependencies
set_execute_permissions
run_experiment
display_results

echo "Amorion setup complete."
