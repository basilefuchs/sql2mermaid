from pyscript import document
import sql2mermaid


def generate_graph(event):
    input_text = document.querySelector("#mermaid-code")
    print("coucou")
    sql_query = input_text.value
    output_div = document.querySelector("#output")
    output_div.innerText = sql2mermaid.sql2mermaid(sql_query)
