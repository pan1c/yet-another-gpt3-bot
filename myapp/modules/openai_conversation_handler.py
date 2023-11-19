from .logging import logging
from openai import OpenAI
from .settings import openai_api_key, gpt_system_role, gpt_model_name


async def generate_response(question: str,prev_message: str) -> str:
    """Use GPT to generate a response to the given question."""
    client = OpenAI(api_key=openai_api_key)
    if question:
        #Make your OpenAI API request here
        response = client.chat.completions.create(
        model=gpt_model_name,
        messages=[
            # https://platform.openai.com/docs/guides/text-generation/chat-completions-api
            # {"role": "system", "content": "You are a helpful assistant."},
            # {"role": "user", "content": "Who won the world series in 2020?"},
            # {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
            {
                "role": "system",
                "content": gpt_system_role
            },
            {
                "role": "user",
                "content": question
            },
            {
                "role": "assistant",
                "content": prev_message
            }
            ])
        logging.info(response)
        response_text = response.choices[0].message.content
        response_text = response.choices[0].message.content
    else:
        response_text = "You didn't ask your question. Try /help"

    return response_text

def generate_image(prompt):
    client = OpenAI(api_key=openai_api_key)
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    logging.info(response)
    image_url = response.data[0].url

    # for debug use
    # image_url = "https://catdoctorofmonroe.com/wp-content/uploads/2020/09/iconfinder_cat_tied_275717.png"
    usage = 1 # reserve for future use
    return (image_url)

