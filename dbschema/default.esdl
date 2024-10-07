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
