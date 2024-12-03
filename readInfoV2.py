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
    generic_options = {
        "names": set(),
        "hobbies": set(),
        "favorite_food": set(),
        "memories": set()
    }

    # Extract grandchildren data
    grandchildren_path = os.path.join(base_path, "grandchildren")
    grandchildren_data, grandchildren_generic = extract_individuals_data(
        grandchildren_path, "grandchildren", base_path
    )
    data["grandchildren"] = grandchildren_data
    for key in generic_options:
        generic_options[key].update(grandchildren_generic[key])

    # Extract children data
    children_path = os.path.join(base_path, "children")
    children_data, children_generic = extract_individuals_data(
        children_path, "children", base_path
    )
    data["children"] = children_data
    for key in generic_options:
        generic_options[key].update(children_generic[key])

    # Add fake examples to generic options
    generic_options["names"].update(["Alex", "Jordan", "Taylor", "Morgan", "Chris"])
    generic_options["hobbies"].update(["Dancing", "Gardening", "Cycling", "Knitting", "Photography"])
    generic_options["favorite_food"].update(["Sushi", "Tacos", "Pancakes", "Steak", "Ramen"])
    generic_options["memories"].update([
        "Camping in the mountains",
        "Beach bonfire",
        "Family karaoke night",
        "Visiting a theme park",
        "Learning to cook together"
    ])

    # Convert sets to lists for serialization
    for key in generic_options:
        generic_options[key] = list(generic_options[key])

    return data, generic_options


def extract_individuals_data(directory_path, relationship_type, base_path):
    """
    Extract data for individuals (children or grandchildren).
    """
    individuals = []
    generic_options = {"names": set(), "hobbies": set(), "favorite_food": set(), "memories": set()}

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
                    info = parse_info_file(info_path)
                    individual_data["info"] = info

                    # Update generic options
                    generic_options["names"].add(individual)
                    for key in ["hobbies", "favorite_food", "memories"]:
                        if key in info and isinstance(info[key], list):
                            generic_options[key].update(info[key])

                # Add to list of individuals
                individuals.append(individual_data)
    return individuals, generic_options


def update_html(data, generic_options, html_path):
    """
    Update the index.html file with extracted data and generic options.
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
        generic_options_js = json.dumps(generic_options, indent=4)

        # Replace the placeholder section
        updated_section = f"""
        const data = {data_js};
        const genericOptions = {generic_options_js};
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
    html_path = "indexV2.html"

    # Extract data and update HTML
    extracted_data, generic_options = extract_data(base_path)
    update_html(extracted_data, generic_options, html_path)
    print("indexV2.html updated successfully!")


if __name__ == "__main__":
    main()
