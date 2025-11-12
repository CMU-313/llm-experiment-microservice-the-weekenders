import ollama

def translate_content(content: str) -> tuple[bool, str]:
    """
    Translates non-English content to English using Qwen.
    Returns (is_english, translated_content).
    """
    if not content or not content.strip():
        return True, content
    
    try:
        # Use system message to enforce behavior
        response = ollama.chat(
            model='qwen2.5:0.5b',
            messages=[
                {
                    'role': 'system',
                    'content': 'You are a translator. You ONLY output the English translation of the input text. If the input is already in English, output it exactly as-is. Output NOTHING else - no explanations, no quotes, no extra words.'
                },
                {
                    'role': 'user',
                    'content': content
                }
            ],
            options={'temperature': 0.1}
        )
        
        translated = response['message']['content'].strip()
        
        # Clean up any remaining artifacts
        translated = translated.strip('"').strip("'").strip()
        
        # If translation is very similar to original, it was probably English
        is_english = (translated.lower().strip() == content.lower().strip())
        
        print(f"[DEBUG] Original: {content}")
        print(f"[DEBUG] Translated: {translated}")
        print(f"[DEBUG] is_english: {is_english}")
        
        return is_english, translated
        
    except Exception as e:
        # Fallback: assume English if LLM fails
        print(f"Translation error: {e}")
        return True, content
#LLM generated code