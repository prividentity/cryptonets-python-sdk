#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Sample file demonstrating all public methods of the Session class.
This script shows how to use the cryptonets_python_sdk with type-safe Session API.
"""
from ast import List
import sys
import pathlib
from typing import List, Optional, Union
from matplotlib import pyplot as plt
from msgspec import UNSET, UnsetType

# Import SDK components
from cryptonets_python_sdk.library import PrivIDFaceLib
from cryptonets_python_sdk.session import Session, SessionError, ImageInputArg
from cryptonets_python_sdk.flags import FlagUtil
from cryptonets_python_sdk.library_loader import LibraryLoadError
from cryptonets_python_sdk.idl.gen.privateid_types import (
    SessionSettings,
    Collection,
    OperationConfig,
    FaceResult,
    FaceTraitsFlags,
    DocumentTraits,
    ReturnStatus,
    CallResult,
)
import numpy as np
 


# Global configuration
BASE_URL = "https://xxxxxxxxxxxxxxxxxxx"  # Replace with your actual base URL
API_KEY = "xxxxxxxxxxxxxxxx"  # Replace with your actual API key

# Image paths
IMAGE_DIR = pathlib.Path(__file__).parent / "images"
OUTPUT_DIR = pathlib.Path(__file__).parent / "output"
FACE_IMAGE = str(IMAGE_DIR / "tom_hanks_1.png")
FACE_IMAGE_2 = str(IMAGE_DIR / "tom_hanks_2.jpg")
COMPARE_FACE = str(IMAGE_DIR / "compare_face1.png")
COMPARE_DOC = str(IMAGE_DIR / "compare_doc1.png")
ISO_IMAGE = str(IMAGE_DIR / "tom_hanks_1.png")
SPOOF_IMAGE = str(IMAGE_DIR / "spoof.png")
CONSIDER_BIG_FACE = str(IMAGE_DIR / "consider_big_face.png")
INVALID_FACE = str(IMAGE_DIR / "invalid_face.png")
NO_FACE = str(IMAGE_DIR / "no_face.png")


def ensure_output_dir() -> pathlib.Path:
    """Ensure output directory exists and return its path.

    Returns:
        Path to the output directory
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUTPUT_DIR


def create_session_settings(api_key: str, base_url: str) -> SessionSettings:
    """Create SessionSettings with multiple collections.

    Args:
        api_key: API key for authentication
        base_url: Base URL for the API

    Returns:
        SessionSettings configured with default, RES100, and RES200 collections
        Routes can be custoimized as needed as per the API deployment.
    """
    return SessionSettings(
        collections={
            "default": Collection(
                named_urls= {
                    "base_url" : base_url,
                    "predict": f"{base_url}/FACE3_4/predict",
                    "enroll": f"{base_url}/FACE3_4/enroll",
                    "deleteUser": f"{base_url}/FACE3_4/deleteUser"
                }
            ),
            "RES100": Collection(
                named_urls= {
                    "base_url" :    base_url,
                    "predict": f"{base_url}/RES100/predict",
                    "enroll": f"{base_url}/RES100/enroll",
                    "deleteUser": f"{base_url}/RES100/deleteUser"
                },
                embedding_model_id=14
            ),
            "RES200": Collection(
                named_urls= {
                    "base_url" : base_url,
                    "predict": f"{base_url}/RES200/predict",
                    "enroll": f"{base_url}/RES200/enroll",
                    "deleteUser": f"{base_url}/RES200/deleteUser"
                },
                embedding_model_id=19
            )
        },
        session_token=api_key
    )


def display_face_object(face: FaceResult,index: int):
    """Display information about a detected face object."""
    print(f"\nFace #{index + 1}:")
    traits = FlagUtil.get_active_flags(FaceTraitsFlags, face.face_traits_flags)
    print(f"\n Face Traits Flags:")
    for flag in traits:
        print(f"\n  -{flag.name}")
    if face.geometry is not None:
        print(f"\n  Confidence: {face.geometry.face_confidence_score}")
        print(f"\n  Bounding Box: {face.geometry.bounding_box}")
    if face.age_data is not UNSET:
        print(f"\n  Estimated Age: {face.age_data.estimated_age} , Confidence Score: {face.age_data.age_confidence_score}")
    if face.ids is not UNSET:
        print(f"\n  Face ID - PUID: {face.ids.puid}, GUID: {face.ids.guid}")
    if face.spoof_status is not None:
        print(f"\n  Spoof Status: {face.spoof_status.name}")        

