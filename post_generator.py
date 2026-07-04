from llm_helper import llm
from few_shot import FewShotPosts
from tavily_helper import fetch_tavily_context

few_shot = FewShotPosts()


def get_length_str(length):
    if length == "Short":
        return "1 to 5 lines"
    if length == "Medium":
        return "6 to 10 lines"
    if length == "Long":
        return "11 to 15 lines"


def generate_post(
    length,
    language,
    tag,
    tone="Professional",
    custom_topic=None,
    hook="None",
    emoji_density="Medium",
    variant_count=1,
):
    topic = custom_topic if custom_topic else tag
    filter_tag = None if custom_topic else tag
    tavily_context = fetch_tavily_context(topic)

    prompt = get_prompt(
        length,
        language,
        topic,
        tone,
        hook,
        emoji_density,
        filter_tag,
        tavily_context,
    )

    variants = []
    for _ in range(max(1, variant_count)):
        response = llm.invoke(prompt)
        variants.append(response.content.strip())

    return variants, tavily_context


def get_prompt(length, language, topic, tone, hook, emoji_density, filter_tag, tavily_context=None):
    length_str = get_length_str(length)

    prompt = f'''
Generate a LinkedIn post using the below information. No preamble.

1) Topic: {topic}
2) Length: {length_str}
3) Language: {language}
4) Tone: {tone}
5) Emoji density: {emoji_density}
'''

    if hook != "None":
        prompt += "6) Start the post with a strong opening based on the chosen hook."
        if hook == "Question hook":
            prompt += " Use a thoughtful question to pull the reader in."
        elif hook == "Contrarian take":
            prompt += " Use a subtle contrarian angle that challenges common thinking."
        elif hook == "Story hook":
            prompt += " Open with a short story, personal anecdote, or quick scene."
        elif hook == "Stat hook":
            prompt += " Open with a compelling statistic or trend statement."
    else:
        prompt += "6) Begin with a confident but natural opening sentence."

    prompt += '''

If Language is Hinglish then it means it is a mix of Hindi and English.
The script for the generated post should always be English.
'''

    if emoji_density == "None":
        prompt += " Avoid using emojis in the content."
    elif emoji_density == "Low":
        prompt += " Use at most 1-2 emojis to keep the post professional."
    elif emoji_density == "Medium":
        prompt += " Use a small number of emojis to add warmth and emphasis."
    else:
        prompt += " Use emojis sparingly to support the message and tone."

    examples = few_shot.get_filtered_posts(length, language, filter_tag)
    if examples:
        prompt += "\n\nUse the writing style from the following examples to shape the post."

    for i, post in enumerate(examples):
        post_text = post["text"]
        prompt += f"\n\nExample {i+1}:\n{post_text}"
        if i == 1:
            break

    if tavily_context:
        prompt += (
            "\n\nUse this current trending context to ground the post. "
            "If you use a specific fact or stat from the source, keep it accurate and phrase it naturally. "
            "Do not invent a numeric stat that was not present in the context."
        )
        prompt += "\nContext:\n"
        for item in tavily_context:
            prompt += f"- {item['content']}\n"

    return prompt


if __name__ == "__main__":
    print(generate_post("Medium", "English", "Mental Health"))