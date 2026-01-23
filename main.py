import streamlit as st
from scrape import scrape_web,split_dom_content,clean_body_content,extract_body_content,sorted_id_content,split_id_content
from parse import parse_with_ollama
import pandas as pd
from io import StringIO
import json
import time

st.title("Ai web scraper & JSON analyzer")
st.write("Upload a JSON file or scrape a site")

########JSON reading#######

uploaded_file = st.file_uploader("Upload a file (JSON only)")

if uploaded_file is not None and json:
    @st.cache_data

    
    def load_json(file):
        data = pd.read_json(file)

        st.write(data)
        return sorted_id_content(data)
    
    try: 
        grouped = load_json(uploaded_file)

        json_description = st.text_area("Descrivi quale informazione vuoi recuperare ",placeholder="Es: Un commento su ristorante con id 5")

        if st.button("Analizza il file"):
            if json_description:
                st.write("Analizzo..")
                start_time = time.time()

                if "id" in json_description.lower() or "ristorante" in json_description.lower():
                    import re
                    ids = re.findall(r'\d+', json_description)
                    
                    if ids:
                        filtered_data = {k: v for k, v in grouped.items() if k in ids}
                        elapsed = time.time()-start_time
                        
                        if filtered_data:
                            grouped = filtered_data
                            elapsed = time.time()-start_time

                json_chunks = split_id_content(grouped)
                result = parse_with_ollama(json_chunks,json_description)
                elapsed = time.time()-start_time

                
                st.write(result,"\nTempo passato: ",elapsed)

    except Exception as e:
        st.error(f"Errore nel caricamento del file{e}")












#######Web scraping#######

url = st.text_input("Inserisci un URL")

if st.button("Scrape Site"):
    st.write("Scraping...")
    
    result = scrape_web(url)

    print(result)

    body_cont = extract_body_content(result)
    cleaned_cont = clean_body_content(body_cont)

    st.session_state.dom_content = cleaned_cont

    with st.expander("view DOM content"):
        st.text_area("DOM content", cleaned_cont,height=300)


if "dom_content" in st.session_state:
    parse_description = st.text_area("Descrivi quale informazione vuoi recuperare")

    if st.button("Analizza la pagina"):
        if parse_description:
            st.write("Analizzo..")

            dom_chunks = split_dom_content(st.session_state.dom_content)
            result = parse_with_ollama(dom_chunks,parse_description)
            st.write(result)




