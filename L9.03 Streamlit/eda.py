
def eda():
    # Import python modules
    import streamlit as st
    import matplotlib.pyplot as plt
    import seaborn as sns
    import plotly.express as px

    # Immport user modules
    from engine import get_engine
    from functions import get_loans, get_debt

    sns.set_theme(style="darkgrid")
    password = st.text_input("Restricted access, please enter your password: ", type="password")
    myengine = get_engine(password)
    if ( password ):
        data = get_loans(myengine)

        fig1, ax1 = plt.subplots(figsize=(20,10))
        sns.countplot(data = data, x='Region', hue='status',ax= ax1)
        ax1.set_title("Number of loans of in each status by Region")
        st.pyplot(fig1)

        data = get_debt(myengine)

        fig2 = px.bar(data, y='Region', x='Debt', color = 'Status')
        st.plotly_chart(fig2)
