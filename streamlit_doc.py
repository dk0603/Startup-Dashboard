import streamlit as st
import pandas as pd
import time
st.title('Startup-Dashboard')
st.markdown("""
### My favorite movies
- Race 3
- Humshakals
- Housefull
""")

df=pd.DataFrame({
    'name': ['nitish','Ankit','Anupam'],
    'marks':[50,60,70],
    'package':[10,12,14]
})
st.dataframe(df)
st.metric('Revenue','Rs 3L','-3%')
st.image('shiv.png')
col1,col2=st.columns(2)
with col1:
    st.image('shiv.png')
with col2:
    st.image('shiv.png')

bar=st.progress(0)
for i in range(1,101):
  time.sleep(0.1)
  bar.progress(i)


email=st.text_input('Enter Email')
file=st.file_uploader('Upload a csv file')
if file is not None:
    df=pd.read_csv(file)
    st.dataframe(df.describe())



