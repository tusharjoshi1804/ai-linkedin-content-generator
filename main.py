import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post
from gtts import gTTS
import tempfile
from textblob import TextBlob
import textstat

# ----------------------------------
# PAGE CONFIG — MUST BE FIRST STREAMLIT COMMAND
# ----------------------------------
st.set_page_config(
    page_title="AI-Powered LinkedIn Content Generator",
    layout="wide"
)

# ----------------------------------
# Reduce top padding (CSS)
# ----------------------------------
st.markdown("""
<style>
.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------
# Options
# ----------------------------------
length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish", "French", "Spanish"]
tone_options = ["Professional", "Casual", "Motivational", "Storytelling"]

LANG_MAP = {
    "English": "en",
    "Hinglish": "hi",
    "French": "fr",
    "Spanish": "es"
}

# ----------------------------------
# Sentiment + Readability
# ----------------------------------
def analyze_text(text):
    blob = TextBlob(text)
    polarity = round(blob.sentiment.polarity, 2)

    if polarity > 0.1:
        sentiment = "Positive 😊"
    elif polarity < -0.1:
        sentiment = "Negative 😟"
    else:
        sentiment = "Neutral 😐"

    readability = round(textstat.flesch_reading_ease(text), 1)

    if readability >= 70:
        level = "Easy 📗"
    elif readability >= 50:
        level = "Medium 📘"
    else:
        level = "Hard 📕"

    return sentiment, polarity, readability, level


# ----------------------------------
# MAIN APP
# ----------------------------------
def main():

    # Header
    st.title("🚀 AI-Powered LinkedIn Content Generator")
    st.caption("Generate professional LinkedIn posts instantly using AI.")
    st.divider()

    # Sidebar
    st.sidebar.header("⚙️ Post Settings")

    fs = FewShotPosts()
    tags = fs.get_tags()

    selected_tag = st.sidebar.selectbox("📌 Topic", options=tags)
    selected_length = st.sidebar.selectbox("📏 Length", options=length_options)
    selected_language = st.sidebar.selectbox("🌍 Language", options=language_options)
    selected_tone = st.sidebar.selectbox("🎭 Tone", options=tone_options)
    use_emoji = st.sidebar.checkbox("😊 Include Emojis", value=True)

    post = ""

    # Generate button
    if st.button("✨ Generate Post", use_container_width=True):
        with st.spinner("Generating your post..."):
            post = generate_post(
                selected_length,
                selected_language,
                selected_tag,
                use_emoji,
                selected_tone
            )

        st.success("✅ Post generated successfully!")

        # ---------------------------
        # Text to Speech
        # ---------------------------
        try:
            tts_lang = LANG_MAP.get(selected_language, "en")
            tts = gTTS(text=post, lang=tts_lang)
            tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tts.save(tmp_file.name)
            st.audio(tmp_file.name, format="audio/mp3")

        except Exception as e:
            st.warning("⚠️ Audio generation failed.")
            st.error(str(e))

        # ---------------------------
        # Sentiment + Readability
        # ---------------------------
        sentiment, polarity, readability, level = analyze_text(post)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Sentiment", sentiment)
        col2.metric("Polarity", polarity)
        col3.metric("Readability", readability)
        col4.metric("Level", level)

        # ---------------------------
        # Output
        # ---------------------------
        with st.container(border=True):
            st.subheader("📄 Generated Post")
            st.text_area(
                "Tap and hold to copy",
                post,
                height=260
            )


# ----------------------------------
# Run App
# ----------------------------------
if __name__ == "__main__":
    main()
