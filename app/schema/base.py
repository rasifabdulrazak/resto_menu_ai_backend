from pydantic import BaseModel
from datetime import datetime
from app.util.datetime.datetime_utils import to_client_timezone


class BaseSchema(BaseModel):
    model_config = {
        "from_attributes": True,
    }

    @classmethod
    def _convert_datetime(cls, value):
        if isinstance(value, datetime):
            return to_client_timezone(value)
        return value

    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        return {
            k: self._convert_datetime(v)
            for k, v in data.items()
        }
