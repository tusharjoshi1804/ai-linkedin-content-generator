import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post


# Options for length and language
length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish", "French", "Spanish"]


# Main app layout
def main():
    st.subheader("AI-Powered LinkedIn Content Generator")

    # Create three columns for the dropdowns
    col1, col2, col3 = st.columns(3)

    fs = FewShotPosts()
    tags = fs.get_tags()
    with col1:
        # Dropdown for Topic (Tags)
        selected_tag = st.selectbox("Topic", options=tags)

    with col2:
        # Dropdown for Length
        selected_length = st.selectbox("Length", options=length_options)

    with col3:
        # Dropdown for Language
        selected_language = st.selectbox("Language", options=language_options)
        
        use_emoji = st.checkbox("✨ Include Emojis", value=True)


    # Generate Button
    if st.button("Generate"):
    post = generate_post(
        selected_length,
        selected_language,
        selected_tag,
        use_emoji
    )

    st.success("Post generated successfully!")

    # Copy-friendly text area
    st.text_area(
        "Your Generated Post (Tap and hold to copy)",
        post,
        height=250
    )


# Run the app
if __name__ == "__main__":
    main()
