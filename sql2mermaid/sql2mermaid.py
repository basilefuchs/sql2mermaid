import polars as pl
import re

# add query here
q = """
SELECT 
  a.patient_id,
  a.last_name,
  a.first_name,
  b.drug,
  b.date
FROM employee a
INNER JOIN drugs b on a.patient_id = b.patient_id
LEFT JOIN deaths c on a.patient_id = c.patient_id
WHERE
c.patient_id is null
ORDER BY b.date
"""

def sql2mermaid(q) :
    
    q = q.lower()
    q = re.sub(r"\n"," ", q)
    q = re.sub(r"\s+"," ", q)
    q = re.sub(r","," ,", q)
    q = re.sub(r"\s+as\s+"," ", q)
    q = re.sub(r"(?<=where).+","", q)
    q = re.sub(r"(\w+)?(\s+)?\(.+?\)","function", q)
    q = re.sub(r"case.+end\s+\w+","case_when", q)
    
    if re.search(r"union|minus|intersect", q):
        print("WARNING : sql2mermaid does not support UNION, INTERSECT, MINUS operators.")
    elif re.search(r"^((?!join).)*$", q):
        print("WARNING : sql2mermaid needs a JOIN operation to make a mermaid erDiagram.")
    elif re.search(r"^((?!where).)*$", q):
        print("WARNING : sql2mermaid needs a WHERE clause, so add a dummy 'WHERE 1=1'.")
    elif len(re.findall(r"from", q)) > 1 :
        print("WARNING : sql2mermaid does not support multiple FROM clauses.")
    else:
        select_clause = re.findall(r"(?<=select).+(?=from)", q)[0]
        select_clause = select_clause+","
        from_clause = re.findall(r"from.+(?=where)", q)[0]

        column = pl.DataFrame(
            {
                "identifier" : [],
                "name" : [],
                "alias" : []
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

        for x in re.findall(r"\w+\.\w+.+?,", select_clause) :
            if re.search(r"(?<=\s)\w+",x):
                df = pl.DataFrame(
                    {
                        "identifier" : [re.search(r"\w+(?=\.)",x)[0]],
                        "name" : [re.search(r"(?<=\.)\w+",x)[0]],
                        "alias" : [re.search(r"(?<=\s)\w+",x)[0]]
                    }
                )
            else:
                 df = pl.DataFrame(
                    {
                        "identifier" : [re.search(r"\w+(?=\.)",x)[0]],
                        "name" : [re.search(r"(?<=\.)\w+",x)[0]],
                        "alias" : [re.search(r"(?<=\.)\w+",x)[0]],
                    }
                 )
            column = pl.concat([column,df])

        column = column.with_columns(
            ("dtype "+pl.col("name")+" \""+pl.col("alias")+"\"").alias("name"),
        ).group_by("identifier").agg(pl.col("name").str.concat("\n"))
        
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

        entities = table.join(
            column,
            on= "identifier",
            how="left"
        ).with_columns(
            (pl.col("identifier") + "[\"" + pl.col("name") + " as " + pl.col("identifier") + "\"] {\n" + pl.col("name_right").fill_null("") + "\n}").alias("mermaid"),
        )
        # print(entities)
        relations = join.with_columns(
            (pl.col("first_table") + "||--||" + pl.col("second_table") + " : \"" + pl.col("text") + "\"").alias("mermaid"),
        )
        print("%% Note : sql2mermaid does not support SQL functions.\n")
        print("erDiagram")
        [print(row["mermaid"]) for row in entities.iter_rows(named=True)]
        [print(row["mermaid"]) for row in relations.iter_rows(named=True)]

sql2mermaid(q)
