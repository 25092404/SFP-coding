import streamlit as st
import google.generativeai as genai
import urllib.parse

# ----------------------------
# 1. Configure Gemini API
# ----------------------------
GOOGLE_API_KEY = "AIzaSyB8Ju8Vv-gvNw9kQmsz1K6iRMX0T6aWckQ"  # Replace with your key
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# ----------------------------
# 2. Setup Streamlit Page
# ----------------------------
st.set_page_config(
    page_title="🎧 AI Music Recommender",
    page_icon="🎵",
    layout="wide"
)

# ----------------------------
# 3. Custom CSS (Gradient + Font)
# ----------------------------
custom_css = """
<style>
body {
    background: linear-gradient(to bottom right, #0f0f0f, #1DB954);
    background-attachment: fixed;
    font-family: 'Segoe UI', sans-serif;
    color: white;
}

html, body, [class*="css"] {
    font-size: 20px;
    color: white;
}

h1, h2, h3, h4, h5, h6 {
    color: #1DB954 !important;
    font-weight: bold;
}

.song-card {
    background-color: rgba(0, 0, 0, 0.75);
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.4);
}

.song-title {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 8px;
}

.song-link {
    font-size: 18px;
    color: #1DB954;
    text-decoration: none;
}

.song-link:hover {
    text-decoration: underline;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ----------------------------
# 4. Gemini Song Generator
# ----------------------------
def get_gemini_song_suggestions(genre_or_mood):
    prompt = f"""
    Suggest 10 trending or iconic songs based on the theme, genre, or mood: '{genre_or_mood}'.
    Include both the song title and artist name. Format like:
    1. Song Title - Artist
    """
    response = model.generate_content(prompt)
    return response.text

# ----------------------------
# 5. Google Search Link
# ----------------------------
def create_google_search_link(song):
    query = urllib.parse.quote(song)
    return f"https://www.google.com/search?q={query}"

# ----------------------------
# 6. App UI
# ----------------------------
st.markdown("<h1>🎧 AI Music Recommender</h1>", unsafe_allow_html=True)
st.markdown("Enter a **genre**, **mood**, or **vibe** like `K-pop`, `Lofi`, `Workout`, `Romantic`, `80s Rock`, `Anime`, etc.")

user_input = st.text_input("🎶 What's your vibe today?", value="Pop")

if st.button("Get Recommendations 🎵"):
    with st.spinner("🎤 Gemini is mixing your playlist..."):
        suggestions = get_gemini_song_suggestions(user_input)
        songs = suggestions.strip().split("\n")

        st.subheader(f"🔊 Playlist for: `{user_input}`")

        cols = st.columns(2)  # Two columns
        index = 0

        for song in songs:
            if song.strip():
                song_info = song.split(". ", 1)[-1]
                link = create_google_search_link(song_info)

                with cols[index % 2]:
                    st.markdown(f"""
                        <div class="song-card">
                            <div class="song-title">🎵 {song_info}</div>
                            <a href="{link}" target="_blank" class="song-link">🔎 Search on Google</a>
                        </div>
                    """, unsafe_allow_html=True)
                index += 1
