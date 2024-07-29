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
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

st.set_page_config(page_title="main", page_icon="💯")

if 'selected_type' not in st.session_state:
    st.session_state.selected_type = 0

if 'multiple_choice_type' not in st.session_state:
    st.session_state.multiple_choice_type = []
    
if 'current_page' not in st.session_state:
    st.session_state.current_page = "main"

if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = ""

def changepage(name): st.session_state.current_page = name

placeholder = st.empty()


if st.session_state.current_page == "main":
    # print("main")
    
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
        st.session_state.multiple_choice_type = st.multiselect(
                "객관식의 유형을 선택해주세요 (선택)",
                ["하나만 고르기", "여러개 고르기"],
                ["하나만 고르기", "여러개 고르기"])
    elif st.session_state.selected_type == 2:
        st.write("주관식 선택")
    elif st.session_state.selected_type == 3:
        st.write("서술형 선택")

    uploaded_file = st.file_uploader("문제를 낼 학습자료를 업로드 해주세요")
    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file
        st.write("uploaded!")
        
    st.button("문제 생성하기", on_click=lambda :changepage("problem"))

elif st.session_state.current_page == "problem":
    # print("problem")
    # print(st.session_state.multiple_choice_type)
    # print(st.session_state.uploaded_file)
    st.title("문제 생성 페이지")
    
    tmp = st.session_state.selected_type
    tmp_choice = st.session_state.multiple_choice_type
    
    temp_file = "./temp.pdf"
    with open(temp_file, "wb") as file:
        file.write(st.session_state.uploaded_file.getvalue())
        file_name = st.session_state.uploaded_file.name

    loader = PyPDFLoader(temp_file)
    documents = loader.load_and_split()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=64)
    docs = text_splitter.split_documents(documents)    

    # print(docs[0])
    
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)

    # retriever = vectorstore.as_retriever()
    # docs = retriever.invoke("what did the president say about ketanji brown jackson?")

    qa_retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3},
    )
    
    from langchain_core.prompts import PromptTemplate

    prompt_template = """
    당신은 첨부된 문서에 대한 문제를 만드는 역할입니다.
    모르는 것에 대한 문제를 만들지 마세요.
    관련된 문제를 최소 2문제 생성해주세요.
    주관식 혹은 서술형 문제로 생성해주세요.
    또한 생성한 문제에 대한 답도 함께 제공해주세요.
    그리고 문제에 대한 답은 반드시 줄바꿈으로 구분해주세요.
    
    {context}
    
    Question: {question}
    """
    
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    
    from langchain.chains import RetrievalQA
    from langchain_openai import OpenAI

    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(),
        chain_type="stuff",
        retriever=qa_retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT},
    )

    docs = qa({"query": "첨부된 문서에 대한 문제를 만들어줘."})
    lines = docs["result"].splitlines()    
        
    cnt = 0
    for i in range(len(lines)):
        if len(lines[i].replace(" ", "")) == 0:
            continue
        if cnt == 0:
            st.write(lines[i])
            cnt += 1
        else:
            with st.popover("정답은?"):
                st.write(lines[i])
                cnt = 0        
    
    with st.expander("어디서 나온 문제인가요?"):
        for txt in docs["source_documents"]:
            st.write(txt.page_content)
            st.divider()
    
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