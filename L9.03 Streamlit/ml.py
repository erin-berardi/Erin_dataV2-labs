# Import python libraries
import pickle
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image

# Import user modules
from functions import cleanOperation, cleankSymbol, cleanDuration, preprocess

def ml():

    st.image('images/bank-loan.jpeg')
    st.title("Model to predict loan payment")

    # loading the model
    models_path = 'models/'
    model_name = models_path + 'logistic_model.pkl'
    loaded_model = pickle.load(open(model_name, 'rb'))

    # loading the scaler
    transformers_path = 'transformers/'
    transformer_name = transformers_path + 'standard_scaler.pkl'
    loaded_transformer = pickle.load(open(transformer_name, 'rb'))

    # loading the encoder
    encoders_path = 'encoders/'
    encoder_name = encoders_path + 'one_hot_encoder.pkl'
    loaded_encoder = pickle.load(open(encoder_name, 'rb'))

    # Lists of accptable values
    valid_types = ['PRIJEM', 'VYDAJ', 'VYBER']
    valid_operation = ['PREVOD Z UCTU', 'VKLAD', 'VYBER', 'PREVOD NA UCET','VYBER KARTOU']
    valid_ksymbol = ['UROK', 'SIPO', 'SLUZBY']
    valid_duration = ['24', '12', '36', '48', '60']

    # Get input values.
    type = st.selectbox("Please enter the type of transaction: ",valid_types, key = '2')
    operation = st.selectbox("Please enter the operation: ",valid_operation, key = '3')
    t_amount = st.number_input("Please enter the transaction amount: ")
    balance = st.number_input("Please enter the balance: ")
    k_symbol = st.selectbox("Please enter the k_symbol: ",valid_ksymbol, key = '4')
    l_amount = st.number_input("Please enter the loan amount: ")
    duration = st.radio("Please enter the loan duration: ",valid_duration, key = '5')
    payments = st.number_input("Please enter the payments: ")

    # when 'Predict' is clicked, make the prediction and store it
    if st.button("Get Your Prediction"):

        X = pd.DataFrame({'type':[type],
                      'operation':[operation],
                      't_amount':[t_amount],
                      'balance':[balance],
                      'k_symbol':[k_symbol],
                      'l_amount':[l_amount],
                      'duration':[duration],
                      'payments':[payments]
                     })

        X = preprocess(X)
        numerical = X.select_dtypes(include = np.number)
        categorical = X.select_dtypes(include = np.object)

        cat_transformed = loaded_encoder.transform(categorical)
        col_names = ['type_VYDAJ','type_VYBER','operation_vklad','operation_unknown','operation_vyber','k_symbol_UROK',
                 'k_symbol_SIPO','k_symbol_SLUZBY','k_symbol_POJISTNE','duration_12','duration_36','duration_other']
        categorical = pd.DataFrame(cat_transformed.toarray(), columns = col_names)

        # Joning dataframes
        X = pd.concat([numerical, categorical], axis=1)
        # Scaling data
        X_scaled = loaded_transformer.transform(X)
        X_scaled_df = pd.DataFrame(X_scaled, columns = X.columns)

        # Making predictions
        prediction = loaded_model.predict(X_scaled_df)
        prediction_probs = loaded_model.predict_proba(X_scaled_df)


        if ( prediction == 'A' ):
            st.success("The model predicts a status of {} with a probability of {:.2f}".format('A',prediction_probs[0,0]))
        else:
            st.error("The model predicts a status of {} with a probability of {:.2f}".format('B',prediction_probs[0,1]))
