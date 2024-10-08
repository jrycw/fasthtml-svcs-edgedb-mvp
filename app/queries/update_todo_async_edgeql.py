# AUTOGENERATED FROM 'app/queries/update_todo.edgeql' WITH:
#     $ edgedb-py


from __future__ import annotations
import dataclasses
import edgedb
import uuid


class NoPydanticValidation:
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):
        # Pydantic 2.x
        from pydantic_core.core_schema import any_schema
        return any_schema()

    @classmethod
    def __get_validators__(cls):
        # Pydantic 1.x
        from pydantic.dataclasses import dataclass as pydantic_dataclass
        pydantic_dataclass(cls)
        cls.__pydantic_model__.__get_validators__ = lambda: []
        return []


@dataclasses.dataclass
class UpdateTodoResult(NoPydanticValidation):
    id: uuid.UUID
    title: str


async def update_todo(
    executor: edgedb.AsyncIOExecutor,
    *,
    id: str,
    new_title: str,
) -> UpdateTodoResult:
    return await executor.query_single(
        """\
        with id:=<uuid><str>$id,
             new_title:=<str>$new_title,
             todo:= (select (select_todo_by_id(id)))
        select (update todo
        set {
            title:= new_title
        }) {id, title};\
        """,
        id=id,
        new_title=new_title,
    )
