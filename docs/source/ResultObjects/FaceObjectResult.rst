================
FaceObjectResult
================

.. module:: cryptonets_python_sdk.helper.result_objects.faceObjectResult
    :noindex:

This section covers how to use the Face Object Result Object.

Check :ref:`return codes <return_codes>` for all possible result codes and its status

.. autoclass:: FaceObjectResult
   :members: return_code, message, age, bounding_box

.. toctree::
   :maxdepth: 2

   Utils

.. _return_codes:

Return Codes for is valid and Error Messages
--------------------------------------------

.. list-table::
   :widths: 25 50
   :header-rows: 1

   * - Return Code
     - Return Message /  Error Description
   * - -100
     - InvalidImage
   * - -1
     - NoFace
   * - 0
     - Valid Biometric
   * - 1
     - Face is an image of an image (spoof). Please only provide live facial image(s). (Under implementation)
   * - 2
     - Face is an image of a video (spoof). Please only provide live facial image(s). (Under implementation)
   * - 3
     - Face in image is too close to the camera. Please move away from the camera.
   * - 4
     - Face in image is too far away.
   * - 5
     - Face in image is too far to the right.
   * - 6
     - Face in image is too far to the left.
   * - 7
     - Face in image is too high.
   * - 8
     - Face in image is too low.
   * - 9
     - Face in image is too blurry.
   * - 10
     - Please remove eyeglasses during registration.
   * - 11
     - Please remove face mask  during registration.
   * - 12
     - Head in image turned too far towards the left. Please face the camera.
   * - 13
     - Head in image turned too far towards the right. Please face the camera.
   * - 14
     - Head in image turned too far up. Please face the camera.
   * - 15
     - Head in image turned too far down. Please face the camera.
   * - 16
     - Exposure too dark. Low Light Condition
   * - 17
     - Exposure too bright. Bright Light Condition
   * - 18
     - Face detection Confidence low. Adjust spatial resolution
   * - 19
     - Invalid face background. Too noisy to capture face
   * - 20
     - Eye blink detected.
   * - 21
     - Mouth open detected.
