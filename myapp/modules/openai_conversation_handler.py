from .logging import logging
import openai
from .settings import openai_api_key, gpt_system_role, gpt_model_name

openai.api_key = openai_api_key

async def generate_response(question: str) -> str:
    """Use GPT-3 to generate a response to the given question."""
    if question:
        response = openai.ChatCompletion.create(
            model=gpt_model_name,
            messages=[
                #{"role": "system", "content": "You are a helpful assistant."},
                # {"role": "user", "content": "Who won the world series in 2020?"},
                # {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
                {
                    "role": "system",
                    "content": gpt_system_role
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        )
        logging.info(response)
        response_text = response['choices'][0]['message']['content']
    else:
        response_text = "You didn't ask your question. Try /help"

    return response_text

def generate_image(prompt):
    response = openai.Image.create(prompt = prompt, n=1, size = "512x512")
    logging.info(response)
    image_url = response["data"][0]["url"]
    # for debug use
    # image_url = "https://catdoctorofmonroe.com/wp-content/uploads/2020/09/iconfinder_cat_tied_275717.png"
    usage = 1 # reserve for future use
    return (image_url)

