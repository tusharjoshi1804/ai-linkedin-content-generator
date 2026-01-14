import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post


# Options for length and language
length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish", "French", "Spanish"]

def main():
    # Page settings
    st.set_page_config(
        page_title="AI LinkedIn Content Generator",
        page_icon="🚀",
        layout="centered"
    )

    # Header
    st.title("🚀 AI-Powered LinkedIn Content Generator")
    st.caption("Generate professional LinkedIn posts instantly using AI.")
    st.divider()

    # Sidebar controls
    st.sidebar.header("⚙️ Post Settings")

    fs = FewShotPosts()
    tags = fs.get_tags()

    selected_tag = st.sidebar.selectbox("📌 Topic", options=tags)
    selected_length = st.sidebar.selectbox("📏 Length", options=length_options)
    selected_language = st.sidebar.selectbox("🌍 Language", options=language_options)
    use_emoji = st.sidebar.checkbox("😄 Include Emojis", value=True)

    st.divider()

    # Generate button
    generate = st.button("✨ Generate Post", use_container_width=True)

    if generate:
        with st.spinner("Generating your post..."):
            post = generate_post(
                selected_length,
                selected_language,
                selected_tag,
                use_emoji
            )

        st.success("✅ Post generated successfully!")

    # Output section
with st.container(border=True):
    st.subheader("📄 Generated Post")
    st.text_area(
        "Tap and hold to copy",
        post,
        height=260
    )
    
# 👇 ADD THIS BELOW
if __name__ == "__main__":
    main()


