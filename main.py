import os
import ast
import subprocess
import sys
import glob
import pyfiglet
from colorama import Fore, Style, init
import pkgutil
from tqdm import tqdm

# Initialize colorama
init(autoreset=True)

# List of standard libraries (dynamically determined)
STANDARD_LIBRARIES = {module.name for module in pkgutil.iter_modules() if module.module_finder.path == ''}

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

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
    imports = extract_imports_from_file(file_path)
    filtered_imports = [lib for lib in imports if lib not in STANDARD_LIBRARIES]

    requirements = []
    for library in tqdm(filtered_imports, desc="Checking library versions"):
        version = get_installed_version(library)
        if version:
            requirements.append(f"{library}=={version}")
        else:
            print(Fore.YELLOW + f"Warning: Could not determine version for {library} (it might not be installed).")
    
    if requirements:
        if os.path.exists(output_file):
            confirm = input(Fore.RED + f"{output_file} already exists. Overwrite? (y/n): ").strip().lower()
            if confirm != 'y':
                print(Fore.YELLOW + "Operation cancelled.")
                return

        try:
            with open(output_file, 'w') as f:
                f.write("\n".join(requirements) + "\n")
            print(Fore.GREEN + f"requirements.txt has been created at {output_file}")
        except Exception as e:
            print(Fore.RED + f"Failed to write requirements.txt: {e}")
    else:
        print(Fore.RED + "No third-party libraries detected.")

def find_python_files_in_directory(directory):
    """Finds all Python (.py) files in the given directory."""
    return glob.glob(os.path.join(directory, '**', '*.py'), recursive=True)

def display_logo():
    """Displays the CyberFantics logo using pyfiglet with color."""
    clear_screen()
    logo = pyfiglet.figlet_format("CyberFantics")
    print(Fore.CYAN + logo)

def search_python_files(directory):
    """Search for specific Python files in a directory."""
    search_term = input(Fore.MAGENTA + "Enter the filename or keyword to search for: ").strip()
    python_files = find_python_files_in_directory(directory)
    results = [file for file in python_files if search_term in os.path.basename(file)]
    
    if results:
        print(Fore.GREEN + f"Found {len(results)} matching files:")
        for idx, file in enumerate(results, 1):
            print(Fore.CYAN + f"{idx}. {file}")
    else:
        print(Fore.RED + "No matching files found.")

def main():
    """Main function to run the menu and execute actions based on user input."""
    display_logo()
    print(Fore.GREEN + "\nWelcome to the Interactive CyberFantics Python Dependency Generator!")
    input(Fore.YELLOW + "Press Enter to start...")
    
    while True:
        display_logo()
        print(Fore.YELLOW + "\nMenu:")
        print(Fore.CYAN + "1. Generate requirements.txt for an entire project folder")
        print(Fore.CYAN + "2. Generate requirements.txt for a specific Python file")
        print(Fore.CYAN + "3. Search for Python files in a folder")
        print(Fore.CYAN + "4. Display standard libraries (excluded by default)")
        print(Fore.RED + "5. Exit")
        
        choice = input(Fore.MAGENTA + "Enter your choice (1/2/3/4/5): ").strip()
        if choice == '1':
            project_folder = input(Fore.MAGENTA + "Enter the path of your project folder: ").strip()
            if not os.path.isdir(project_folder):
                print(Fore.RED + "Invalid folder path. Please try again.")
                continue

            python_files = find_python_files_in_directory(project_folder)
            if not python_files:
                print(Fore.RED + "No Python files found in the specified folder.")
                continue
            
            print(Fore.GREEN + f"\nFound {len(python_files)} Python files.")
            requirements_path = os.path.join(project_folder, 'requirements.txt')
            all_imports = set()
            for py_file in tqdm(python_files, desc="Processing files"):
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
            file_path = input(Fore.MAGENTA + "Enter the path of the Python file: ").strip()
            if not os.path.isfile(file_path):
                print(Fore.RED + "Invalid file path. Please try again.")
                continue

            output_path = os.path.join(os.path.dirname(file_path), 'requirements.txt')
            generate_requirements_txt(file_path, output_path)
        
        elif choice == '3':
            folder_path = input(Fore.MAGENTA + "Enter the path of the folder: ").strip()
            if not os.path.isdir(folder_path):
                print(Fore.RED + "Invalid folder path. Please try again.")
                input()
                continue
            search_python_files(folder_path)
            input()
        
        elif choice == '4':
            print(Fore.CYAN + "Standard Libraries (excluded from requirements.txt):")
            print(Fore.MAGENTA + ", ".join(sorted(STANDARD_LIBRARIES)))
            print('-'*50)
            input()

        elif choice == '5':
            display_logo()
            print(Fore.GREEN + "Thank you for using CyberFantics Dependency Generator!")
            input()
            break
        
        else:
            print(Fore.RED + "Invalid choice. Please try again.")
            input()
        input(Fore.YELLOW + "Press Enter to return to the menu...")


if __name__ == "__main__":
    main()
