Changelog
=========

Version 1.3.8 (2025-02-25)
--------------------------

Updates:

* Add new configuration parameter `ESTIMATE_AGE_FACE_VALIDATIONS_OFF` hat affect teh age prediction method.
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


=========
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