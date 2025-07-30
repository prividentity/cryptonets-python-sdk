Changelog
=========

Version 1.3.19 (2025-07-28)
-----------------------------

Updates:

* Add configuration parameter `AGE_FACE_LANDMARK_MODEL_ID`: This is a model ID value. Use this parameter to the  face landmark model used in age estimation operation. The only possible values are : 6 , 18 and 21.
* The native library points to '25.07.21-542b11e'.

Version 1.3.18 (2025-07-21)
-----------------------------

Updates:

* Fix bug exception : `TypeError: AgeEstimateResult.__init__() got an unexpected keyword argument 'message'` in `estimate_age` method.
* Add configuration parameter `CONSIDER_BIGGEST_FACE` to change the default behaviour of the face detection.
* Add configuration parameter `SINGLE_FACE_VALIDATION_RESULT` to change the default behaviour of the face validation result.
* Add configuration parameter `SINGLE_FACE_AGE_RESULT` to change the default behaviour of the age estimation result.
* The native library points to '25.07.21-542b11e'.


Version 1.3.17 (2025-07-04)
-----------------------------

Updates:

* Add new field to the result object `AgeEstimateResult` to return the antispoofing status. See `ANTISPOOFING_STATUSES` for possible values. 
* The antispoof pass is not enabled by default. You need to set the new configuration parameter `DISABLE_AGE_ESTIMATION_ANTISPOOF` to False (default value is `True`) to enable it.
* The native library points to '25.07.04-b9c50c6'.


Version 1.3.16 (2025-06-18)
-----------------------------

Updates:

* Update message returned in `estimate_age` to include all detected face traits `issue <https://github.com/prividentity/cryptonets-python-sdk/issues/39>`_.
* Add new result object `AgeEstimateResult` to to be used as distinct return type for `estimate_age` operations.
* The native library points to '25.06.18-d1a2cf0'.

Version 1.3.15 (2025-06-12)
-----------------------------

Updates:

* Update message returned in `estimate_age` to be non prompting `issue <https://github.com/prividentity/cryptonets-python-sdk/issues/37>`_.
* Native library change: Enhancement of `estimate age with stddev` returned stddev. 
* Native library change: In `estimate age` full face  analysis is done and therefore more possible face statuses can be returned (eye glasses, face mask, blurriness status). 
* Enhance eyes and mouth statuses detection.
* The native library points to '25.06.12-f293068'.


Version 1.3.14 (2025-06-04)
-----------------------------

Updates:

* Solve  `issue <https://github.com/prividentity/cryptonets-python-sdk/issues/32>`_. 
* Implement  `issue <https://github.com/prividentity/cryptonets-python-sdk/issues/34>`_.
* Update Updates to face validation error codes to align with the native library status codes.
* Updated the error messages in messages.py to reflect the new error codes and removed unused messages for image and video spoofing.
* Age Estimation calls now return a message for face validation even if face validation is relaxed with the parameter: `ESTIMATE_AGE_FACE_VALIDATIONS_OFF`.
* The native library points to '25.06.04-21817a7'.


Version 1.3.13 (2025-05-23)
-----------------------------

Updates:

* Solve  `issue <https://github.com/prividentity/cryptonets-python-sdk/issues/30>`_. 
* Update the semantics and structure of result object `FaceCompareResult`. 
* The methods `compare` and `compare_doc_with_face` will return the a single `distance` float value. `distance_min/mean|max` are removed.
* Update the `compare` and `compare_doc_with_face` methods to return the new `FaceCompareResult` object.
* Update the configuration parameter `FACE_THRESHOLD`.
* Update default value for `FACE_THRESHOLD` to suit the 3 current embeddings types `1.0`.
* Remove field legacy `token` from `FaceEnrollPredictResult`.
* Update docs & samples `FaceCompareResult`  `issue <https://github.com/prividentity/cryptonets-python-sdk/issues/30>`_  
* The native library still points to '25.05.07-6491ced'.


Version 1.3.12 (2025-05-07)
-----------------------------

Updates:

