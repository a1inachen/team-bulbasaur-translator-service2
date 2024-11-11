from openai import AzureOpenAI
import string
import os
from dotenv import load_dotenv


load_dotenv()

client = AzureOpenAI (
        api_key = os.getenv('AZURE_OPENAI_API_KEY'),
        api_version="2024-02-15-preview",
        azure_endpoint="https://team-bulbasaur.openai.azure.com/"
    )

def get_language(post) -> str:
    context = "You are a helpful assistant that classifies the language of given text (respond in English). If you cannot determine any specific language, return the original text"
    # ---------------- YOUR CODE HERE ---------------- #
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
              "role": "system",
              "content": context
            },
            {
                "role": "user",
                "content": post
            }
        ]
    )
    return response.choices[0].message.content

def get_translation(post) -> str:
    context = "You are a helpful assistant that translates given input into English text. If you are unable to translate the given text into English, return the original text"
    # ---------------- YOUR CODE HERE ---------------- #
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
              "role": "system",
              "content": context
            },
            {
                "role": "user",
                "content": post
            }
        ]
    )
    return response.choices[0].message.content




def is_english(text: str) -> bool:
  """
    Determines if a string is primarily in English, allowing special characters, digits, and whitespace.
    Note that lanugages which use English characters (such as Dutch) can return false positives.

    Parameters:
    - text (str): The input string to check.

    Returns:
    - bool: True if the text is likely English or contains allowed special characters, False otherwise.
  """

  allowed_chars = set(string.ascii_letters + string.punctuation + string.whitespace + string.digits)

  allowed_char_count = sum(1 for char in text if char in allowed_chars)
  allowed_ratio = allowed_char_count / len(text) if text else 0

  return allowed_ratio == 1




def translate_content(content: str) -> tuple[bool, str]:
   
    try:
        languageResponse = get_language(content)
        if not isinstance(languageResponse, str) or len(languageResponse) == 0 or not is_english(languageResponse):
            raise ValueError("Invalid format for get_language response")

        isEnglish = "english" in languageResponse.lower()

        if isEnglish:
            return (True, content)

        englishTranslation = get_translation(content)
        if not isinstance(englishTranslation, str) or len(englishTranslation) == 0 or not is_english(englishTranslation):
            raise ValueError("Invalid format for get_translation response")

        return (False, englishTranslation)


    except Exception as e:
        print(f"Error in translate_content: {e}")
        return (False, "Error in processing the post. Please try again later.")

