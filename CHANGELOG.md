# Changelog

All notable changes to the CryptoNets Python SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-01-02

### Changed

#### Configuration API Updates

This release updates the SDK to align with the Generic V2 native library. Several configuration parameters have been modernized and enhanced:

**Face Detection and Selection**

- **BREAKING**: Replaced `single_face` and `consider_biggest_face` boolean parameters with unified `face_detection_strategy` integer parameter
  - `0` = Multiple faces (all detected faces returned)
  - `1` = Best confidence score (single face with highest confidence) - default
  - `2` = Biggest face (single face with largest area)
  - `3` = Hybrid (best score of area × confidence)

**Anti-Spoofing Configuration**

- **BREAKING**: Replaced `skip_antispoof` and `use_jdb_antispoof` boolean parameters with unified `anti_spoofing_mode` integer parameter
  - `0` = Off (no anti-spoofing)
  - `1` = XMS (dual XMS models, works with head pose landmarks) - default
  - `2` = JPD (JPD model, works with yolov5n_05_float16 landmarks)
  - `3` = Recognito Android (for Android platforms)

**Face Landmarks Configuration**

- Generalized the facelanmark selection for age to all operations to be configured via `base_face_landmarks_model_id` and `age_face_landmarks_model_id` was removed.
- Added `base_landmarks_model_id` parameter for selecting face landmark detection model
  - `0` = Head pose model (default)
  - `22` = Yolov5n05 model

### Added

- `landmark_confidence_score_threshold` configuration parameter (default: 0.5) for face landmarks detection
- `base_landmarks_model_id` configuration for selecting between head pose and Yolov5n05 models
- Documentation for barcode detection features (previously marked as "future versions")

### Documentation

- Updated README.md to reflect Generic V2 native library capabilities
- Clarified face landmark model configuration section
- Removed "for future versions" notes for available features
- Improved configuration parameter descriptions with model compatibility notes

### Migration Guide

If you're upgrading from 2.0.0b1:

**Face Selection Migration:**

```python
# Old (2.0.0b1)
config = OperationConfig(
    single_face=True,
    consider_biggest_face=False
)

# New (2.0.0)
config = OperationConfig(
    face_detection_strategy=1  # Best confidence score
)

# Equivalent mappings:
# single_face=True → face_detection_strategy=1 (best confidence)
# consider_biggest_face=True → face_detection_strategy=2 (biggest face)
# Multiple faces → face_detection_strategy=0
```

**Anti-Spoofing Migration:**

```python
# Old (2.0.0b1)
config = OperationConfig(
    skip_antispoof=False,
    use_jdb_antispoof=False
)

# New (2.0.0)
config = OperationConfig(
    anti_spoofing_mode=1  # XMS mode (default)
)

# Equivalent mappings:
# skip_antispoof=True → anti_spoofing_mode=0 (off)
# use_jdb_antispoof=True → anti_spoofing_mode=2 (JPD)
# Default → anti_spoofing_mode=1 (XMS)
```

**Face Landmarks Migration:**
```python
# Old (2.0.0b1)
config = OperationConfig(
    age_face_landmarks_model_id=-1
)

# New (2.0.0)
config = OperationConfig(
    base_face_landmarks_model_id=-1  # Use default model
    # OR explicitly set:
    # base_landmarks_model_id=0   # Head pose model
    # base_landmarks_model_id=22  # Yolov5n05 model
)
```

## [2.0.0b1] - 2025-12-16

### Added

- Initial beta release of version 2.0.0
- Support for Generic V2 native library features

---

## Earlier Versions

For changes in versions prior to 2.0.0b1, please refer to V1 Documentation: [SDK Docs](https://privid-sdk.s3.us-east-2.amazonaws.com/cryptonets-python-sdk/last_stable/)
