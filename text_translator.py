from googletrans import Translator

def translate_text(text, target_language):
    translator = Translator()
    translated = translator.translate(text, dest=target_language)
    return translated.text

# Test
text_to_translate = "Hello, how are you?"
target_language = "hi"  # Spanish
try:
    translated_text = translate_text(text_to_translate, target_language)
    print(translated_text)
except Exception as e:
    print(f"Error: {e}")
