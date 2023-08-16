import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.switch_page_button import switch_page

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


# -- Report Listing Options --
reportList = ['FFB Receiption & Pricing', 'Daily FFB Proceeds', 'FFB Proceeds Summary',
              'FFB Proceeds Detail', 'FFB Proceeds Statement']

comboBoxReport = st.sidebar.selectbox(
    'Please select a report: ',
    (reportList)
)


if comboBoxReport == 'FFB Receiption & Pricing':
    js = '''
    // Server Site (Function App) Url
    var getEmbedToken = "https://powerbisample-01.azurewebsites.net/api/HttpTriggerCSharp1?code=TY1xGH30Yxr0/W3SD/FJuvhHxIT0OfDbsLCjEL7Giky9lmx7NRTdYQ==";

    var tokenExpiration = Date.now();

    // Start to preview report
    // ***********************
    function previewReport() {
        $.ajax({
            url: getEmbedToken,
            data: { PBIE_GROUP_ID: '645a9f59-ea89-457e-9a5a-68832c747f5a', PBIE_REPORT_ID : '7b7f5bc3-1f93-470a-99e3-1ada1e9032ee'},
            jsonpCallback: 'callback',
            contentType: 'application/javascript',
            dataType: "jsonp",
            success: function (json) {
                var models = window['powerbi-client'].models;
                var embedConfiguration = {
                    type: 'report',
                    id: json.ReportId,
                    embedUrl: json.EmbedUrl,
                    tokenType: models.TokenType.Embed,
                    accessToken: json.EmbedToken,
                    permissions: models.Permissions.All,
                    viewMode: models.ViewMode.View,
                    settings: {
                        filterPaneEnabled: false,
                        navContentPaneEnabled: false
                    }
                };
                
                var $reportContainer = $('#reportContainer');
                var report = powerbi.embed($reportContainer.get(0), embedConfiguration);
            },
            error: function () {
                alert("Error");
            }
        });
    }


    // Refresh Report Data
    // *******************
    function refreshReport() {
            // Get a reference to the embedded report HTML element
            var $reportContainer = $('#reportContainer'); 
    
            // Get a reference to the embedded report.
            report = powerbi.get($reportContainer.get(0));
    
            // Refresh the displayed report
            report.refresh()
                .then(function (result) {
                    console.log("Refreshed");
                })
                .catch(function (errors) {
                    console.log(errors);
                });
    }


    // Reload Report
    // *************
    function reloadReport() {
            // Get a reference to the embedded report HTML element
            var $reportContainer = $('#reportContainer'); 
    
            // Get a reference to the embedded report.
            report = powerbi.get($reportContainer.get(0));
    
            // Reload the displayed report
            report.reload()
                .then(function (result) {
                console.log("Report Reloaded");
            })
            .catch(function (errors) {
                console.log(errors);
            });
    }


    // Refresh Token
    // *************
    function setTokenExpirationListener(tokenExpiration, minutesToRefresh = 2,)
    {
            // get current time
            var currentTime = Date.now();
            var expiration = Date.parse(tokenExpiration);
            var safetyInterval = minutesToRefresh* 60 * 1000;

            // time until token refresh in milliseconds
            var timeout = expiration - currentTime - safetyInterval;

            // if token already expired, generate new token and set the access token
            if (timeout<=0)
            {
            console.log("Updating Report Embed Token");
            updateToken();
            }
            // set timeout so minutesToRefresh minutes before token expires, token will be updated
            else 
            {
            console.log("Report Embed Token will be updated in " + timeout + " milliseconds.");
            setTimeout(function() {
            updateToken();
                }, timeout);
            }
    }

    function updateToken() {
        $.ajax({  
            url: getEmbedToken,  
            jsonpCallback: 'callback',  
            contentType: 'application/javascript',  
            dataType: "jsonp",  
            success: function (json) {  


                // Get a reference to the embedded report.
                var $reportContainer = $('#reportContainer'); 
                var report = powerbi.get($reportContainer.get(0));

                // Set AccessToken
                report.setAccessToken(json.EmbedToken)
                .then(function() {
                // Set token expiration listener
                // result.expiration is in ISO format
                console.log("Token being renewed!" + json.EmbedToken)
                //setTokenExpirationListener(Token.expiration,2 /*minutes before expiration*/);
                });
            
            },  
            error: function () {  
                alert("Error");  
            }  
        });  
    }
    
    previewReport()
    '''

    components.html(f""" 
    <html>
        <head>
            <meta http-equiv="Content-type" content="text/html; charset=utf-8">
            <meta name="viewport" content="width=device-width,initial-scale=1">
            <title>Power BI Embedded Demo - Part 5</title>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
            <script type="text/javascript" language="javascript" src="https://code.jquery.com/jquery-1.12.4.js"></script>
            <script type="text/javascript" language="javascript" src="https://rawgit.com/Microsoft/PowerBI-JavaScript/master/dist/powerbi.min.js"></script> </script>
        </head>
        
    <body style="background-color: black; color: white;">
        <div class="container-fluid">
            <div class="row">
                <div class="col-md-12">
                    <form>
                        <div class="col-md-12">
                            <h1>FFB Receiption & Pricing</h1>
                        </div>
                        <div class="col-md-12 mb-5">
                            <button type="button" class="btn btn-primary pull-right" onclick="reloadReport()">Reload Report</button>
                        </div>
                    </form>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12">
                    <div id="reportContainer" style="width: 100%; height: 1000px;"></div>
                </div>
            </div>
        </div>
        <script>
            {js}
        </script>
    </body>
    </html>
    """, width=None, height=1200, scrolling=True)
