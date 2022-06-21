###############################
# This program lets you       #
# - Create a dashboard        #
# - Evevry dashboard page is  #
# created in a separate file  #
###############################

# Python libraries
import streamlit as st
from PIL import Image

# User module files
from ml import ml
from eda import eda

def main():

    #############
    # Main page #
    #############

    options = ['Home','EDA','Prediction','Stop']
    choice = st.sidebar.selectbox("Menu",options, key = '1')

    if ( choice == 'Home' ):
      st.title("Welcome to the Czech bank, where your dreams can come true!!")
      st.image('./images/photo-1501167786227-4cba60f6d58f.jpeg')
      pass

    elif ( choice == 'EDA' ):
      eda()
      pass

    elif ( choice == 'Prediction' ):
      ml()

    else:
      st.stop()


main()
