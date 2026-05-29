import streamlit as st
import pandas as pd
import requests

@st.cache_data
def charger_donnees():
    url = "https://data.culture.gouv.fr/api/explore/v2.1/catalog/datasets/etablissements-cinematographiques/records"
    all_records = []
    offset = 0
    while True:
        r = requests.get(url, params={"limit": 100, "offset": offset})
        results = r.json()["results"]
        all_records.extend(results)
        if len(results) < 100:
            break
        offset += 100
    return pd.DataFrame(all_records)
