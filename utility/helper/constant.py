from enum import Enum, IntEnum, StrEnum
import uuid

# from dataclasses import dataclass

# @dataclass(frozen=True)
class ErrorCodes(IntEnum):
    SUCCESS: int = 0,
    UPDATE: int = 1,
    FAILED: int = 2,
    EXIST: int = 3,
    NOT_EXIST: int = 4,
    EXCEPTION: int = 5


class Categories(StrEnum):
    UNDERWRITING = "653b59afea1e5dc6adbeb94f"
    CARRIER_CHOICE = "653b5a1dea1e5dc6adbeb953"
    PRODUCTS = "653b5a29ea1e5dc6adbeb955"
    LAWS = "653b5a5cea1e5dc6adbeb95b"
    MISC = "653b5a8fea1e5dc6adbeb961"
    SALES = "65fa7fb58ca327f54d0173ea"


class ActivityFlag(IntEnum):
    ADDED = 1
    EDITED = 2,
    DELETED = 3,


class FilePaths(StrEnum):  # will be relative to storage
    USER_IMAGE = "userimages"
    STRIPE_EVENT_LOGS = "stripeeventlogs"
    EMAIL_TEMPLATES = "emailtemplates"


class Lookups(StrEnum):
    BUSINESS_ROLE = '66595696e9a53d62ad7140d2'
    HEAR_FROM = '66596708e9a53d62ad7140e6'
    DESIGNATION = str(uuid.UUID("7b629e05-d189-4a3c-b4bf-eef38a9ca407"))
    USER_TYPE =str( uuid.UUID("9a607523-0585-4bfc-90ca-92ac1e46b0b2"))
    CITY = str(uuid.UUID("1bc09a9a-37bd-460d-952c-d877ca32e8aa"))
    TOKEN_TYPE =str( uuid.UUID("259cbf1f-bea6-4d72-b95d-c22bbd368675"))
    CASE_TYPE = str(uuid.UUID("30e342a7-642a-4915-9a09-708f57c5d16d"))
    CASE_PRIORITY = str(uuid.UUID("1dd30eb7-bf0c-44b9-9fc5-d6b8f2c0fc08"))
    CASE_STATUS = str(uuid.UUID("1392894e-4da5-442c-8c4e-1fe5b519f8df"))
    CASE_ROLE = str(uuid.UUID("3a383bc8-969b-4db8-afbe-e1fa2e7d3366"))
    CASE_DOCUMENT_TYPE = str(uuid.UUID("7403406c-5d9d-4e56-ad06-75d7a8853b3c"))
    CASE_NOTE_TYPE = str(uuid.UUID("21e56e8d-c6fe-4ffd-bba8-e831da26eed9"))
    BILLING_STATUS = str(uuid.UUID("3c4947ca-4037-4851-ba87-bc51f26c5779"))
    CASE_DIARY_TYPE = str( uuid.UUID("d37fa262-e980-45cb-983b-9d154c867184"))
    # CHAT_ROLE = uuid.UUID("11111111-0000-0000-0000-000000000006")
    # CASE_TYPE = uuid.UUID("11111111-0000-0000-0000-000000000007")
    # SIDE_TYPE = uuid.UUID("11111111-0000-0000-0000-000000000008")
    # EVENT_TYPE = uuid.UUID("11111111-0000-0000-0000-000000000009")
    # SEARCH_TYPE = uuid.UUID("11111111-0000-0000-0000-000000000010")
    # CATEGORY = uuid.UUID("11111111-0000-0000-0000-000000000011")
    # COURT = uuid.UUID("11111111-0000-0000-0000-000000000012")
    # DOCKET_TYPE = uuid.UUID("11111111-0000-0000-0000-000000000013")
    # STAGE = uuid.UUID("11111111-0000-0000-0000-000000000014")
    # TEMPLATE_TYPE = uuid.UUID("11111111-0000-0000-0000-000000000015")
    # CASE_STATUS = uuid.UUID("11111111-0000-0000-0000-000000000016")


class DurationType(StrEnum):
    FIXED = '6659ae4c9bbb09e0e72c5f76'
    DAILY = '6659ae4c9bbb09e0e72c5f77'
    WEEKLY = '6659ae4c9bbb09e0e72c5f78'
    MONTHLY = '6659ae4c9bbb09e0e72c5f79'
    YEARLY = '6659ae4c9bbb09e0e72c5f7a'


class StripePaymentIntentStatus(StrEnum):
    SUCCESS = 'succeeded'
    PROCESSING = 'processing'
    FAILED = 'failed'


class EmployeeStatus(IntEnum):
    INACTIVE = 0
    ACTIVE = 1


class DiscountType(StrEnum):
    FXIED = 'fixed'
    PERCENTAGE = 'percentage'


class UserRole(StrEnum):
    ADMIN = "66ec3ad7d8d900edca9ae257"



  