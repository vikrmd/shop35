import streamlit as st
import csv


def main(session_state):
    st.title('Check Order Status')
    cart_id = st.text_input("Enter Order ID and Press Enter")

    if cart_id:
        with open('order_book.csv', 'r') as file:
            reader = csv.reader(file)
            lookup = cart_id
            mob_found = False
            for row in reader:
                if lookup in row:
                    prod_text = '''
                        <p><span style="font-size:18px;">'''+ str(row[-6]).split('/')[-3].replace('-',' ') +'''</span><br>
                        <span style="font-size:12px;">Order Date: <span style="font-size:14px;">'''+ str(row[2]) +'''</span></span><br>
                        Status: <span style="color:#FF0000;"><span style="font-size:16px;">'''+ str(row[-7]) +'''</span></span></p>
                    '''
                    st.markdown(prod_text, unsafe_allow_html=True)