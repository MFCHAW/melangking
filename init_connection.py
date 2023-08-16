import streamlit as st
import pymssql

def qconnection():
    return pymssql.connect(server='quarto-vm2.southeastasia.cloudapp.azure.com', port='14336', user='quartobi', password='Rohs85#', database='LONE_PTWP')  
    
    
    # return pymssql.connect(
    #     "server"
    #     + st.secrets["server"]
    #     + ";database="
    #     + st.secrets["database"]
    #     + ";user"
    #     + st.secrets["username"]
    #     + ";password"
    #     + st.secrets["password"]
    # )