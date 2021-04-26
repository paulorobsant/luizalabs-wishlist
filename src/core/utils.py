import datetime
from fastapi.encoders import jsonable_encoder


def from_schema_to_model(schema: any, model: any):
    """
        Transforms schema to a model
    """

    obj_data = jsonable_encoder(model)

    if isinstance(schema, dict):
        update_data = schema
    else:
        update_data = schema.dict(exclude_unset=True)
    for field in obj_data:
        if field in update_data:
            setattr(model, field, update_data[field])

    return model


def get_datetime():
    return datetime.datetime.now(datetime.timezone.utc)
