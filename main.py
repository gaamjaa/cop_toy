import streamlit as st
import os

# from dotenv import load_dotenv
# load_dotenv()

# os.environ["OPENAI_API_KEY"] = os.getenv("openai_api_key")
os.environ["OPENAI_API_KEY"] = st.secrets["openai_api_key"]

from langchain_openai import ChatOpenAI
model = ChatOpenAI(model="gpt-3.5-turbo")

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


st.set_page_config(page_title="main", page_icon="💯")

if 'selected_type' not in st.session_state:
    st.session_state.selected_type = 0

if 'current_page' not in st.session_state:
    st.session_state.current_page = "main"

def changepage(name): st.session_state.current_page = name

placeholder = st.empty()


if st.session_state.current_page == "main":
    print("main")
    
    st.title("문제 만들기 :memo::100:")
    st.divider()
    st.subheader("원하는 문제 스타일을 선택해주세요.")

    st.columns(3)
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("객관식"):
            st.session_state.selected_type = 1
    with col2:
        if st.button("주관식"):
            st.session_state.selected_type = 2
    with col3:
        if st.button("서술형"):
            st.session_state.selected_type = 3
        
    if st.session_state.selected_type == 1:
        options = st.multiselect(
                "객관식의 유형을 선택해주세요 (선택)",
                ["하나만 고르기", "여러개 고르기"],
                ["하나만 고르기", "여러개 고르기"])
    elif st.session_state.selected_type == 2:
        st.write("주관식 선택")
    elif st.session_state.selected_type == 3:
        st.write("서술형 선택")

    uploaded_file = st.file_uploader("문제를 낼 학습자료를 업로드 해주세요")
    if uploaded_file is not None:
        st.write("uploaded!")
        
    st.button("문제 생성하기", on_click=lambda :changepage("problem"))

elif st.session_state.current_page == "problem":
    print("problem")
    st.title("문제 생성 페이지")
    prompt = ChatPromptTemplate.from_template("tell me a short joke about {topic}")
    output_parser = StrOutputParser()

    chain = prompt | model | output_parser

    prompt_value = chain.invoke({"topic": "ice cream"})
    print(prompt_value)
    st.write("hello world!")
    st.write(prompt_value)
    
    st.button("돌아가기", on_click=lambda :changepage("main"))
    
    
    
    
    
    
    
#######################################################################    
# st.title("문제 만들기 :memo::100:")
# st.divider()
# st.subheader("원하는 문제 스타일을 선택해주세요.")

# st.columns(3)
# col1, col2, col3 = st.columns(3)

# with col1:
#     if st.button("객관식"):
#         st.session_state.selected_type = 1
# with col2:
#     if st.button("주관식"):
#         st.session_state.selected_type = 2
# with col3:
#     if st.button("서술형"):
#         st.session_state.selected_type = 3
    
# if st.session_state.selected_type == 1:
#     options = st.multiselect(
#             "객관식의 유형을 선택해주세요 (선택)",
#             ["하나만 고르기", "여러개 고르기"],
#             ["하나만 고르기", "여러개 고르기"])
# elif st.session_state.selected_type == 2:
#     st.write("주관식 선택")
# elif st.session_state.selected_type == 3:
#     st.write("서술형 선택")

# uploaded_file = st.file_uploader("문제를 낼 학습자료를 업로드 해주세요")
# if uploaded_file is not None:
#     st.write("uploaded!")
    
# if st.button("문제 생성하기"):
#     prompt = ChatPromptTemplate.from_template("tell me a short joke about {topic}")
#     output_parser = StrOutputParser()

#     chain = prompt | model | output_parser

#     prompt_value = chain.invoke({"topic": "ice cream"})
#     print(prompt_value)
#     st.write("hello world!")
#     st.write(prompt_value)