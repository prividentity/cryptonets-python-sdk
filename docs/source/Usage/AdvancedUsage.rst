Advanced Usage
==============

Environment Setup
-----------------

Server URL and API Key are prerequisites for accessing factor server

To control the number of threads the Tensorflow uses for model inference, use the below environment variable

.. code-block:: sh

    export PI_TF_NUM_THREAD = 3

Or you can pass the variable in the factor object directly.

.. code-block:: py

    # Import the cryptonets sdk class
    from cryptonets_python_sdk.factor import FaceFactor

    # Replace with the provided server URL
    server_url = "https://sample.url.domain"

    # Replace with your API key
    api_key = "your-api-key"

    # Create a Face factor class instance
    face_factor = FaceFactor(server_url = server_url, api_key = api_key, tf_num_thread = 1)

Configuration Setup
-------------------

Additional configuration parameters can be setup using ConfigObject class for processing the image

Instance of Configobject provides various customizations on how to process the image.

See the :ref:`parameter <param_list>` section for complete list of parameters and valid values.

Sample code block for initializing the config object follows:

.. code-block:: py

    from cryptonets_python_sdk.settings.configuration import ConfigObject
    from src.cryptonets_python_sdk.settings.configuration import PARAMETERS
    config_object = ConfigObject(config_param={PARAMETERS.INPUT_IMAGE_FORMAT: "rgb"})


Validation
----------

All the configuration parameters will be validated with the set of values respective to them.

After initialization, you can view the configuration parameters using the following call.

.. code-block:: py

    print(config_object.get_config_param())

Output:

.. code-block:: py

    {"input_image_format": "rgb"}

Usage - Session
---------------

Once you have setup config_object, you can pass it to factor object

This will set the configuration object for the entire session of the Face factor

.. code-block:: py

    # Import the cryptonets sdk class
    from cryptonets_python_sdk.factor import FaceFactor

    # Create a Face factor class instance with config object
    face_factor = FaceFactor(config=config_object)

or you can use built in method for updating the config object

.. code-block:: py

    # Import the cryptonets sdk class
    from cryptonets_python_sdk.factor import FaceFactor

    # Create face factor class and then update the config object
    face_factor = FaceFactor()
    face_factor.update_config(config=config_object)

Usage - Local
-------------

You can set the configuration object for each methods of the factor class too.

This will override the configuration only for the single method call.

All the subsequent calls will use the session initialized if not provided.

.. _isvalid_advanced:

is_valid: Advanced instructions
-------------------------------

See the :ref:`parameter <param_list>` section for complete list of parameters and valid values.


Example 1:

If you want to have a strict validation of the face for enroll purpose,
you can override the configuration context string to ``enroll`` like below.

.. code-block:: py

    # Check if the image is valid
    is_valid_config_object = ConfigObject(config_param={PARAMETERS.CONTEXT_STRING: "enroll"})
    is_valid_handle = face_factor.is_valid(image_path = "path_to_the_image", config=is_valid_config_object)


Example 2:

If you want to decrease the threshold for enroll crop confidence,
you can override the configuration context of ``CONF_SCORE_THR_ENROLL`` like below.

.. code-block:: py

    # Check if the image is valid
    is_valid_config_object = ConfigObject(config_param={PARAMETERS.CONTEXT_STRING: "enroll",
                                                        PARAMETERS.CONF_SCORE_THR_ENROLL: 0.5})
    is_valid_handle = face_factor.is_valid(image_path = "path_to_the_image", config=is_valid_config_object)

.. _age_advanced:

estimate_age: Advanced instructions
-----------------------------------

See the :ref:`parameter <param_list>` section for complete list of parameters and valid values.


Example 1:

If you want to have a strict validation of the face,
you can override the configuration context string to ``enroll`` like below.

.. code-block:: py

    # Estimate user's age
    age_config_object = ConfigObject(config_param={PARAMETERS.CONTEXT_STRING: "enroll"})
    age_handle = face_factor.estimate_age(image_path = "path_to_the_image", config=age_config_object)


Example 2:

If you want to increase the threshold for predict crop confidence,
you can override the configuration context of ``CONF_SCORE_THR_PREDICT`` like below.

.. code-block:: py

    # Check if the image is valid
    age_config_object = ConfigObject(config_param={PARAMETERS.CONTEXT_STRING: "predict",
                                                   PARAMETERS.CONF_SCORE_THR_PREDICT: 0.25})
    age_handle = face_factor.estimate_age(image_path = "path_to_the_image", config=age_config_object)


.. _compare_advanced:

compare: Advanced instructions
------------------------------


See the :ref:`parameter <param_list>` section for complete list of parameters and valid values.

.. code-block:: py

    # Check if the images are of same person
    compare_config_object = ConfigObject(config_param={PARAMETERS.CONTEXT_STRING: "predict")
    compare_handle = face_factor.compare(image_path_1 = "path_to_the_image1", image_path_2 = "path_to_the_image2",
                                         config=compare_config_object)


.. _enroll_advanced:

enroll: Advanced instructions
-----------------------------

See the :ref:`parameter <param_list>` section for complete list of parameters and valid values.

.. code-block:: py

    # Enroll the image
    enroll_handle = face_factor.enroll(image_path = "path_to_the_image", config=config_object)

.. _predict_advanced:

predict: Advanced instructions
------------------------------

See the :ref:`parameter <param_list>` section for complete list of parameters and valid values.

.. code-block:: py

    # Predict the image
    predict_handle = face_factor.predict(image_path = "path_to_the_image", config=config_object)

.. _iso_face_advanced:

iso_face: Advanced instructions
-------------------------------

See the :ref:`parameter <param_list>` section for complete list of parameters and valid values.

.. code-block:: py

    # Get ISO face for the image
    iso_face_handle = face_factor.get_iso_face(image_path = "path_to_the_image", config=config_object)

