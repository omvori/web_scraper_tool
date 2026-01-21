import streamlit as st
from scrape import scrape_web,split_dom_content,clean_body_content,extract_body_content
from parse import parse_with_ollama
import pandas as pd
from io import StringIO
import json

st.title("Ai web scraper")
st.write("Upload a JSON file or scrape a site")

########JSON reading#######

uploaded_file = st.file_uploader("Upload a file (JSON only)")

if uploaded_file is not None and json:
    
    data = pd.read_json(uploaded_file)
    
    st.write(data)

    if data is not None: 
        json_description = st.text_area("Descrivi quale informazione vuoi recuperare")

        if st.button("Analizza il file"):
            if json_description:
                st.write("Analizzo..")
                
                json_chunks = split_dom_content(data)
                result = parse_with_ollama(json_chunks,json_description)

                st.write(result)


        
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




