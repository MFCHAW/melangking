import streamlit as st
import pymssql

def qconnection():
    return pymssql.connect(server=st.secrets["server"], port=st.secrets["port"], user=st.secrets["username"], password=st.secrets["password"], database=st.secrets["database"])