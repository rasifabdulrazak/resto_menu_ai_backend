from fastapi import Header
from typing import Annotated


TimezoneHeader = Annotated[
    str,
    Header(
        default="UTC",
        description="Client timezone (IANA format)",
        example="Asia/Kolkata",
    ),
]

LanguageHeader = Annotated[
    str,
    Header(
        default="en",
        alias="Accept-Language",
        description="Response language",
        example="en-IN",
    ),
]
