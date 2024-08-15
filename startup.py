import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
st.set_page_config(page_title='Startup Analysis')
df=pd.read_csv('startup_cleaned.csv')
df['date']=pd.to_datetime(df['date'],format='mixed',dayfirst=True,errors='coerce')

def load_investor_details(investor):
    st.title(investor)
    # recent investment of a investor
    last5_df=df[df['investors'].str.contains(investor)].head()[['date', 'startup', 'vertical', 'city', 'round', 'amount_in_cr']]
    st.subheader('Most Recent Investment')
    st.dataframe(last5_df)
    col1,col2,col3,col4=st.columns(4)
    with col1:
        biggest_investment = df[df['investors'].str.contains(investor)].groupby('startup')['amount_in_cr'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investment')
        st.dataframe(biggest_investment)
        fig, ax = plt.subplots()
        ax.bar(biggest_investment.index, biggest_investment.values)
        st.pyplot(fig)

    with col2:
        verticalss=df[df['investors'].str.contains(investor)].groupby('vertical')['amount_in_cr'].sum()
        st.subheader('Sectors Invested In')
        fig1, ax1 = plt.subplots()
        ax1.pie(verticalss,labels=verticalss.index,autopct='%0.01f%%')
        st.pyplot(fig1)
    with col3:
        rounds=df[df['investors'].str.contains(investor)].groupby('round')['amount_in_cr'].sum()
        st.subheader('Stages Invested In')
        fig2, ax2 = plt.subplots()
        ax2.pie(rounds,labels=rounds.index, autopct='%0.01f%%')
        st.pyplot(fig2)
    with col4:
        cities=df[df['investors'].str.contains(investor)].groupby('city')['amount_in_cr'].sum()
        st.subheader('Cities Invested In')
        fig3, ax3 = plt.subplots()
        ax3.pie(cities, labels=cities.index, autopct='%0.01f%%')
        st.pyplot(fig3)
    df['year'] = df['date'].dt.year
    yoy=df[df['investors'].str.contains(investor)].groupby('year')['amount_in_cr'].sum()
    st.subheader('YOY Investment')
    fig4, ax4 = plt.subplots()
    ax4.plot(yoy.index,yoy.values)
    st.pyplot(fig4)
    st.subheader('Similar Investors')
    verticals = df.groupby('vertical')[['amount_in_cr', 'investors']].sum().sort_values('amount_in_cr', ascending=False)
    similar=verticals[verticals['investors'].str.contains(investor)].drop(columns='amount_in_cr')
    st.dataframe(similar)


def load_overall_Analysis():
    st.title('Overall Analysis')
    col1,col2,col3,col4=st.columns(4)
    # total amount
    total=round(df['amount_in_cr'].sum())
    # Max Amount
    maxi=round(df.groupby('startup')['amount_in_cr'].sum().sort_values(ascending=False).head(1).values[0])
    # avg_funding
    avg_funding=round(df.groupby('startup')['amount_in_cr'].sum().mean())
    # total funded startups
    funded=df['startup'].nunique()
    with col1:
        st.metric('Total amount invested in Indian market', str(total) + ' Cr')
    with col2:
        st.metric('Maximum amount invested in a Startup', str(maxi) + ' Cr')
    with col3:
        st.metric('Average Funding', str(avg_funding) + ' Cr')
    with col4:
        st.metric('Total Funded Startups', str(funded) )
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    temp_df = df.groupby(['year', 'month'])['amount_in_cr'].sum().reset_index()
    temp_df['x-axis'] = temp_df['month'].astype(str) + '-' + temp_df['year'].astype(str)
    temp_count = df.groupby(['year', 'month'])['startup'].count().reset_index()
    temp_count['x-axis'] = temp_count['month'].astype(str) + '-' + temp_count['year'].astype(str)

    selected_option=st.selectbox('Select Type',['Total','Count'])
    if selected_option=='Total':
        st.subheader('MOM Graph-Amount Invested')
        fig5, ax5 = plt.subplots()
        ax5.plot(temp_df['x-axis'], temp_df['amount_in_cr'])
        st.pyplot(fig5)
    elif selected_option=='Count':
        st.subheader('MOM Graph-Total Startups Launched')
        fig6, ax6= plt.subplots()
        ax6.plot(temp_count['x-axis'], temp_count['startup'])
        st.pyplot(fig6)

st.sidebar.title('Startup Funding Analysis')
option= st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investor'])
if option == 'Overall Analysis':
        load_overall_Analysis()
elif option=='Startup':
    st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    btn1=st.sidebar.button('Find Startup Details')
    st.title('Startup Analysis')
else:
    selected_investor=st.sidebar.selectbox('Select Investor',sorted(set(df['investors'].str.split(',').sum())))
    btn2=st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)