def display_faces_collection(faces: Union[List[FaceResult], UnsetType]):
    """Display information about a collection of detected faces."""
    if faces is not UNSET  and faces is not None and len(faces) > 0:
        print(f"\nDetected {len(faces)} face(s):")
        for i, face in enumerate(faces):
            display_face_object(face, i)
    else:
        print("\nNo faces detected.")



def display_returned_status(op_id: int, call_result: CallResult):
    """Display the returned status (CallHeader) from a call result."""
    header = call_result.call_status
    assert header is not None, "CallResult should contain a CallResultHeader"

    
    # When a call fails, op_id is negative (-1)
    # The call_result will still contain the status information
    if op_id < 0:
        print(f"\nOperation failed with:")        
        print(f"\n Status code: {header.return_status.name}")
        print(f"\n Message: {header.return_message}")
        return

    # When call is successful, op_id is non-negative

    assert op_id >= 0, "Operation ID should be non-negative for successful calls"
    assert header.return_status == ReturnStatus.API_NO_ERROR, "Return status should indicate no error for successful calls"
    assert header.operation_id == op_id, "Operation ID in header should match the returned operation ID"

    print(f"\nCall Result for Operation ID {op_id}:")
    print(f"\n  Return Status: {call_result.call_status.return_status}")    

    # Information about what the `CallResult` contains
    # depends on the specific API method called
    
    print("\nThe result contains the following data object(s):")
    if call_result.faces is not UNSET:
        print(f"\n - Faces collection with {len(call_result.faces)} face(s)")
    if call_result.enroll is not UNSET:
        print("\n - Enroll data")
    if call_result.predict is not UNSET:
        print("\n - Predict data")
    if call_result.user_delete is not UNSET:
        print("\n - User delete data")
    if call_result.compare is not UNSET:
        print("\n - Compare data")
    if call_result.iso_image is not UNSET:
        print("\n - ISO image data")
    if call_result.document is not UNSET:
        print("\n - Document data")    
    


def sample_validate(session: Session, image_path: str = FACE_IMAGE):
    """Sample: Validate a face image.

    Demonstrates face detection, quality check, pose estimation, and anti-spoofing.
    """

    try:
        # Pick an image and specify its format
        image = ImageInputArg(image_path, "rgb")

        # Configure thresholds for face detection
        config = OperationConfig   (
            angle_rotation_left_threshold=6.0,
            angle_rotation_right_threshold=5.0,
            anti_spoofing_threshold=0.9,
            eyes_blinking_threshold=0.3
        )

        # Call validate method return operation ID and result object
        op_id, result = session.validate(image, config)

        # Display the call result status header
        display_returned_status(op_id, result)

        # `validate` result contains only a face collection object
        display_faces_collection(result.faces)
        return result

    except Exception as e:
        print(f"Error: {e}")
        return None


def sample_validate_no_face(session: Session):
    """Sample: Validate an image with no face.

    Demonstrates validation failure when no face is detected in the image.
    This shows how the SDK handles cases where face detection fails.
    """

    print("\n" + "="*80)
    print("Testing validation with image containing no face")
    print("="*80)

    try:
        # Load image with no face
        image = ImageInputArg(NO_FACE, "rgb")

        # Configure thresholds for face detection
        config = OperationConfig(
            angle_rotation_left_threshold=6.0,
            angle_rotation_right_threshold=5.0,
            anti_spoofing_threshold=0.9,
            eyes_blinking_threshold=0.3
        )

        # Call validate method - expected to fail since no face is present
        op_id, result = session.validate(image, config)

        # Display the call result status header
        # When no face is detected, op_id will be negative (-1)
        display_returned_status(op_id, result)

        # Display faces collection (should be empty or None)
        display_faces_collection(result.faces)

        return result

    except Exception as e:
        print(f"Error: {e}")
        return None


