import re

from sqlalchemy.exc import IntegrityError

from ..exceptions import  DomainException, UniqueConstraintError

def exception_handler(exc: Exception):
    str_error = str(exc)
    print(str_error)

    if isinstance(exc, IntegrityError) and "UNIQUE constraint failed" in str_error:
        field_match = re.search(r"UNIQUE constraint failed: (?P<field>\S+)", str_error)
        if field_match:
            raise UniqueConstraintError(f"Unique constraint error on field: {field_match.group('field')}")

    raise DomainException(str_error)
