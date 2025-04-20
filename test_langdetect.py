# test_langdetect.py
try:
    from langdetect import detect
    print("Langdetect imported successfully!")
except ModuleNotFoundError as e:
    print("Langdetect not found.")
    print(e)  # Print the error message for more details

# Optional: Test the detect function
try:
    text = "This is a test sentence."
    language = detect(text)
    print(f"The detected language is: {language}")
except Exception as e:
    print("Error using langdetect:", e)
