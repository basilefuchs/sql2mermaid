# sql2mermaid
a function to convert an SQL query into a mermaid erDiagram.

# use

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
WHERE 1=1
ORDER BY b.date"""

# execute function
sql2mermaid(q)
```
