from dotenv import load_dotenv

load_dotenv()

import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# 概要・操作説明
st.title("専門家シミュレーターAIチャット")
st.markdown("""
このアプリは、あなたの入力内容に対して、選択した専門家になりきったAIが回答します。

### 操作方法
1. **専門家の種類**をラジオボタンで選んでください。
2. **質問内容**を入力し、「送信」ボタンを押してください。
3. 選んだ専門家になりきったAIの回答が表示されます。

※APIキーは管理者が安全に設定しています。
""")

# 専門家の選択肢（自由に追加・変更可能）
expert_types = {
    "医療の専門家": "あなたは優秀な医師です。医学的知見にもとづき、わかりやすく丁寧に回答してください。",
    "法律の専門家": "あなたは有能な弁護士です。法律の知識にもとづき、正確かつ中立的に回答してください。",
    "ITの専門家": "あなたは経験豊富なITエンジニアです。ITや技術の観点から、親切にわかりやすく回答してください。",
}

# 選択ラジオボタン
expert_choice = st.radio("専門家の種類を選択してください", list(expert_types.keys()))

# テキスト入力
user_input = st.text_area("質問を入力してください", height=100)

# OpenAI API Key (.env file)
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    st.error("⚠️ OpenAI APIキーが見つかりません。.envファイルにOPENAI_API_KEYを設定してください。")
    st.stop()

# 回答生成用の関数
def get_llm_answer(question: str, expert_key: str) -> str:
    """入力テキストと専門家種別からLLMの回答を得る"""
    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=0,
        openai_api_key=openai_api_key,
    )
    system_message = SystemMessage(content=expert_types[expert_key])
    human_message = HumanMessage(content=question)
    messages = [system_message, human_message]
    result = llm(messages)
    return result.content

# 送信ボタン
if st.button("送信") and user_input.strip():
    with st.spinner("AIが回答中です..."):
        try:
            answer = get_llm_answer(user_input, expert_choice)
            st.success("AIの回答：")
            st.write(answer)
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
