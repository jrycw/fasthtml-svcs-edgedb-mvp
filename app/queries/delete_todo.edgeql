with id:= <uuid><str>$id,
     todo:= (select (select_todo_by_id(id)))
select (delete todo) {id, title};