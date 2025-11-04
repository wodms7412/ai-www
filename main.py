import streamlit as st
st.title('나의 첫 웹 서비스 만들기!')
name=st.text_input('이름 말해라 준호야')
st.selectbox('좋아하는 음식준호 골라주세염',['치킨','펩시콜라','준호',])
if st.button('인사준호 생성'):
  st.info(name+'님! 안녕준호!')
  st.warning(menu+'을(를) 좋아하나 준호!, 나도 좋아우주')
  st.error('안녕안녕하세요!!')
