import os
from PIL import Image, ExifTags

def create_folder(directory):  # renamed to make it more descriptive and concise
    """Creates a new folder in the current working directory with the given name.
    :param directory: The path to the folder to be created, including the file system path.
    """
    try:
        os.makedirs(directory, exist_ok=True)  # added exist_ok parameter for improved efficiency
        # print(f"Directory {directory} created successfully.")
    except OSError:
        print(f"Directory {directory} already exists.")

def get_content_list(directory):
    """Gets a list of files and subdirectories in the given directory.
    :param directory: The path to the directory to be searched, including the file system path.
    :return: A list of file and subdirectory names.
    """
    content = []  # initialized an empty list
    try:
        files = os.listdir(directory)  # list all files and subdirectories in the directory
        for file in files:
            if os.path.isfile(os.path.join(directory, file)):  # check if the file exists
                content.append(file)
            elif os.path.isdir(os.path.join(directory, file)):  # check if the subdirectory exists
                content.extend(get_content_list(os.path.join(directory, file)))  # recursive function call to get contents of subdirectory
    except FileNotFoundError:
        print(f"Directory {directory} not found")
    return content


def get_image_meta(image_path):  # renamed to make it more descriptive and concise
    """Gets the metadata of an image file, including EXIF data if available.
    :param image_path: The path to the image file, including the file system path.
    :return: A dictionary of metadata, including EXIF tags and values. If no EXIF data is found, returns an empty dictionary.
    """
    try:
        image = Image.open(image_path)  # open the image file using PIL
        exif_data = image.getexif()  # retrieve EXIF data from the image file
        meta_data = {}  # initialized an empty dictionary to store metadata
        if exif_data:
            for tag, value in exif_data.items():
                tag_name = ExifTags.TAGS.get(tag)  # map EXIF tags to their names
                meta_data[tag_name] = value
        return meta_data
    except:
        print(f"Error reading image meta data.")


def main():
    #make grouped folder
    grouped_folder_name = "destination_folder"
    create_folder(grouped_folder_name)


    #list down content of source folder
    source_directory = "source_images"
    files = get_content_list(source_directory)

    for image in files:

        image_path = f"./source_images/{image}"
        meta_data = get_image_meta(image_path)

        try:
            output_folder_name = meta_data['DateTime'].split(' ')[0].replace(":", ".")
        except KeyError:
            output_folder_name = 'Uncategorized'
        except TypeError:
            continue

        output_image_path = f"./{grouped_folder_name}/{output_folder_name}/{image}"

        # print("------------------------------------------")
        # print(f"output content {output_contents}")
        # print(f"output folder name {output_folder_name}")
        # print(output_folder_name in output_contents)
        # print("------------------------------------------")
    
        try:
            os.makedirs(f"./{grouped_folder_name}/{output_folder_name}")
        except FileExistsError:
            pass
        
        with open(image_path, 'rb') as source_image:
            image_data = source_image.read()
        
        with open(output_image_path, 'wb+') as destination_image:
            destination_image.write(image_data)


if __name__ == "__main__":
    main()
    print("Categorized Successfully!")



