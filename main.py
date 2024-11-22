import os
import ast
import subprocess
import sys
import glob
import pyfiglet
from colorama import Fore, Style, init
import pkgutil

# Initialize colorama
init(autoreset=True)

# List of standard libraries (dynamically determined)
STANDARD_LIBRARIES = {module.name for module in pkgutil.iter_modules() if module.module_finder.path == ''}

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
    try:
        with open(file_path, 'r') as file:
            tree = ast.parse(file.read(), filename=file_path)
        
        imports = set()  # Use a set to avoid duplicates
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split('.')[0])  # Extract only the top-level package
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split('.')[0])
        
        return imports
    except Exception as e:
        print(Fore.RED + f"Error parsing file {file_path}: {e}")
        return set()

def generate_requirements_txt(file_path, output_file='requirements.txt'):
    """Generates a requirements.txt file based on the imports in a Python file."""
    # Step 1: Extract the imports
    imports = extract_imports_from_file(file_path)
    filtered_imports = [lib for lib in imports if lib not in STANDARD_LIBRARIES]

    # Step 2: Check the versions of the imported libraries
    requirements = []
    for library in filtered_imports:
        version = get_installed_version(library)
        if version:
            requirements.append(f"{library}=={version}")
        else:
            print(Fore.YELLOW + f"Warning: Could not determine version for {library} (it might not be installed).")
    
    # Step 3: Write the requirements.txt file
    if requirements:
        try:
            with open(output_file, 'w') as f:
                f.write("\n".join(requirements) + "\n")
            print(Fore.GREEN + f"requirements.txt has been created at {output_file}")
        except Exception as e:
            print(Fore.RED + f"Failed to write requirements.txt: {e}")
    else:
        print(Fore.RED + "No requirements to write (no third-party libraries detected).")

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
    
    print(Fore.GREEN + "Welcome to the Advanced CyberFantics Python Dependency Generator!")
    
    while True:
        print(Fore.YELLOW + "\nMenu:")
        print(Fore.CYAN + "1. Generate requirements.txt for an entire project folder")
        print(Fore.CYAN + "2. Generate requirements.txt for a specific Python file")
        print(Fore.CYAN + "3. Display standard libraries (excluded by default)")
        print(Fore.RED + "4. Exit")
        
        choice = input(Fore.MAGENTA + "Enter your choice (1/2/3/4): ").strip()
        
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
            all_imports = set()
            for py_file in python_files:
                print(Fore.CYAN + f"Processing {py_file}...")
                all_imports.update(extract_imports_from_file(py_file))
            
            filtered_imports = [lib for lib in all_imports if lib not in STANDARD_LIBRARIES]
            with open(requirements_path, 'w') as req_file:
                for library in filtered_imports:
                    version = get_installed_version(library)
                    if version:
                        req_file.write(f"{library}=={version}\n")
                    else:
                        print(Fore.YELLOW + f"Warning: Could not find version for {library}.")
            
            print(Fore.GREEN + f"requirements.txt has been generated at {requirements_path}")
        
        elif choice == '2':
            # Ask for a specific file
            file_path = input(Fore.MAGENTA + "Enter the path of the Python file: ").strip()
            if not os.path.isfile(file_path):
                print(Fore.RED + "Invalid file path. Please try again.")
                continue

            # Generate the requirements.txt for the given file
            output_path = os.path.join(os.path.dirname(file_path), 'requirements.txt')
            generate_requirements_txt(file_path, output_path)

        elif choice == '3':
            print(Fore.CYAN + "Standard Libraries (excluded from requirements.txt):")
            print(Fore.MAGENTA + ", ".join(sorted(STANDARD_LIBRARIES)))

        elif choice == '4':
            print(Fore.RED + "Exiting the program...")
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
