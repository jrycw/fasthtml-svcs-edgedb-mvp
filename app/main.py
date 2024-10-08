from dataclasses import asdict

import edgedb
import svcs
from edgedb.asyncio_client import AsyncIOClient
from fasthtml.common import (H1, Button, Card, Div, Form, Group, Input, Main,
                             Title, Ul, add_toast, fast_app, setup_toasts)
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
setup_toasts(app)


def mk_input(**kw):
    return Input(id="new-title", name="title", placeholder="New Todo", **kw)


def query2ft(FTdataclass, query_results):
    def _query2ft(FTdataclass, query_result):
        return FTdataclass(**asdict(query_result))

    try:
        return [
            _query2ft(FTdataclass, query_result)
            for query_result in query_results
        ]
    except TypeError:  # not iterable
        return _query2ft(FTdataclass, query_results)


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
    card = (
        Card(
            Ul(*query2ft(Todo, todos), id="todo-list"),
            header=add,
            footer=Div(id="current-todo"),
        ),
    )
    return Title("Todo list built with SVCS, FastHTML, and EdgeDB."), Main(
        H1("Todo list"), card, cls="container"
    )


@rt("/")
async def post(session, request: Request, todo_create: TodoCreate):
    try:
        db_client = await svcs.starlette.aget(request, AsyncIOClient)
        todo = await create_todo_qry.create_todo(
            db_client, **asdict(todo_create)
        )
        return query2ft(Todo, todo), mk_input(hx_swap_oob="true")
    except edgedb.errors.ConstraintViolationError:
        add_toast(
            session,
            f'The title "{todo_create.title}" is duplicated.',
            "error",
        )


@rt("/{tid}")
async def delete(request: Request, tid: str):
    db_client = await svcs.starlette.aget(request, AsyncIOClient)
    await delete_todo_qry.delete_todo(db_client, **{"id": tid})
