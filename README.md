# fasthtml-svcs-edgedb-mvp
![todo-list](https://raw.githubusercontent.com/jrycw/fasthtml-svcs-edgedb-mvp/refs/heads/master/todo-list.png)

## Description
This repository is focused on building an MVP todo app using `EdgeDB`, `SVCS`, and `FastHTML`.

## EdgeDB schema
```elm
module default {
   type Todo {
      required title: str {
         constraint exclusive;
         constraint min_len_value(1);
         constraint max_len_value(50);
      };
   }

   function select_todo_by_id(tid: uuid) -> Todo
   using (
      select (assert_exists(assert_single((select Todo filter .id=tid))))
   )
}
```

## Steps for this repo
1. Write EdgeQL queries and generate code using `edgedb-py` (stick with version 1.9.0, as v2 may have compatibility issues).
2. Set up the `db_client` in `lifespan.py`.
3. Define the `dataclass` models.
4. Implement the `__ft__()` method for the `Todo` dataclass.
5. Use `svcs.starlette.aget()` to obtain the `AsyncIOClient`.
6. Execute the generated queries to fetch results.
7. Convert the results into `Todo` instances, which FastHTML recognizes as a type of FT component, utilizing the `__ft__()` method we defined.
8. Return the output as FT components.
9. To get started, ensure `EdgeDB` is set up and then run `uvicorn app.main:app --port 8000 --reload`.

## Refs
* [FastHTML todo app](https://gallery.fastht.ml/start_simple/sqlite_todo/app/)
* [FastHTML todo app code](https://gallery.fastht.ml/start_simple/sqlite_todo/code)
* [SVCS Starlette](https://svcs.hynek.me/en/stable/integrations/starlette.html)
* [EdgeDB python query builder](https://docs.edgedb.com/guides/tutorials/rest_apis_with_fastapi)
