import os
import ast
import subprocess
import sys
import glob
import pyfiglet
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def get_installed_version(library_name):
    """Returns the installed version of a library using pip."""
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', 'show', library_name], capture_output=True, text=True)
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                if line.startswith("Version:"):
                    return line.split("Version:")[1].strip()
        return None
    except Exception as e:
        print(Fore.RED + f"Error checking version for {library_name}: {e}")
        return None

def extract_imports_from_file(file_path):
    """Extracts import statements from a Python file."""
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read(), filename=file_path)
    
    imports = set()  # Use a set to avoid duplicates
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            imports.add(node.module)
    
    return imports

def generate_requirements_txt(file_path, output_file='requirements.txt'):
    """Generates a requirements.txt file based on the imports in a Python file."""
    # Step 1: Extract the imports
    imports = extract_imports_from_file(file_path)
    
    # Step 2: Check the versions of the imported libraries
    requirements = []
    for library in imports:
        version = get_installed_version(library)
        if version:
            requirements.append(f"{library}=={version}")
        else:
            print(Fore.YELLOW + f"Warning: Could not find version for {library}")
    
    # Step 3: Write the requirements.txt file
    if requirements:
        with open(output_file, 'w') as f:
            f.write("\n".join(requirements) + "\n")
        print(Fore.GREEN + f"requirements.txt has been created at {output_file}")
    else:
        print(Fore.RED + "No requirements to write.")

def find_python_files_in_directory(directory):
    """Finds all Python (.py) files in the given directory."""
    return glob.glob(os.path.join(directory, '**', '*.py'), recursive=True)

def display_logo():
    """Displays the CyberFantics logo using pyfiglet with color."""
    logo = pyfiglet.figlet_format("CyberFantics")
    print(Fore.CYAN + logo)

def main():
    """Main function to run the menu and execute actions based on user input."""
    display_logo()
    
    print(Fore.GREEN + "Welcome to CyberFantics Python Dependency Generator!")
    
    while True:
        print(Fore.YELLOW + "\nMenu:")
        print(Fore.CYAN + "1. Get imports from a project folder and create a requirements.txt file")
        print(Fore.CYAN + "2. Generate requirements.txt for a specific Python file")
        print(Fore.RED + "3. Exit")
        
        choice = input(Fore.MAGENTA + "Enter your choice (1/2/3): ").strip()
        
        if choice == '1':
            # Ask the user for the project folder
            project_folder = input(Fore.MAGENTA + "Enter the path of your project folder: ").strip()
            if not os.path.isdir(project_folder):
                print(Fore.RED + "Invalid folder path. Please try again.")
                continue

            # Find all Python files in the directory
            python_files = find_python_files_in_directory(project_folder)
            if not python_files:
                print(Fore.RED + "No Python files found in the specified folder.")
                continue
            
            print(Fore.GREEN + f"\nFound {len(python_files)} Python files in the project folder.")
            print(Fore.GREEN + "Generating requirements.txt for the entire project...")

            # Create a requirements.txt file in the project folder
            requirements_path = os.path.join(project_folder, 'requirements.txt')
            with open(requirements_path, 'w') as req_file:
                for py_file in python_files:
                    print(Fore.CYAN + f"Processing {py_file}...")
                    imports = extract_imports_from_file(py_file)
                    for library in imports:
                        version = get_installed_version(library)
                        if version:
                            req_file.write(f"{library}=={version}\n")
            print(Fore.GREEN + f"requirements.txt has been generated at {requirements_path}")
        
        elif choice == '2':
            # Ask for a specific file
            file_path = input(Fore.MAGENTA + "Enter the path of the Python file: ").strip()
            if not os.path.isfile(file_path):
                print(Fore.RED + "Invalid file path. Please try again.")
                continue

            # Generate the requirements.txt for the given file
            generate_requirements_txt(file_path, os.path.join(os.path.dirname(file_path), 'requirements.txt'))

        elif choice == '3':
            print(Fore.RED + "Exiting the program...")
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
