# sql2mermaid
re polars based function to convert a SQL query to mermaid erdiagram

# use

```python
# add your SQL query
q = """SELECT RSS.ID_RSS, D.TYPE_DIAG
FROM CORA_REC.TB_SYNTH_RSS RSS
INNER JOIN CORA_REC.TB_DIAG D ON RSS.ID_SEJOUR=D.ID_SEJOUR AND D.CODE_DIAG = 'C34'
WHERE 1=1"""

# execute function
sql2mermaid(q)
```
