from pydantic import BaseModel, Field, validator


class StepModel(BaseModel):
    command: str


class Step(StepModel):
    id: str = Field(..., alias="_id")

    @validator("id", pre=True, always=True)
    def transform_id(cls, v, values):
        return str(v)
