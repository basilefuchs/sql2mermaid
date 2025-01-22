import polars as pl
import re


def open_sql_file(path: str) -> str:
    try:
        file = open(path, 'r')
        sql_file = file.read()
        file.close()
        return (sql_file)

    except FileNotFoundError as e:
        print(e)


def sql2mermaid(query: str) -> str:

    query = query.lower()
    query = re.sub(r"\n", " ", query)
    query = re.sub(r"\s+", " ", query)
    query = re.sub(r",", " ,", query)
    query = re.sub(r"\s+as\s+", " ", query)
    query = re.sub(r"(?<=where).+", "", query)
    query = re.sub(r"(\w+)?(\s+)?\(.+?\)", "function", query)
    query = re.sub(r"case.+end\s+\w+", "case_when", query)

    if re.search(r"union|minus|intersect", query):
        print("WARNING : sql2mermaid does not support UNION, INTERSECT, MINUS operators.")
    elif re.search(r"^((?!join).)*$", query):
        print("WARNING : sql2mermaid needs a JOIN operation to make a mermaid erDiagram.")
    elif re.search(r"^((?!where).)*$", query):
        print("WARNING : sql2mermaid needs a WHERE clause, so add a dummy 'WHERE 1=1'.")
    elif len(re.findall(r"from", query)) > 1:
        print("WARNING : sql2mermaid does not support multiple FROM clauses.")
    else:
        select_clause = re.findall(r"(?<=select).+(?=from)", query)[0]
        select_clause = select_clause+","
        from_clause = re.findall(r"from.+(?=where)", query)[0]

        column = pl.DataFrame(
            {
                "identifier": [],
                "name": [],
                "alias": []
            }
        ).cast(pl.Utf8)

        table = pl.DataFrame(
            {
                "identifier": [],
                "name": [],
            }
        ).cast(pl.Utf8)

        join = pl.DataFrame(
            {
                "first_table": [],
                "second_table": [],
                "text": []
            }
        ).cast(pl.Utf8)

        for x in re.findall(r"\w+\.\w+.+?,", select_clause):
            if re.search(r"(?<=\s)\w+", x):
                df = pl.DataFrame(
                    {
                        "identifier": [re.search(r"\w+(?=\.)", x)[0]],
                        "name": [re.search(r"(?<=\.)\w+", x)[0]],
                        "alias": [re.search(r"(?<=\s)\w+", x)[0]]
                    }
                )
            else:
                df = pl.DataFrame(
                    {
                        "identifier": [re.search(r"\w+(?=\.)", x)[0]],
                        "name": [re.search(r"(?<=\.)\w+", x)[0]],
                        "alias": [re.search(r"(?<=\.)\w+", x)[0]],
                    }
                )
            column = pl.concat([column, df])

        column = column.with_columns(
            ("dtype "+pl.col("name")+" \""+pl.col("alias")+"\"").alias("name"),
        ).group_by("identifier").agg(pl.col("name").str.concat("\n"))

        for x in re.findall(r"(?<=from|join)\s+\w+\.?\w+\s\w+", from_clause):
            df = pl.DataFrame(
                {
                    "identifier": [re.search(r"\w+$", x)[0]],
                    "name": [re.search(r"\w+\.?\w+(?=\s)", x)[0]],
                }
            )
            table = pl.concat([table, df])

        for x in re.findall(r"\w+\.\w+\s?=\s?\w+\.\w+", from_clause):
            df = pl.DataFrame(
                {
                    "first_table": [re.search(r"\w+(?=\.)", x)[0]],
                    "second_table": [re.search(r"\w+(?=\.\w+$)", x)[0]],
                    "text": [x]
                }
            )
            join = pl.concat([join, df])

        entities = table.join(
            column,
            on="identifier",
            how="left"
        ).with_columns(
            (pl.col("identifier") + "[\"" + pl.col("name") + " as " + pl.col(
                "identifier") + "\"] {\n" + pl.col("name_right").fill_null("") + "\n}").alias("mermaid"),
        )
        # print(entities)
        relations = join.with_columns(
            (pl.col("first_table") + "||--||" + pl.col("second_table") +
             " : \"" + pl.col("text") + "\"").alias("mermaid"),
        )
        result = ""

        # Ajoute chaque contenu avec des retours à la ligne si nécessaire
        result += "%% Note : sql2mermaid does not support SQL functions.\n\n"
        result += "erDiagram\n"
        result += "\n".join(row["mermaid"]
                            for row in entities.iter_rows(named=True)) + "\n"
        result += "\n".join(row["mermaid"]
                            for row in relations.iter_rows(named=True)) + "\n"

        return result