def sample_enroll_onefa(session: Session, image_path: str = FACE_IMAGE, collection: str = "default") -> Optional[str]:
    """Sample: Enroll a face for 1FA authentication.
    Returns the PUID (Private User ID) on success.
    """
        
    try:
        image = ImageInputArg(image_path, "rgb")
        config = OperationConfig(
            collection_name=collection,
            angle_rotation_left_threshold=6.0,
            angle_rotation_right_threshold=5.0,
            anti_spoofing_threshold=0.9,
            eyes_blinking_threshold=0.3
        )

        op_id, result = session.enroll_onefa(image, config)

        # Display the call result status header
        display_returned_status(op_id, result)

        # `enroll_onefa` result contains enrollment data object + faces data object      
        display_faces_collection(result.faces)
        enroll_data = result.enroll
        if enroll_data is not UNSET:
            print("\n Enrollment Data:")
            print(f"\n - Enroll Performed: {enroll_data.enroll_performed}")
            print(f"\n - User puid: {enroll_data.api_response.puid}")
            print(f"\n - User guid: {enroll_data.api_response.guid}")
            print(f"\n - Backend API reesponse status (0 mean success): {enroll_data.api_response.status}")
            print(f"\n - Backend API reesponse message: {enroll_data.api_response.message}")
            return enroll_data.api_response.puid
        else:
            print("Enrollment data not available")   
            return None         

    except Exception as e:
        print(f"Error: {e}")
        return None


def sample_face_predict_onefa(session: Session, image_path: str = FACE_IMAGE, collection: str = "default"):
    """Sample: Predict/authenticate using enrolled face.

    Matches face against enrolled faces in the collection.
    """
    
    try:
        image = ImageInputArg(image_path, "rgb")
        config = OperationConfig(
            collection_name=collection,
            angle_rotation_left_threshold=6.0,
            angle_rotation_right_threshold=5.0,
            anti_spoofing_threshold=0.9,
            eyes_blinking_threshold=0.3
        )

        op_id, result = session.face_predict_onefa(image, config)

        # Display the call result status header
        display_returned_status(op_id, result)

        # `face_predict_onefa` result contains predict data object + faces data object      
        display_faces_collection(result.faces)
        predict_data = result.predict
        if predict_data is not UNSET:
            print("\n Predict Data:")
            print(f"\n - Predict Performed: {predict_data.predict_performed}")
            print(f"\n - User puid: {predict_data.api_response.puid}")
            print(f"\n - User guid: {predict_data.api_response.guid}")
            print(f"\n - Backend API reesponse status (0 mean success): {predict_data.api_response.status}")
            print(f"\n - Backend API reesponse message: {predict_data.api_response.message}")
            return predict_data.api_response.puid
        else:
            print("Predict data not available")  
            return None          

    except Exception as e:
        print(f"Error: {e}")
        return None


def sample_face_compare_files(session: Session,
                              image_path_1: str = FACE_IMAGE,
                              image_path_2: str = FACE_IMAGE_2,
                              collection: str = "default"):
    """Sample: Compare two face images (1:1 comparison).

    Demonstrates 1:1 face comparison between two images.
    Returns similarity score and match result.
    """

    try:
        # Load both images
        image_a = ImageInputArg(image_path_1, "rgb")
        image_b = ImageInputArg(image_path_2, "rgb")

        # Configure comparison thresholds
        config = OperationConfig(
            angle_rotation_left_threshold=6.0,
            angle_rotation_right_threshold=5.0,
            anti_spoofing_threshold=0.9,
            eyes_blinking_threshold=0.3
        )

        # Call face_compare_files method
        op_id, result = session.face_compare_files(image_a, image_b, config)

        # Display the call result status header
        display_returned_status(op_id, result)

        # Display face detection results if available as compare should return the faces to compare
        if result.faces is not UNSET:
            display_faces_collection(result.faces)

        # Display comparison results
        if result.compare is not UNSET:
            compare_data = result.compare
            print("\n Comparison Results:")
            print(f"\n - Face Detected in Image A: {compare_data.face_detected_a}")
            print(f"\n - Face Detected in Image B: {compare_data.face_detected_b}")
            print(f"\n - Is Match: {compare_data.is_match}")
            print(f"\n - Similarity Score: {compare_data.similarity_score:.4f}")
            print(f"\n - Confidence: {compare_data.confidence:.4f}")
            print(f"\n - Distance Max: {compare_data.distance_max:.4f}")
            print(f"\n - Distance Mean: {compare_data.distance_mean:.4f}")
            print(f"\n - Distance Min: {compare_data.distance_min:.4f}")
            print(f"\n - Face Thresholds: {compare_data.face_thresholds}")
        else:
            print("\n Comparison data not available")

        return result

    except Exception as e:
        print(f"Error: {e}")
        return None


