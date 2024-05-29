class Message:
    def __init__(self):
        self.IS_VALID_ERROR = "Unknown error while validating the image"
        self.AGE_ESTIMATE_ERROR = "Unknown error while predicting the age."
        self.EXCEPTION_ERROR_ENROLL = "Something went wrong while doing enroll."
        self.EXCEPTION_ERROR_GET_ISO_FACE = "ISO face validation failed."
        self.EXCEPTION_ERROR_PREDICT = "Something went wrong while doing predict."
        self.EXCEPTION_ERROR_DELETE = "Something went wrong while doing delete."
        self.EXCEPTION_ERROR_COMPARE = "Something went wrong while doing compare."
        self.EXCEPTION_ERROR_ANTISPOOF_CHECK = "Something went wrong while doing antispoof."
        self.ENROLL_PROCESSED = (
            "Enroll request successfully processed, Waiting for server response."
        )
        self.PREDICT_PROCESSED = (
            "Predict request successfully processed, Waiting for server response."
        )

        self.APP_MESSAGES = {
            -100:"	Error occurred during the antispoofing.",
             -6: "Antispoofing detection was not performed and was skipped.",
            -5: "A grayscale image has been detected, which may indicate a spoof attempt.",
            -4: "Invalid face detected, unable to apply antispoofing procedures.",
            -3: "Face too close to the edge; please center your face in the image.",
            -2: "Mobile phone detected in the vicinity, which may indicate a spoof attempt.",
             -1: "Invalid image, No face detected in the image.",
            0: "Valid face.",
            1: "Error Description: Image spoof detected. Please provide a live facial image.",
            2: "Error Description: Video spoof detected. Please provide a live facial image.",
            3: "Error Description: Face too close to the camera. Please move back.",
            4: "Error Description: Face too far from the camera.",
            5: "Error Description: Face too close to the right edge of the frame.",
            6: "Error Description: Face too close to the left edge of the frame.",
            7: "Error Description: Face too close to the top edge of the frame.",
            8: "Error Description: Face too close to the bottom edge of the frame.",
            9: "Error Description: Face is too blurry.",
            10: "Error Description: Eyeglasses detected.",
            11: "Error Description: Facemask detected.",
            12: "Error Description: Chin positioned too far to the left.",
            13: "Error Description: Chin positioned too far to the right.",
            14: "Error Description: Chin positioned too far up.",
            15: "Error Description: Chin positioned too far down.",
            16: "Error Description: Image too dim. Please increase lighting.",
            17: "Error Description: Image too bright. Please reduce lighting.",
            18: "Error Description: Face detection confidence too low.",
            19: "Error Description: Invalid face background. Please ensure a plain background.",
            20: "Error Description: Eyes are closed. Please open your eyes.",
            21: "Error Description: Mouth is open. Please close your mouth.",
            22: "Error Description: Face tilted too far to the right.",
            23: "Error Description: Face tilted too far to the left.",
            100: "Successfully registered",
            101: "Error Description: Image file does not exist.",
            102: "Error Description: Input image quality is low.",
            103: "Error Description: There is an error in endpoint.",
            104: "Factor object successfully created.",
            105: "Error Description: Something went wrong while initializing.",
            106: self.IS_VALID_ERROR,
            107: self.EXCEPTION_ERROR_ENROLL,
            108: self.EXCEPTION_ERROR_PREDICT,
            109: "Error Description: Incorrect Usage.",
        }

    def get_message(self, code):
        return self.APP_MESSAGES.get(code,"Something went wrong!")
