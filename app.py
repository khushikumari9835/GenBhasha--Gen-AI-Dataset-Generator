
import streamlit as st
from core.generator import generate_variations

# Page configuration
st.set_page_config(
    page_title="GenAI Dataset Generator",
    page_icon="🤖",
    layout="wide"
)

# Title
st.title("🤖 GenAI Dataset Generator")

st.write(
    "Generate diverse Hindi and English sentences using Generative AI."
)

st.divider()

# Input method
st.subheader("1. Choose Input Method")

input_method = st.radio(
    "How do you want to provide your data?",
    ["Enter Sentence", "Upload File"],
    horizontal=True
)

# Sentence input
if input_method == "Enter Sentence":

    st.subheader("2. Enter Your Sentence")

    sentence = st.text_area(
        "Write a sentence:",
        placeholder="Example: राम बाजार जा रहा है।"
    )

    st.subheader("3. Generation Settings")

    col1, col2 = st.columns(2)

    with col1:
        language = st.selectbox(
            "Language",
            ["Auto Detect", "Hindi", "English"]
        )

    with col2:
        variations = st.number_input(
            "Number of variations",
            min_value=1,
            max_value=100,
            value=10
        )

    flavor = st.selectbox(
    "Generation Flavor",
    [
        "Mixed",
        "Natural Paraphrase",
        "Verb Variation",
        "Noun Variation",
        "Sentence Structure",
        "Formal",
        "Informal"
    ]
)

    if st.button("🚀 Generate Dataset"):

        if sentence.strip():

            with st.spinner("🤖 Generating variations using Qwen AI..."):

                try:

                    result = generate_variations(
                            sentence,
                            language,
                            variations,
                            flavor
                        )

                    st.success(
                        "✅ Dataset generated successfully!"
                    )

                    st.subheader("Generated Variations")
                    for i, variation in enumerate(result, start=1):
                        st.write(f"**{i}.** {variation}")
                except Exception as e:

                    st.error(
                        f"❌ Error while generating dataset: {e}"
                    )

        else:

            st.warning("⚠️ Please enter a sentence.")


# File upload
else:

    st.subheader("2. Upload Your Dataset")

    uploaded_file = st.file_uploader(
        "Upload DOCX or Excel file",
        type=["docx", "xlsx", "xls"]
    )

    if uploaded_file is not None:

        st.success(
            f"File uploaded: {uploaded_file.name}"
        )

        st.subheader("3. Generation Settings")

        col1, col2 = st.columns(2)

        with col1:
            language = st.selectbox(
                "Language",
                ["Auto Detect", "Hindi", "English"]
            )

        with col2:
            target_size = st.number_input(
                "Target dataset size",
                min_value=1,
                max_value=100000,
                value=1000
            )

        if st.button("🚀 Generate Dataset"):

            st.info(
                "File processing will be added in the next step."
            )
