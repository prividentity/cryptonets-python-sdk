"""Unit tests for the FlagUtil utility class.

This module tests the flag manipulation utilities with FaceTraitsFlags
and DocumentTraits from the SDK's data types.
"""

import pytest
from cryptonets_python_sdk.flags import FlagUtil
from cryptonets_python_sdk.idl.gen.privateid_types import (
    FaceTraitsFlags,
    DocumentTraits,
)


class TestFlagUtilWithFaceTraits:
    """Test FlagUtil methods with FaceTraitsFlags."""

    def test_get_active_flags_single_flag(self):
        """Test extracting a single active flag."""
        # FT_FACE_TOO_CLOSE = 1
        active = FlagUtil.get_active_flags(FaceTraitsFlags, 1)
        assert len(active) == 1
        assert FaceTraitsFlags.FT_FACE_TOO_CLOSE in active

    def test_get_active_flags_multiple_flags(self):
        """Test extracting multiple active flags."""
        # FT_FACE_TOO_CLOSE (1) | FT_FACE_RIGHT (4) = 5
        active = FlagUtil.get_active_flags(FaceTraitsFlags, 5)
        assert len(active) == 2
        assert FaceTraitsFlags.FT_FACE_TOO_CLOSE in active
        assert FaceTraitsFlags.FT_FACE_RIGHT in active

    def test_get_active_flags_complex_combination(self):
        """Test extracting flags from complex combination."""
        # FT_FACE_TOO_CLOSE (1) | FT_IMAGE_BLURR (64) | FT_FACE_WITH_GLASS (128) = 193
        active = FlagUtil.get_active_flags(FaceTraitsFlags, 193)
        assert len(active) == 3
        assert FaceTraitsFlags.FT_FACE_TOO_CLOSE in active
        assert FaceTraitsFlags.FT_IMAGE_BLURR in active
        assert FaceTraitsFlags.FT_FACE_WITH_GLASS in active

    def test_get_active_flags_no_flags(self):
        """Test with no active flags (zero value)."""
        active = FlagUtil.get_active_flags(FaceTraitsFlags, 0)
        assert len(active) == 0

    def test_get_active_flags_all_position_flags(self):
        """Test with all position-related flags."""
        # FT_FACE_RIGHT (4) | FT_FACE_LEFT (8) | FT_FACE_UP (16) | FT_FACE_DOWN (32) = 60
        active = FlagUtil.get_active_flags(FaceTraitsFlags, 60)
        assert len(active) == 4
        assert FaceTraitsFlags.FT_FACE_RIGHT in active
        assert FaceTraitsFlags.FT_FACE_LEFT in active
        assert FaceTraitsFlags.FT_FACE_UP in active
        assert FaceTraitsFlags.FT_FACE_DOWN in active

    def test_get_flag_names_single(self):
        """Test getting flag names for a single flag."""
        names = FlagUtil.get_flag_names(FaceTraitsFlags, 1)
        assert names == ["FT_FACE_TOO_CLOSE"]

    def test_get_flag_names_multiple(self):
        """Test getting flag names for multiple flags."""
        # FT_FACE_TOO_CLOSE (1) | FT_IMAGE_BLURR (64) = 65
        names = FlagUtil.get_flag_names(FaceTraitsFlags, 65)
        assert len(names) == 2
        assert "FT_FACE_TOO_CLOSE" in names
        assert "FT_IMAGE_BLURR" in names

    def test_get_flag_names_empty(self):
        """Test getting flag names with no active flags."""
        names = FlagUtil.get_flag_names(FaceTraitsFlags, 0)
        assert names == []

    def test_has_flag_present(self):
        """Test checking for a flag that is present."""
        flags = FaceTraitsFlags.FT_FACE_TOO_CLOSE | FaceTraitsFlags.FT_IMAGE_BLURR
        assert FlagUtil.has_flag(flags, FaceTraitsFlags.FT_FACE_TOO_CLOSE) is True
        assert FlagUtil.has_flag(flags, FaceTraitsFlags.FT_IMAGE_BLURR) is True

    def test_has_flag_absent(self):
        """Test checking for a flag that is not present."""
        flags = FaceTraitsFlags.FT_FACE_TOO_CLOSE
        assert FlagUtil.has_flag(flags, FaceTraitsFlags.FT_FACE_LEFT) is False

    def test_has_flag_zero_value(self):
        """Test has_flag with FT_FACE_NO_TRAIT."""
        flags = FaceTraitsFlags.FT_FACE_NO_TRAIT
        # FT_FACE_NO_TRAIT should always be present in zero value
        assert FlagUtil.has_flag(flags, FaceTraitsFlags.FT_FACE_NO_TRAIT) is True

    def test_has_any_true(self):
        """Test has_any when at least one flag is present."""
        flags = FaceTraitsFlags.FT_FACE_TOO_CLOSE | FaceTraitsFlags.FT_IMAGE_BLURR
        result = FlagUtil.has_any(
            flags,
            FaceTraitsFlags.FT_FACE_LEFT,
            FaceTraitsFlags.FT_IMAGE_BLURR,
            FaceTraitsFlags.FT_FACE_WITH_GLASS,
        )
        assert result is True

    def test_has_any_false(self):
        """Test has_any when no flags are present."""
        flags = FaceTraitsFlags.FT_FACE_TOO_CLOSE
        result = FlagUtil.has_any(
            flags, FaceTraitsFlags.FT_FACE_LEFT, FaceTraitsFlags.FT_FACE_UP
        )
        assert result is False

    def test_has_any_single_flag(self):
        """Test has_any with a single flag check."""
        flags = FaceTraitsFlags.FT_FACE_TOO_CLOSE
        result = FlagUtil.has_any(flags, FaceTraitsFlags.FT_FACE_TOO_CLOSE)
        assert result is True

    def test_has_all_true(self):
        """Test has_all when all flags are present."""
        flags = (
            FaceTraitsFlags.FT_FACE_TOO_CLOSE
            | FaceTraitsFlags.FT_IMAGE_BLURR
            | FaceTraitsFlags.FT_FACE_WITH_GLASS
        )
        result = FlagUtil.has_all(
            flags,
            FaceTraitsFlags.FT_FACE_TOO_CLOSE,
            FaceTraitsFlags.FT_IMAGE_BLURR,
            FaceTraitsFlags.FT_FACE_WITH_GLASS,
        )
        assert result is True

    def test_has_all_false(self):
        """Test has_all when not all flags are present."""
        flags = FaceTraitsFlags.FT_FACE_TOO_CLOSE | FaceTraitsFlags.FT_IMAGE_BLURR
        result = FlagUtil.has_all(
            flags,
            FaceTraitsFlags.FT_FACE_TOO_CLOSE,
            FaceTraitsFlags.FT_IMAGE_BLURR,
            FaceTraitsFlags.FT_FACE_WITH_GLASS,
        )
        assert result is False

    def test_has_all_single_flag(self):
        """Test has_all with a single flag check."""
        flags = FaceTraitsFlags.FT_FACE_TOO_CLOSE
        result = FlagUtil.has_all(flags, FaceTraitsFlags.FT_FACE_TOO_CLOSE)
        assert result is True

    def test_brightness_flags(self):
        """Test flags for brightness issues."""
        # FT_FACE_TOO_DARK (8192) | FT_FACE_TOO_BRIGHT (16384) = 24576
        flags = FaceTraitsFlags.FT_FACE_TOO_DARK | FaceTraitsFlags.FT_FACE_TOO_BRIGHT
        active = FlagUtil.get_active_flags(FaceTraitsFlags, flags.value)
        assert len(active) == 2
        assert FaceTraitsFlags.FT_FACE_TOO_DARK in active
        assert FaceTraitsFlags.FT_FACE_TOO_BRIGHT in active

    def test_eye_and_mouth_flags(self):
        """Test flags for eye blinking and mouth opened."""
        # FT_EYE_BLINK (131072) | FT_MOUTH_OPENED (262144) = 393216
        flags = FaceTraitsFlags.FT_EYE_BLINK | FaceTraitsFlags.FT_MOUTH_OPENED
        names = FlagUtil.get_flag_names(FaceTraitsFlags, flags.value)
        assert "FT_EYE_BLINK" in names
        assert "FT_MOUTH_OPENED" in names

    def test_looking_direction_flags(self):
        """Test flags for looking direction."""
        flags = (
            FaceTraitsFlags.FT_LOOKING_LEFT
            | FaceTraitsFlags.FT_LOOKING_RIGHT
            | FaceTraitsFlags.FT_LOOKING_HIGH
            | FaceTraitsFlags.FT_LOOKING_DOWN
        )
        active = FlagUtil.get_active_flags(FaceTraitsFlags, flags.value)
        assert len(active) == 4
        assert all(
            flag in active
            for flag in [
                FaceTraitsFlags.FT_LOOKING_LEFT,
                FaceTraitsFlags.FT_LOOKING_RIGHT,
                FaceTraitsFlags.FT_LOOKING_HIGH,
                FaceTraitsFlags.FT_LOOKING_DOWN,
            ]
        )

    def test_rotation_flags(self):
        """Test flags for face rotation."""
        flags = (
            FaceTraitsFlags.FT_FACE_ROTATED_RIGHT
            | FaceTraitsFlags.FT_FACE_ROTATED_LEFT
        )
        assert FlagUtil.has_all(
            flags,
            FaceTraitsFlags.FT_FACE_ROTATED_RIGHT,
            FaceTraitsFlags.FT_FACE_ROTATED_LEFT,
        )


