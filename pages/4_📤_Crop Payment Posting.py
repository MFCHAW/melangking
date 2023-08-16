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
if 'posting_status' not in st.session_state:
    st.session_state['posting_status'] = ''
    
if 'posting_message' not in st.session_state:
    st.session_state['posting_message'] = ''

if 'posting_error_message' not in st.session_state:
    st.session_state['posting_error_message'] = pd.DataFrame()
    
url = 'https://prod-44.southeastasia.logic.azure.com:443/workflows/389a4f7fe50a4859b5ad82e0c1e07a06/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=df4frEQoTAazd3SFMO6bs0NYlOW1GXFHXk5CnnUccko'



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
</style>
"""
st.markdown(hide_menu, unsafe_allow_html=True)



# -- Declare containers --
pageSection = st.container()
placeholder = st.empty()
statusMsgSection = st.container()
errorMsgSection = st.container()
retrySection = st.container()


# -- Get Operating Unit Lookup Records --
def get_OUKey(ou):
    if ou == 'LIBO SAWIT PERKASA PALM OIL MILL':
        return 6
    elif ou == 'SEMUNAI SAWIT PERKASA PALM OIL MILL 1':
        return 8
    elif ou == 'SEMUNAI SAWIT PERKASA PALM OIL MILL 2':
        return 9

# -- Get Excel Template: 'Daily Pricing' Lookup Records --
def get_PriceExcelName(ou):
    if ou == 'LIBO SAWIT PERKASA PALM OIL MILL':
        return 'LIBO_FFB Daily Pricing.xlsx'
    elif ou == 'SEMUNAI SAWIT PERKASA PALM OIL MILL 1':
        return 'SSP1_FFB Daily Pricing.xlsx'
    elif ou == 'SEMUNAI SAWIT PERKASA PALM OIL MILL 2':
        return 'SSP2_FFB Daily Pricing.xlsx'

# -- Get Batch No String --
def get_BatchSuppSheetName(batch):
    return 'Batch' + str(batch)

# -- Get Excel Template: 'Payment' Lookup Records --
def get_BatchExcelName(ou):
    if ou == 'LIBO SAWIT PERKASA PALM OIL MILL':
        return 'LIBO_FFB Payment.xlsx'
    elif ou == 'SEMUNAI SAWIT PERKASA PALM OIL MILL 1':
        return 'SSP1_FFB Payment.xlsx'
    elif ou == 'SEMUNAI SAWIT PERKASA PALM OIL MILL 2':
        return 'SSP2_FFB Payment.xlsx'



# -- Trigger Azure Logic App to post the crop payment to account module --
async def paymentPosting(ou, batch):
    session_timeout = aiohttp.ClientTimeout(total=60 * 60 * 24)
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.post(url, data=json.dumps({
            "OUKey": get_OUKey(ou),
            "Batch": batch,
            "BatchSuppSheetName": get_BatchSuppSheetName(batch),
            "PriceExcelName": get_PriceExcelName(ou),
            "BatchExcelName": get_BatchExcelName(ou),
            "UserKey": st.session_state['UserKey']
        }, sort_keys=True), headers={'content-type': 'application/json'}) as response:
            data = await response.json()
            print(data)

            # -- Check the ErrorList table got records. --
            # -- If got record, system show error and return the error records --
            conn = qconnection()
            cursor = conn.cursor()
            
            try:
                cursor.execute(f"""Select OUKey, FPSBatchCode, ErrorMsg as [Error Message] 
                                   from FPS_YYT_BatchErrorList 
                                   Where OUKey = {get_OUKey(ou)} and FPSBatchCode = '{batch}' and 
                                         ProcessType = 'POST'""")
                
                result = []
                columns = [column[0] for column in cursor.description]
                for row in cursor.fetchall():
                    result.append(dict(zip(columns, row)))

                df = pd.DataFrame(result)
                st.session_state['posting_error_message'] = df
                # print(df)
                
            except pymssql.Error as e:
                st.write(f'Error executing query: {e}')
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
            
            if response.status == 200 and data['Status'] == 'Succeeded' and len(result) == 0:
                st.session_state['posting_status'] = 'Succeeded'
                st.session_state['posting_message'] = 'All related payments already being posted!'
            else:
                st.session_state['posting_status'] = 'Failed'
                st.session_state['posting_message'] = 'Error occured during crop payment posting!'

            
def postPayment(ou, batch):
    
    st.session_state['posting_status'] = 'Process'
    st.session_state['posting_message'] = 'Crop payment posting in progress...'
    
    hide_MainPage()
    show_StatusMsg()
    hide_ErrorMsg() 
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(paymentPosting(ou, batch)) 
    
    # time.sleep(3) 
    # st.session_state['posting_status'] = 'Succeeded'
    # st.session_state['posting_message'] = 'All related payments already being posted!'
    
    st.markdown('#')

# -- UI Session --
def show_MainPage():
    with placeholder.container():
        if st.session_state['posting_status'] == '':
            ou = st.selectbox(
                'Mill: ',
                ('LIBO SAWIT PERKASA PALM OIL MILL',
                    'SEMUNAI SAWIT PERKASA PALM OIL MILL 1',
                    'SEMUNAI SAWIT PERKASA PALM OIL MILL 2')
                )

            batch = st.number_input('Batch: ', 1)

            st.markdown('#')

            st.button('Post',
                    on_click=postPayment,
                    args=(ou, batch),
                    help='Click to start the payment posting.')

            st.markdown('#')

            st.write('Please fill in all the information and click "Post" button.')
        

def hide_MainPage():
    placeholder.empty()
    
def show_StatusMsg():
    with statusMsgSection:
        statusMsg.empty()
        
        if st.session_state['posting_status'] == 'Process':
            statusMsg.info(st.session_state['posting_message'])
        elif st.session_state['posting_status'] == 'Succeeded':
            statusMsg.success(st.session_state['posting_message'])
        elif st.session_state['posting_status'] == 'Failed':
            statusMsg.error(st.session_state['posting_message'])
        
def show_ErrorMsg():
    with errorMsgSection:
        if st.session_state['posting_error_message'].any().any():
            # Configure grid options using GridOptionsBuilder
            builder = GridOptionsBuilder.from_dataframe(st.session_state['posting_error_message'])
            builder.configure_pagination(enabled=False)
            builder.configure_selection(selection_mode='single', use_checkbox=False)
            grid_options = builder.build()

            # Display AgGrid
            st.write("Error Details: ")
            st.table(st.session_state['posting_error_message'])
            # ag = AgGrid(st.session_state['pricing_error_message'],
            #         gridOptions=grid_options,
            #         editable=False,
            #         allow_unsafe_jscode=True,
            #         theme='balham',
            #         height=500,
            #         fit_columns_on_grid_load=True,
            #         reload_data=False)

def hide_StatusMsg():
    statusMsgSection.empty()
    
def hide_ErrorMsg():
    errorMsgSection.empty()
    
def show_Retry():
    with retrySection:
        st.button('Retry',
                    on_click=reset_Form,
                    help='Click to retry.')
        
def hide_Retry():
    retrySection.empty()

def reset_Form():
    st.session_state['posting_status'] = ''
    st.session_state['posting_message'] = ''
    st.session_state['posting_error_message'] = ''


with pageSection:
    st.title('Crop Payment Posting')
    statusMsg = st.empty()
    
    if st.session_state['posting_status'] == '':
        show_MainPage()
        hide_StatusMsg()
        hide_ErrorMsg()
        hide_Retry()
    elif st.session_state['posting_status'] == 'Succeeded':
        hide_MainPage()
        show_StatusMsg()
        hide_ErrorMsg()
        hide_Retry()
    elif st.session_state['posting_status'] == 'Failed':
        hide_MainPage()
        show_StatusMsg()
        show_ErrorMsg()
        show_Retry()
            
        
      