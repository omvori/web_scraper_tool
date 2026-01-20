import streamlit as st
from scrape import scrape_web,split_dom_content,clean_body_content,extract_body_content
from parse import parse_with_ollama

st.title("Ai web scraper")
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




#Analizzando le recensioni lasciate su questo sito riassumi una valutazione del ristorante descrivendolo cercando di capire l'umore generale delle recensioni lasciate. NON INVENTARE e ATTIENITI ALLA RICHIESTA