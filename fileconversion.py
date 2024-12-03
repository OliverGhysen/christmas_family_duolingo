"""
    for each *name* is a name in "Big surprise tegen niemand zeggen .csv": (so for each answer row)
    
    automatically take the info from  *name* and convert it to 
    - a folder named *name* inside google_drive_data_converted
    - within this folder:
        - info.txt with the information from the google form converted 
        
            google form is exported in a .csv, example: 
                "Tijdstempel","Wat is je naam","Wat zijn je hobbies","Wat is je lievelingseten","Wat studeer je","Lievelings herinnering aan daddy","Upload 5 foto's van jezelf"
                "2024/12/03 8:48:17 p.m. CET","Vladimir Mylle","Flight Simulator + Tennis ","Lasagne","Luchtvaarttechnologie","Noten uit een boom slaan met een wandelstok in hof ter linden ","https://drive.google.com/u/0/open?usp=forms_web&id=12zynwZzHMlZvhwfDDxL2r61NDtpn5M-a;https://drive.google.com/u/0/open?usp=forms_web&id=1eN-3CUZL_ajzhFPAZOI_SzYMN0yO9dwl;https://drive.google.com/u/0/open?usp=forms_web&id=1MC0kBdfpWyNJ-BrOJlBbsM5oXX9QeeuV;https://drive.google.com/u/0/open?usp=forms_web&id=1Q3-gFiF7OCMoIUYqxUbqq_SnyuQeZNh2;https://drive.google.com/u/0/open?usp=forms_web&id=1QM44_bxA--A8txD8Fmoe5BPcF7yLEKgj"
             
            
            info.txt format example: 
                name: Isabelle
                hobbies: ["Hiking"]
                memories: ["In de tuin werken"]
                favorite_food: ["Quiche"]
        
        - an folder named "images" containing the images in folder "Upload 5 foto_s van jezelf (File responses)" that contain *name*, they are marked by who posted them, eg:
            IMG20240912164016 - Vladimir Mylle.jpg
    
"""

import os
import csv
import shutil

# Define paths
input_csv = "google_drive_data/Big surprise tegen niemand zeggen .csv"
input_images_folder = "google_drive_data/Upload 5 foto_s van jezelf (File responses)"
output_folder = "google_drive_data_converted"

def sanitize_filename(name):
    """Sanitize file or folder names to ensure compatibility with file systems."""
    return "".join(c if c.isalnum() or c in " ._-" else "_" for c in name)

def create_info_txt(folder_path, data_row):
    """Create the info.txt file with the required format."""
    info_txt_path = os.path.join(folder_path, "info.txt")
    info_content = f"""name: {data_row['Wat is je naam']}
hobbies: [{', '.join(f'"{hobby.strip()}"' for hobby in data_row['Wat zijn je hobbies'].split('+'))}]
memories: ["{data_row['Lievelings herinnering aan daddy'].strip()}"]
favorite_food: ["{data_row['Wat is je lievelingseten'].strip()}"]
"""
    with open(info_txt_path, "w") as file:
        file.write(info_content)

def copy_images_for_name(name, output_images_folder):
    """Copy images from the input folder to the new images folder."""
    os.makedirs(output_images_folder, exist_ok=True)
    for image_file in os.listdir(input_images_folder):
        if name in image_file:
            source = os.path.join(input_images_folder, image_file)
            destination = os.path.join(output_images_folder, image_file)
            shutil.copyfile(source, destination)

def process_csv(input_csv, input_images_folder, output_folder):
    """Process the CSV file and create folders for each entry."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(input_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row["Wat is je naam"].strip()
            folder_name = sanitize_filename(name)
            person_folder = os.path.join(output_folder, folder_name)

            # Create person's folder
            os.makedirs(person_folder, exist_ok=True)

            # Create info.txt
            create_info_txt(person_folder, row)

            # Create images folder and copy relevant images
            images_folder = os.path.join(person_folder, "images")
            copy_images_for_name(name, images_folder)

if __name__ == "__main__":
    process_csv(input_csv, input_images_folder, output_folder)
    print(f"Conversion completed! Data saved to {output_folder}")
