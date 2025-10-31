#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test file for loading the PrivIDFaceLib and creating a session.
This script demonstrates how to initialize and use the cryptonets_python_sdk.
"""
import os
import json
import sys
import time
import logging
from datetime import datetime

# For JSON format handling with protobuf
# from google.protobuf import json_format
from cryptonets_python_sdk.privid_face import ImageInputArg, PrivIDFaceLib, SessionError, Session
from cryptonets_python_sdk.library_loader import LibraryLoadError
# from messages.operation_results import api_result_pb2
 

def main():
    """Main test function to load the library and create a session."""
    
    try:
        # Load the library using the DefaultLibraryLoadStrategy
        print("Loading library...")       
        PrivIDFaceLib.initialize()

        print("Library loaded successfully!")
        
        # Get library version
        version = PrivIDFaceLib.get_version()
        print(f"Library version: {version}")
        
        # API configuration
        base_url = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # Replace with your actual base URL
        api_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # Replace with your actual API key
        
        # Create session settings
        settings = json.dumps({
            "collections": {
                "default": {
                    "named_urls": {
                        "base_url": base_url,
                        "predict": f"{base_url}/FACE3_4/predict",
                        "enroll": f"{base_url}/FACE3_4/enroll",
                        "deleteUser": f"{base_url}/FACE3_4/deleteUser"
                    }
                },
                "RES100": {
                    "named_urls": {
                        "base_url": base_url,
                        "predict": f"{base_url}/RES100/predict",
                        "enroll": f"{base_url}/RES100/enroll",
                        "deleteUser": f"{base_url}/RES100/deleteUser"
                    },
                    "embedding_model_id": 14
                },
                "RES200": {
                    "named_urls": {
                        "base_url": base_url,
                        "predict": f"{base_url}/RES200/predict",
                        "enroll": f"{base_url}/RES200/enroll",
                        "deleteUser": f"{base_url}/RES200/deleteUser"
                    },
                    "embedding_model_id": 19
                }
            },
            "session_token": api_key
        })      
    
        
        # Create a session
        print("Creating session...")
        session = Session(settings)
        print("Session created successfully!")

        # Test new library-level methods
        log_level = PrivIDFaceLib.get_log_level()
        print(f"Current log level: {log_level}")

        cache_dir = PrivIDFaceLib.get_models_cache_directory()
        print(f"Models cache directory: {cache_dir}")

        is_init = PrivIDFaceLib.is_library_initialized()
        print(f"Library initialized: {is_init}")

        img_path =  os.path.join(os.path.dirname(__file__), "img.png")  # Adjust to your test image path
        # Only run this 
        print(f"Validating image: {img_path}")
        op_id, result  = session.validate(ImageInputArg(img_path, "rgb"), "{}")

        print(f"Returned data:\n- `operation number` {op_id} \n- `call result`: {result}")


    except LibraryLoadError as e:
        print(f"{e}")
        return 1
    except SessionError as e:
        print(f"{e}")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
