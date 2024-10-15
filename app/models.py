from dataclasses import dataclass

from fasthtml.common import A, Li, Strong

from .utils import get_todo_id


# TODO: Would `Todo` be improved by subclassing `TodoCreate`?
@dataclass
class Todo:
    id: str
    title: str

    def __ft__(self):
        show = Strong(self.title, target_id="current-todo")
        delete = A(
            "delete",
            hx_delete=f"/{self.id}",
            hx_target=f"#{get_todo_id(self.id)}",
            hx_swap="outerHTML",
        )
        return Li(show, " | ", delete, id=get_todo_id(self.id))


@dataclass
class TodoCreate:
    title: str
