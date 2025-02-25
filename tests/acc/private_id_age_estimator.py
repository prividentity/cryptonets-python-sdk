import csv
import os
import sys
import time
import pandas as pd

from cryptonets_python_sdk.factor import FaceFactor
from cryptonets_python_sdk.settings.loggingLevel import LoggingLevel
from cryptonets_python_sdk.settings.configuration import ConfigObject
from cryptonets_python_sdk.settings.configuration import PARAMETERS
import os
from os import path

from tqdm import tqdm

SERVER_URL = "https://api.cryptonets.ai/node"
API_KEY = "accsb18b5f17d924db88"

# Get a list of images from a directory
def list_images(base_path):
    # loop over the directory structure
    image_types = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff")
    for (rootDir, dirNames, filenames) in os.walk(base_path):
        # loop over the filenames in the current directory
        for filename in filenames:
            # determine the file extension of the current file
            ext = filename[filename.rfind("."):].lower()
            # check to see if the file is an image and should be processed
            if ext.endswith(image_types):
                # construct the path to the image and yield it
                imagePath = os.path.join(rootDir, filename)
                yield imagePath

# Calculate a float age from the  years and months values in the AGEOFVISITMONTHS column
def parse_age(age_str):
    try:
        years_part, months_part = age_str.split(",")
        years = int(years_part.replace("Years", "").strip())
        months = int(months_part.replace("Months", "").strip())
        return years + months/12
    except:
        return None
 

if __name__ == "__main__":

    # Create FaceFactor config 
    config_param = {
        PARAMETERS.INPUT_IMAGE_FORMAT: "rgb",
        PARAMETERS.CONTEXT_STRING: "predict",
        # Relax the face validation settings to allow all faces to be predicted
        PARAMETERS.ESTIMATE_AGE_FACE_VALIDATIONS_OFF: True
    }

    config_object = ConfigObject(config_param)

    # Create FaceFactor object
    face_factor = FaceFactor(server_url=SERVER_URL, 
                            api_key=API_KEY,
                            config=config_object)
    

    if len(sys.argv) < 2:
        print("Usage: python private_id_age_estimator.py <relative_image_folder_path>")
        sys.exit(1)

    relative_image_folder_path = sys.argv[1]
    image_folder_path = path.join(path.dirname(__file__), relative_image_folder_path)

    if not os.path.exists(image_folder_path):
        print(f"Error: The folder {image_folder_path} does not exist.")
        sys.exit(1)    
    
   # Read CSV data
    csv_path = path.join(image_folder_path, "result.csv")
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)  # Get original header row
        rows = [row for row in reader]

    # Add new columns to header
    header.append("predicted age")
    header.append("real age")


    # Create prediction mapping
    predictions = {}

    image_path_list = list(list_images(image_folder_path))
    print("Processing {} images".format(len(image_path_list)))

    # Read existing CSV data
    csv_path = path.join(image_folder_path, 'result.csv')
    df = pd.read_csv(csv_path)

    with open(f'result_{time.time_ns()}.csv', 'w', newline='') as csvfile:
        fieldnames = ['image_path', 'error', 'message', 'return_code', 'return_message', 'age']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for image_path in tqdm(image_path_list):
            age_handle = face_factor.estimate_age(image_path=image_path)
            age_result = {"image_path": image_path.replace(image_folder_path, ""), "error": age_handle.error,
                          "message": age_handle.message}
            for index, face in enumerate(age_handle.face_objects):
                age_face_result = {"return_code": face.return_code, "return_message": face.message, "age": face.age}
                
                # Extract SELFIEIMAGEID from filename (e.g. 0010008_0.jpg -> 10008)
                filename = path.basename(image_path)
                selfie_id = filename.split("_")[0].lstrip("0")
                predictions[selfie_id] = face.age

                age_face_result = age_result | age_face_result
                writer.writerow(age_face_result)

    # Add predictions to CSV rows
    for row in rows:
        selfie_id = row[4].strip()  # SELFIEIMAGEID is 5th column (index 4)
        row.append(str(predictions.get(selfie_id, "N/A")))
        # Calculate real age
        age_str = row[2].strip()  # AGEOFVISITMONTHS is 3rd column (index 2)
        real_age = parse_age(age_str)
        row.append(str(real_age) if real_age is not None else "N/A")

    # Write updated CSV
    output_path = path.join(image_folder_path, "result_with_predictions.csv")
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
    print(f"\nPredictions saved to {output_path}")
