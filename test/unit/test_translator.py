from unittest.mock import patch
import src.translator
from src.translator import translate_content
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('all-MiniLM-L6-v2')



def eval_single_response_translation(expected_answer: str, llm_response: str) -> float:
  # ----------------- YOUR CODE HERE ------------------ #
  sentences = [expected_answer, llm_response]
  embeddings = model.encode(sentences)
  similarities = model.similarity(embeddings, embeddings)
  # extract similarity score from tensor into float
  return similarities[0, 1].item()


# -----------------------
# Unit Tests
# -----------------------
def test_translate_chinese_message():
    is_english, translated_content = translate_content("这是一条中文消息")
    assert is_english == False, "Expected the content to be recognized as non-English"
    similarity_score = eval_single_response_translation("This is a Chinese message.", translated_content)
    assert similarity_score >= 0.9, f"Similarity is actually {similarity_score}"


def test_translate_turkish_message():
    is_english, translated_content = translate_content("Bu bir Türkçe mesajdır")
    assert is_english == False, "Expected the content to be recognized as non-English"
    similarity_score = eval_single_response_translation("This is a Turkish message.", translated_content)
    assert similarity_score >= 0.9, f"Similarity is actually {similarity_score}"


def test_translate_vietnamese_message():
    is_english, translated_content = translate_content("Đây là một tin nhắn bằng tiếng Việt")
    assert is_english == False, "Expected the content to be recognized as non-English"
    similarity_score = eval_single_response_translation("This is a Vietnamese message.", translated_content)
    assert similarity_score >= 0.9, f"Similarity is actually {similarity_score}"


def test_translate_catalan_message():
    is_english, translated_content = translate_content("Esto es un mensaje en catalán")
    assert is_english == False, "Expected the content to be recognized as non-English"
    similarity_score = eval_single_response_translation("This is a Catalan message.", translated_content)
    assert similarity_score >= 0.9, f"Similarity is actually {similarity_score}"


def test_translate_english_message():
    is_english, translated_content = translate_content("This is an English message")
    assert is_english == True, "Expected the content to be recognized as English"
    similarity_score = eval_single_response_translation("This is an English message.", translated_content)
    assert similarity_score >= 0.9, f"Similarity is actually {similarity_score}"



# -----------------------
# Mock Tests
# -----------------------
@patch.object(src.translator.client.chat.completions, 'create')
def test_llm_normal_response(mocker):
    mocker.return_value.choices[0].message.content = "This is a Thai message"
    is_english, translated_content = translate_content("นี่คือข้อความภาษาไทย")
    assert is_english == False, "Expected the content to be recognized as non-English"
    similarity_score = eval_single_response_translation("This is a Thai message.", translated_content)
    assert similarity_score >= 0.9, f"Similarity is actually {similarity_score}"
    

    mocker.return_value.choices[0].message.content = "This is a Korean message"
    is_english, translated_content = translate_content("이것은 한국어 메시지입니다")
    assert is_english == False, "Expected the content to be recognized as non-English"
    similarity_score = eval_single_response_translation("This is a Korean message.", translated_content)
    assert similarity_score >= 0.9, f"Similarity is actually {similarity_score}"

    mocker.return_value.choices[0].message.content = "This is a Russian message"
    is_english, translated_content = translate_content("Это сообщение на русском")
    assert is_english == False, "Expected the content to be recognized as non-English"
    similarity_score = eval_single_response_translation("This is a Russian message.", translated_content)
    assert similarity_score >= 0.9, f"Similarity is actually {similarity_score}"



@patch.object(src.translator.client.chat.completions, 'create')
def test_llm_gibberish_response(mocker):
    mocker.return_value.choices[0].message.content = "askdlf; jsadfewio"
    is_english, translated_content = translate_content("Hello")
    assert is_english == False, "Expected the content to be not recognized as English since LLM giberish"
    similarity_score = eval_single_response_translation("askdlf; jsadfewio", translated_content)
    assert similarity_score >= 0.9, f"Similarity is actually {similarity_score}"

    mocker.return_value.choices[0].message.content = "こんにちは、元気ですか？"
    is_english, translated_content = translate_content("Hello")
    assert is_english == False, "Expected the content to be not recognized as English since LLM giberish"
    assert translated_content == "Error in processing the post. Please try again later."

    mocker.return_value.choices[0].message.content = ""
    is_english, translated_content = translate_content("Hello")
    assert is_english == False, "Expected the content to be not recognized as English since LLM giberish"
    assert translated_content == "Error in processing the post. Please try again later."

    mocker.return_value.choices[0].message.content = 1000
    is_english, translated_content = translate_content("Hello")
    assert is_english == False, "Expected the content to be not recognized as English since LLM giberish"
    assert translated_content == "Error in processing the post. Please try again later."