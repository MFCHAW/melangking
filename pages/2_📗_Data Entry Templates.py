import streamlit as st
from streamlit_extras.switch_page_button import switch_page

# --- Auto Navigate to Login form if haven't login yet --
if 'loggedIn' not in st.session_state:
    st.session_state['loggedIn'] = False

if st.session_state['loggedIn'] == False:
    switch_page('Home')
    st.stop()
  1  
# 1-- Remove the 'Streamlit' label at Page title --    
def set_page_title(title):
    st.sidebar.markdown(unsafe_allow_html=True, body=f"""
        <iframe height=0 srcdoc="<script>
            const title = window.parent.document.querySelector('title') \
                
            const oldObserver = window.parent.titleObserver
            if (oldObserver) {{
                oldObserver.disconnect()
            }} \

            const newObserver = new MutationObserver(function(mutations) {{
                const target = mutations[0].target
                if (target.text !== '{title}') {{
                    target.text = '{title}'
                }}
            }}) \

            newObserver.observe(title, {{ childList: true }})
            window.parent.titleObserver = newObserver \

            title.text = '{title}'
        </script>" />
    """)


set_page_title("PT Wilian - FFB Procurement")
    

# --- Display Client Logo ---
def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url('https://lmquartobistorage.blob.core.windows.net/pt-wilian-perkasa/PTWP_Logo.png');
                background-repeat: no-repeat;
                padding-top: 10px;
                background-position: 20px 25px;
            }
            # [data-testid="stSidebarNav"]::before {
            #     content: "FFB Procurement Application";
            #     margin-left: 10px;
            #     margin-top: 20px;
            #     font-size: 19px;
            #     position: relative;
            #     top: 100px;
            # }
        </style>
        """,
        unsafe_allow_html=True,
    )

add_logo()  


# --- Hide the Streamlit Menu Button and Trade Marks ---
hide_menu = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.viewerBadge_link_qRIco {visibility: hidden;}
</style>
"""
st.markdown(hide_menu, unsafe_allow_html=True)  



st.title('Data Entry Template')

st.markdown('''
    ## Spreadsheet Links:
    ### A) Daily Pricing:
    #### 1. [Libo - FFB Daily Pricing](https://lintramaxmy.sharepoint.com/:x:/r/sites/LMShared/Shared%20Documents/Wilian%20Perkasa/FFB%20Procurement%20Live%20Templates/Libo_FFB%20Daily%20Pricing.xlsx?d=wef3f86df1dd34f8bbf5ae08d84ab71f5&csf=1&web=1&e=MgfU31)
    #### 2. [SSP1 - FFB Daily Pricing](https://lintramaxmy.sharepoint.com/:x:/r/sites/LMShared/Shared%20Documents/Wilian%20Perkasa/FFB%20Procurement%20Live%20Templates/SSP1_FFB%20Daily%20Pricing.xlsx?d=w3075a5e13f4142b8be39d3361549243d&csf=1&web=1&e=NLm3Fm)
    #### 3. [SSP2 - FFB Daily Pricing](https://lintramaxmy.sharepoint.com/:x:/r/sites/LMShared/Shared%20Documents/Wilian%20Perkasa/FFB%20Procurement%20Live%20Templates/SSP2_FFB%20Daily%20Pricing.xlsx?d=wd1d318dc86bc4bb69331d345a9289ef5&csf=1&web=1&e=OU1BRA)
''')

st.markdown('#')

st.markdown('''
    ### A) Crop Payment:
    #### 1. [Libo - FFB Payment](https://lintramaxmy.sharepoint.com/:x:/r/sites/LMShared/Shared%20Documents/Wilian%20Perkasa/FFB%20Procurement%20Live%20Templates/Libo_FFB%20Payment.xlsx?d=w9692e6b3654e45859262acbf82d0ff5a&csf=1&web=1&e=H0l5AN)
    #### 2. [SSP1 - FFB Payment](https://lintramaxmy.sharepoint.com/:x:/r/sites/LMShared/Shared%20Documents/Wilian%20Perkasa/FFB%20Procurement%20Live%20Templates/SSP1_FFB%20Payment.xlsx?d=wc6637a0b448247b0979a912a9bfa1c6c&csf=1&web=1&e=F3EhYg)
    #### 3. [SSP2 - FFB Payment](https://lintramaxmy.sharepoint.com/:x:/r/sites/LMShared/Shared%20Documents/Wilian%20Perkasa/FFB%20Procurement%20Live%20Templates/SSP2_FFB%20Payment.xlsx?d=wcd35c797c71942858854c0634abd7598&csf=1&web=1&e=mXbVls)
''')
