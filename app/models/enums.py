"""
Enumerations for NovaBot system
"""
from enum import Enum


class InputMode(Enum):
    """Enumeration for input modes"""
    SPOKEN = "spoken"
    SIGN_LANGUAGE = "sign_language"
    TOUCH = "touch"


class NotificationType(Enum):
    """Enumeration for notification types"""
    VISUAL = "visual"
    AUDIO = "audio"
    HAPTIC = "haptic"


class FollowMode(Enum):
    """Enumeration for follow modes"""
    ACTIVE = "active"
    INACTIVE = "inactive"


class DataSharingLevel(Enum):
    """Enumeration for data sharing preferences"""
    NONE = "none"
    MINIMAL = "minimal"
    STANDARD = "standard"
    FULL = "full"


class AccessibilityMode(Enum):
    """Enumeration for accessibility preferences"""
    TEXT_ONLY = "text_only"
    VOICE_ENABLED = "voice_enabled"
    MULTIMODAL = "multimodal"

