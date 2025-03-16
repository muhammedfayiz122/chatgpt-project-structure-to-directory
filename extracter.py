import os

def code_snippet_extractor(file_name, input_file_name):
    def extract_text(lines, file_name, keyword, end_string):
        result = {}
        capture = False
        text = ""
        found_file = None

        for i, line in enumerate(lines):
            # Check if the file name is found in the current line
            if file_name in line:
                found_file = file_name

            # Start capturing if the keyword appears after a file name is found
            if found_file and keyword in line:
                capture = True
                continue  # Move to the next line to start capturing content

            # Capture text until the end_string is found
            if capture:
                if end_string in line:
                    result[found_file] = text.strip()
                    return result  # Stop processing after extracting one block
                text += line  # Keep appending lines

        return result  # Return the result even if end_string is not found

    keyword = "```python"  # Extract text after this
    end_string = "```"  # Stop capturing at this

    with open(input_file_name, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Extract text only if the file name is found first
    result = extract_text(lines, file_name, keyword, end_string)

    return result

if __name__ == "__main__":
    file_name = "main.py"
    input_file_name = "chatgpt.txt"
    extracted_code = code_snippet_extractor(file_name, input_file_name)
    print(extracted_code)