def sample_estimate_age(session: Session, image_path: str = FACE_IMAGE):
    """Sample: Estimate age from a face image.

    Demonstrates age estimation from a face image.
    Returns only faces data object with age information.
    """

    try:
        # Load the image
        image = ImageInputArg(image_path, "rgb")

        # Configure thresholds for age estimation
        config = OperationConfig(
            angle_rotation_left_threshold=6.0,
            angle_rotation_right_threshold=5.0,
            anti_spoofing_threshold=0.9,
            eyes_blinking_threshold=0.3
        )

        # Call estimate_age method
        op_id, result = session.estimate_age(image, config)

        # Display the call result status header
        display_returned_status(op_id, result)

        # `estimate_age` result contains only a face collection object with age data
        display_faces_collection(result.faces)

        return result

    except Exception as e:
        print(f"Error: {e}")
        return None


def sample_face_iso(session: Session, image_path: str = ISO_IMAGE):
    """Sample: Process face image according to ISO standards.

    Demonstrates ISO-compliant face image generation.
    Returns ISO-compliant face image cropped with ISO standards and background replaced with
    compliant background color RGB(200, 100, 127).
    """

    try:
        # Load the image
        image = ImageInputArg(image_path, "rgb")

        # Configure thresholds for ISO processing
        config = OperationConfig(
            angle_rotation_left_threshold=6.0,
            angle_rotation_right_threshold=5.0,
            anti_spoofing_threshold=0.9,
            eyes_blinking_threshold=0.3
        )

        # Call face_iso method - returns operation ID, result, and ISO image bytes and the Face collection
        op_id, result, iso_image_bytes = session.face_iso(image, config)

        # Save ISO image to output directory
        if result.iso_image is not UNSET and result.iso_image.image:
            output_dir = ensure_output_dir()

            # Get image dimensions from the result metadata
            iso_info = result.iso_image.image.info
            iso_width = iso_info.width
            iso_height = iso_info.height
            iso_channels = iso_info.channels

            # Reconstruct ISO image from raw RGB bytes
            iso_array = np.frombuffer(iso_image_bytes, dtype=np.uint8)
            iso_array = iso_array.reshape((iso_height, iso_width, iso_channels))

            # Save ISO image to output directory
            iso_output_path = output_dir / "face_iso_image.png"
            plt.imsave(str(iso_output_path), iso_array)

            print(f"\n ISO image saved: {iso_output_path}")

        # Display the call result status header
        display_returned_status(op_id, result)

        # Display face detection results if available
        if result.faces is not UNSET:
            display_faces_collection(result.faces)

        # Display ISO image processing results
        if result.iso_image is not UNSET:
            iso_data = result.iso_image
            print("\n ISO Image Processing Results:")
            print(f"\n - Success: {iso_data.success}")
            if iso_data.image:
                print(f"\n - Image Width: {iso_data.image.info.width}")
                print(f"\n - Image Height: {iso_data.image.info.height}")
                print(f"\n - Image Channels: {iso_data.image.info.channels}")
                print(f"\n - Image Depth: {iso_data.image.info.depth.name}")
                print(f"\n - Image Color Format: {iso_data.image.info.color.name}")
            print(f"\n - ISO Image Bytes Size: {len(iso_image_bytes)} bytes")
        else:
            print("\n ISO image data not available")

        return result, iso_image_bytes

    except Exception as e:
        print(f"Error: {e}")
        return None, None


def sample_anti_spoofing(session: Session, image_path: str = FACE_IMAGE):
    """Sample: Perform anti-spoofing detection.

    Demonstrates liveness detection to identify spoofed faces.
    Returns faces data object with anti-spoofing status code.
    """

    try:
        # Load the image
        image = ImageInputArg(image_path, "rgb")

        # Configure anti-spoofing thresholds
        config = OperationConfig(
            skip_antispoof=False,
            anti_spoofing_threshold=0.9,
            angle_rotation_left_threshold=6.0,
            angle_rotation_right_threshold=5.0,
            eyes_blinking_threshold=0.3
        )

        # Call anti_spoofing method - returns status code only
        op_id, result = session.anti_spoofing(image, config)

        # Display the call result status header
        display_returned_status(op_id, result)

        # Display face detection results if available
        if result.faces is not UNSET:
            display_faces_collection(result.faces)

        return result

    except Exception as e:
        print(f"Error: {e}")
        return None


