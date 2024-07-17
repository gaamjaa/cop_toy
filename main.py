import streamlit as st

st.set_page_config(page_title="main", page_icon="💯")

if 'selected_type' not in st.session_state:
    st.session_state.selected_type = 0

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
    
st.button("문제 생성하기")


# 이렇게 만들어서 제출하기 누르면 없애버리자..
# placeholder = st.empty()

# # Replace the placeholder with some text:
# placeholder.text("Hello")

# # Replace the text with a chart:
# placeholder.line_chart({"data": [1, 5, 2, 6]})

# # Replace the chart with several elements:
# with placeholder.container():
#     st.write("This is one element")
#     st.write("This is another")

# # Clear all those elements:
# placeholder.empty()