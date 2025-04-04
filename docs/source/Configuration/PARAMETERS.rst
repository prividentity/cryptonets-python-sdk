==========
PARAMETERS
==========

.. module:: cryptonets_python_sdk.settings.configuration
    :noindex:

This section covers the valid values for setting up additional configurations pertaining to face factor.

.. autoclass:: PARAMETERS
    :members: OFF

.. _param_list:

Configurable Parameter List and Valid values
--------------------------------------------

.. list-table::
   :widths: 25 50 25
   :header-rows: 1

   * - Name
     - Description
     - Valid Values
   * - K
     - Defines the maximum number of nearest neighbors to return for a prediction. If the number of reasonable matches is less than the requested k, only the available reasonable matches are returned. When K=1 or not specified, a single EnrollPredictResult is returned instead of a list of EnrollPredictResult object.
     - 1 to 100 Default Value is 1
   * - INPUT_IMAGE_FORMAT
     - Input image format and byte arrangement.
     - "rgb", "rgba", "bgr"
   * - CONTEXT_STRING
     - Context for computation call. Not applicable for session.
     - "enroll", "predict" (Only allowed for each operation)
   * - CONF_FAST_PROCESS
     - Enable fast search mode. Typically enabled for realtime camera processing.
     - True, False
   * - INPUT_TYPE
     - Input type of the image sent (Under Development)
     - "face", "document-id", "document-barcode"
   * - FACE_THRESHOLDS_REM_BAD_EMB
     - Threshold for geometric distance based embedding removal.
     - 0, 1, 2
   * - BLUR_THRESHOLD_ENROLL_PRED
     - Threshold for blur based image rejection for face. Checked on cropped image.
     - 0 to 10000
   * - THRESHOLD_PROFILE_ENROLL
     - Threshold for rejecting a (horizontal) profile image - enroll context
     - -0.1 to 2
   * - THRESHOLD_PROFILE_PREDICT
     - Threshold for rejecting a (horizontal) profile image - predict context
     - -0.1 to 2
   * - THRESHOLD_VERTICAL_ENROLL
     - Threshold for rejecting a vertical profile image - enroll context
     - -0.1 to 2
   * - THRESHOLD_VERTICAL_PREDICT
     - Threshold for rejecting a vertical profile image - predict context
     - -0.1 to 2
   * - THRESHOLD_USER_RIGHT
     - Threshold to reject a face if the user face is more aligned sideways - right
     - -0.1 to 2
   * - THRESHOLD_USER_LEFT
     - Threshold to reject a face if the user face is more aligned sideways - left
     - -0.1 to 2
   * - THRESHOLD_USER_TOO_FAR
     - Threshold to reject a face if the user face is too far
     - -0.1 to 2
   * - THRESHOLD_USER_TOO_CLOSE
     - Threshold to reject a face if the user face is too close
     - -0.1 to 2
   * - IMAGE_BORDER
     - Border ( as % of size) to be set while padding. Typically needed for document id
     - 0 to 0.1
   * - IMAGE_PRE_PROC
     - Enable additional image processing prior to validity check / cropping
     - "zoom_pan", "rotate90", "rotate180", "rotate270", "blur", "fliplr", "none"
   * - THRESHOLD_GLASS
     - Threshold to detect glass (eye wear)
     - -0.1 to 2
   * - THRESHOLD_MASK
     - Threshold to detect mask on a face
     - -0.1 to 2
   * - ENROLL_ALLOW_EYE_GLASS
     - Allow eyeglasses for enroll if within threshold
     - True, False
   * - CONF_SCORE_THR_ENROLL
     - Threshold to reject a face if the crop confidence score is lesser than this value - enroll
     - -0.1 to 2
   * - CONF_SCORE_THR_PREDICT
     - Threshold to reject a face if the crop confidence score is lesser than this value - predict
     - -0.1 to 2
   * - BLUR_THRESHOLD_DOC_LEVEL_1
     - Threshold for blur based image rejection for document type - 1st level checking. full document
     - 0 to 10000
   * - BLUR_THRESHOLD_DOC_LEVEL_2
     - Threshold for blur based image rejection for document type - 2nd level checking. extracted face.
     - 0 to 10000
   * - DOCUMENT_FACE_CHECK_VALIDITY
     - Enable cropped face validity check as part of document id verification
     - True, False
   * - DOCUMENT_CHECK_VALIDITY
     - Enable cropped document validity check as part of document id verification
     - True, False
   * - DOCUMENT_FACE_PREDICT
     - Enable prediction using cropped face image as part of document id verification
     - True, False
   * - MIN_DOCUMENT_BORDER
     - Minimum border (in pixels) to be added when padding. typically used for document along with image border
     - 0 to 10% of image size in pixel
   * - FACE_DETECT_PREFERRED_SIZE
     - Preferred size of the cropped face image. typically used during face extraction from image with multiple faces
     - 448
   * - SEND_ORIGINAL_IMAGES
     - Get the original images from the server. Default false
     - True, False
   * - COMPARE_RESERVATION_CALLS
     - Number of calls to be set for compare in billing reservation.
     - 0 to 100000000
   * - ESTIMATE_AGE_RESERVATION_CALLS
     - Number of calls to be set for estimate age in billing reservation.
     - 0 to 100000000
   * - FACE_ISO_RESERVATION_CALLS
     - Number of calls to be set for face ISO in billing reservation.
     - 0 to 100000000
   * - ESTIMATE_AGE_FACE_VALIDATIONS_OFF
     - `False`` by default, If set `True`, disables the face validation in the age estimation method, the method will return an age estimation unless no face is detected.
     - True, False
   * - COLLECTION_NAME
     - Collection name to be used for the operation: possible values are `default`, `RES100``and `RES200`. Each collection is tied a sepcfic enmbeddings, you can't predict a face that was enrolled with different collection, so you need to specify the name of the collection you are targetting. if you leave it empty, the `default`` collection will be used.
     - `default`, `RES100``and `RES200`.     
   * - RELAX_FACE_VALIDATION
     - `False` by default, if set to `True`, the face validation step in any operation is going to be permissive. 
     - True, False