def sample_doc_scan_face(session: Session, image_path: str = COMPARE_DOC):
    """Sample: Scan document and extract face.

    Demonstrates document scanning and face extraction from ID documents.
    Returns cropped document image and extracted face.
    """

    try:
        # Load the document image
        image = ImageInputArg(image_path, "rgb")

        # Configure document scanning thresholds and options
        config = OperationConfig(
            detect_and_recognize_mrz_code = True,
            calculate_age_from_ocr_text = True,
            blur_threshold_enroll_pred = 0.0,
            conf_score_thr_doc = 0.001,
            blur_threshold_doc = 50.0,
            threshold_doc_too_close = 0.99,
            threshold_doc_too_far = 0.03,
            threshold_doc_x = 0.01,
            threshold_doc_y = 0.01
        )

        # Call doc_scan_face method - returns op_id, document bytes, face bytes, and result
        op_id, result ,doc_image_bytes, face_image_bytes = session.doc_scan_face(image, config)

        # Save both images to output directory
        if result.document is not UNSET and result.faces is not UNSET:
            output_dir = ensure_output_dir()

            # Get image dimensions from the result metadata
            doc_info = result.document.cropped_document_image_info.info
            doc_width = doc_info.width
            doc_height = doc_info.height
            doc_channels = doc_info.channels

            # Reconstruct document image from raw RGB bytes
            doc_array = np.frombuffer(doc_image_bytes, dtype=np.uint8)
            doc_array = doc_array.reshape((doc_height, doc_width, doc_channels))

            # Get face image dimensions from first face result
            face_info = result.faces[0].cropped_image_info.info
            face_width = face_info.width
            face_height = face_info.height
            face_channels = face_info.channels

            # Reconstruct face image from raw RGB bytes
            face_array = np.frombuffer(face_image_bytes, dtype=np.uint8)
            face_array = face_array.reshape((face_height, face_width, face_channels))

            # Save both images to output directory
            doc_output_path = output_dir / "doc_scan_document.png"
            face_output_path = output_dir / "doc_scan_face.png"

            plt.imsave(str(doc_output_path), doc_array)
            plt.imsave(str(face_output_path), face_array)

            print(f"\n Images saved:")
            print(f"   - Document: {doc_output_path}")
            print(f"   - Face: {face_output_path}")
        else:
            print("\n Note: Image saving requires document and face results")

        # Display the call result status header
        display_returned_status(op_id, result)

        # Display face detection results if available
        if result.faces is not UNSET:
            display_faces_collection(result.faces)

        # Display document scanning results
        if result.document is not UNSET:
            doc_data = result.document.detected_document
            print("\n Document Scanning Results:")
            print(f"\n - Document Confidence Score: {doc_data.confidence_score:.4f}")
            print(f"\n - Document Box Center: ({doc_data.document_box_center.x:.2f}, {doc_data.document_box_center.y:.2f})")

            # Display document traits flags
            doc_traits = FlagUtil.get_active_flags(DocumentTraits, doc_data.document_traits)
            if doc_traits:
                print(f"\n - Document Traits:")
                for trait in doc_traits:
                    print(f"\n   * {trait.name}")
            else:
                print(f"\n - Document Traits: No issues detected")

            # Display MRZ data if available
            if doc_data.mrz_data:
                print(f"\n - MRZ Data Lines: {len(doc_data.mrz_data)}")
                for i, line in enumerate(doc_data.mrz_data):
                    print(f"\n   Line {i+1}: {line}")

            # Display OCR age data if available
            if doc_data.ocr_age_data:
                print(f"\n - OCR Age: {doc_data.ocr_age_data.age}")

            # Display image information
            if result.document.cropped_document_image_info:
                img_info = result.document.cropped_document_image_info.info
                print(f"\n - Cropped Document Image Info:")
                print(f"\n   * Width: {img_info.width}")
                print(f"\n   * Height: {img_info.height}")
                print(f"\n   * Channels: {img_info.channels}")

            print(f"\n - Document Image Bytes Size: {len(doc_image_bytes)} bytes")
            print(f"\n - Face Image Bytes Size: {len(face_image_bytes)} bytes")
        else:
            print("\n Document scanning data not available")

        return result, doc_image_bytes, face_image_bytes

    except Exception as e:
        print(f"Error: {e}")
        return None, None, None


