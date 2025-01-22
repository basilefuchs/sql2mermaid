# sql2mermaid
A module to convert an SQL query into a mermaid erDiagram.

# use CLI

```bash
python -m sql2mermaid --input /my/sqlfile.sql
```

# use API

```python
# add your SQL query
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
ORDER BY b.date"""

# execute function
sql2mermaid(q)
```
# result

```
%% Note : sql2mermaid does not support SQL functions.

erDiagram
a["employee as a"] {
dtype patient_id "patient_id"
dtype last_name "last_name"
dtype first_name "first_name"
}
b["drugs as b"] {
dtype drug "drug"
dtype date "date"
}
c["deaths as c"] {

}
a||--||b : "a.patient_id = b.patient_id"
a||--||c : "a.patient_id = c.patient_id"
```
> Note : past result on [Mermaid Live editor](https://mermaid.live/)
