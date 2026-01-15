import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post
from gtts import gTTS
import tempfile
from textblob import TextBlob
import textstat
import time

# ---------------- PAGE CONFIG (ONLY ONCE) ----------------
st.set_page_config(
    page_title="AI LinkedIn Content Generator",
    layout="wide"
)

# ---------------- UI SPACING FIX ----------------
st.markdown("""
<style>
.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ---------------- OPTIONS ----------------
length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish", "French", "Spanish"]
tone_options = ["Professional", "Casual", "Motivational", "Storytelling"]

# ---------------- TTS LANGUAGE MAP ----------------
LANG_MAP = {
    "English": "en",
    "Hinglish": "hi",
    "French": "fr",
    "Spanish": "es"
}

# ---------------- MAIN APP ----------------
def main():

    # Header
    st.title("AI-Powered LinkedIn Content Generator")
    st.caption("Generate professional LinkedIn posts instantly using AI.")

    # Sidebar controls
    st.sidebar.header("⚙️ Post Settings")

    fs = FewShotPosts()
    tags = fs.get_tags()

    selected_tag = st.sidebar.selectbox("📌 Topic", options=tags)
    selected_length = st.sidebar.selectbox("📏 Length", options=length_options)
    selected_language = st.sidebar.selectbox("🌍 Language", options=language_options)
    selected_tone = st.sidebar.selectbox("🎭 Tone", options=tone_options)
    use_emoji = st.sidebar.checkbox("😄 Include Emojis", value=True)

    st.divider()

    # Initialize variables
    post = ""
    hashtags = ""
    sentiment_score = "N/A"
    readability_score = "N/A"

    # Generate button
    generate = st.button("✨ Generate Post", use_container_width=True)

    if generate:
       progress = st.progress(0)

       with st.spinner("⏳ Generating your post..."):
         progress.progress(20)

         result = generate_post(
           selected_length,
           selected_language,
           selected_tag,
           use_emoji,
           selected_tone
         )

         progress.progress(80)
 
       progress.progress(100)

            # ---------- SAFELY HANDLE TUPLE OR STRING ----------
            if isinstance(result, tuple):
               post = str(result[0])
               hashtags = str(result[1]) if len(result) > 1 else ""
            else:
              post = str(result)
              hashtags = ""

         st.success("✅ Post generated successfully!")

        # ---------------- SENTIMENT ANALYSIS ----------------
        try:
            blob = TextBlob(post)
            sentiment_score = round(blob.sentiment.polarity, 2)
        except:
            sentiment_score = "N/A"

        # ---------------- READABILITY SCORE ----------------
        try:
            readability_score = round(textstat.flesch_reading_ease(post), 2)
        except:
            readability_score = "N/A"

        # ---------------- TEXT TO SPEECH ----------------
        try:
            tts_lang = LANG_MAP.get(selected_language, "en")
            tts = gTTS(text=post, lang=tts_lang)

            tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tts.save(tmp_file.name)

            st.audio(tmp_file.name, format="audio/mp3")

        except Exception as e:
            st.warning("⚠️ Audio generation failed.")
            st.error(str(e))

    # ---------------- OUTPUT SECTION ----------------
    if post:
        with st.container(border=True):
            st.subheader("Generated Post")
            st.text_area(
                "Tap and hold to copy",
                post,
                height=260
            )

            if hashtags:
                st.markdown("### Suggested Hashtags")
                st.code(hashtags)

        col1, col2 = st.columns(2)

        with col1:
            st.metric("😊 Sentiment Score", sentiment_score)

        with col2:
            st.metric("📖 Readability Score", readability_score)

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    main()