class TestFlagUtilWithDocumentTraits:
    """Test FlagUtil methods with DocumentTraits."""

    def test_get_active_flags_single_document_trait(self):
        """Test extracting a single document trait."""
        # DT_DOCUMENT_WITH_LOW_CONFIDENCE_SCORE = 1
        active = FlagUtil.get_active_flags(DocumentTraits, 1)
        assert len(active) == 1
        assert DocumentTraits.DT_DOCUMENT_WITH_LOW_CONFIDENCE_SCORE in active

    def test_get_active_flags_multiple_document_traits(self):
        """Test extracting multiple document traits."""
        # DT_DOCUMENT_IS_BLURRY (2) | DT_DOCUMENT_IS_CLOSE (4) = 6
        active = FlagUtil.get_active_flags(DocumentTraits, 6)
        assert len(active) == 2
        assert DocumentTraits.DT_DOCUMENT_IS_BLURRY in active
        assert DocumentTraits.DT_DOCUMENT_IS_CLOSE in active

    def test_document_position_flags(self):
        """Test document position flags."""
        # DT_DOCUMENT_IS_LEFT (16) | DT_DOCUMENT_IS_RIGHT (32) | DT_DOCUMENT_IS_UP (64) = 112
        flags = (
            DocumentTraits.DT_DOCUMENT_IS_LEFT
            | DocumentTraits.DT_DOCUMENT_IS_RIGHT
            | DocumentTraits.DT_DOCUMENT_IS_UP
        )
        active = FlagUtil.get_active_flags(DocumentTraits, flags.value)
        assert len(active) == 3
        names = FlagUtil.get_flag_names(DocumentTraits, flags.value)
        assert "DT_DOCUMENT_IS_LEFT" in names
        assert "DT_DOCUMENT_IS_RIGHT" in names
        assert "DT_DOCUMENT_IS_UP" in names

    def test_document_distance_flags(self):
        """Test document distance flags."""
        # DT_DOCUMENT_IS_CLOSE (4) | DT_DOCUMENT_IS_FAR (8) = 12
        flags = DocumentTraits.DT_DOCUMENT_IS_CLOSE | DocumentTraits.DT_DOCUMENT_IS_FAR
        assert FlagUtil.has_all(
            flags, DocumentTraits.DT_DOCUMENT_IS_CLOSE, DocumentTraits.DT_DOCUMENT_IS_FAR
        )

    def test_fingers_detected_flag(self):
        """Test fingers detected flag."""
        # DT_FINGERS_DETECTED = 256
        flags = DocumentTraits.DT_FINGERS_DETECTED
        assert FlagUtil.has_flag(flags, DocumentTraits.DT_FINGERS_DETECTED)
        names = FlagUtil.get_flag_names(DocumentTraits, flags.value)
        assert names == ["DT_FINGERS_DETECTED"]

    def test_document_quality_flags(self):
        """Test combination of document quality flags."""
        # DT_DOCUMENT_WITH_LOW_CONFIDENCE_SCORE (1) | DT_DOCUMENT_IS_BLURRY (2) = 3
        flags = (
            DocumentTraits.DT_DOCUMENT_WITH_LOW_CONFIDENCE_SCORE
            | DocumentTraits.DT_DOCUMENT_IS_BLURRY
        )
        assert FlagUtil.has_any(
            flags,
            DocumentTraits.DT_DOCUMENT_WITH_LOW_CONFIDENCE_SCORE,
            DocumentTraits.DT_DOCUMENT_IS_BLURRY,
        )

    def test_document_no_trait(self):
        """Test DT_DOC_NO_TRAIT (zero value)."""
        flags = DocumentTraits.DT_DOC_NO_TRAIT
        active = FlagUtil.get_active_flags(DocumentTraits, flags.value)
        assert len(active) == 0

    def test_all_document_traits_combined(self):
        """Test combination of all document traits."""
        # Combine all document traits except DT_DOC_NO_TRAIT
        flags = (
            DocumentTraits.DT_DOCUMENT_WITH_LOW_CONFIDENCE_SCORE
            | DocumentTraits.DT_DOCUMENT_IS_BLURRY
            | DocumentTraits.DT_DOCUMENT_IS_CLOSE
            | DocumentTraits.DT_DOCUMENT_IS_FAR
            | DocumentTraits.DT_DOCUMENT_IS_LEFT
            | DocumentTraits.DT_DOCUMENT_IS_RIGHT
            | DocumentTraits.DT_DOCUMENT_IS_UP
            | DocumentTraits.DT_DOCUMENT_IS_DOWN
            | DocumentTraits.DT_FINGERS_DETECTED
        )
        active = FlagUtil.get_active_flags(DocumentTraits, flags.value)
        assert len(active) == 9


