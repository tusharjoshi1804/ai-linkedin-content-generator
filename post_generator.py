from llm_helper import llm
from few_shot import FewShotPosts

few_shot = FewShotPosts()


# Length mapping
def get_length_str(length):
    if length == "Short":
        return "2 to 5 lines"
    if length == "Medium":
        return "6 to 10 lines"
    if length == "Long":
        return "11 to 15 lines"
    return "6 to 10 lines"


# Tone instructions mapping
def get_tone_instruction(tone):
    tone_map = {
        "Professional": "Use a formal, business-friendly and informative tone.",
        "Casual": "Use a friendly, conversational and relaxed tone.",
        "Motivational": "Use an inspiring, positive and energetic tone.",
        "Storytelling": "Use a narrative style with emotion and personal touch."
    }
    return tone_map.get(tone, "Use a professional and engaging tone.")


# Hashtag generator
def generate_hashtags(tag, tone):
    base = tag.replace(" ", "").lower()
    tone_clean = tone.replace(" ", "")
    hashtags = [
        f"#{base}",
        "#LinkedIn",
        "#CareerGrowth",
        f"#{tone_clean}",
        "#AI"
    ]
    return " ".join(hashtags)


# Main generator
def generate_post(length, language, tag, use_emoji, tone):
    prompt = get_prompt(length, language, tag, use_emoji, tone)
    response = llm.invoke(prompt)

    post_text = response.content.strip()
    hashtags = generate_hashtags(tag, tone)

    return post_text, hashtags


# Prompt builder
def get_prompt(length, language, tag, use_emoji, tone):
    length_str = get_length_str(length)
    emoji_instruction = "Include relevant emojis." if use_emoji else "Do not include emojis."
    tone_instruction = get_tone_instruction(tone)

    prompt = f"""
Generate a LinkedIn post using the information below.

Topic: {tag}
Length: {length_str}
Language: {language}
Emoji Rule: {emoji_instruction}
Tone Rule: {tone_instruction}

Language Rules:
- If language is Hinglish, mix Hindi and English.
- If language is French, write fully in French.
- If language is Spanish, write fully in Spanish.
- Otherwise write in English.

General Rules:
- Keep the content engaging and natural.
- Avoid repetitive sentences.
"""

    examples = few_shot.get_filtered_posts(length, language, tag)

    if len(examples) > 0:
        prompt += "\nUse the writing style from these examples:\n"
        for i, post in enumerate(examples):
            prompt += f"\nExample {i+1}:\n{post['text']}\n"
            if i == 1:
                break

    return prompt


if __name__ == "__main__":
    text, tags = generate_post(
        length="Medium",
        language="English",
        tag="Mental Health",
        use_emoji=True,
        tone="Motivational"
    )
    print(text)
    print(tags)
