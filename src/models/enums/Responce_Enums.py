from enum import Enum

class ResponseSignal(Enum):
    FILE_UPLODED_SUCCESS = "file_uloded_success"
    FILE_UPLODED_FAILED = "file_uloded_failed"
    FILE_TYPE_NOT_SUPPORTED = "file_type_not_supported_opop"
    FILE_SIZE_EXCEEDED = "file_size_exceeded"
    FILE_VALIDATED_SUCCESS = "file_validated_success"
    PROCESSING_FAILED = "file_processing_failed"