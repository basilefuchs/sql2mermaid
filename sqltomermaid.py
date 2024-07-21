import polars as pl
import re

def sql2mermaid(q) :
    q = re.sub(r"\n"," ", q).lower()
    if re.search(r"union", q):
        print("WARNING : sql2mermaid does not support SQL queries with UNION.")
    elif re.search(r"^((?!join).)*$", q):
        print("WARNING : sql2mermaid needs a JOIN argument to make a mermaid erDiagram.")
    elif re.search(r"^((?!where).)*$", q):
        print("WARNING : sql2mermaid needs a WHERE clause, so add a dummy 'WHERE 1=1'.")
    else:
        select_clause = re.findall(r"(?<=select).+(?=from)", q)[0]
        from_clause = re.findall(r"(?<=from).+(?=where)", q)[0]
        from_clause = "from"+from_clause

        column = pl.DataFrame(
            {
                "identifier" : [],
                "name" : []
            }
        ).cast(pl.Utf8)

        table = pl.DataFrame(
            {
                "identifier" : [],
                "name" : [],
            }
        ).cast(pl.Utf8)

        join = pl.DataFrame(
            {
                "first_table" : [],
                "second_table" : [],
                "text" : []
            }
        ).cast(pl.Utf8)

        for x in re.findall(r"\w+\.\w+", select_clause) :
            df = pl.DataFrame(
                {
                    "identifier" : [re.search(r"\w+(?=\.)",x)[0]],
                    "name" : [re.search(r"(?<=\.)\w+",x)[0]]
                }
            )
            column = pl.concat([column,df])

        for x in re.findall(r"(?<=from|join)\s+\w+\.?\w+\s\w+", from_clause) :
            df = pl.DataFrame(
                {
                    "identifier" : [re.search(r"\w+$",x)[0]],
                    "name" : [re.search(r"\w+\.?\w+(?=\s)",x)[0]],
                }
            )
            table = pl.concat([table,df])


        for x in re.findall(r"\w+\.\w+\s?=\s?\w+\.\w+", from_clause) :
            df = pl.DataFrame(
                {
                    "first_table" : [re.search(r"\w+(?=\.)",x)[0]],
                    "second_table" : [re.search(r"\w+(?=\.\w+$)",x)[0]],
                    "text" : [x]
                }
            )
            join = pl.concat([join,df])

        column = column.with_columns(
            ("dtype "+pl.col("name")).alias("name"),
        ).group_by("identifier").agg(pl.col("name").str.concat("\n"))

        entities = table.join(
            column,
            on= "identifier",
            how="left"
        ).with_columns(
            (pl.col("name_right").fill_null("")),
        ).with_columns(
            (pl.col("identifier") + "[\"" + pl.col("name") + " AS " + pl.col("identifier") + "\"] {\n" + pl.col("name_right") + "\n}").alias("mermaid"),
        )

        relations = join.with_columns(
            (pl.col("first_table") + "||--||" + pl.col("second_table") + " : \"" + pl.col("text") + "\"").alias("mermaid"),
        )
        print("erDiagram")
        [print(row["mermaid"]) for row in entities.iter_rows(named=True)]
        [print(row["mermaid"]) for row in relations.iter_rows(named=True)]