def sample_user_delete(session: Session, puid: str, collection: str = "default"):
    """Sample: Delete a user by PUID.

    Demonstrates user deletion from a collection by PUID.

    Args:
        puid: User's unique identifier to delete
        collection: Collection name where user is enrolled
    """

    try:
        # Configure collection for user deletion
        config = OperationConfig(
            collection_name=collection,
            angle_rotation_left_threshold=6.0,
            angle_rotation_right_threshold=5.0,
            anti_spoofing_threshold=0.9,
            eyes_blinking_threshold=0.3
        )

        # Call user_delete method - returns operation ID and result
        op_id, result = session.user_delete(puid, config)

        # Display the call result status header
        display_returned_status(op_id, result)

        # Display user deletion results
        if result.user_delete is not UNSET:
            delete_data = result.user_delete
            print("\n User Deletion Results:")
            print(f"\n - PUID: {puid}")
            print(f"\n - Collection: {collection}")
            print(f"\n - Delete Status Code: {delete_data.status}")

            # Interpret status code
            if delete_data.status == 0:
                print(f"\n - Result: User deleted successfully ✓")
            else:
                print(f"\n - Result: Delete operation failed")

            # Display uuid count if available
            if delete_data.uuid_count is not None:
                print(f"\n - UUID Count: {delete_data.uuid_count}")

            # Display message if available
            if delete_data.message:
                print(f"\n - Message: {delete_data.message}")
        else:
            print("\n User deletion data not available")

        return result

    except Exception as e:
        print(f"Error: {e}")
        return None


def sample_enroll_predict_delete_workflow(session: Session, collection: str = "default"):
    """Sample: Complete workflow - enroll, predict, and delete.

    Demonstrates a typical authentication workflow with face enrollment,
    prediction/authentication, and user deletion.

    Args:
        session: Active Session instance
        collection: Collection name for enrollment

    Returns:
        bool: True if workflow completed successfully, False otherwise
    """

    try:
        print("\n" + "=" * 70)
        print(f"WORKFLOW: Enroll -> Predict -> Delete")
        print(f"Collection: {collection}")
        print("=" * 70)

        # Step 1: Enroll a user
        print("\n[Step 1/3] Enrolling user...")
        puid = sample_enroll_onefa(session, FACE_IMAGE, collection)
        if not puid:
            print("\n✗ Workflow failed: Enrollment unsuccessful")
            return False
        print(f"\n✓ Enrollment successful - PUID: {puid}")

        # Step 2: Predict/authenticate the user
        print("\n[Step 2/3] Authenticating user...")
        predicted_puid = sample_face_predict_onefa(session, FACE_IMAGE, collection)
        if not predicted_puid:
            print("\n✗ Workflow failed: Prediction unsuccessful")
            # Clean up enrolled user even if prediction failed
            print("\nCleaning up enrolled user...")
            sample_user_delete(session, puid, collection)
            return False

        # Verify PUID match
        if puid != predicted_puid:
            print(f"\n✗ Workflow warning: PUID mismatch")
            print(f"  - Enrolled PUID: {puid}")
            print(f"  - Predicted PUID: {predicted_puid}")
        else:
            print(f"\n✓ Authentication successful - PUID matched: {puid}")

        # Step 3: Delete the user 
        print("\n[Step 3/3] Deleting user...")
        result = sample_user_delete(session, puid, collection)
        if result and result.user_delete is not UNSET and result.user_delete.status == 0:
            print("\n✓ User deleted successfully")
            print("\n" + "=" * 70)
            print("WORKFLOW COMPLETED SUCCESSFULLY")
            print("=" * 70)
            return True
        else:
            print("\n✗ Workflow warning: Delete operation may have failed")
            return False

    except Exception as e:
        print(f"\n✗ Workflow failed with error: {e}")
        return False


