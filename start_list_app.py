import streamlit as st
import pandas as pd

# Inizializza gli stati della sessione
if 'data_a' not in st.session_state:
    st.session_state['data_a'] = pd.DataFrame(columns=[
        "Batteria", "Corsia", "Nome e Cognome", "Classe e Sezione", "Scuola"
    ])

if 'data_b' not in st.session_state:
    st.session_state['data_b'] = pd.DataFrame(columns=[
        "Batteria", "Corsia", "Tempo"
    ])

# Sidebar di navigazione
page = st.sidebar.radio("Vai a", ["Inserisci Atleti", "Inserisci Tempi", "Start List Finale"])

# Pagina 1 – Inserimento Atleti
if page == "Inserisci Atleti":
    st.title("Inserimento Atleti (Tabella A)")

    with st.form("form_a"):
        batteria = st.number_input("Numero Batteria", min_value=1, step=1)
        corsia = st.number_input("Numero Corsia", min_value=1, step=1)
        nome_cognome = st.text_input("Nome e Cognome")
        classe_sezione = st.text_input("Classe e Sezione (es. 2B)")
        scuola = st.text_input("Nome della Scuola (opzionale)")

        submitted = st.form_submit_button("Aggiungi Atleta")

        if submitted:
            new_row = {
                "Batteria": batteria,
                "Corsia": corsia,
                "Nome e Cognome": nome_cognome,
                "Classe e Sezione": classe_sezione,
                "Scuola": scuola
            }
            # CORRETTO: usa concat al posto di append
            st.session_state['data_a'] = pd.concat(
                [st.session_state['data_a'], pd.DataFrame([new_row])],
                ignore_index=True
            )
            st.success("Atleta aggiunto!")

    st.dataframe(st.session_state['data_a'])

# Pagina 2 – Inserimento Tempi
elif page == "Inserisci Tempi":
    st.title("Inserimento Tempi (Tabella B)")

    with st.form("form_b"):
        batteria = st.number_input("Numero Batteria", min_value=1, step=1, key="batt_b")
        corsia = st.number_input("Numero Corsia", min_value=1, step=1, key="corsia_b")
        tempo = st.text_input("Tempo (secondi.centesimi)", key="tempo_b")

        submitted = st.form_submit_button("Aggiungi Tempo")

        if submitted:
            new_row = {
                "Batteria": batteria,
                "Corsia": corsia,
                "Tempo": tempo
            }
            # CORRETTO: usa concat al posto di append
            st.session_state['data_b'] = pd.concat(
                [st.session_state['data_b'], pd.DataFrame([new_row])],
                ignore_index=True
            )
            st.success("Tempo aggiunto!")

    st.dataframe(st.session_state['data_b'])

# Pagina 3 – Start List Finale
elif page == "Start List Finale":
    st.title("Start List Finale")

    if st.session_state['data_a'].empty or st.session_state['data_b'].empty:
        st.warning("Inserisci prima almeno un atleta e un tempo.")
    else:
        # Merge tra le due tabelle su Batteria e Corsia
        merged = pd.merge(
            st.session_state['data_a'],
            st.session_state['data_b'],
            on=["Batteria", "Corsia"],
            how="inner"
        )

        # Ordina per batteria e tempo crescente
        try:
            merged["Tempo_ordinabile"] = merged["Tempo"].apply(lambda x: float(x.replace(",", ".").strip()))
            merged = merged.sort_values(by=["Batteria", "Tempo_ordinabile"])
        except ValueError:
            st.error("Errore nel formato del tempo. Usa formato numerico: es. 10.34")

        st.subheader("Classifiche per Batteria")
        for batteria in sorted(merged["Batteria"].unique()):
            st.markdown(f"### Batteria {batteria}")
            classifica = merged[merged["Batteria"] == batteria][[
                "Corsia", "Nome e Cognome", "Classe e Sezione", "Tempo"
            ]]
            st.dataframe(classifica.reset_index(drop=True))
