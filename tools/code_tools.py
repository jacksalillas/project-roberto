from langchain.tools import tool
import os
import subprocess

@tool
def read_code_file(file_path: str) -> str:
    """Reads and returns the content of a specified code file from the local filesystem.
    Returns the file content as a string.
    """
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return f"Error: File not found at {file_path}"
    except Exception as e:
        return f"Error reading file {file_path}: {e}"

@tool
def write_code_file(file_path: str, content: str) -> str:
    """Writes content to a specified code file on the local filesystem. Creates the file if it doesn't exist.
    Returns a success message or an error message.
    """
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)
        return f"Successfully wrote to {file_path}"
    except Exception as e:
        return f"Error writing to file {file_path}: {e}"

@tool
def execute_code(code: str, language: str = "python") -> str:
    """Executes a given code snippet in a specified language (default: python) and returns its stdout and stderr.
    Supports 'python' and 'bash'.
    """
    if language.lower() == "python":
        try:
            result = subprocess.run(["python3", "-c", code], capture_output=True, text=True, check=True)
            return f"Stdout:\n{result.stdout}\nStderr:\n{result.stderr}"
        except subprocess.CalledProcessError as e:
            return f"Error executing Python code:\nStdout:\n{e.stdout}\nStderr:\n{e.stderr}"
        except FileNotFoundError:
            return "Error: python3 command not found. Is Python installed and in PATH?"
    elif language.lower() == "bash":
        try:
            result = subprocess.run(["bash", "-c", code], capture_output=True, text=True, check=True)
            return f"Stdout:\n{result.stdout}\nStderr:\n{result.stderr}"
        except subprocess.CalledProcessError as e:
            return f"Error executing Bash code:\nStdout:\n{e.stdout}\nStderr:\n{e.stderr}"
        except FileNotFoundError:
            return "Error: bash command not found."
    else:
        return f"Error: Unsupported language '{language}'. Only 'python' and 'bash' are supported."

@tool
def refactor_code(code: str) -> str:
    """Improve or refactor Python or Bash code passed in as a string."""
    # LLM handles logic; just structure input/output.
    return f"Please improve this code:\n\n{code}"