class TestFlagUtilEdgeCases:
    """Test edge cases and error conditions."""

    def test_large_flag_value(self):
        """Test with a large flag value."""
        # FT_FACE_NOT_IN_OVAL = 2097152 (largest FaceTraitsFlags value)
        flags = FaceTraitsFlags.FT_FACE_NOT_IN_OVAL
        active = FlagUtil.get_active_flags(FaceTraitsFlags, flags.value)
        assert len(active) == 1
        assert FaceTraitsFlags.FT_FACE_NOT_IN_OVAL in active

    def test_combined_large_values(self):
        """Test combination of large flag values."""
        flags = (
            FaceTraitsFlags.FT_FACE_ROTATED_RIGHT
            | FaceTraitsFlags.FT_FACE_ROTATED_LEFT
            | FaceTraitsFlags.FT_FACE_NOT_IN_OVAL
        )
        active = FlagUtil.get_active_flags(FaceTraitsFlags, flags.value)
        assert len(active) == 3

    def test_has_any_with_no_flags_provided(self):
        """Test has_any with empty flag list."""
        flags = FaceTraitsFlags.FT_FACE_TOO_CLOSE
        # Calling has_any with no flags should return False
        result = FlagUtil.has_any(flags)
        assert result is False

    def test_has_all_with_no_flags_provided(self):
        """Test has_all with empty flag list."""
        flags = FaceTraitsFlags.FT_FACE_TOO_CLOSE
        # Calling has_all with no flags should return True (vacuous truth)
        result = FlagUtil.has_all(flags)
        assert result is True


