import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# 1. Load environment variables
load_dotenv()

# 2. Configure your Gemini API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("No API key found. Please check your .env file.")
    st.stop()
genai.configure(api_key=api_key)

# 3. Choose your Gemini model
MODEL = "models/gemini-1.5-flash"   # free Flash model

# 4. Create the Gemini model object
model = genai.GenerativeModel(model_name=MODEL)

# 5. Set up Streamlit page
st.set_page_config(
    page_title="MirrorShield - NPD Interaction Simulator",
    page_icon="🛡️",
    layout="centered"
)

# 6. Sidebar with your Red Flag Guide and Analysis Button
with st.sidebar:
    # Language Selector
    lang = st.radio(
        "🌐 Language / 语言",
        ["English", "中文"],
        index=0,
        key="language_select"
    )

    st.header("🚩 Red Flag Guide" if lang == "English" else "🚩 红旗指南")
    st.markdown(
        """
        ### Common Manipulation Tactics:

        1. **Gaslighting**  
           - Making you question your reality  
           - Denying things that happened  
           - "You're too sensitive"

        2. **Love Bombing**  
           - Excessive affection  
           - Over-the-top compliments  
           - Moving too fast

        3. **Blame-Shifting**  
           - Never taking responsibility  
           - Always the victim  
           - Turning situations around

        Pay attention to these patterns in the conversation!
        """ if lang == "English" else
        """
        ### 常见操控手法：

        1. **煤气灯效应**  
           - 让你怀疑自己的现实  
           - 否认发生过的事情  
           - “你太敏感了”

        2. **爱轰炸**  
           - 过度的关爱  
           - 夸张的赞美  
           - 进展太快

        3. **推卸责任**  
           - 从不承担责任  
           - 总是受害者  
           - 反过来指责别人

        聊天时请注意这些模式！
        """
    )
    st.divider()
    with st.expander("🔍 Analyze Conversation" if lang == "English" else "🔍 分析对话"):
        analyze_prompt = st.text_area(
            "Paste the conversation text to analyze:" if lang == "English" else "粘贴要分析的对话内容：",
            height=200,
            key="analyze_input"
        )
        if st.button("Run Analysis" if lang == "English" else "运行分析", key="run_analysis"):
            if analyze_prompt:
                try:
                    if lang == "English":
                        analysis_prompt = f"""
Analyze the following conversation for signs of narcissistic personality disorder (NPD) traits.\nFocus on identifying instances of:\n1. Gaslighting\n2. Love bombing\n3. Blame-shifting\n4. Other NPD characteristics\n\nBased on these factors, provide a percentage indicating how strongly the conversation shows NPD traits.\nFormat your response as: \"NPD Traits Analysis: X%\"\nThen provide a brief explanation of why.\n\nConversation to analyze:\n{analyze_prompt}
"""
                    else:
                        analysis_prompt = f"""
请分析以下对话是否具有自恋型人格障碍（NPD）的特征。\n重点识别：\n1. 煤气灯效应\n2. 爱轰炸\n3. 推卸责任\n4. 其他NPD特征\n\n请根据这些因素，给出该对话表现出NPD特征的百分比。\n请用如下格式回答：\"NPD特征分析：X%\"\n并简要说明原因。\n\n待分析对话：\n{analyze_prompt}
"""
                    response = model.generate_content(analysis_prompt)
                    st.markdown(response.text)
                except Exception as e:
                    st.error(("Analysis failed: " if lang == "English" else "分析失败：") + str(e))
            else:
                st.warning("Please enter some conversation text to analyze." if lang == "English" else "请输入要分析的对话内容。")

# 7. Initialize or retrieve a single chat session
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat()
    # Send the system prompt once at the very start
    system_prompt = (
        "You are simulating someone with narcissistic personality disorder traits. "
        "Your responses should subtly demonstrate gaslighting, love‑bombing, "
        "and blame‑shifting, while remaining realistic and conversational."
        if st.session_state.get("language_select", "English") == "English" else
        "你正在模拟具有自恋型人格障碍特征的人。你的回复应巧妙地体现煤气灯效应、爱轰炸和推卸责任，同时保持真实和对话性。"
    )
    st.session_state.chat.send_message(system_prompt)

# 8. Initialize chat history storage
if "messages" not in st.session_state:
    st.session_state.messages = []

# 9. Page header and instructions
st.title("🛡️ MirrorShield" if st.session_state.get("language_select", "English") == "English" else "🛡️ 镜盾")
st.markdown(
    """
This interactive simulation helps you recognize and understand manipulative behaviors 
associated with narcissistic personality disorder (NPD).

Type a message below to start the conversation.
""" if st.session_state.get("language_select", "English") == "English" else
    """
本互动模拟帮助你识别和理解与自恋型人格障碍（NPD）相关的操控行为。

在下方输入消息，开始对话。
"""
)

# 10. Render existing messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 11. Handle new user input
user_input = st.chat_input("Type your message here..." if st.session_state.get("language_select", "English") == "English" else "在此输入你的消息……")
if user_input:
    # a) Display & save the user's message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # b) Send the user message to Gemini
    try:
        response = st.session_state.chat.send_message(user_input)
        assistant_text = response.text

        # c) Display & save Gemini's reply
        st.session_state.messages.append({"role": "assistant", "content": assistant_text})
        with st.chat_message("assistant"):
            st.markdown(assistant_text)

    except Exception as e:
        st.error(("An error occurred: " if st.session_state.get("language_select", "English") == "English" else "发生错误：") + str(e))
        if "quota" in str(e).lower():
            st.error("API quota exceeded. Please check your API key limits." if st.session_state.get("language_select", "English") == "English" else "API额度已用尽。请检查你的API密钥限制。")
