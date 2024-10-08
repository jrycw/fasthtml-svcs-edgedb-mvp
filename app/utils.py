from dataclasses import asdict


def get_todo_id(id: str):
    return f"todo-{id}"


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
