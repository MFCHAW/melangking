import streamlit as st
import asyncio
import aiohttp
import json
from azure.storage.blob import generate_blob_sas, AccountSasPermissions
from datetime import datetime, timedelta


rpt1_url = 'https://prod-63.southeastasia.logic.azure.com:443/workflows/05c11e1ceecd43ab8b795898fddc0a0f/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=1kBL1jblszIunn9t3x1ZGPuICAz_NDCCmWjTQkiME7w'

# statusMsg = st.empty()

if 'message' not in st.session_state:
    st.session_state['message'] = ''
if 'download_link' not in st.session_state:
    st.session_state['download_link'] = ''

btn_download_report1 = st.button('Financial Profit & Loss Report')

container1 = st.container()
container2 = st.container()

container1.write(st.session_state['message'])
container2.write(st.session_state['download_link'])


def get_download_url(reportName):
    account_name = "lmquartobistorage"
    container_name = "pt-wilian-perkasa/exported_powerbi_reports"
    blob_name = f"{reportName}.xlsx"
    account_key = "wZ/K603M+Z+xTsttYIpbphSeFCuaFG/sQrkwXoeYzRVqUurTsvjJ5nwOLNc3wNOTABpG5Ey/QXmE/dalB5WF8Q=="
    url = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}"
    sas_token = generate_blob_sas(
        account_name=account_name,
        account_key=account_key,
        container_name=container_name,
        blob_name=blob_name,
        permission=AccountSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1)
    )

    report_Url = f"{url}?{sas_token}"
    return report_Url


async def download_financialreport():

    # st.session_state['message'] = 'Processing...'
    # container1.write(st.session_state['message'])

    async with aiohttp.ClientSession() as session:
        async with session.post(rpt1_url, data=json.dumps({
            "reportName": "Financial Report"
        }, sort_keys=True), headers={'content-type': 'application/json'}) as response:
            # data = await response.json()
            # st.write(data)

            if response.status == 200:
                st.session_state['message'] = 'Report processing done! Click the link below to start the report download.'
                container1.write(st.session_state['message'])
                st.session_state['download_link'] = get_download_url(
                    'FinancialReports')
                container2.write(st.session_state['download_link'])
            else:
                st.session_state['message'] = 'Error occured during downloading the report!'
                container1.write(st.session_state['message'])
                st.session_state['download_link'] = ''
                container2.write(st.session_state['download_link'])


if btn_download_report1:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(download_financialreport())
