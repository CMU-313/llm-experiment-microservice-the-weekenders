from src.translator import translate_content


def test_chinese():
    is_english, translated_content = translate_content("这是一条中文消息")
    assert is_english == False
    assert translated_content == "This is a Chinese message"

def test_llm_normal_response():
    is_english, translated_content = translate_content("Dies ist eine Nachricht auf Deutsch")
    assert is_english is False
    assert translated_content == "This is a German message"

def test_llm_gibberish_response():
    gibberish = "asdf qwer zxcv"
    is_english, translated_content = translate_content(gibberish)
    assert is_english is True
    assert translated_content == gibberish