class TestRealWorldScenarios:
    """Test real-world usage scenarios."""

    def test_enrollment_validation_scenario(self):
        """Test typical enrollment validation with multiple issues."""
        # Simulate a face that is blurry, wearing glasses, and too close
        flags = (
            FaceTraitsFlags.FT_IMAGE_BLURR
            | FaceTraitsFlags.FT_FACE_WITH_GLASS
            | FaceTraitsFlags.FT_FACE_TOO_CLOSE
        )

        # Check for any quality issues
        has_quality_issues = FlagUtil.has_any(
            flags,
            FaceTraitsFlags.FT_IMAGE_BLURR,
            FaceTraitsFlags.FT_FACE_TOO_DARK,
            FaceTraitsFlags.FT_FACE_TOO_BRIGHT,
        )
        assert has_quality_issues is True

        # Get all active issues for user feedback
        issues = FlagUtil.get_flag_names(FaceTraitsFlags, flags.value)
        assert len(issues) == 3
        assert "FT_IMAGE_BLURR" in issues
        assert "FT_FACE_WITH_GLASS" in issues
        assert "FT_FACE_TOO_CLOSE" in issues

    def test_document_scan_scenario(self):
        """Test typical document scanning with positioning issues."""
        # Simulate a document that is far, blurry, and to the left
        flags = (
            DocumentTraits.DT_DOCUMENT_IS_FAR
            | DocumentTraits.DT_DOCUMENT_IS_BLURRY
            | DocumentTraits.DT_DOCUMENT_IS_LEFT
        )

        # Check for distance issues
        has_distance_issue = FlagUtil.has_any(
            flags, DocumentTraits.DT_DOCUMENT_IS_FAR, DocumentTraits.DT_DOCUMENT_IS_CLOSE
        )
        assert has_distance_issue is True

        # Check for position issues
        has_position_issue = FlagUtil.has_any(
            flags,
            DocumentTraits.DT_DOCUMENT_IS_LEFT,
            DocumentTraits.DT_DOCUMENT_IS_RIGHT,
            DocumentTraits.DT_DOCUMENT_IS_UP,
            DocumentTraits.DT_DOCUMENT_IS_DOWN,
        )
        assert has_position_issue is True

    def test_perfect_face_capture(self):
        """Test a perfect face capture with no issues."""
        flags = FaceTraitsFlags.FT_FACE_NO_TRAIT

        # Verify no quality issues
        has_quality_issues = FlagUtil.has_any(
            flags,
            FaceTraitsFlags.FT_IMAGE_BLURR,
            FaceTraitsFlags.FT_FACE_TOO_DARK,
            FaceTraitsFlags.FT_FACE_TOO_BRIGHT,
            FaceTraitsFlags.FT_FACE_TOO_CLOSE,
            FaceTraitsFlags.FT_FACE_TOO_FAR,
        )
        assert has_quality_issues is False

        # Verify no active flags
        active = FlagUtil.get_active_flags(FaceTraitsFlags, flags.value)
        assert len(active) == 0

    def test_mask_detection_scenario(self):
        """Test face with mask detection."""
        flags = FaceTraitsFlags.FT_FACE_WITH_MASK

        assert FlagUtil.has_flag(flags, FaceTraitsFlags.FT_FACE_WITH_MASK)
        names = FlagUtil.get_flag_names(FaceTraitsFlags, flags.value)
        assert "FT_FACE_WITH_MASK" in names

    def test_fingers_over_document_scenario(self):
        """Test document with fingers detected."""
        flags = DocumentTraits.DT_FINGERS_DETECTED | DocumentTraits.DT_DOCUMENT_IS_CLOSE

        # Check if fingers are covering the document
        if FlagUtil.has_flag(flags, DocumentTraits.DT_FINGERS_DETECTED):
            # Would prompt user to remove fingers
            assert True

        # Get all issues
        issues = FlagUtil.get_flag_names(DocumentTraits, flags.value)
        assert "DT_FINGERS_DETECTED" in issues
        assert "DT_DOCUMENT_IS_CLOSE" in issues


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
