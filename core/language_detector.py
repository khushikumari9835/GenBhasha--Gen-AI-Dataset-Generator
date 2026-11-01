"""Language detection utilities."""

def detect_language(text):
    """
    Detect whether the input text is Hindi or English.
    Currently supports Hindi and English.
    """

    hindi_characters = 0
    english_characters = 0

    for char in text:

        # Hindi / Devanagari Unicode range
        if "\u0900" <= char <= "\u097F":
            hindi_characters += 1

        # English alphabet
        elif ("a" <= char.lower() <= "z"):
            english_characters += 1

    # Hindi
    if hindi_characters > english_characters:
        return "Hindi"

    # English
    elif english_characters > hindi_characters:
        return "English"

    # If no recognizable characters
    return "Unknown"

