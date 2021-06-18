
import catalog
import order_mgr
import check_order_status
import streamlit as st
import SessionState

st.set_page_config(page_title ='BASEOCA')

# st.markdown(""" <style>
# #MainMenu {visibility: hidden;}
# footer {visibility: hidden;}
# </style> """, unsafe_allow_html=True)

hide_footer_style = """
<style>
.reportview-container .main footer {visibility: hidden;}   
</style> 
"""
st.markdown(hide_footer_style, unsafe_allow_html=True)


session_state = SessionState.get(prod_arr = [[],[],[],[]],
                                 tshirt_count = 156,
                                 shirts_count = 32,
                                 sarees_count = 137,
                                 kurtis_count = 142,
                                 prev_prod_typ = '',
                                 resend = 1,
                                 mobile = '',
                                 session_order_id = '',
                                 user_status = 'non_verify',
                                 order_mgr_valid_mobile = '',
                                 otp_resend_allowed = 2,
                                 access_as_guest = False,
                                 successful_order = False)


PAGES = {
    "Select Products": catalog,
    "Create Order": order_mgr,
    "Check Order Status": check_order_status
}
st.sidebar.title('Go to :')
selection = st.sidebar.radio(" ", list(PAGES.keys()))
page = PAGES[selection]
page.main(session_state)