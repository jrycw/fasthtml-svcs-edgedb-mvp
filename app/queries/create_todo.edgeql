with title:= <str>$title,
     todo:= (insert Todo {title:=title})
select todo {id, title};