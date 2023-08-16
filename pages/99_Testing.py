import streamlit as st


text = "geryryryt"
edit = st.checkbox("Edit")
ph = st.empty()
text = ph.text_area("Your code here 👇", text)
if not edit:
    ph.empty()
    # save(code)
    st.code(text, "c++")
