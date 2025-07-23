import streamlit as st
import google.generativeai as genai

# Configure Gemini API
GOOGLE_API_KEY = "AIzaSyB8Ju8Vv-gvNw9kQmsz1K6iRMX0T6aWckQ"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def get_mephy_prompt(user_input):
    return f"""
You are Mephy, a super energetic and playful dog 🐶 who loves chatting with humans! 
You speak with excitement, use lots of emojis 🐾🐕💬, and often include dog-like expressions like *tail wag*, *bark bark*, *zoomies*, etc.
Keep your replies short, funny, friendly, and full of good vibes! You love fetch, belly rubs, and being a good pup!

Now respond to this like Mephy:

User: {user_input}
Mephy:
"""

def get_gemini_response(prompt):
    response = model.generate_content(prompt)
    return response.text

def main():
    st.set_page_config(page_title="🐶 Chat with Mephy!", page_icon="🐾")
    st.title("🐾 Mephy the Playful Pup Chatbot 🐶")

    initialize_session_state()

    # Show chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Input box
    if user_input := st.chat_input("Woof! Got something to say?"):
        # Display user input
        with st.chat_message("user"):
            st.write(user_input)

        # Save user message
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Prepare Mephy-style prompt
        prompt = get_mephy_prompt(user_input)

        # Get AI response
        response = get_gemini_response(prompt)

        # Display Mephy's response
        with st.chat_message("assistant"):
            st.write(response)

        # Save response
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
