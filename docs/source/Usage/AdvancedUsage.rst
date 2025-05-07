Advanced Usage
==============

Configuration Setup
-------------------

Additional configuration parameters for image processing can be set up using the ConfigObject class.
An instance of ConfigObject allows various customizations, enabling fine-tuned control over how images are processed.

For a complete list of parameters and valid values, refer to the :ref:`parameter <param_list>` section.

Sample Code for Initializing ConfigObject for the session initialization or for individual method calls:

.. code-block:: py

    # Import ConfigObject and PARAMETERS
    from cryptonets_python_sdk.settings.configuration import ConfigObject
    from cryptonets_python_sdk.settings.configuration import PARAMETERS

    # Initialize ConfigObject with custom collection name:    
    def create_config_object(collection_name=""):
        config_param = { PARAMETERS.INPUT_IMAGE_FORMAT: "rgb" }
        if collection_name!="":
            config_param[PARAMETERS.COLLECTION_NAME] = collection_name
        return ConfigObject(config_param)

    # Pass this configuration object to the FaceFactor object method (enroll, predict, etc.)
     result = face_factor.enroll(image_path=image_file_path,config=create_config_object("RES200"))

This setup allows you to specify configurations such as the input image format, among other options, to meet your processing needs.


Using Collections
-----------------
When calling the following methods: 

- compare(): 1:1 Verification of Face Images
- compare_doc_with_face(): 1:1 Verification of a Face Image and Document Image
- enroll(): Initialize Subject’s Face in the Identification System
- predict(): 1:N Matching of a Probe Image to the Enrolled Gallery
- delete(): Remove a User’s PUID from the Server

You can set the configuration parameter :ref:`PARAMETERS.COLLECTION_NAME <param_list>`  to specify the collection name.
The collection name is an optional configuration parameter, that indicates which embedding model to use. 
The default value is an empty string, which means that the default collection will be used.
If a user is enrolled in a specific collection, the same collection should be used for prediction and deletion.
Also you can't compare between users enrolled in different collections.


Here is a sample code to create a configuration object:

.. code-block:: py

    def create_config_object(collection_name=""):
        """
        Creates a basic configuration object (used for in here for the operation calls).

        Args:
            collection_name (str, optional): The name of the collection to be added to the configuration. Defaults to an empty string.            
        Returns:
            ConfigObject: A configuration object initialized with the specified parameters.
        """

        config_param = { 
        PARAMETERS.INPUT_IMAGE_FORMAT: "rgb",
        PARAMETERS.THRESHOLD_USER_TOO_FAR: 0.0,
        PARAMETERS.THRESHOLD_USER_RIGHT: 0.0,
        PARAMETERS.THRESHOLD_USER_LEFT: 1.1,
        PARAMETERS.THRESHOLD_USER_TOO_CLOSE: 1.0 ,
        PARAMETERS.RELAX_FACE_VALIDATION: True,      
        }
        if collection_name!="":
            config_param[PARAMETERS.COLLECTION_NAME] = collection_name
            print(f"collection name: {collection_name}")
        return ConfigObject(config_param)


 
Configuration Validation
------------------------

Each configuration parameter in ConfigObject is validated against a predefined set of acceptable values.
After initializing the configuration, you can view the parameters currently set by using the following call:

.. code-block:: py

    print(config_object.get_config_param())

Output:

.. code-block:: py

    {"input_image_format": "rgb"}


Usage - Session
---------------

Once config_object is set up, you can pass it to the FaceFactor object to apply the configuration across the entire session.

.. code-block:: py

    # Import the FaceFactor class from the CryptoNets SDK
    from cryptonets_python_sdk.factor import FaceFactor

    # Create a FaceFactor instance with the configuration object
    face_factor = FaceFactor(config=config_object)

Alternatively, you can update the configuration using a built-in method:

.. code-block:: py

    # Import the FaceFactor class from the CryptoNets SDK
    from cryptonets_python_sdk.factor import FaceFactor

    # Initialize FaceFactor and update the configuration object
    face_factor = FaceFactor()
    face_factor.update_config(config=config_object)


Usage - Local
-------------

You can also set the configuration object for individual method calls within the FaceFactor class.
This approach overrides the session configuration only for that specific method call.
All subsequent calls will revert to the session configuration unless a new configuration is provided.

This flexibility allows for fine-tuned control, enabling session-wide settings as well as method-specific configurations.

.. _isvalid_advanced:

is_valid: Advanced instructions
-------------------------------

For detailed information on all configurable parameters and their valid values, refer to the :ref:`parameter <param_list>` section.


Example 1: Strict Validation for Enrollment

To perform a stricter validation of the face image for enrollment purposes, you can override the configuration by setting the context string to ``enroll`` as shown below:

