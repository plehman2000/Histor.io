
import utils
from utils import BSTNode, Person, reformat
import altair as alt
import numpy as np
# import pandas as pd
import pydeck as pdk
import streamlit as st
import random
import pandas as pd
import pickle



st.set_page_config(layout="wide", page_title="3a", page_icon=":skull:")
st.header("Histor.io - Finding Contemporary Media for Historical Figures")
st.session_state["algotype"] = st.select_slider("Data Structure:", ["Hashmap", "BST"])

st.session_state['random'] = st.button("Random")
# if "random" not in st.session_state.keys() or st.session_state['random'] == False:



   
if st.session_state['random']:
    HISTORY_DF = pd.read_csv("ages_trimmed.csv")
    MOVIES = pickle.load(open("age-movies.pkl", "rb"))
    print("loaded")
    index = random.randrange(0, len(HISTORY_DF))
    option = HISTORY_DF.iloc[index]
    print(option)
    p = Person(option)
    st.write(p)
    print(f"|{p.wikidata}|")
    st.write(p.wikidata if hasattr(p, "wikidata") else "No Wikipedia Data Available")
    year = random.randrange(p.birth, p.death)
    st.subheader(f"Movies from the Year {year}")
    st.write(f"{p.name} was {year-p.birth} year(s) old")
    if st.session_state["algotype"] == "Hashmap": 
        if year in MOVIES:
            st.table(MOVIES[year])
        else:
            st.write("No Media Available for selected year")
    elif st.session_state["algotype"] == "BST":
        keys = sorted(MOVIES.keys())
        head = BSTNode(reformat(MOVIES[keys[0]], keys[0]))
        for val in keys[1:]:
            head.insert(reformat(MOVIES[val], val))
        
        st.table(list(head.search(year)))