* Remove all obsolete configuration parameters :
 - CONF_FAST_PROCESS
 - INPUT_TYPE
 - BLUR_THRESHOLD_DOC_LEVEL_1
 - BLUR_THRESHOLD_DOC_LEVEL_2
 - THRESHOLD_VERTICAL_ENROLL
 - THRESHOLD_VERTICAL_PREDICT
 - IMAGE_BORDER
 - IMAGE_PRE_PROC
 - THRESHOLD_GLASS
 - THRESHOLD_MASK
 - FACE_THRESHOLD_RIGHT
 - FACE_THRESHOLD_LEFT
 - FACE_THRESHOLD_VERTICAL
 - DOCUMENT_FACE_CHECK_VALIDITY
 - DOCUMENT_CHECK_VALIDITY
 - DOCUMENT_FACE_PREDICT
 - ENABLE_DOC_PERSPECTIVE_CORRECTION
 - ENROLL_ALLOW_EYE_GLASS
 - FACE_DETECT_PREFERRED_SIZE
 - FACE_DETECT_MAX_OUT_IMAGE_SIZE

* Remove billing methods and related parameters.
* Remove obsolete caching functionality.
* Remove obsolete `tf_num_thread` FaceFactor constructor argument.
* Remove obsolete tests. A new set of tests will be added in the coming version 2.0.0.
* Change the binaries download location to be versioned, where each version download binaries from its own directory. The models download location is not chanegd and and they are shared by all versions. 
* Fix various potential memory leaks and bugs and improve some parts of the code base.
* Fix a bug in compare that discards the collection_name parameter.
* Fix bug occurring in some FaceFactor methods when config is not set.
* Fix and upgrade `face_iso` method.
* Add a complete set of basic samples of all methods under samples folder.
* Expose `delete` method to the `Facefactor` interface.
* Remove obsolete `code`` field from `FaceEnrollPredictResult`.
* Add a convinience `print` method to th class `FaceEnrollPredictResult`.
* Update documentation notable the  AdvancedUsage samples and make it more complete and uptodate.
* Update native library to '25.05.07-6491ced'.


Version 1.3.12b1 (2025-04-23)
-----------------------------

Updates:

* Add new configuration parameter `USE_AGE_ESTIMATION_WITH_MODEL_STDD` that affect the age prediction method.
  The parameter have the value `False` by default.
  If `USE_AGE_ESTIMATION_WITH_MODEL_STDD` set to `True`, it will return a standard deviation of the age estimation based on the model data.
* Remove obsolete configuration parameters `THRESHOLD_GLASS`, `THRESHOLD_MASK` and `ENROLL_ALLOW_EYE_GLASS`
* Remove `billing failed` log message in age operation.
* Update native library to '25.04.23-9b772ba'

Version 1.3.11 (2025-04-04)
-----------------------------

Updates:

* Backend updates to improve performance and stability.

Version 1.3.11b4 (2025-03-24)
-----------------------------

Updates:

* Add 3 properties to the class FaceEnrollPredictResult.
* Add  RELAX_FACE_VALIDATION config parameter.

Version 1.3.11b2 (2025-03-11)
-----------------------------

Updates:

* This a beta version which replace the old model selection with the following 3 collections : `default`, `RES100` and `RES200` which correponds to different embedding models. The collection name is passed through the configuration parameter `COLLECTION_NAME` in the `ConfigObject` class of each each operation. The default collection is `default`. When using `RES100` or `RES200`  the model will be downloaded and cacehd on disk.
* Various fixes.

Version 1.3.10 (2025-02-27)
----------------------------

Updates:

* Fix a memory leak in enroll method.

Version 1.3.9 (2025-02-25)
--------------------------

Updates:

* Add new configuration parameter `ESTIMATE_AGE_FACE_VALIDATIONS_OFF` that affect the age prediction method.
  The parameter have the value `False` by default.
  If `ESTIMATE_AGE_FACE_VALIDATIONS_OFF` set to `True`, it will disable the face validation step in the age
  estimation method and the method will return an age estimation unless no face is detected.
* Documentation and content update.


Version 1.3.8 (2024-11-05)
--------------------------

Documentation and content update

Version 1.3.7 (2024-10-29)
--------------------------

Bug Fixes:

* Resolved bugs in the estimate_age function.

Version 1.3.6 (2024-10-09)
--------------------------

Bug Fixes:

* Added image dimension checks to ensure that all images processed are greater than 224x224 pixels. 


Version 1.3.5 (2024-09-16)
--------------------------

Bug Fixes:

* Resolved issues in the isValid function, which now correctly returns all detected faces along with their bounding boxes.


Version 1.3.3 (2024-05-29)
--------------------------

New Features:

* Added anti-spoofing check support to enhance security and verify the authenticity of user-provided facial images.

Updates:

* Updated document models to improve accuracy and performance in document processing tasks.


Version 1.3.1 (2024-05-15)
--------------------------

New Features:

* ARM-64 Processor Support
* Added DOCUMENT_AUTO_ROTATION parameter for document image rotation

Version 1.3.0 (2024-05-08)
--------------------------

Improvements:

* Updated models to enhance accuracy and performance.
* Improved 'compare', 'predict' and 'enroll' functionalities for more precise predictions.

Version 1.2.3 (2024-04-24)
--------------------------

Improvements:

* Removed unnecessary error logs to streamline application performance.
* Improved validation messages to enhance user experience and error handling.
* Added support for macOS, extending compatibility across more operating systems.

Enhancements:

* Integrated scoring within the `predict` call to provide immediate performance metrics.


Version 1.2.0 (2024-04-08)
--------------------------

New Features:

* Added `compare_doc_with_face` function to compare a face image against a document image, enhancing the SDK’s capabilities in verifying identities by comparing images from different sources.
* Introduced a new `K` parameter in the `predict` function to allow customization of the number of top results returned, offering more flexibility in handling face recognition results.

Improvements:

* Enhanced the comparison algorithm in the existing compare functionality to improve accuracy and efficiency in face matching scenarios.

Version 1.1.5 (2023-11-23)
---------------------------

Bug Fixes and Improvements:

* Default configuration thresholds updated.
* Documentation updated to the latest version of cryptonets python sdk.


Version 1.1.4 (2023-11-21)
---------------------------

Enhancements and New Features:

* Integration of an improved embeddings model to enhance accuracy in various scenarios.
* Implementation of more robust validation models to ensure higher reliability and precision.
* Fixed a critical memory leak issue that impacted system performance and stability.

Version 1.1.3 (2023-03-23)
---------------------------

Bug Fixes and Improvements:

* Strict Face thresholds for avoiding False Positives
* Image aspect ratio bug fix for age estimation
* Performance improvements on compare call
* Billing default thresholds update
* SO library memory footprint improvements

New Features:

* Exposure detection on face recognition
* Face expression detection: Eye blink / Mouth open
* Mouth Bug Fixes and Improvements:
* Improvements on face detection under various conditions
* Improved Face selection thresholds

Version 1.1.2 (2023-02-11)
---------------------------

* The new thresholds for enroll (face too far and head rotation)
* The age estimation function now uses enroll thresholds
* The eyeglasses work for age estimation after zoom

Version 1.1.0 (2023-02-07)
---------------------------

Major release:

* Added Windows Support for the SDK

Version 1.0.15 (2023-02-01)
---------------------------

Bug Fixes and Improvements:

* Improvements on face detection under various conditions
* Improved Face selection thresholds

New Features:

* Billing reservation call parameters

Version 1.0.14 (2023-01-20)
---------------------------

Bug Fixes and Improvements:

* Age Estimation on small resolution images
* ISO image improvements for various conditions
* Bug fixes and Improvements for image capture aspect ratio

New Features:

* Cache Type optional parameter

Version 1.0.12 (2023-01-13)
---------------------------

Enhancements:

* New function to get the ISO of the face image
* Bug fixes and Improvements for memory allocation

Version 1.0.11 (2023-01-10)
---------------------------

Enhancements:

* Introduction of new environment variable for tensorflow thread
* Improvements on best face selection with face recognition model
* Bug fixes for empty configuration object and URL usage
* New parameter update for getting original images (BETA)

Version 1.0.10 (2022-12-14)
---------------------------

Enhancements:

* Introduction of ConfigObject class and PARAMETERS
* Configuration context setting for additional parameters
* Session and local configuration setting
* Bug fixes and improvements

Version 1.0.9 (2022-12-07)
--------------------------

Enhancements:

* Returns bounding boxes for is valid and age estimation
* Environment variables support for API Key and Server URL

Version 1.0.8 (2022-12-07)
--------------------------

* Bug Fixes and improvements

Version 1.0.7 (2022-12-02)
--------------------------

* Bug Fixes for enroll / predict
* New library update
* Documentation usage update with images as example

Version 1.0.6 (2022-12-02)
--------------------------

* Bug fixes and improvements

Version 1.0.5 (2022-12-01)
--------------------------

* Library update
* Edge cases status code mappings
* Multi Face Support integrated for isValid and Age estimate
* Documentation update for multi face images

Version 1.0.4 (2022-11-25)
--------------------------

* Documentation setup and build
* Test file update
* New library file update with improved memory management
* Updated Readme Content
* Updated status code changes
* License update

Version 1.0.3 (2022-11-25)
--------------------------

* Bug fixes and improvements

Version 1.0.2 (2022-11-25)
--------------------------

* Bug fixes and improvements1

Version 1.0.1 (2022-11-24)
--------------------------

* First release