from cryptonets_python_sdk.settings.configuration import FACE_VALIDATION_STATUSES


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

        self.NON_PROMPTING_FACE_STATUS_MESSAGES = {
            FACE_VALIDATION_STATUSES.FV_OK:                    "Face validation is successful.",
            FACE_VALIDATION_STATUSES.FV_ERR:                "Error occurred during face validation.",
            FACE_VALIDATION_STATUSES.FV_MANY_FACES_DETECTED:  "Too many faces detected in the image.",
            FACE_VALIDATION_STATUSES.FV_FACE_NOT_DETECTED:    "Face not detected in the image.",
            FACE_VALIDATION_STATUSES.FV_FACE_TOO_CLOSE:        "Face is too close to the camera.",
            FACE_VALIDATION_STATUSES.FV_FACE_TOO_FAR:          "Face is too far from the camera.",
            FACE_VALIDATION_STATUSES.FV_FACE_RIGHT:            "Face is turned to the right.",
            FACE_VALIDATION_STATUSES.FV_FACE_LEFT:             "Face is turned to the left.",
            FACE_VALIDATION_STATUSES.FV_FACE_UP:               "Face is turned upwards.",
            FACE_VALIDATION_STATUSES.FV_FACE_DOWN:             "Face is turned downwards.",
            FACE_VALIDATION_STATUSES.FV_IMAGE_BLURR:           "Image is blurred.",
            FACE_VALIDATION_STATUSES.FV_FACE_WITH_GLASS:      "Face is wearing glasses.",
            FACE_VALIDATION_STATUSES.FV_FACE_WITH_MASK:       "Face is wearing a mask.",
            FACE_VALIDATION_STATUSES.FV_LOOKING_LEFT:         "Face is looking to the left.",
            FACE_VALIDATION_STATUSES.FV_LOOKING_RIGHT:        "Face is looking to the right.",
            FACE_VALIDATION_STATUSES.FV_LOOKING_HIGH:         "Face is looking upwards.",
            FACE_VALIDATION_STATUSES.FV_LOOKING_DOWN:         "Face is looking downwards.",
            FACE_VALIDATION_STATUSES.FV_FACE_TOO_DARK:        "Face is too dark.",
            FACE_VALIDATION_STATUSES.FV_FACE_TOO_BRIGHT:      "Face is too bright.",
            FACE_VALIDATION_STATUSES.FV_FACE_LOW_VAL_CONF:    "Low confidence in face validation.",
            FACE_VALIDATION_STATUSES.FV_INVALID_FACE_BACKGROUND:   "Invalid face background.",
            FACE_VALIDATION_STATUSES.FV_EYE_BLINK:            "Eye blink detected.",
            FACE_VALIDATION_STATUSES.FV_MOUTH_OPENED:         "Mouth opened detected.",
            FACE_VALIDATION_STATUSES.FV_FACE_ROTATED_RIGHT:   "Face is rotated to the right.",
            FACE_VALIDATION_STATUSES.FV_FACE_ROTATED_LEFT:    "Face is rotated to the left.",
            FACE_VALIDATION_STATUSES.FV_FACE_WITH_EYEGLASSES_AND_FACEMASK:  "The face is wearing eyeglasses and a face mask at the same time.",
            FACE_VALIDATION_STATUSES.FV_FACE_NOT_IN_OVAL:     "The face is not in the anti-spoof recommended position (target oval).",
        }



    def get_message(self, code, prompting_message:bool = True):
        if prompting_message:
            return self.APP_MESSAGES.get(code,"Something went wrong!")
        else:
            # Allow lookup by integer value as well as enum
            if code in self.NON_PROMPTING_FACE_STATUS_MESSAGES:
                return self.NON_PROMPTING_FACE_STATUS_MESSAGES[code]
            # Try to match by integer value of enum
            for k, v in self.NON_PROMPTING_FACE_STATUS_MESSAGES.items():
                if hasattr(k, 'value') and k.value == code:
                    return v
            return "Something went wrong!"