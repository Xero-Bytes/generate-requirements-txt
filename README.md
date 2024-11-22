# CyberFantics Python Dependency Generator

CyberFantics Python Dependency Generator is a powerful and interactive tool for generating `requirements.txt` files. It analyzes your Python project or a specific file, detects third-party libraries, and creates a precise dependency list, excluding standard libraries. With an intuitive menu and visually appealing interface, it simplifies dependency management for your Python projects.

---

## Features
- 📁 **Generate requirements.txt for an entire project folder**  
  Automatically scans all Python files in a directory and creates a `requirements.txt` file.  

- 📄 **Generate requirements.txt for a specific Python file**  
  Detects the third-party libraries used in a single file and creates a `requirements.txt` for it.  

- 📜 **List Standard Libraries**  
  Displays all the Python standard libraries that are excluded from the dependency list.  

- 🎨 **Interactive Interface**  
  A sleek and interactive menu with a **CyberFantics** logo powered by `pyfiglet` and color-coded terminal output using `colorama`.  

- 💡 **Error Handling and Warnings**  
  Notifies users about libraries without version information or missing installations.  

---

## Installation
1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/cyberfantics/python-dependency-generator.git
   cd python-dependency-generator
   ```
2. Install the required libraries:
   ```
   pip install -r requirements.txt
   ```

---

## How to Use
1. Run the script:
```
   python main.py
```
2. Follow the interactive menu:
   - Select the action you want to perform.
   - Provide the folder or file path when prompted.

## Menu Options

### 1. Generate `requirements.txt` for an Entire Project Folder  
- **Input:** Provide the path of your project folder.  
- **Action:** The script scans all `.py` files in the folder and generates a `requirements.txt` file.  

### 2. Generate `requirements.txt` for a Specific Python File  
- **Input:** Provide the path of a Python file.  
- **Action:** The script creates a `requirements.txt` based on the file's imports.  

### 3. Display Standard Libraries  
- **Action:** Shows a list of Python standard libraries excluded from the dependency list.  

### 4. Exit  
- **Action:** Closes the application.  

---

## Example Output  
When generating a `requirements.txt`, the program outputs:  

```
[+] Processing file: example.py
[+] Found dependency: requests==2.28.1
[+] Found dependency: numpy==1.23.4
[+] requirements.txt has been generated at /path/to/project/requirements.txt
```

---

## Author  
`Syed Mansoor ul Hassan Bukhari`  

- **GitHub:** [CyberFantics](https://github.com/CyberFantics)  
- **LinkedIn:** [Mansoor Bukhari](https://www.linkedin.com/in/mansoor-bukhari-77549a264/)  
