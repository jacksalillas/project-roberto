#!/bin/bash

# Get the directory where this setup script is located
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

ROBERTO_SCRIPT_NAME="roberto"
ROBERTO_SCRIPT_PATH="$PROJECT_ROOT/$ROBERTO_SCRIPT_NAME"
TARGET_BIN_DIR="$HOME/bin"
TARGET_ROBERTO_PATH="$TARGET_BIN_DIR/$ROBERTO_SCRIPT_NAME"

echo "Setting up Roberto CLI..."

# 1. Create the roberto executable script
cat << EOF > "$ROBERTO_SCRIPT_PATH"
#!/bin/bash

# Navigate to the project directory
cd "$PROJECT_ROOT"

# Activate the virtual environment
source .venv/bin/activate

# Run the Roberto CLI
python3 cli.py "\$@"
EOF

echo "Created executable script: $ROBERTO_SCRIPT_PATH"

# 2. Make the script executable
chmod +x "$ROBERTO_SCRIPT_PATH"
echo "Made '$ROBERTO_SCRIPT_NAME' executable."

# 3. Create the ~/bin/ directory if it doesn't exist
mkdir -p "$TARGET_BIN_DIR"
echo "Ensured '$TARGET_BIN_DIR' directory exists."

# 4. Move the roberto script to ~/bin/
mv "$ROBERTO_SCRIPT_PATH" "$TARGET_BIN_DIR/"
echo "Moved '$ROBERTO_SCRIPT_NAME' to '$TARGET_BIN_DIR/'."

# 5. Add ~/bin/ to PATH (idempotent)
SHELL_CONFIG_FILE=""
if [[ "$SHELL" == *"/zsh"* ]]; then
    SHELL_CONFIG_FILE="$HOME/.zshrc"
elif [[ "$SHELL" == *"/bash"* ]]; then
    SHELL_CONFIG_FILE="$HOME/.bashrc"
    if [ ! -f "$SHELL_CONFIG_FILE" ]; then
        SHELL_CONFIG_FILE="$HOME/.bash_profile"
    fi
else
    echo "Warning: Could not determine your shell configuration file (.zshrc or .bashrc/.bash_profile)."
    echo "Please manually add 'export PATH=\"$HOME/bin:\$PATH\"' to your shell's config file."
fi

if [ -n "$SHELL_CONFIG_FILE" ]; then
    if ! grep -q "export PATH=\"$HOME/bin:\$PATH\"" "$SHELL_CONFIG_FILE"; then
        echo -e "\\n# Add \$HOME/bin to PATH for Roberto CLI" >> "$SHELL_CONFIG_FILE"
        echo "export PATH=\"$HOME/bin:\$PATH\"" >> "$SHELL_CONFIG_FILE"
        echo "Added '$TARGET_BIN_DIR' to your PATH in '$SHELL_CONFIG_FILE'."
        echo "Please run 'source $SHELL_CONFIG_FILE' or open a new terminal for changes to take effect."
    else
        echo "'$TARGET_BIN_DIR' is already in your PATH in '$SHELL_CONFIG_FILE'."
        echo "Please run 'source $SHELL_CONFIG_FILE' or open a new terminal for changes to take effect."
    fi
else
    echo "Skipping PATH modification due to unknown shell configuration."
fi

echo "Roberto CLI setup script finished."
echo "You should now be able to type 'roberto' in a new terminal, or after sourcing your shell config file."
