from fastapi import APIRouter

from db.steps import StepCRUD
from fastapi import Depends

from model.step import StepModel

steps_router = APIRouter()


@steps_router.get("")
def get_steps(step_crud: StepCRUD = Depends()):
    return [step.dict(by_alias=True) for step in step_crud.get_all()]


@steps_router.get("/{step_id}")
def get_step(step_id: str, step_crud: StepCRUD = Depends()):
    return step_crud.get_by_id(step_id).dict(by_alias=True)


@steps_router.post("")
def create_step(step: StepModel, step_crud: StepCRUD = Depends()):
    return step_crud.insert(step).dict(by_alias=True)


@steps_router.delete("/{step_id}")
def delete_step(step_id, step_crud: StepCRUD = Depends()):

    deleted_element =  step_crud.delete(step_id)
    if not deleted_element:
        return "This document has already been removed."
    return deleted_element.dict(by_alias=True)


@steps_router.put("/{step_id}")
def edit_step(step_id, step: StepModel, step_crud: StepCRUD = Depends()):
    return step_crud.update(step_id, step).dict(by_alias=True)
