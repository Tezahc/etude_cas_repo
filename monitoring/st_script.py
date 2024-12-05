import streamlit as st
import pandas as pd
import numpy as np

st.write("""
# My first app
on essaye de créer un tableau
""")

st.title("Chapitre 0")

df = pd.DataFrame(
    np.random.randn(20, 4),
    columns= [10, 20, 30, 40]
)

x = st.slider('x')
st.write(x, 'squared is:', x * x)

st.line_chart(df)

st.navigation({
    "Page 1": [
        st.Page("chapitre_1.py", title="Chapitre 1"), 
        st.Page("chapitre_2.py", title="Chapitre 2")
    ],
    "Reports": [
        st.Page("overview.py", title="Overview"), 
        st.Page("usage.py", title="Usage")
    ]
})