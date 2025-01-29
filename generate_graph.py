from pyscript import document
from sql2mermaid.sql2mermaid import mermaid_generator


def generate_graph(event):
    input_text = document.querySelector("#mermaid-code")
    print("coucou")
    sql_query = input_text.value
    output_div = document.querySelector("#output")
    output_div.innerText = mermaid_generator(sql_query)
