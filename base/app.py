# Shaheer Syed
# This work was inspired by the ESM Fold Protein Structure Prediction by Meta

# Importing Important Libraries
import streamlit as st
from stmol import showmol
import py3Dmol
import requests
import biotite.structure.io as bsio

# Setting-up Streamlit Web Page Configuration
st.set_page_config(page_title='Protein Structure Prediction using ESMFold')

# Formatting Streamlit Webpage using CSS Style
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#
#
#

# base\app.py

# User Input for Protein Sequence