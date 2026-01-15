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


def generate_post(length, language, tag, tone="Professional", custom_topic=None):
    # If custom topic is provided, use it. Otherwise use the selected tag.
    topic = custom_topic if custom_topic else tag
    
    # If using custom topic, we don't filter by tag to get broader examples
    filter_tag = None if custom_topic else tag

    prompt = get_prompt(length, language, topic, tone, filter_tag)
    response = llm.invoke(prompt)
    return response.content


def get_prompt(length, language, topic, tone, filter_tag):
    length_str = get_length_str(length)

    prompt = f'''
    Generate a LinkedIn post using the below information. No preamble.

    1) Topic: {topic}
    2) Length: {length_str}
    3) Language: {language}
    4) Tone: {tone}
    
    If Language is Hinglish then it means it is a mix of Hindi and English. 
    The script for the generated post should always be English.
    '''
    # prompt = prompt.format(post_topic=tag, post_length=length_str, post_language=language)

    # Use filter_tag (which might be None) to get examples
    examples = few_shot.get_filtered_posts(length, language, filter_tag)

    if len(examples) > 0:
        prompt += "5) Use the writing style as per the following examples."

    for i, post in enumerate(examples):
        post_text = post['text']
        prompt += f'\n\n Example {i+1}: \n\n {post_text}'

        if i == 1: # Use max two samples
            break

    return prompt


if __name__ == "__main__":
    print(generate_post("Medium", "English", "Mental Health"))