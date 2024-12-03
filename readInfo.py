# import os
# import json
# import ast  # To safely evaluate lists from the text file

# def parse_info_file(info_path):
#     """
#     Parse the info.txt file into a dictionary.
#     Supports lists in fields like hobbies or favorite_food.
#     """
#     info = {}
#     try:
#         with open(info_path, "r") as file:
#             for line in file:
#                 line = line.strip()
#                 if ":" in line:
#                     key, value = line.split(":", 1)
#                     key = key.strip()
#                     value = value.strip()
                    
#                     # Safely evaluate list-like values or keep strings
#                     try:
#                         info[key] = ast.literal_eval(value) if value.startswith("[") else value
#                     except (ValueError, SyntaxError):
#                         info[key] = value
#     except Exception as e:
#         print(f"Error parsing {info_path}: {e}")
#     return info

# def extract_data(base_path):
#     data = {"grandchildren": []}

#     # Path to grandchildren directory
#     grandchildren_path = os.path.join(base_path, "grandchildren")

#     # Iterate through each grandchild's folder
#     for grandchild in os.listdir(grandchildren_path):
#         grandchild_path = os.path.join(grandchildren_path, grandchild)
#         if os.path.isdir(grandchild_path):
#             # Initialize grandchild's data
#             grandchild_data = {"name": grandchild, "images": [], "info": {}}

#             # Extract images
#             images_path = os.path.join(grandchild_path, "images")
#             if os.path.exists(images_path):
#                 grandchild_data["images"] = [
#                     os.path.join(base_path, "grandchildren", grandchild, "images", img)
#                     for img in os.listdir(images_path)
#                     if img.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
#                 ]

#             # Extract info.txt content
#             info_path = os.path.join(grandchild_path, "info.txt")
#             if os.path.exists(info_path):
#                 grandchild_data["info"] = parse_info_file(info_path)
            
#             # Add to list of grandchildren
#             data["grandchildren"].append(grandchild_data)

#     return data

# def update_html(data, html_path):
#     """
#     Update the index.html file with extracted data.
#     """
#     with open(html_path, "r") as file:
#         html_content = file.readlines()

#     # Find the placeholders and replace them
#     start_marker = "<!-- readInfo.py can overwrite everything from here -->"
#     end_marker = "// readInfo.py can overwrite up to here"
#     start_index = None
#     end_index = None

#     for i, line in enumerate(html_content):
#         if start_marker in line:
#             start_index = i
#         if end_marker in line:
#             end_index = i

#     if start_index is not None and end_index is not None:
#         # Generate the JavaScript data
#         grandchildren_js = json.dumps(data["grandchildren"], indent=4)

#         # Replace the placeholder section
#         updated_section = f"""
#         const grandchildren = {grandchildren_js};
#         """
#         html_content = (
#             html_content[: start_index + 1]
#             + [updated_section]
#             + html_content[end_index:]
#         )

#         # Write the updated content back to the file
#         with open(html_path, "w") as file:
#             file.writelines(html_content)
#     else:
#         print("Could not find markers in index.html to update.")

# def main():
#     # Specify the base paths
#     base_path = "all"
#     html_path = "index.html"

#     # Extract data and update HTML
#     extracted_data = extract_data(base_path)
#     update_html(extracted_data, html_path)
#     print("index.html updated successfully!")

# if __name__ == "__main__":
#     main()

import os
import json
import ast  # To safely evaluate lists from the text file

def parse_info_file(info_path):
    """
    Parse the info.txt file into a dictionary.
    Supports lists in fields like hobbies or favorite_food.
    """
    info = {}
    try:
        with open(info_path, "r") as file:
            for line in file:
                line = line.strip()
                if ":" in line:
                    key, value = line.split(":", 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Safely evaluate list-like values or keep strings
                    try:
                        info[key] = ast.literal_eval(value) if value.startswith("[") else value
                    except (ValueError, SyntaxError):
                        info[key] = value
    except Exception as e:
        print(f"Error parsing {info_path}: {e}")
    return info

def extract_data(base_path):
    data = {"grandchildren": [], "children": []}

    # Extract grandchildren data
    grandchildren_path = os.path.join(base_path, "grandchildren")
    data["grandchildren"] = extract_individuals_data(grandchildren_path, "grandchildren", base_path)

    # Extract children data
    children_path = os.path.join(base_path, "children")
    data["children"] = extract_individuals_data(children_path, "children", base_path)

    return data

def extract_individuals_data(directory_path, relationship_type, base_path):
    """
    Extract data for individuals (children or grandchildren).
    """
    individuals = []
    if os.path.exists(directory_path):
        for individual in os.listdir(directory_path):
            individual_path = os.path.join(directory_path, individual)
            if os.path.isdir(individual_path):
                # Initialize individual's data
                individual_data = {"name": individual, "images": [], "info": {}}

                # Extract images
                images_path = os.path.join(individual_path, "images")
                if os.path.exists(images_path):
                    individual_data["images"] = [
                        os.path.join(base_path, relationship_type, individual, "images", img)
                        for img in os.listdir(images_path)
                        if img.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
                    ]

                # Extract info.txt content
                info_path = os.path.join(individual_path, "info.txt")
                if os.path.exists(info_path):
                    individual_data["info"] = parse_info_file(info_path)
                
                # Add to list of individuals
                individuals.append(individual_data)
    return individuals

def update_html(data, html_path):
    """
    Update the index.html file with extracted data.
    """
    with open(html_path, "r") as file:
        html_content = file.readlines()

    # Find the placeholders and replace them
    start_marker = "<!-- readInfo.py can overwrite everything from here -->"
    end_marker = "// readInfo.py can overwrite up to here"
    start_index = None
    end_index = None

    for i, line in enumerate(html_content):
        if start_marker in line:
            start_index = i
        if end_marker in line:
            end_index = i

    if start_index is not None and end_index is not None:
        # Generate the JavaScript data
        data_js = json.dumps(data, indent=4)

        # Replace the placeholder section
        updated_section = f"""
        const data = {data_js};
        """
        html_content = (
            html_content[: start_index + 1]
            + [updated_section]
            + html_content[end_index:]
        )

        # Write the updated content back to the file
        with open(html_path, "w") as file:
            file.writelines(html_content)
    else:
        print("Could not find markers in index.html to update.")

def main():
    # Specify the base paths
    base_path = "all"
    html_path = "index.html"

    # Extract data and update HTML
    extracted_data = extract_data(base_path)
    update_html(extracted_data, html_path)
    print("index.html updated successfully!")

if __name__ == "__main__":
    main()

#test
