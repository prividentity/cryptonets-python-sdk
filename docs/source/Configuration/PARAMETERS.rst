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
   * - CONF_SCORE_THR_ENROLL
     - Threshold to reject a face if the crop confidence score is lesser than this value - enroll
     - -0.1 to 2
     - Default is 0.2
   * - CONF_SCORE_THR_PREDICT
     - Threshold to reject a face if the crop confidence score is lesser than this value - predict
     - -0.1 to 2
     - Default is 0.2
   * - MIN_DOCUMENT_BORDER
     - Minimum border (in pixels) to be added when padding. typically used for document along with image border
     - 0 to 10% of image size in pixel
   * - SEND_ORIGINAL_IMAGES
     - Get the original images from the server. Default false
     - True, False
   * - ESTIMATE_AGE_FACE_VALIDATIONS_OFF
     - `False`` by default, If set `True`, disables the face validation in the age estimation method, the method will return an age estimation unless no face is detected.
     - True, False   
   * - COLLECTION_NAME 
     - Collection name to be used for the operation: possible values are `default`, `RES100``and `RES200`. Each collection is tied a sepcfic enmbeddings, you can't predict a face that was enrolled with different collection, so you need to specify the name of the collection you are targetting. if you leave it empty, the `default`` collection will be used.
     - `default`, `RES100``and `RES200`.     
   * - RELAX_FACE_VALIDATION
     - `False` by default, if set to `True`, the face validation step in any operation is going to be permissive. 
     - True, False     
   * - USE_AGE_ESTIMATION_WITH_MODEL_STDD
     - `False` by default, if set to `True`, the age estimation will produce a standard deviation of the age estimation based on the model data
     - True, False
   * - USER_IDENTIFIER
     - A string  representing a supplmentary user identifier, to be added in `enroll`` requests if your enroll workflow needs it. 
     - Any string.
   * - FACE_THRESHOLD
     - Threshold for compare operation. If the calculated distance between 2 faces is strictly less than this value, the faces are considered similar.
     - Default value is 1.0 which suitable for most collections (i.e enmbeddings models) , values are  0 to 2
   * - DISABLE_AGE_ESTIMATION_ANTISPOOF
     - By default set to `True`. If set to `False`, the age estimation will not perform any anti-spoofing checks. 
     - True, False
   * - CONSIDER_BIGGEST_FACE
     - By default set to `False`. If set to `True`, the age estimation will consider only the biggest face in the image. if this option is set to true and the `SINGLE_FACE_VALIDATION_RESULT` or `SINGLE_FACE_AGE_RESULT` (depending on the operation) is not set to `True`  a config error will be returned.
     - True, False
   * - SINGLE_FACE_VALIDATION_RESULT
     - By default set to `False`. If set to `True`, the age estimation will return a single face validation result instead of a list.
     - True, False
   * - SINGLE_FACE_AGE_RESULT
     - By default set to `False`. If set to `True`, the age estimation will return a single face age result instead of a list.
     - True, False
   * - AGE_FACE_LANDMARK_MODEL_ID
     - This is a model ID value. Use this parameter to the  face landmark model used in age estimation operation. The only possible values are : 6 , 18 and 21.
     - 0 to 1000
