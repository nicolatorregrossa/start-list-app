import streamlit as st
import pandas as pd

if 'data_a' not in st.session_state:
    st.session_state['data_a'] = pd.DataFrame(columns=[
        "Batteria", "Corsia", "Nome e Cognome", "Classe e Sezione", "Scuola"
    ])

if 'data_b' not in st.session_state:
    st.session_state['data_b'] = pd.DataFrame(columns=[
        "Batteria", "Corsia", "Tempo"
    ])

page = st.sidebar.radio("Vai a", ["Inserisci Atleti", "Inserisci Tempi", "Start List Finale"])

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
            st.session_state['data_a'] = pd.concat(
                [st.session_state['data_a'], pd.DataFrame([new_row])],
                ignore_index=True
            )
            st.success("Atleta aggiunto!")

    st.dataframe(st.session_state['data_a'])

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
            st.session_state['data_b'] = pd.concat(
                [st.session_state['data_b'], pd.DataFrame([new_row])],
                ignore_index=True
            )
            st.success("Tempo aggiunto!")

    st.dataframe(st.session_state['data_b'])

elif page == "Risultati Finali":

import streamlit as st
import pandas as pd

st.title("Risultati Finali")

if 'data_a' in st.session_state and 'data_b' in st.session_state:
    df_a = st.session_state['data_a']
    df_b = st.session_state['data_b']

    if not df_a.empty and not df_b.empty:
        merged = pd.merge(df_a, df_b, on=['batteria', 'corsia'])

        merged.sort_values(by=['batteria', 'tempo'], inplace=True)

        batterie = merged['batteria'].unique()
        for b in sorted(batterie):
            st.subheader(f"Batteria {b}")
            classifica = merged[merged['batteria'] == b][
                ['corsia', 'nome', 'classe', 'tempo']
            ].reset_index(drop=True)
            classifica.index += 1  # per numerare le posizioni
            st.table(classifica)
    else:
        st.warning("⚠️ Inserisci almeno un dato in entrambe le tabelle.")
else:
    st.warning("⚠️ Le tabelle non sono ancora state inizializzate.")

            st.dataframe(classifica.reset_index(drop=True))
