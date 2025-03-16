import os
import sys
from extracter import code_snippet_extractor

file_names = []

files = {}
# Open and read the file
input_file = "chatgpt.txt"

def build_directory_tree(lines):
    tree = {}
    stack = [("", tree)]  # Stack to track parent folders

    for line in lines:
        depth = line.count('│') + line.count('└') + line.count('├') # Count indent markers
        name = line.replace('│', '').replace('└', '')
        # .replace('──', '').strip()
        
        while name and not name[0].isalpha():
            name = name[1:]  # Remove leading non-alphabetic characters
        name = name.strip()
        # print(f"depth : {depth}, name : {name}  \n line : {line}")


        while len(stack) > depth + 1:
            stack.pop()  # Adjust stack to current depth

        parent = stack[-1][1]  # Get parent dictionary
        if name:  # Ignore empty lines
            parent[name] = {}  # Add folder/file to parent
            stack.append((name, parent[name]))  # Push new folder onto stack

    # print(tree)
    return tree

def print_tree(tree, indent=0):
    for key, value in tree.items():
        print("  " * indent + key)
        print_tree(value, indent + 1)

def create_structure(base_path, tree):
    # print(f"Creating structure in '{base_path}'...")
    """Recursively creates directories and files based on the tree structure."""
    for name, subtree in tree.items():
        if name:
            if not name[0].isalpha():
                name = name[1:]

        path = os.path.join(base_path, name)
        # print(base_path, name)
        # print(f"actual path is : '{path}'...")
        
        if isinstance(subtree, dict):
            if "." in name:  # If the name contains a dot, it's a file
                try:
                    with open(path, 'r', encoding="utf-8") as f:
                        content = ''.join([line for line in f if line.strip()])
                        files[name] = content
                    
                except FileNotFoundError:
                    print(f"File not found: {path}")
                
            else:
                # print(f"Directory created: {path}")
                # os.makedirs(path, exist_ok=True)  # Creates a directory
                # print(f"Directory created: {path}")
                create_structure(path, subtree)  # Recursively create subdirectories and files


if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        print("Please provide a file path as a command-line argument.")
        sys.exit(1)

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding="utf-8") as file:
            lines = [line.split('#', 1)[0].strip() for line in file.readlines() if line.split('#', 1)[0].strip()]
        
        directory_tree = build_directory_tree(lines)
        # print_tree(directory_tree)  # Display the tree
        # print(f"tree : {directory_tree}")
        print("Directory structure:")
        print_tree(directory_tree)

        # Set the base directory (modify this if needed)
        base_directory = os.getcwd()
        create_structure(base_directory, directory_tree) # Create the directory structure

        with open("output_files.txt", "w", encoding="utf-8") as output_file:
            for file_name, content in files.items():
                if file_name.endswith('.py'):
                    output_file.write(f"File: {file_name}\n ```python\n")
                    output_file.write(content + "```" + "\n\n\n")
                else:
                    output_file.write(f"File: {file_name}\n")
                    output_file.write(content + "\n\n\n")
    else:
        print(f"File '{file_path}' does not exist.")
