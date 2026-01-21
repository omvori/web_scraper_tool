from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = (
    "Sei un critico molto famoso che valuta ristoranti in tutto il mondo,sei preciso, esplicativo e in gamba nel tuo lavoro"
    "Analizza queste recensioni di un ristorante e fornisci un commento riassuntivo,di qualche riga che valuti complessivamente il ristorante.\n\n"
    "inoltre valuta in stelle da 1 a 5 la positività o negatività del ristorante, usa un emoji per rappresentare le stelle" \
    "con 1 stella che rappresenta il minimo e 5 stelle che rappresentano il massimo. Sii preciso"
    "****NON DARE NOMI INVENTATI AL  RISTORANTE*****"
    "****ATTIENITI A QUELLO CHE DICE L'UTENTE,SE VIENE OMESSO ANCHE DALL'UTENTE NON INCLUDERE IL NOME DEL RISTORANTE****"
    "Recensioni:\n{dom_content}\n\n"
    "TIENI CONTO che il campo GRADIMENTO e CONTRASTO si riferiscono all'apprezzamento del commento da parte di altri utenti"
    "Commento riassuntivo:"
)



model = OllamaLLM(model="gemma3:4b")

def parse_with_ollama(dom_chunks, parse_descr):
    
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model 

    parsed_results = []

    for i,chunk in enumerate(dom_chunks,start=1):
        response = chain.invoke(
            {"dom_content":chunk,"parse_descr":parse_descr}
        )

        print(f"Parsed batch {i} of {len(dom_chunks)}")
        parsed_results.append(response)

    return "\n".join(parsed_results)