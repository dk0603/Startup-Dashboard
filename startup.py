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
    # total funded df
    funded=df['startup'].nunique()
    with col1:
        st.metric('Total amount invested in Indian market', str(total) + ' Cr')
    with col2:
        st.metric('Maximum amount invested in a Startup', str(maxi) + ' Cr')
    with col3:
        st.metric('Average Funding', str(avg_funding) + ' Cr')
    with col4:
        st.metric('Total Funded df', str(funded) )
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
        st.subheader('MOM Graph-Total df Launched')
        fig6, ax6= plt.subplots()
        ax6.plot(temp_count['x-axis'], temp_count['startup'])
        st.pyplot(fig6)
    st.subheader('Sector-Wise Analysis')
    df['vertical'] = df['vertical'].str.replace('ECommerce', 'eCommerce')
    df['vertical'] = df['vertical'].str.replace('E-commerce', 'eCommerce')
    df['vertical'] = df['vertical'].str.replace('Ecommerce', 'eCommerce')
    df['vertical'] = df['vertical'].str.replace('E-Commerce', 'eCommerce')
    temp1 = df.groupby('vertical')['startup'].count().sort_values(ascending=False)
    df3 = pd.DataFrame({'vertical': temp1.index, 'startup': temp1.values})
    df_bool = df3.startup < 25
    df3.iloc[df3[df_bool].index, 0] = 'others'
    k = df3.iloc[df3[df_bool].index, 1].sum()
    df3.drop_duplicates('vertical', keep='first', inplace=True)
    df3['startup'].replace(df3[df3['vertical'] == 'others']['startup'].values[0], k, inplace=True)
    temp2 = df.groupby('vertical')['amount_in_cr'].sum().sort_values(ascending=False)
    df4 = pd.DataFrame({'vertical': temp2.index, 'amount': temp2.values})
    df1_bool = df4.amount < 10000
    df4.iloc[df4[df1_bool].index, 0] = 'others'
    j = df4.iloc[df4[df1_bool].index, 1].sum()
    df4.drop_duplicates('vertical', keep='first', inplace=True)
    df4['amount'].replace(df4[df4['vertical'] == 'others']['amount'].values[0], j, inplace=True)



    select_option=st.selectbox('Select Type',['Count','Sum'])
    if select_option=='Count':
        st.subheader('Sector-Startup Analysis')
        fig7, ax7 = plt.subplots()
        ax7.pie(df3['startup'], labels=df3['vertical'], autopct='%0.01f%%')
        st.pyplot(fig7)
    else:
        st.subheader('Sector-Amount Analysis')
        fig8, ax8 = plt.subplots()
        ax8.pie(df4['amount'], labels=df4['vertical'], autopct='%0.01f%%')
        st.pyplot(fig8)
    df['city'] = df['city'].str.replace('Bengaluru', 'Bangalore')
    df['city'] = df['city'].str.replace('Kormangala', 'Bangalore')
    df['city'] = df['city'].str.replace('Gurgaon', 'Gurugram')
    df['city'] = df['city'].str.replace('New Delhi', 'Delhi')
    df['city'] = df['city'].str.replace('Menlo Park', 'California')
    df['city'] = df['city'].str.replace('San Francisco', 'California')
    df['city'] = df['city'].str.replace('San Jose,', 'California')
    temp3 = df.groupby('city')['amount_in_cr'].sum().sort_values(ascending=False)
    df5 = pd.DataFrame({'city': temp3.index, 'amount': temp3.values})
    df2_bool = df5.amount < 10000
    df5.iloc[df5[df2_bool].index, 0] = 'others'
    j = df5.iloc[df5[df2_bool].index, 1].sum()
    df5.drop_duplicates('city', keep='first', inplace=True)
    df5['amount'].replace(df5[df5['city'] == 'others']['amount'].values[0], j, inplace=True)
    st.subheader('City-Wise Funding')
    fig9, ax9 = plt.subplots()
    ax9.bar(df5['city'], df5['amount'])
    st.pyplot(fig9)
    df['round'] = df['round'].str.replace('Private Equity Round', 'Private Equity')
    df['round'] = df['round'].str.replace('Seed Round', 'Seed Funding')
    temp4 = df.groupby('round')['amount_in_cr'].sum().sort_values(ascending=False)
    df6 = pd.DataFrame({'round': temp4.index, 'amount': temp4.values})
    df3_bool = df6.amount < 7000
    df6.iloc[df6[df3_bool].index, 0] = 'others'
    l = df6.iloc[df6[df3_bool].index, 1].sum()
    df6.drop_duplicates('round', keep='first', inplace=True)
    df6['amount'].replace(df6[df6['round'] == 'others']['amount'].values[0], l, inplace=True)
    st.subheader('Round-Wise Funding')
    fig10, ax10= plt.subplots()
    ax10.bar(df6['round'], df6['amount'])
    st.pyplot(fig10)
    st.subheader('Top Startups')
    selection_box=st.selectbox('Select Type',['Year-Wise','Overall'])
    if selection_box=='Year-Wise':
        pk=pd.DataFrame()
        pk['yyear']=df['year'].unique()
        selected_year = st.selectbox('Select Year', pk['yyear'])
        years = df.groupby(['year', 'startup']).agg({'amount_in_cr': sum}).sort_values(['year', 'amount_in_cr'],ascending=[True, False])
        d=years[years.index.get_level_values('year') == selected_year].head(5)
        st.dataframe(d)
    else:
        gk=df.groupby('startup')['amount_in_cr'].sum().sort_values(ascending=False).head(5)
        st.dataframe(gk)
    st.subheader('Top Investors')
    df['investors'] = df['investors'].str.replace('SoftBank Group', 'Softbank')
    df['investors'] = df['investors'].str.replace('SoftBank', 'Softbank')

    df['investors'] = df['investors'].str.replace('Microsoft, eBay, Tencent Holdings', 'Microsoft')
    df['investors'] = df['investors'].str.replace('Steadview Capital and existing investors','Steadview Capital')
    kd=df.groupby('investors')['amount_in_cr'].sum().sort_values(ascending=False).head(5)
    st.dataframe(kd)

