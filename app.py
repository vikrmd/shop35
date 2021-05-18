import streamlit as st
import numpy as np
import pandas as pd
from openpyxl import load_workbook
import time
import SessionState

session_state = SessionState.get(cart_log = '')

def main():
    st.markdown(""" <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style> """, unsafe_allow_html=True)

    st.sidebar.header('Order Creation')
    st.sidebar.info('Order creation is automated based on products selected')

    st.title('Y V I K')
    st.spinner()
    with st.spinner(text='In progress'):
        time.sleep(5)
        st.success('Page loaded successfully')

    wb = load_workbook('productlog.xlsx')
    sheet = wb.active
    max_row = sheet.max_row

    product_type = []

    for j in range(1, max_row):
        if sheet.cell(row=j+1, column=6).value not in product_type:
            product_type.append(sheet.cell(row=j+1, column=6).value)

    prod_typ = st.multiselect("Product Type: ",
                             product_type)

    # write the selected options
    if len(prod_typ) == 0:
        st.warning("Kindly select atleast 1 product type from list to proceed")
    else:
        st.info("You selected " + str(len(prod_typ)) + ' Product type(s)')

    load_products(prod_typ)


def load_products(prod_typ):

    wb = load_workbook('productlog.xlsx')
    sheet = wb.active
    max_row = sheet.max_row

    for i in range(1,max_row):
        if sheet.cell(row=i+1, column=6).value in prod_typ:
            col1, col2 = st.beta_columns([80, 40])

            col1.subheader(sheet.cell(row=i+1, column=2).value)
            #print(str(sheet.cell(row=i+1, column=1).value).split('/')[-1].strip())
            col1.image('img_folder/'+ str(sheet.cell(row=i+1, column=1).value).split('/')[-1].strip() +'.png', use_column_width=80)

            col2.subheader("__Cost :__ Rs." + str(sheet.cell(row=i+1, column=4).value).replace('?',''))


            st.markdown("""<hr>""", unsafe_allow_html=True)
            if col2.button('Add to Cart', key = i):
                session_state.cart_log = session_state.cart_log + 'Product added'
                st.sidebar.text(session_state.cart_log)


if __name__ == "__main__":
    main()
