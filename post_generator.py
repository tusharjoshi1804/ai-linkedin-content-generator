from llm_helper import llm
from few_shot import FewShotPosts

few_shot = FewShotPosts()


def get_length_str(length):
    if length == "Short":
        return "1 to 5 lines"
    if length == "Medium":
        return "6 to 10 lines"
    if length == "Long":
        return "11 to 15 lines"


def generate_post(length, language, tag, use_emoji):
    prompt = get_prompt(length, language, tag, use_emoji)
    response = llm.invoke(prompt)
    return response.content


def get_prompt(length, language, tag, use_emoji):
    length_str = get_length_str(length)

    emoji_instruction = "Include relevant emojis." if use_emoji else "Do not include emojis."

    prompt = f"""
Generate a LinkedIn post using the information below.

Topic: {tag}
Length: {length_str}
Language: {language}
Emoji Rule: {emoji_instruction}

Rules:
- If language is Hinglish, mix Hindi and English.
- If language is French, write fully in French.
- If language is Spanish, write fully in Spanish.
- Otherwise write in English.
- Keep the tone professional and engaging.
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
    print(generate_post("Medium", "English", "Mental Health"))
