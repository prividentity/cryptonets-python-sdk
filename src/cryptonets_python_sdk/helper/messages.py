class Message:
    def __init__(self):
        self.IS_VALID_ERROR = "Unknown error while validating the image"
        self.AGE_ESTIMATE_ERROR = "Unknown error while predicting the age."
        self.EXCEPTION_ERROR_ENROLL = "Something went wrong while doing enroll."
        self.EXCEPTION_ERROR_GET_ISO_FACE = "ISO face validation failed."
        self.EXCEPTION_ERROR_PREDICT = "Something went wrong while doing predict."
        self.EXCEPTION_ERROR_DELETE = "Something went wrong while doing delete."
        self.EXCEPTION_ERROR_COMPARE = "Something went wrong while doing compare."
        self.ENROLL_PROCESSED = "Enroll request successfully processed, Waiting for server response."
        self.PREDICT_PROCESSED = "Predict request successfully processed, Waiting for server response."

        self.APP_MESSAGES = {
            0: "Valid Image",
            1: "Error Description: Face is an image of an image (spoof). Please only provide live facial image(s).",
            2: "Error Description: Face is an image of a video (spoof). Please only provide live facial image(s).",
            3: "Error Description: Face in image is too close to the camera. Please move away from the camera.",
            4: "Error Description: Face in image is too far away.",
            5: "Error Description: Face in image is too far to the right.",
            6: "Error Description: Face in image is too far to the left.",
            7: "Error Description: Face in image is too high.",
            8: "Error Description: Face in image is too low.",
            9: "Error Description: Face in image is too blurry.",
            10: "Error Description: Please remove eyeglasses during registration.",
            11: "Error Description:  Please remove face mask  during registration. ",
            12: "Head in image turned too far toward the left/right. Please face the camera",
            13: "Head in image turned too far toward the up/down. Please face the camera",
            14: "UNUSED ERROR CODE",
            15: "UNUSED ERROR CODE",
            16: "Error Description: No face found in image.",
            17: "Error Description: API Error",
            18:	"Error Description: Local Storage Error",
            19: "Error Description: Memory Error",
            100: "Successfully registered",
            101: "Error Description: Image file does not exist.",
            102: "Error Description: Input image quality is low.",
            103: "Error Description: There is an error in endpoint.",
            104: "Factor object successfully created.",
            105: "Error Description: Something went wrong while initializing.",
            106: self.IS_VALID_ERROR,
            107: self.EXCEPTION_ERROR_ENROLL,
            108: self.EXCEPTION_ERROR_PREDICT,
            109: "Error Description: Incorrect Usage."
        }

    def get_message(self, code):
        return self.APP_MESSAGES[code]
