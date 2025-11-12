from unittest.mock import patch, MagicMock
from src.translator import translate_content

@patch('src.translator.ollama.chat')
def test_llm_normal_translation(mock_chat):
    mock_chat.return_value = {
        'message': {
            'content': 'LANGUAGE: Not English\nTRANSLATION: This is a German message'
        }
    }
    
    is_english, translated = translate_content("Dies ist eine Nachricht auf Deutsch")
    assert is_english is False
    assert "German message" in translated


@patch('src.translator.ollama.chat')
def test_llm_english_detection(mock_chat):
    mock_chat.return_value = {
        'message': {
            'content': 'English'
        }
    }
    
    is_english, translated = translate_content("This is an English message")
    assert is_english is True


@patch('src.translator.ollama.chat')
def test_llm_malformed_response(mock_chat):
    mock_chat.return_value = {
        'message': {
            'content': 'Some gibberish without proper format'
        }
    }
    
    original_text = "Test content"
    is_english, translated = translate_content(original_text)
    # Should fallback to treating as English
    assert isinstance(is_english, bool)
    assert isinstance(translated, str)


@patch('src.translator.ollama.chat')
def test_llm_exception_handling(mock_chat):
    mock_chat.side_effect = Exception("Connection failed")
    
    original_text = "Test content"
    is_english, translated = translate_content(original_text)
    assert is_english is True
    assert translated == original_text


@patch('src.translator.ollama.chat')
def test_llm_empty_content(mock_chat):
    is_english, translated = translate_content("")
    assert is_english is True
    assert translated == ""
    # Should not call LLM for empty content
    mock_chat.assert_not_called()


@patch('src.translator.ollama.chat')
def test_llm_missing_translation_field(mock_chat):
    mock_chat.return_value = {
        'message': {
            'content': 'LANGUAGE: Not English'
        }
    }
    
    original_text = "Hola mundo"
    is_english, translated = translate_content(original_text)
    # Should still return something
    assert isinstance(is_english, bool)
    assert isinstance(translated, str)