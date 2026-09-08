import config_data as config
from rag import RagService
import streamlit as st

st.title("智能穿搭助手")
st.divider()

if "message" not in st.session_state:
    st.session_state["message"] = [
        {"role": "assistant", "content": "你好，有什么可以帮助你？"}
    ]

if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input()

if prompt is not None:
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})

    ai_response_list = []

    with st.spinner("AI思考中"):
        response_stream = st.session_state["rag"].chain.stream(
            {"input": prompt},
            config.session_config
        )


        def capture(generator, cache_list):
            for chunk in generator:
                # 判断chunk是字典就提取output文本，是字符串直接使用
                if isinstance(chunk, dict):
                    text = chunk.get("output", "")
                else:
                    text = chunk
                cache_list.append(text)
                yield text

        st.chat_message("assistant").write_stream(capture(response_stream, ai_response_list))

        # "".join[a, b, c] -> abc, "|".join[a, b, c] -> a|b|c
        st.session_state["message"].append({"role": "assistant", "content": "".join(ai_response_list)})