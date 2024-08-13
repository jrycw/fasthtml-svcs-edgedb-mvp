with id:= <uuid><str>$id,
     todo:= (select (select_todo_by_id(id)))
select todo {id, title};