import streamlit as st
from anthropic import Anthropic
from PIL import Image
import io
import base64
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import pillow-heif for HEIC support
from pillow_heif import register_heif_opener

# Register HEIC support
register_heif_opener()

# Page configuration
st.set_page_config(
    page_title="Claude OCR",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Anthropic client
client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

# Function to preprocess image
def preprocess_image(uploaded_file):
    """
    Preprocess the uploaded image to ensure compatibility with Claude API
    """
    # Open the image
    image = Image.open(uploaded_file)
    
    # Convert to RGB if not already
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Resize large images to reduce file size
    max_size = (2000, 2000)  # Adjust as needed
    image.thumbnail(max_size, Image.LANCZOS)
    
    # Save to a bytes buffer
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=85)
    buffer.seek(0)
    
    # Convert to base64
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

# Function to process a single image
def process_image(uploaded_file, index):
    base64_image = preprocess_image(uploaded_file)
    
    # Call Claude API with increased token limit
    response = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=4000,  # Adjust as needed
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """Analyze the text in the provided image. Extract all readable content
                        and present it in a structured Markdown format that is clear, concise, 
                        and well-organized."""
                    },
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": base64_image
                        }
                    }
                ]
            }
        ]
    )
    
    return {
        "filename": uploaded_file.name,
        "content": response.content[0].text
    }

# Initialize session state for results if it doesn't exist
if 'all_results' not in st.session_state:
    st.session_state['all_results'] = []

# Title and description in main area
st.markdown("""
    # Note Extraction
""", unsafe_allow_html=True)

# Add clear button to top right
col1, col2 = st.columns([6,1])
with col2:
    if st.button("Clear 🗑️"):
        if 'all_results' in st.session_state:
            st.session_state['all_results'] = []
        st.rerun()

st.markdown('<p style="margin-top: -20px;">Input multiple images and have Claude use OCR to extract your text! How cool is that!</p>', unsafe_allow_html=True)
st.markdown("---")

# Move upload controls to sidebar
with st.sidebar:
    st.header("Upload Images")
    uploaded_files = st.file_uploader("Choose images...", type=['png', 'jpg', 'jpeg', 'heic', 'webp'], accept_multiple_files=True)
    
    if uploaded_files:
        # Display thumbnails of the uploaded images
        st.subheader(f"Uploaded {len(uploaded_files)} Images")
        
        # Display thumbnails in a grid
        cols = st.columns(min(3, len(uploaded_files)))
        for i, uploaded_file in enumerate(uploaded_files):
            with cols[i % 3]:
                image = Image.open(uploaded_file)
                st.image(image, caption=uploaded_file.name, width=150)
        
        if st.button("Extract Text from All Images 🔍", type="primary"):
            st.session_state['all_results'] = []  # Clear previous results
            
            # Process each image with a progress bar
            progress_bar = st.progress(0)
            for i, uploaded_file in enumerate(uploaded_files):
                with st.spinner(f"Processing image {i+1}/{len(uploaded_files)}..."):
                    try:
                        result = process_image(uploaded_file, i)
                        st.session_state['all_results'].append(result)
                    except Exception as e:
                        st.error(f"Error processing {uploaded_file.name}: {str(e)}")
                
                # Update progress bar
                progress_bar.progress((i + 1) / len(uploaded_files))
            
            progress_bar.empty()

# Main content area for results
if st.session_state['all_results']:
    for i, result in enumerate(st.session_state['all_results']):
        st.markdown(f"## Image {i+1}: {result['filename']}")
        st.markdown(result['content'])
        
        # Add separator between results except for the last one
        if i < len(st.session_state['all_results']) - 1:
            st.markdown("---")
else:
    st.info("Upload one or more images and click 'Extract Text from All Images' to see the results here.")
