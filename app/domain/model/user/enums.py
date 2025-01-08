from enum import StrEnum


class Statuses(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DELETED = "deleted"


class Specializations(StrEnum):
    BACKEND = "backend"
    FRONTEND = "frontend"
    FULLSTACK = "fullstack"
    DEVOPS = "devops"
    QA = "qa"
    MOBILE = "mobile"
    DATA_ENGINEER = "data_engineer"
    DATA_SCIENTIST = "data_scientist"
    MACHINE_LEARNING = "machine_learning"
    SECURITY = "security"
    CLOUD_ARCHITECT = "cloud_architect"
    UI_UX = "ui_ux"
    EMBEDDED = "embedded"
    GAME_DEV = "game_dev"
    BLOCKCHAIN = "blockchain"
    DBA = "database_administrator"
    SYSTEMS_ARCHITECT = "systems_architect"
    IOT = "iot"
    AR_VR = "ar_vr"
    TECHNICAL_LEAD = "technical_lead"


class Languages(StrEnum):
    ENGLISH = "english"
    SPANISH = "spanish"
    CHINESE = "chinese"
    HINDI = "hindi"
    ARABIC = "arabic"
    FRENCH = "french"
    BENGALI = "bengali"
    PORTUGUESE = "portuguese"
    RUSSIAN = "russian"
    JAPANESE = "japanese"
    GERMAN = "german"
    KOREAN = "korean"
    TURKISH = "turkish"
    ITALIAN = "italian"
    VIETNAMESE = "vietnamese"
