import openai
import streamlit as st

openai.api_key = st.secrets['API']

page_element="""
<style>
[data-testid="stAppViewContainer"]{
background-image: url("https://wallpapercave.com/wp/wp5463543.jpg");
background-size: cover;
}
[data-testid="stHeader"]{
background-color: rgba(0,0,0,0);
}

[data-testid="stChatFloatingInputContainer css-90vs21 ehod42b2"]{
background-color: rgba(0,0,0,0);
}

[data-testid="stToolbar"]{
right: 2rem;
background-image: url("");
background-size: cover;
}

[data-testid="stSidebar"]> div:first-child{
background-image: url("https://img.freepik.com/premium-vector/skyblue-gradient-background-advertisers-gradient-hq-wallpaper_189959-513.jpg");
background-size: cover;
}
</style>

"""
st.markdown(page_element, unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: white';>Personality.AI 🖼️</h1>", unsafe_allow_html=True)
st.markdown("---")

genres = ["Action", "Comedy", "Drama", "Romance", "Sci-Fi"]
genre = st.selectbox("Select a genre", genres)

options= ["Kapil Sharma", "Akshay Kumar", "Shahrukh Khan", "Salman Khan", "Alia Bhatt", "Tom Cruise", "Tom Holland"]
personality = st.selectbox("Select a personality", options)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": f"Imitate as {personality} and give reply in {genre} tone Sometime, reply to {prompt}"})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})