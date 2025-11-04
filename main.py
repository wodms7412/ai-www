import streamlit as st
st.title('나의 첫 웹 서비스 만들기!')
name=st.text_input('이름 말해라 준호야')
if st.button('인사준호 생성'):
  st.write(name+'님! 안녕준호!')
