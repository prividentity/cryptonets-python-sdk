"""CryptoNets Python SDK - PrivID Face Recognition Library
"""


# Export unified Session (supports both JSON and typed interfaces)
from cryptonets_python_sdk.session import (
    Session,
    SessionError,
    SessionNative,
    ImageInputArg
)

# Export SessionNative and library classes
from cryptonets_python_sdk.library import (
    PrivIDFaceLib,
    PrivIDError
)

# Export all typed data structures from generated types
from cryptonets_python_sdk.idl.gen.privateid_types import (
    # Configuration types
    SessionSettings,
    Collection,
    OperationConfig,

    # Result types
    CallResult,
    CallResultHeader,
    FaceResult,
    DocumentResult,
    CompareResult,
    EnrollData,
    PredictData,
    IsoImageResult,
    BarcodeDetectionResult,
    UserDeleteResponse,

    # Geometry types
    PointF,
    BoxF,
    TrapezeF,
    OvalF,
    FaceGeometry,

    # Detail types
    FaceId,
    FaceMetric,
    AgeData,
    DocumentData,
    DocumentOcrAgeData,
    BarCodeData,
    EnrollResponse,
    PredictResponse,
    PredictUserInformation,
    AntispoofingHint,
    FaceDetectionData,
    Image,
    ImageInfo,
    NamedUrl,

    # Enum types
    ReturnStatus,
    FaceTraitsFlags,
    DocumentTraits,
    SpoofStatus,
    BarCodeDetectionStatus,
    Depth,
    Color,
)

# Export flag utility class
from cryptonets_python_sdk.flags import (
    FlagUtil,
)

__all__ = [
    # Version
    "__version__",

    # Main classes
    "Session",           # Unified session supporting both JSON and typed interfaces
    "SessionNative",     # Direct native session (JSON only, for advanced use)
    "ImageInputArg",
    "PrivIDFaceLib",

    # Exceptions
    "PrivIDError",
    "SessionError",

    # Configuration types
    "SessionSettings",
    "Collection",
    "OperationConfig",

    # Result types
    "CallResult",
    "CallResultHeader",
    "FaceResult",
    "DocumentResult",
    "CompareResult",
    "EnrollData",
    "PredictData",
    "IsoImageResult",
    "BarcodeDetectionResult",
    "UserDeleteResponse",

    # Geometry types
    "PointF",
    "BoxF",
    "TrapezeF",
    "OvalF",
    "FaceGeometry",

    # Detail types
    "FaceId",
    "FaceMetric",
    "AgeData",
    "DocumentData",
    "DocumentOcrAgeData",
    "BarCodeData",
    "EnrollResponse",
    "PredictResponse",
    "PredictUserInformation",
    "AntispoofingHint",
    "FaceDetectionData",
    "Image",
    "ImageInfo",
    "NamedUrl",

    # Enums
    "ReturnStatus",
    "FaceTraitsFlags",
    "DocumentTraits",
    "SpoofStatus",
    "BarCodeDetectionStatus",
    "Depth",
    "Color",

    # Utility class for flag operations
    "FlagUtil",
]