def display_menu():
    """Display the sample selection menu."""
    print("\n" + "=" * 70)
    print("CRYPTONETS PYTHON SDK - SAMPLE SELECTOR")
    print("=" * 70)
    print("\nAvailable Samples:")
    print("\n  1. Validate - Face detection, quality check, and pose estimation")
    print("  2. Estimate Age - Estimate age from face image")
    print("  3. Face ISO - Generate ISO-compliant face image")
    print("  4. Anti-Spoofing - Detect liveness and spoofing")
    print("  5. Face Compare - Compare two face images (1:1)")
    print("  6. Document Scan - Scan document and extract face")
    print("  7. Enroll (1FA) - Enroll a face for authentication")
    print("  8. Predict (1FA) - Authenticate using enrolled face")
    print("  9. User Delete - Delete enrolled user by PUID")
    print(" 10. Complete Workflow - Enroll, Predict, and Delete")
    print("  0. Run All Samples")
    print("\n  Q. Quit")
    print("\n" + "=" * 70)


def run_selected_sample(session: Session, choice: str) -> bool:
    """Run the selected sample.

    Args:
        session: Active Session instance
        choice: User's menu choice

    Returns:
        bool: True to continue, False to quit
    """

    if choice == '1':
        sample_validate(session)
    elif choice == '2':
        sample_estimate_age(session)
    elif choice == '3':
        sample_face_iso(session)
    elif choice == '4':
        sample_anti_spoofing(session)
    elif choice == '5':
        sample_face_compare_files(session)
    elif choice == '6':
        sample_doc_scan_face(session)
    elif choice == '7':
        collection = input("\nEnter collection name (default: 'default'): ").strip() or "default"
        sample_enroll_onefa(session, FACE_IMAGE, collection)
    elif choice == '8':
        collection = input("\nEnter collection name (default: 'default'): ").strip() or "default"
        sample_face_predict_onefa(session, FACE_IMAGE, collection)
    elif choice == '9':
        puid = input("\nEnter PUID to delete: ").strip()
        if puid:
            collection = input("Enter collection name (default: 'default'): ").strip() or "default"
            sample_user_delete(session, puid, collection)
        else:
            print("Error: PUID is required")
    elif choice == '10':
        collection = input("\nEnter collection name (default: 'default'): ").strip() or "default"
        sample_enroll_predict_delete_workflow(session, collection)
    elif choice == '0':
        print("\n" + "=" * 70)
        print("RUNNING ALL SAMPLES")
        print("=" * 70)

        sample_validate(session)
        sample_estimate_age(session)
        sample_face_iso(session)
        sample_anti_spoofing(session)
        sample_face_compare_files(session)
        sample_doc_scan_face(session)

        print("\n" + "=" * 70)
        print("TESTING WORKFLOWS FOR ALL COLLECTIONS")
        print("=" * 70)

        collections = ["default", "RES100", "RES200"]
        for collection in collections:
            sample_enroll_predict_delete_workflow(session, collection)

        print("\n" + "=" * 70)
        print("ALL SAMPLES COMPLETED")
        print("=" * 70)
    elif choice.upper() == 'Q':
        print("\nExiting...")
        return False
    else:
        print("\nInvalid choice. Please try again.")

    return True


def main():
    """Main function with interactive sample selection."""

    try:
        # Initialize the library
        print("\n" + "=" * 70)
        print("INITIALIZING CRYPTONETS SDK")
        print("=" * 70)
        print("\nInitializing PrivIDFaceLib...")
        PrivIDFaceLib.initialize()
        print(f"✓ Native Library version: {PrivIDFaceLib.get_native_sdk_version()}")

        # Create session
        print("\nCreating session...")
        settings = create_session_settings(API_KEY, BASE_URL)
        session = Session(settings)
        print("✓ Session created successfully!")        
        # Interactive menu loop
        while True:
            display_menu()
            choice = input("\nEnter your choice: ").strip()

            if not run_selected_sample(session, choice):
                break

            # Prompt to continue
            if choice.upper() != 'Q':
                input("\nPress Enter to continue...")
         
        
        PrivIDFaceLib.shutdown()
        return 0

    except LibraryLoadError as e:
        print(f"\n✗ Library load error: {e}")        
        PrivIDFaceLib.shutdown()
        return 1
    except SessionError as e:
        print(f"\n✗ Session error: {e}")
        PrivIDFaceLib.shutdown()
        return 1
    except KeyboardInterrupt:
        print("\n\n✗ Interrupted by user")
        PrivIDFaceLib.shutdown()
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        PrivIDFaceLib.shutdown()
        return 1    


if __name__ == "__main__":
    sys.exit(main())
