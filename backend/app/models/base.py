from datetime import UTC, datetime
from typing import Annotated, Any, Optional

from bson import ObjectId
from pydantic import BaseModel, Field
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema


class ObjectIdPydanticAnnotation:
    @classmethod
    def validate_object_id(cls, v: Any, handler) -> ObjectId:
        if isinstance(v, ObjectId):
            return v

        s = handler(v)
        if ObjectId.is_valid(s):
            return ObjectId(s)
        else:
            raise ValueError("Invalid ObjectId")

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, _handler) -> core_schema.CoreSchema:
        assert source_type is ObjectId
        return core_schema.no_info_wrap_validator_function(
            cls.validate_object_id,
            core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(cls, _core_schema, handler) -> JsonSchemaValue:
        return handler(core_schema.str_schema())


class Model(BaseModel):
    id: Optional[Annotated[ObjectId, ObjectIdPydanticAnnotation]] = None
    created_at: datetime = Field(...,
                                 default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(...,
                                 default_factory=lambda: datetime.now(UTC))

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {datetime: str}
    }
