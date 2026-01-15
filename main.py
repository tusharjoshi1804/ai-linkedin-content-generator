import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post
from gtts import gTTS
import tempfile

# Language options
length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish", "French", "Spanish"]
tone_options = ["Professional", "Casual", "Motivational", "Storytelling"]

# Map UI language to TTS language code
LANG_MAP = {
    "English": "en",
    "Hinglish": "hi",
    "French": "fr",
    "Spanish": "es"
}

# Reduce top padding for better UI spacing
st.markdown("""
<style>
.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

def main():

    # Page settings
    st.set_page_config(
        page_title="AI LinkedIn Content Generator",
        layout="wide"
    )

    # Header
    st.title("🚀 AI-Powered LinkedIn Content Generator")
    st.caption("Generate professional LinkedIn posts instantly using AI.")

    # Sidebar controls
    st.sidebar.header("⚙️ Post Settings")

    fs = FewShotPosts()
    tags = fs.get_tags()

    selected_tag = st.sidebar.selectbox("📌 Topic", options=tags)
    selected_length = st.sidebar.selectbox("📏 Length", options=length_options)
    selected_language = st.sidebar.selectbox("🌍 Language", options=language_options)
    selected_tone = st.sidebar.selectbox("🎭 Tone", options=tone_options)
    use_emoji = st.sidebar.checkbox("😊 Include Emojis", value=True)

    # Initialize post variable
    post = ""

    # Generate button
    generate = st.button("✨ Generate Post", use_container_width=True)

    if generate:
        with st.spinner("Generating your post..."):
            post = generate_post(
              selected_length,
              selected_language,
              selected_tag,
              use_emoji,
              selected_tone
            )

        st.success("✅ Post generated successfully!")

        # Text to Speech
        try:
            tts_lang = LANG_MAP.get(selected_language, "en")
            tts = gTTS(text=post, lang=tts_lang)

            tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tts.save(tmp_file.name)

            st.audio(tmp_file.name, format="audio/mp3")

        except Exception as e:
            st.warning("⚠️ Audio generation failed.")
            st.error(str(e))

    # Output Section
    if post:
        with st.container(border=True):
            st.subheader("📄 Generated Post")
            st.text_area(
                "Tap and hold to copy",
                post,
                height=260
            )

# Run App
if __name__ == "__main__":
    main()
