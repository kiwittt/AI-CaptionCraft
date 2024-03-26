import streamlit as st
from dotenv import load_dotenv
import openai
import os

# Load environment variables from .env file
load_dotenv(".env")

# Load OpenAI API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

openai.api_key = openai_api_key  

def generate_caption(product_description, key_features, brand_style, platform, char_limit=None):
    """
    This function uses OpenAI API to generate a caption based on user input.

    Args:
        product_description: Description of the product/service (string).
        key_features: List of key features (strings).
        brand_style: Selected brand style (string).
        platform: Chosen social media platform (string).
        char_limit: Preferred character limit (int, optional).

    Returns:
        A generated caption (string).
    """

    # Combine key features into a string
    features_list = "\n".join(key_features)

    # Define platform-specific instructions
    platform_instructions = {
        "Twitter": f"Write an engaging Twitter caption (max 280 characters) promoting {product_description} with key features: {features_list}. Use a {brand_style} tone. Include relevant hashtags like #yourhashtag.",
        "Facebook": f"Craft a compelling Facebook post (no strict character limit) about {product_description}, highlighting its benefits ({features_list}) and aligning with your {brand_style} brand voice. Add relevant hashtags like #yourhashtag.",
        "Instagram": f"Generate a catchy Instagram caption (max 2200 characters) for {product_description}. Emphasize key features ({features_list}) and maintain a {brand_style} style. Suggest relevant hashtags like #yourhashtag."
    }

    instruction = platform_instructions[platform]

    # Set character limit based on platform or user input
    if char_limit is None:
        if platform == "Twitter":
            char_limit = 280
        elif platform == "Instagram":
            char_limit = 2200
        else:
            char_limit = None

    
    chat_completion = openai.chat.completions.create(
        messages=[
            {"role": "user", "content": instruction}
        ],
        model='gpt-3.5-turbo',
        max_tokens=char_limit
    )

    if chat_completion and chat_completion.choices:
        response = chat_completion.choices[0].message.content
        return response
    else:
        return "Error generating caption."


# Custom CSS styling
custom_css = """
<style>
.title-text {
    border-bottom: 2px solid #ff6347;
    padding-bottom: 10px;
    margin-bottom: 20px;
}
.caption-text {
    font-size: 18px;
    font-weight: bold;
    color: #333333;
}
</style>
"""

# Apply the custom CSS styling
st.markdown(custom_css, unsafe_allow_html=True)

# Set the title with a line underneath
st.title("AI CaptionCraft: Social Media Caption Generator")
st.markdown("<p class='title-text'>Empower your brand with AI-generated captivating captions!</p>", unsafe_allow_html=True)

product_desc = st.text_area("Describe your product or service:")
key_features = st.text_area("List your product's key features (separate by line):")
brand_style = st.radio("Choose your brand style:", ("Professional", "Playful", "Educational", "Witty", "Elegant", "Modern", "Edgy", "Sophisticated", "Humorous"))
platform = st.radio("Select your platform:", ("Twitter", "Facebook", "Instagram"))
char_limit = st.number_input("Preferred character limit (leave blank for platform defaults):", min_value=0)

# Custom style for the generate button
button_style = """
    <style>
    .stButton>button {
        background-color: #ff6347 !important; 
        color: white !important; 
        font-weight: bold; 
    }
    </style>
    """

st.markdown(button_style, unsafe_allow_html=True)  # Apply the custom button style

if st.button("Generate Caption"):
    caption = generate_caption(product_desc, key_features.splitlines(), brand_style, platform, char_limit)
    st.markdown("<p class='caption-text'>Generated Caption:</p>", unsafe_allow_html=True)
    st.write(caption)
