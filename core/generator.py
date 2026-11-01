
import ollama
from core.language_detector import detect_language

def generate_variations(
    sentence,
    language,
    number_of_variations,
    flavor="Mixed"
):
    """
    Generate sentence variations in the selected language.
    """

    # -----------------------------
    # Language instruction
    # -----------------------------
    if language == "Auto Detect":
       detected_language = detect_language(sentence)
    else:
        detected_language = language

    if detected_language == "Hindi":

        language_instruction = """
The output language MUST be Hindi.

Translate the meaning of the original sentence into Hindi
and then generate natural Hindi variations.

Use Devanagari script (हिंदी).
Do NOT write the output in English.
Do NOT use Roman Hindi.
Every generated sentence must be written completely in Hindi.
"""

    elif detected_language == "English":

        language_instruction = """
The output language MUST be English.

Generate all variations in natural English.
Do NOT translate the output into Hindi.
Do NOT use Hindi or Devanagari script.
"""

    else:

        language_instruction = """
Detect the language of the original sentence.

Generate all variations in the same language as the
original sentence.
"""

    # -----------------------------
    # Flavor instruction
    # -----------------------------

    if flavor == "Natural Paraphrase":

        flavor_instruction = """
Create natural paraphrases.
Use different wording and sentence constructions
while preserving the exact meaning.
"""

    elif flavor == "Verb Variation":

        flavor_instruction = """
Focus on varying verbs and verb phrases.
Keep the meaning, subject and tense unchanged.
"""

    elif flavor == "Noun Variation":

        flavor_instruction = """
Vary nouns or noun phrases where naturally possible.
Do not introduce new entities or change the meaning.
"""

    elif flavor == "Sentence Structure":

        flavor_instruction = """
Create variations by changing the grammatical structure
and word order while preserving the original meaning.
"""

    elif flavor == "Formal":

        flavor_instruction = """
Create natural formal versions of the sentence.
Keep the original meaning unchanged.
"""

    elif flavor == "Informal":

        flavor_instruction = """
Create natural conversational and informal versions.
Keep the original meaning unchanged.
"""

    else:

        # Mixed
        flavor_instruction = """
Use a balanced mixture of:

- Natural paraphrasing
- Verb variation
- Noun variation
- Sentence structure variation
- Formal phrasing
- Informal phrasing
- Natural vocabulary variation

Do not use only one technique repeatedly.
Make the generated sentences genuinely different.
"""

    # -----------------------------
    # Prompt
    # -----------------------------

    prompt = f"""
You are an expert multilingual dataset augmentation system.

ORIGINAL SENTENCE:
{sentence}

TARGET LANGUAGE:
{detected_language}

LANGUAGE RULE:
{language_instruction}

GENERATION FLAVOR:
{flavor}

FLAVOR RULE:
{flavor_instruction}

Generate exactly {number_of_variations} variations.

VERY IMPORTANT:

1. The output MUST be in the TARGET LANGUAGE.
2. Follow the language instruction strictly.
3. Preserve the exact meaning of the original sentence.
4. Do not change the main event or intent.
5. Do not introduce new facts.
6. Do not introduce new people, places or objects.
7. Keep the original tense whenever possible.
8. Every sentence must be grammatically correct.
9. Every sentence must sound natural to a native speaker.
10. Do not create awkward word order.
11. Do not repeatedly use the same sentence structure.
12. Avoid simple synonym replacement repeatedly.
13. Make the variations meaningfully different.
14. Generate exactly {number_of_variations} sentences.
15. Put each sentence on a separate line.

OUTPUT FORMAT:

Return ONLY the sentences.

Do NOT include:
- numbering
- bullet points
- flavor names
- explanations
- arrows
- quotation marks
- headings
- English text when the target language is Hindi
- Hindi text when the target language is English

Example for Hindi target language:

राम बाजार की ओर जा रहा है।
राम बाजार जाने के लिए निकल रहा है।
राम बाजार की तरफ बढ़ रहा है।
राम बाजार जा रहा है।

Example for English target language:

Rama is heading towards the market.
Rama is making his way to the market.
Rama is on his way to the market.
Rama is heading for the market.

Now generate the requested variations.
"""

    # -----------------------------
    # Call Ollama
    # -----------------------------

    response = ollama.chat(
        model="qwen2.5:7b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    result = response["message"]["content"]

    # -----------------------------
    # Clean output
    # -----------------------------

    lines = result.splitlines()

    variations = []

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # Remove numbering
        if line[0].isdigit():

            if "." in line:
                line = line.split(".", 1)[1].strip()

            elif ")" in line:
                line = line.split(")", 1)[1].strip()

        # Remove bullet points
        if line.startswith("-"):
            line = line[1:].strip()

        # Remove markdown bold
        line = line.replace("**", "").strip()

        # Remove accidental flavor labels
        if "→" in line:
            line = line.split("→", 1)[0].strip()

        if line:
            variations.append(line)

    # -----------------------------
    # Remove duplicates
    # -----------------------------

    unique_variations = []
    seen = set()

    for variation in variations:

        normalized = variation.lower().strip()

        if normalized not in seen:

            seen.add(normalized)
            unique_variations.append(variation)

    return unique_variations