.. code-block:: py

    # Import ConfigObject and PARAMETERS
    from cryptonets_python_sdk.settings.configuration import ConfigObject
    from cryptonets_python_sdk.settings.configuration import PARAMETERS

    # Configure strict validation for enrollment
    is_valid_config_object = ConfigObject(config_param={
        PARAMETERS.CONTEXT_STRING: "enroll"
        })

    # Check if the image is valid with the specified configuration
    is_valid_result = face_factor.is_valid(image_path="path_to_the_image", config=is_valid_config_object)


Example 2:

Example 2: Lowering the Threshold for Enrollment Crop Confidence
If you want to decrease the confidence threshold for the enrollment crop, you can adjust the ``CONF_SCORE_THR_ENROLL`` parameter along with the ``enroll`` context as follows:

.. code-block:: py

    # Configure strict validation for enrollment with a lower confidence threshold
    is_valid_config_object = ConfigObject(config_param={
        PARAMETERS.CONTEXT_STRING: "enroll",
        PARAMETERS.CONF_SCORE_THR_ENROLL: 0.5
    })

    # Check if the image is valid with the modified configuration
    is_valid_result = face_factor.is_valid(image_path="path_to_the_image", config=is_valid_config_object)

These configurations allow you to customize the is_valid validation criteria, tailoring the enrollment process to specific requirements for accuracy and confidence.

.. _age_advanced:

estimate_age: Advanced instructions
-----------------------------------

For a comprehensive list of configurable parameters and their valid values, please refer to the :ref:`parameter <param_list>` section.


Example 1: Strict Validation for Age Estimation

To apply strict validation when estimating age,
you can set the configuration context string to ``enroll`` for tighter control, as shown below:

.. code-block:: py

    # Import ConfigObject and PARAMETERS
    from cryptonets_python_sdk.settings.configuration import ConfigObject
    from cryptonets_python_sdk.settings.configuration import PARAMETERS

    # Configure strict validation for age estimation
    age_config_object = ConfigObject(config_param={PARAMETERS.CONTEXT_STRING: "enroll"})

    # Estimate user's age with strict validation
    age_handle = face_factor.estimate_age(image_path="path_to_the_image", config=age_config_object)



Example 2: Increasing the Threshold for Prediction Crop Confidence

If you want to increase the confidence threshold for age prediction,
you can set the ``CONF_SCORE_THR_PREDICT`` parameter along with the ``predict`` context as follows:

.. code-block:: py

    # Configure increased confidence threshold for prediction
    age_config_object = ConfigObject(config_param={
        PARAMETERS.CONTEXT_STRING: "predict",
        PARAMETERS.CONF_SCORE_THR_PREDICT: 0.25
    })

    # Estimate user's age with modified configuration
    age_handle = face_factor.estimate_age(image_path="path_to_the_image", config=age_config_object)

These configurations enable you to fine-tune the ``estimate_age`` method for specific use cases,
ensuring that the validation criteria align with your accuracy and confidence requirements.

.. _compare_advanced:

compare: Advanced instructions
------------------------------


For a complete list of configurable parameters and their valid values, refer to the :ref:`parameter <param_list>` section.

Example: Configuring Prediction Context for Comparison

To perform a comparison with a specific validation context, such as ``predict``, you can customize the configuration as follows:

.. code-block:: py

    # Import ConfigObject and PARAMETERS
    from cryptonets_python_sdk.settings.configuration import ConfigObject
    from cryptonets_python_sdk.settings.configuration import PARAMETERS

    # Set up the configuration for prediction context
    compare_config_object = ConfigObject(config_param={PARAMETERS.CONTEXT_STRING: "predict"})

    # Perform comparison with specified configuration
    compare_handle = face_factor.compare(
        image_path_1="path_to_the_image1",  # Replace with the actual path to the first image
        image_path_2="path_to_the_image2",  # Replace with the actual path to the second image
        config=compare_config_object
    )

This configuration allows you to tailor the ``compare`` method to specific contexts, ensuring that the validation and comparison criteria align with your requirements for accuracy and confidence.

.. _enroll_advanced:

enroll: Advanced instructions
-----------------------------

For a comprehensive list of parameters and their valid values, refer to the :ref:`parameter <param_list>` section.

.. code-block:: py

    # Enroll the image with custom configuration
    enroll_handle = face_factor.enroll(image_path="path_to_the_image", config=config_object)

.. _predict_advanced:

predict: Advanced instructions
------------------------------

For a comprehensive list of parameters and their valid values, refer to the :ref:`parameter <param_list>` section.

.. code-block:: py

    # Perform 1:N prediction on the image with custom configuration
    predict_handle = face_factor.predict(image_path="path_to_the_image", config=config_object)


.. _iso_face_advanced:

iso_face: Advanced instructions
-------------------------------

For a comprehensive list of parameters and their valid values, refer to the :ref:`parameter <param_list>` section.

.. code-block:: py

    # Extract ISO-compliant face image with custom configuration
    iso_face_handle = face_factor.get_iso_face(image_path="path_to_the_image", config=config_object)

These examples demonstrate how to use a ConfigObject to pass custom parameters for each method, allowing for flexible configurations tailored to your specific requirements.

