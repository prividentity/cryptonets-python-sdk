Usage
=====


Python Version
--------------

We recommend using the latest version of Python. PrivateID supports
Python 3.6 and newer.


Install Cryptonets SDK
----------------------

.. code-block:: sh

    pip3 install cryptonets_python_sdk

Import and Usage
----------------

.. code-block:: py

    # Import the cryptonets sdk class
    from cryptonets_python_sdk.factor import FaceFactor

    # Replace with the provided server URL
    server_url = "https://sample.url.domain"

    # Replace with your API key
    api_key = "your-api-key"

    # Create a Face factor class instance
    face_factor = FaceFactor(server_url = server_url, api_key = api_key)

Check Validity of the image
----------------------------
| Replies in 50ms
| Operates locally, does not call server
| Acceptable head rotation: -22.5 to 22.5 degrees 
| Pose: uncontrolled, does not accept profile images

.. image:: images/isvalid_example.png
   :width: 600
.. code-block:: py

    # Check if the image is valid

    is_valid_handle = face_factor.is_valid(image_path = "path_to_the_image") ## Replace with the path to the image

Output:

.. code-block:: py

    is_valid_handle.error # Error code of the operation
    is_valid_handle.message # Message of the operation
    is_valid_handle.face_objects # List of Face objects with results

Example:

.. image:: images/test.jpeg
   :width: 400
.. code-block:: py

   	#Create a Face factor class instance
	face_factor = FaceFactor(server_url=SERVER_URL, api_key=api_key)
	
	is_valid_handle = face_factor.is_valid(image_path=img_path)
	for index, face in enumerate(is_valid_handle.face_objects):
            print("Face#:{}\nReturn Code:{}\nMessage:{}\nBBox TL:{}\nBBox BR:{}\n".format(index + 1,face.return_code,face.message,face.bounding_box.top_left_coordinate.__str__(), face.bounding_box.bottom_right_coordinate.__str__()))  
        
Output:

.. code-block:: py

	Face#:1
	Return Code:0
	Message:ValidBiometric
	BBox TL:Point(257.5,151.0)
	BBox BR:Point(430.5,313.0)

	Face#:2
	Return Code:0
	Message:ValidBiometric
	BBox TL:Point(130.0,45.5)
	BBox BR:Point(290.0,212.5)

	
Check Age of the image	
----------------------------
| Replies in 50ms
| Operates locally, does not call server
| Acceptable head rotation: -22.5 to 22.5 degrees 
| Pose: uncontrolled, does not accept profile images

.. image:: images/age_example.png
   :width: 600
   
.. code-block:: py

    # Estimate age of the image

    age_handle = face_factor.estimate_age(image_path = "path_to_the_image") ## Replace with the path to the image

Output:

.. code-block:: py

    age_handle.error # Error code of the operation
    age_handle.message # Message of the operation
    age_handle.face_objects # List of Face objects with results
    
Example:

.. image:: images/test.jpeg
   :width: 400
.. code-block:: py

   	#Create a Face factor class instance
	face_factor = FaceFactor(server_url=SERVER_URL, api_key=api_key)
	
	age_handle = face_factor.estimate_age(image_path=img_path)
	for index, face in enumerate(age_handle.face_objects):
    		print("Face#:{}\nReturn Code:{}\nMessage:{}\nAge:{}\nBBox TL:{}\nBBox BR:{}\n".format(index + 1,face.return_code,face.message,face.age,face.bounding_box.top_left_coordinate.__str__(),face.bounding_box.bottom_right_coordinate.__str__())) 
        
Output:

.. code-block:: py

	Face#:1
	Return Code:0
	Message:ValidBiometric
	Age:29.490659713745117
	BBox TL:Point(257.5,151.0)
	BBox BR:Point(430.5,313.0)

	Face#:2
	Return Code:0
	Message:ValidBiometric
	Age:20.64322280883789
	BBox TL:Point(130.0,45.5)
	BBox BR:Point(290.0,212.5)

Compare identity of the image
-----------------------------

.. code-block:: py

    # Check if the image is valid

    compare_handle = face_factor.compare(image_path_1 = "path_to_the_image1", image_path_2 = "path_to_the_image2") ## Replace with the path to the image

Output:

.. code-block:: py

    compare_handle.status # Status of the operation
    compare_handle.result # Result of the operation
    compare_handle.message # Message of the operation
    compare_handle.distance_min # Min distance of compare
    compare_handle.distance_mean # Mean distance of compare
    compare_handle.distance_max # Max distance of compare
    compare_handle.first_validation_result #Image 1 validation result
    compare_handle.second_validation_result #Image 2 validation result


Enroll the image and get the UUID
---------------------------------

.. code-block:: py

    # Enroll the image

    enroll_handle = face_factor.enroll(image_path = "path_to_the_image") ## Replace with the path to the image

Output:

.. code-block:: py

    enroll_handle.status # Status of the operation
    enroll_handle.message # Message of the operation
    enroll_handle.enroll_level
    enroll_handle.uuid
    enroll_handle.guid
    enroll_handle.token

Predict the image to verify the identity
----------------------------------------

.. code-block:: py

    # Predict the image

    predict_handle = face_factor.predict(image_path = "path_to_the_image") ## Replace with the path to the image

Output:

.. code-block:: py

    predict_handle.status # Status of the operation
    predict_handle.message # Message of the operation
    predict_handle.enroll_level
    predict_handle.uuid
    predict_handle.guid
    predict_handle.token

Delete the enrollment from the server
-------------------------------------

.. code-block:: py

    # Delete the enrollment

    delete_handle = face_factor.delete(uuid="uuid") ## Replace with the UUID

Output:

.. code-block:: py

    delete_handle.status # Status of the operation
    delete_handle.message # Message of the operation

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
     - Valid Image
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