def load_startup_details(startupss):
    st.title(startupss)

    df12=df[df['startup'].str.contains(startupss)]['amount_in_cr'].sum()
    st.metric('Total amount raised', str(df12) + ' Cr')

    col1,col2,col3=st.columns(3)
    with col1:
        st.subheader('Industries Involved in')
        df8=df[df['startup'].str.contains(startupss)]['vertical'].drop_duplicates(keep='first')
        st.dataframe(df8)
    with col2:
        st.subheader('Domains Involved in')
        df9=df[df['startup'].str.contains(startupss)]['subvertical'].drop_duplicates(keep='first').dropna()
        st.dataframe(df9)
    with col3:
        st.subheader('Cities Present in')
        df10 = df[df['startup'].str.contains(startupss)]['city'].drop_duplicates(keep='first').dropna()
        st.dataframe(df10)
    st.subheader('Funding')
    df11= df[df['startup'].str.contains(startupss)][['round', 'investors', 'date', 'amount_in_cr']].sort_values('amount_in_cr', ascending=False)
    st.dataframe(df11)
    st.subheader('Similar Startups')
    df_new = df.copy()
    df_new['startup']= df_new['startup'].apply(lambda x: "{:}, ".format(x))
    verticals = df_new.groupby('subvertical')[['amount_in_cr', 'startup']].sum().sort_values('amount_in_cr',ascending=False)
    df13=verticals[verticals['startup'].str.contains(startupss)].drop(columns='amount_in_cr')
    st.dataframe(df13)

st.sidebar.title('Startup Funding Analysis')
option= st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investor'])
if option == 'Overall Analysis':
        load_overall_Analysis()
elif option=='Startup':
    selected_startup=st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    btn1=st.sidebar.button('Find Startup Details')
    if btn1:
        load_startup_details(selected_startup)


else:
    selected_investor=st.sidebar.selectbox('Select Investor',sorted(set(df['investors'].str.split(',').sum())))
    btn2=st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)
