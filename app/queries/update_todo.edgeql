with id:=<uuid><str>$id,
     new_title:=<str>$new_title,
     todo:= (select (select_todo_by_id(id)))
select (update todo
set {
    title:= new_title
}) {id, title};