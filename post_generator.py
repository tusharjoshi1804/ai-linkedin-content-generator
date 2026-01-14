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
Generate a LinkedIn post using the below information. No preamble.

1) Topic: {tag}
2) Length: {length_str}
3) Language: {language}
4) Emoji Rule: {emoji_instruction}

Rules:
- If language is Hinglish, mix Hindi and English.
- If language is French, generate the post fully in French.
- If language is Spanish, generate the post fully in Spanish.
- Otherwise generate in English.
"""

    examples = few_shot.get_filtered_posts(length, language, tag)

    if len(examples) > 0:
        prompt += "\nUse the writing style as per the following examples."

        for i, post in enumerate(examples):
            post_text = post["text"]
            prompt += f"\n\nExample {i+1}:\n\n{post_text}"

            if i == 1:
                break

    return prompt

if __name__ == "__main__":
    print(generate_post("Medium", "English", "Mental Health"))
