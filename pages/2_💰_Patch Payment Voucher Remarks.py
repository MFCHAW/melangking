import streamlit as st
import asyncio
import aiohttp
import json
import pymssql
from streamlit_javascript import st_javascript
from streamlit_extras.switch_page_button import switch_page
from init_connection import qconnection
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
import time

# -- Variables and Session States Initialization --
if 'patch_status' not in st.session_state:
    st.session_state['patch_status'] = ''
    
if 'patch_message' not in st.session_state:
    st.session_state['patch_message'] = ''

url = 'https://prod-27.southeastasia.logic.azure.com:443/workflows/0c80d99c63e64c27925ded0ea3f8bbaf/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=vLWcNfx7Bp_OBclccXV-dWFzDu_b5Waa1w-nkmw9m4Q'



# --- Auto Navigate to Login form if haven't login yet --
if 'loggedIn' not in st.session_state:
    st.session_state['loggedIn'] = False

if st.session_state['loggedIn'] == False:
    switch_page('Home')
    st.stop()
    
# -- Remove the 'Streamlit' label at Page title --    
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
                background-image: url('https://lmquartobistorage.blob.core.windows.net/melangking/mopp.png');
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
</style>
"""
st.markdown(hide_menu, unsafe_allow_html=True)



# -- Declare containers --
pageSection = st.container()
placeholder = st.empty()
statusMsgSection = st.container()
errorMsgSection = st.container()
retrySection = st.container()

# -- Trigger Azure Logic App to compute the crop payment pricing --
async def patchRemarks(year, month):
    session_timeout = aiohttp.ClientTimeout(total=60 * 60 * 24)
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.post(url, data=json.dumps({
            "Year": year,
            "Month": month
        }, sort_keys=True), headers={'content-type': 'application/json'}) as response:
            data = await response.json()
            print(data)

            if response.status == 200 and data['Status'] == 'Succeeded':
                st.session_state['patch_status'] = 'Succeeded'
                st.session_state['patch_message'] = 'Payment voucher Remarks already being patched!'
            else:
                st.session_state['patch_status'] = 'Failed'
                st.session_state['patch_message'] = 'Error occured during payment voucher remark patching!'

            
def callPatchRemarks(year, month):
    
    st.session_state['patch_status'] = 'Process'
    st.session_state['patch_message'] = 'Processing...'
    
    hide_MainPage()
    show_StatusMsg()
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(patchRemarks(year, month)) 
    
    st.markdown('#')

# -- UI Session --
def show_MainPage():
    with placeholder.container():
        if st.session_state['patch_status'] == '':

            year = st.number_input('Payment Year: ', 2023)
            
            month = st.number_input('Payment Month: ', 8)

            st.markdown('#')

            st.button('Patch',
                    on_click=callPatchRemarks,
                    args=(year, month),
                    help='Click to start patch the payment voucher remarks.')

            st.markdown('#')

            st.write('Please fill in all the information and click "Patch" button.')
        

def hide_MainPage():
    placeholder.empty()
    
def show_StatusMsg():
    with statusMsgSection:
        statusMsg.empty()
        
        if st.session_state['patch_status'] == 'Process':
            statusMsg.info(st.session_state['patch_message'])
        elif st.session_state['patch_status'] == 'Succeeded':
            statusMsg.success(st.session_state['patch_message'])
        elif st.session_state['patch_status'] == 'Failed':
            statusMsg.error(st.session_state['patch_message'])
        

def hide_StatusMsg():
    statusMsgSection.empty()
    
def show_Retry():
    with retrySection:
        st.button('Retry',
                    on_click=reset_Form,
                    help='Click to retry.')
        
def hide_Retry():
    retrySection.empty()

def reset_Form():
    st.session_state['patch_status'] = ''
    st.session_state['patch_message'] = ''

with pageSection:
    st.title('Patch Payment Voucher Remarks')
    statusMsg = st.empty()
    
    if st.session_state['patch_status'] == '':
        show_MainPage()
        hide_StatusMsg()
        hide_Retry()
    elif st.session_state['patch_status'] == 'Succeeded':
        hide_MainPage()
        show_StatusMsg()
        show_Retry()
    elif st.session_state['patch_status'] == 'Failed':
        hide_MainPage()
        show_StatusMsg()
        show_Retry()
            
        
      