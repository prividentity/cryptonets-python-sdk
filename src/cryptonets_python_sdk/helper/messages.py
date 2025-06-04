class Message:
    def __init__(self):
        self.MISSING_ARGUMENT = "Missing argument: {}"
        self.INVALID_ARGUMENT = "Invalid argument: {}"
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
            -2: "Too many faces detected.",
            -1: "Invalid image, No face detected in the image.",
            0: "Valid face.",
            3: "Face too close to the camera. Please move back.",
            4: "Face too far from the camera.",
            5: "Face too close to the right edge of the frame.",
            6: "Face too close to the left edge of the frame.",
            7: "Face too close to the top edge of the frame.",
            8: "Face too close to the bottom edge of the frame.",
            9: "Face is too blurry.",
            10: "Eyeglasses detected.",
            11: "Facemask detected.",
            12: "Chin positioned too far to the left.",
            13: "Chin positioned too far to the right.",
            14: "Chin positioned too far up.",
            15: "Chin positioned too far down.",
            16: "Image too dim. Please increase lighting.",
            17: "Image too bright. Please reduce lighting.",
            18: "Face detection confidence too low.",
            19: "Invalid face background. Please ensure a plain background.",
            20: "Eyes are closed. Please open your eyes.",
            21: "Mouth is open. Please close your mouth.",
            22: "Face tilted too far to the right.",
            23: "Face tilted too far to the left.",
            24: "The face is wearing eyeglasses and a face mask at the same time.",
            25: "The face is not in the anti-spoof recommended position (target oval).",
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
        return self.APP_MESSAGES.get(code,"Something went wrong!")
