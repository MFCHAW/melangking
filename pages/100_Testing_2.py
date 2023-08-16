# import streamlit as st
# import os
# from pathlib import Path
# download_path = str(Path.home()/'Downloads')
# st.write(download_path)


# path = 'C:/FPS_Downloaded_Reports'

# # check whether directory already exists
# if not os.path.exists(path):
#     os.mkdir(path)
#     print("Folder %s created!" % path)
# else:
#     print("Folder %s already exists" % path)


# import requests

# url = 'https://www.facebook.com/favicon.ico'
# response = requests.get(url, allow_redirects=True)

# open('C:/Downloads/facebook.ico', 'wb').write(response.content)


# st.header("Container")
# chk1 = st.checkbox(label="Trigger Text change")

# container = st.container()

# with st.container():
#     st.write("This is inside the container 1")

# with st.container():
#     st.write("This is inside the container 2")

# if chk1:
#     container.write("First Choice")
# else:
#     container.write("Second Choice")
