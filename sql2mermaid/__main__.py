from . import sql2mermaid, open_sql_file

if __name__ == "__main__":
    query = open_sql_file("./test.sql")
    restuls = sql2mermaid(query)
    print(restuls)
