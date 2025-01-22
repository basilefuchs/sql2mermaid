from . import sql2mermaid

if __name__ == "__main__":
    query = """
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
    restuls = sql2mermaid(query)
    print(restuls)
