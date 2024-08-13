from dataclasses import asdict

import edgedb
import svcs
from edgedb.asyncio_client import AsyncIOClient
from fasthtml.common import (H1, Button, Card, Div, Form, Group, Input, Main,
                             Title, Ul, fast_app)
from starlette.middleware import Middleware
from starlette.requests import Request

from .lifespan import lifespan
from .models import Todo, TodoCreate
from .queries import create_todo_async_edgeql as create_todo_qry
from .queries import delete_todo_async_edgeql as delete_todo_qry
from .queries import get_todos_async_edgeql as get_todos_qry

app, rt = fast_app(
    lifespan=lifespan,
    middleware=[Middleware(svcs.starlette.SVCSMiddleware)],
)


def mk_input(**kw):
    return Input(id="new-title", name="title", placeholder="New Todo", **kw)


@app.get("/")
async def homepage(request: Request):
    add = Form(
        Group(mk_input(), Button("Add")),
        hx_post="/",
        target_id="todo-list",
        hx_swap="beforeend",
    )
    db_client = await svcs.starlette.aget(request, AsyncIOClient)
    todos = await get_todos_qry.get_todos(db_client)
    todos = [Todo(**asdict(todo)) for todo in todos]
    card = (
        Card(Ul(*todos, id="todo-list"), header=add, footer=Div(id="current-todo")),
    )
    title = "Todo list"
    return Title(title), Main(H1(title), card, cls="container")


@rt("/")
async def post(request: Request, todo: TodoCreate):
    try:
        db_client = await svcs.starlette.aget(request, AsyncIOClient)
        todo = await create_todo_qry.create_todo(db_client, **asdict(todo))
    except edgedb.errors.ConstraintViolationError:
        return
    todo = Todo(**asdict(todo))
    return todo, mk_input(hx_swap_oob="true")


@rt("/{tid}")
async def delete(request: Request, tid: str):
    db_client = await svcs.starlette.aget(request, AsyncIOClient)
    await delete_todo_qry.delete_todo(db_client, **{"id": tid})
