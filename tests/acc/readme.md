# Private ID Age Estimator

This is a sample cde on how to use the very last  `PrivateID Python SDK` to estimates the age of individuals from images under the directory `.\30-images` which contains 30 face images and their true ages compiled in a CSV file (converted from the excel one ACC provided).

The script `private_id_age_estimator.py` will read images from the [30-images](./30-images/) folder and generate the following outpt files. 

1.  `result_<timestamp>.cvs` which will contain the output of the API method ` face_factor.estimate_age` :

```csv
image_path,error,message,return_code,return_message,age
/0009408_0.jpg,0,OK,0,ValidBiometric,22.4467316
/0010360_0.jpg,0,OK,0,ValidBiometric,16.1714134
/0010205_0.jpg,0,OK,0,ValidBiometric,16.9407234
/0009935_0.jpg,0,OK,0,ValidBiometric,17.8899536
/0010069_0.jpg,0,OK,0,ValidBiometric,17.7541122
/0010069_0.jpg,0,OK,0,ValidBiometric,18.5010529
/0007938_0.jpg,0,OK,0,ValidBiometric,23.7965488
/0010326_0.jpg,0,OK,0,ValidBiometric,18.6120682
/0010328_0.jpg,0,OK,0,ValidBiometric,19.2227516
/0009726_0.jpg,0,OK,0,ValidBiometric,17.0432281
/0010281_0.jpg,0,OK,0,ValidBiometric,17.412241
/0010277_0.jpg,0,OK,0,ValidBiometric,20.5784988
/0018957_0.jpg,0,OK,0,ValidBiometric,22.0033684
/0010448_0.jpg,0,OK,0,ValidBiometric,17.3935738
/0010302_0.jpg,0,OK,0,ValidBiometric,18.1522217
/0010037_0.jpg,0,OK,0,ValidBiometric,13.7925081
/0010227_0.jpg,0,OK,0,ValidBiometric,17.4310074
/0010008_0.jpg,0,OK,0,ValidBiometric,17.0484047
/0010217_0.jpg,0,OK,0,ValidBiometric,22.305809
/0010294_0.jpg,0,OK,0,ValidBiometric,18.0234337
/0001176_0.jpg,0,OK,0,ValidBiometric,17.8276672
/0009633_0.jpg,0,OK,0,ValidBiometric,17.3623638
/0010223_0.jpg,0,OK,0,ValidBiometric,18.103611
/0009947_0.jpg,0,OK,0,ValidBiometric,16.9253693
/0010316_0.jpg,0,OK,0,ValidBiometric,17.5700073
/0010263_0.jpg,0,OK,0,ValidBiometric,14.7835379
/0010397_0.jpg,0,OK,0,ValidBiometric,13.8309441
/0009975_0.jpg,0,OK,0,ValidBiometric,20.002388
/0010455_0.jpg,0,OK,0,ValidBiometric,18.9202194
/0009363_0.jpg,0,OK,0,ValidBiometric,17.3886337
/0009876_0.jpg,0,OK,0,ValidBiometric,23.1265545
```

2. `30-images\result_with_predictions.csv` which will add 2 columns `predicted age` (by the Python SDK)  ,`real age` (real age in float converted the column `AGEOFVISITMONTHS`)  :

```csv
WORKERPAYROLL,WORKERAGEYEARS,AGEOFVISITMONTHS,WORKERGENDER,SELFIEIMAGEID,SKINTONE,predicted age,real age
TP205,18,"18 Years, 1 Months ",Male,1176,12,17.8276672,18.083333333333332
TP833,18,"18 Years, 5 Months ",Female,10448,34,17.3935738,18.416666666666668
TP837,18,"18 Years, 10 Months ",Female,10455,12,18.9202194,18.833333333333332
TP1776,18,"18 Years, 4 Months ",Male,18957,34,22.0033684,18.333333333333332
....
```
- The Jupyter Notebook will do a similar task.


## Setup

### Prerequisites

- Python 3.x
- pip

### Preparing the Environment


2. **Create a virtual environment**:
    ```bash
    python -m venv .venv
    pip install -r requirements.txt 
    python .\private_id_age_estimator.py
    ```

3. **Activate the virtual environment**:
    - On Windows:
        ```bash
        .venv\Scripts\activate        
        ```
    - On macOS/Linux:
        ```bash
        source .venv/bin/activate
        ```

4. **Install the required packages**:
    ```bash
    pip install -r requirements.txt 
    ```

### Running the Script

1. **Run the main script**:
    - On Windows:
        ```bash
        # <relative_path_of_inmages_directory> : is a subdirectory containing the images
        python .\private_id_age_estimator.py <relative_path_of_inmages_directory>
        ```
    - On macOS/Linux:
        ```bash
         python private_id_age_estimator.py
        ```

2. **Run the Jupyter Notebook for visualization**:
    ```bash
    # Need manual setting of the image directory see the notebook comments.
    jupyter notebook private_id_age_estimator.ipynb
    ```
3. Note about the comfiguration to run the benchmark

The age prediction functionality in the SDK is built to be tailored according to the user needs. 
User can select a precise way validate a face before predicting its age via the configuration object.
For this benchmark we use he following configuration:

```python
# Create FaceFactor config 
config_param = {
    PARAMETERS.INPUT_IMAGE_FORMAT: "rgb",
    PARAMETERS.CONTEXT_STRING: "predict",
    # Relax the face validation settings to allow
    # all faces to be predicted
    PARAMETERS.ESTIMATE_AGE_FACE_VALIDATIONS_OFF: True
}
```


