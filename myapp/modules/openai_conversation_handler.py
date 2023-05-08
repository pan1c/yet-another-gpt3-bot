from .logging import logging
import openai
from .settings import openai_api_key, gpt_system_role, gpt_model_name

openai.api_key = openai_api_key

async def generate_response(question: str,prev_message: str) -> str:
    """Use GPT-3 to generate a response to the given question."""
    if question:

        try:
  #Make your OpenAI API request here
            response = openai.ChatCompletion.create(
                model=gpt_model_name,
                messages=[
                    # https://platform.openai.com/docs/guides/chat?utm_medium=email&_hsmi=248356722
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
                ]
            )
        except openai.error.Timeout as e:
            #Handle timeout error, e.g. retry or log
            print(f"OpenAI API request timed out: {e}")
            pass
        except openai.error.APIError as e:
            #Handle API error, e.g. retry or log
            print(f"OpenAI API returned an API Error: {e}")
            pass
        except openai.error.APIConnectionError as e:
            #Handle connection error, e.g. check network or log
            print(f"OpenAI API request failed to connect: {e}")
            pass
        except openai.error.InvalidRequestError as e:
            #Handle invalid request error, e.g. validate parameters or log
            print(f"OpenAI API request was invalid: {e}")
            pass
        except openai.error.AuthenticationError as e:
            #Handle authentication error, e.g. check credentials or log
            print(f"OpenAI API request was not authorized: {e}")
            pass
        except openai.error.PermissionError as e:
            #Handle permission error, e.g. check scope or log
            print(f"OpenAI API request was not permitted: {e}")
            pass
        except openai.error.RateLimitError as e:
            #Handle rate limit error, e.g. wait or log
            print(f"OpenAI API request exceeded rate limit: {e}")
            pass
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

