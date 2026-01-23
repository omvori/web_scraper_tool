from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import time

template = (
    "Analizza le recensioni qui sotto e forniscimi solo le informazioni richieste.\n\n"
    "REVISIONI DA ANALIZZARE:\n{dom_content}\n\n"
    "RICHIESTA UTENTE:\n{json_descr}\n\n"
    "ISTRUZIONI:\n"
    "1. Cerca specificamente l'idRistorante menzionato nella richiesta\n"
    "2. Raggruppa le recensioni per quell'id\n"
    "3. Fornisci un riassunto conciso\n"
    "4. Aggiungi una valutazione in stelle con emoji\n"
    "5. Formato: 'Commento recensione: [testo] "
    "e valutazione in stelle con emoji IN BASE AL NUMERO DI STELLE CHE FORNISCI DEVONO ESSERE LE EMOJI'\n\n"
    "NON inventare informazioni. Rispondi solo in base ai dati forniti."
    "UTILIZZA UN MARKDOWN CHE SIA BELLO DA VEDERE"
)

model = OllamaLLM(model="gemma3:4b",temperature=0.0)

def parse_with_ollama(dom_chunks, json_descr):
    
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model 

    parsed_results = []

    for i,chunk in enumerate(dom_chunks,start=1):

        if len(chunk) > 8000:
            chunk = chunk[:8000]

        start_time = time.time()

        response = chain.invoke(
            {"dom_content":chunk,
             "json_descr":json_descr}
        )
        elapsed = time.time() - start_time

        print(f"Parsed batch {i} of {len(dom_chunks)} in {elapsed:.2f}")
        parsed_results.append(response)

    return "\n".join(parsed_results)