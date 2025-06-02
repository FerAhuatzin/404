from enum import Enum
from sqlalchemy import Enum as SQLAlchemyEnum

class UserType(str, Enum):
    individual = "individual"
    organization = "organization"

user_type_enum = SQLAlchemyEnum(
    UserType,
    name="user_type_enum",
    create_type=True,
    validate_strings=True
)

class PackageType(str, Enum):
    free = "free"
    basic = "basic"
    pro = "pro"

package_type_enum =  SQLAlchemyEnum(
    PackageType,
    name="package_type_enum",
    create_type=True,
    validate_strings=True
)
