import pandas as pd 
import streamlit as st
import eda 
import prediction
from PIL import Image
page = st.sidebar.selectbox('Choose Pages: ' , 
                                ('Landing Page',
                                 'Data Exploration','Data Prediction'))

def run ():
    if page == 'Landing Page':
        st.title('  **Campaign Prediction**     ')
        st.write('')
        st.write('## Our Team :')
        st.write('#### [Betara Candra]() | [Github]()')
        st.write('#### [Dicky Gabriel Partogi Sarumpaet]() | [Github]()')
        st.write('#### [Erlangga Jayadipraja]() | [Github]()')
        st.write('## Batch     : SBY - 002')
        st.write('#### Please select menu on left bar')
        image = Image.open('Logo_Abank.png')
        st.image(image,caption="Abank")
        st.write('### Background :')
        st.markdown(''' The bank's marketing team wants to predict whether 
                    bank customers will subscribe to bank deposit products
                    based on campaigns carried out by the bank using telephone and 
                    identifying the characteristics of each bank customer.
                    ''')
        st.write('### Objective :')
        st.markdown(''' ----
                    ''')
    elif page == 'Data Exploration' :
        eda.run()
    else:
        prediction.run()
   
if __name__ == '__main__':
    run()