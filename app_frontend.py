import streamlit as st
from backend import chatbot, retrieve_all_threads
from langchain_core.messages import HumanMessage,AIMessage
import uuid
from langchain_core.messages import ToolMessage
import datetime

# **************************************** utility functions *************************

def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
    return state.values.get('messages', [])

# **************************************** Session Setup / Initialization ******************************
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_threads()

add_thread(st.session_state['thread_id'])

# **************************************** Sidebar UI *********************************

st.sidebar.title('Start a New Chat ')

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('My Conversations')

for thread_id in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)

        temp_messages = []

        for msg in messages:
            if isinstance(msg, HumanMessage):
                role='user'
            else:
                role='assistant'
            temp_messages.append({
                'role': role, 
                'content': msg.content,
                'timestamp': datetime.datetime.now().strftime("%H:%M:%S")
            })

        st.session_state['message_history'] = temp_messages

# **************************************** Main UI ************************************

st.title(" AI Chatbot Assistant")

# loading the conversation history / Render history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.text(message['content'])
        with col2:
            if 'timestamp' in message:
                st.caption(message['timestamp'])

user_input = st.chat_input('Type here')

if user_input:
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    
    # first add the message to message_history / Show user's message
    st.session_state['message_history'].append({
        'role': 'user', 
        'content': user_input,
        'timestamp': current_time
    })
    with st.chat_message('user'):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.text(user_input)
        with col2:
            st.caption(current_time)

    #CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}

    CONFIG = {
        "configurable": {"thread_id": st.session_state["thread_id"]},
        "metadata": {
            "thread_id": st.session_state["thread_id"]
        },
        "run_name": "chat_turn",
    }

    # Assistant streaming block
    with st.chat_message("assistant"):
        # Use a mutable holder so the generator can set/modify it
        status_holder = {"box": None}

        def ai_only_stream():
            for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages",
            ):
                # Lazily create & update the SAME status container when any tool runs
                if isinstance(message_chunk, ToolMessage):
                    tool_name = getattr(message_chunk, "name", "tool")
                    if status_holder["box"] is None:
                        status_holder["box"] = st.status(
                            f"🔧 Using `{tool_name}` …", expanded=True
                        )
                    else:
                        status_holder["box"].update(
                            label=f"🔧 Using `{tool_name}` …",
                            state="running",
                            expanded=True,
                        )

                # Stream ONLY assistant tokens
                if isinstance(message_chunk, AIMessage):
                    yield message_chunk.content

        ai_message = st.write_stream(ai_only_stream())

        # Finalize only if a tool was actually used
        if status_holder["box"] is not None:
            status_holder["box"].update(
                label="✅ Tool finished", state="complete", expanded=False
            )

    assistant_time = datetime.datetime.now().strftime("%H:%M:%S")
    
    # Save assistant message
    st.session_state["message_history"].append({
        "role": "assistant", 
        "content": ai_message,
        "timestamp": assistant_time
    })
