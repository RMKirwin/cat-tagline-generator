#!/usr/bin/env python3
"""
Streamlit Web Interface for Cat Tagline Generator

This script demonstrates how to build a beautiful web application using Streamlit,
a Python framework that lets you create web apps without HTML, CSS, or JavaScript.

Key concepts demonstrated:
- Streamlit app structure and lifecycle
- Custom CSS styling within Streamlit
- Interactive widgets and user input handling
- State management and session handling
- Frontend/backend separation and integration
- Responsive web design principles
- User experience (UX) best practices

Streamlit works by:
1. Running Python code from top to bottom
2. Re-running the entire script when users interact with widgets
3. Automatically creating a web interface from Python functions
4. Handling all the web server complexity behind the scenes
"""

# ============================================================================
# IMPORTS SECTION
# ============================================================================
# Streamlit - the main web application framework
import streamlit as st

# Our backend logic - this demonstrates separation of concerns
# The web interface (frontend) calls the AI pipeline (backend)
from cat_tagline_generator import CatTaglineGenerator

# Standard library imports
import os                # For environment variables and file operations
from PIL import Image    # For image handling and display

# ============================================================================
# STREAMLIT PAGE CONFIGURATION
# ============================================================================
# This MUST be the first Streamlit command in your script
# It configures how the web page looks and behaves
st.set_page_config(
    page_title="Cat Tagline Generator",    # Shows in browser tab
    page_icon="🐱",                        # Emoji icon in browser tab
    layout="centered",                     # "centered" vs "wide" layout
    initial_sidebar_state="collapsed"      # Start with sidebar hidden for cleaner look
)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================
def is_running_locally():
    """
    Detect if the app is running locally or deployed to Streamlit Community Cloud.

    Returns:
        bool: True if running locally, False if deployed
    """
    # Check for common indicators of local development
    # Streamlit Community Cloud sets specific environment variables
    return (
        os.getenv('STREAMLIT_SHARING_MODE') is None and
        os.getenv('STREAMLIT_SERVER_PORT') is None and
        'streamlit.io' not in os.getenv('STREAMLIT_SERVER_ADDRESS', '')
    )

def get_api_key():
    """
    Get the OpenAI API key from either environment variables (local) or user input (deployed).

    Returns:
        str or None: The API key if available, None otherwise
    """
    if is_running_locally():
        # Running locally - try to get from .env file
        return os.getenv('OPENAI_API_KEY')
    else:
        # Running deployed - get from Streamlit secrets or user input
        # First try Streamlit secrets (recommended for deployment)
        try:
            return st.secrets["OPENAI_API_KEY"]
        except (KeyError, FileNotFoundError):
            # If not in secrets, ask user for input
            return None

# ============================================================================
# CUSTOM CSS STYLING
# ============================================================================
# Streamlit allows custom CSS to make your app look professional
# st.markdown() with unsafe_allow_html=True lets us inject HTML/CSS
st.markdown("""
<style>
    /* Main header styling - large, centered, coral color */
    .main-header {
        text-align: center;
        color: #FF6B6B;           /* Coral color for warmth and friendliness */
        font-size: 3rem;         /* Large size for impact */
        margin-bottom: 1rem;     /* Space below header */
    }

    /* Subtitle styling - smaller, centered, turquoise color */
    .subtitle {
        text-align: center;
        color: #4ECDC4;           /* Turquoise color for contrast */
        font-size: 1.2rem;       /* Readable but not overpowering */
        margin-bottom: 2rem;     /* More space to separate from content */
    }

    /* Tagline display box - warm gray background with coral accent */
    .tagline-box {
        background-color: #F7F7F7;  /* Light gray background */
        padding: 1rem;              /* Internal spacing */
        border-radius: 10px;        /* Rounded corners for modern look */
        border-left: 5px solid #FF6B6B;  /* Coral accent bar */
        margin: 1rem 0;             /* Vertical spacing */
    }

    /* Description display box - blue theme to differentiate from tagline */
    .description-box {
        background-color: #E8F4FD;  /* Light blue background */
        padding: 1rem;              /* Internal spacing */
        border-radius: 10px;        /* Rounded corners for consistency */
        border-left: 5px solid #4ECDC4;  /* Turquoise accent bar */
        margin: 1rem 0;             /* Vertical spacing */
    }

    /* API key input styling */
    .api-key-section {
        background-color: #FFF9E6;  /* Light yellow background */
        padding: 1rem;              /* Internal spacing */
        border-radius: 10px;        /* Rounded corners */
        border-left: 5px solid #FFD700;  /* Gold accent bar */
        margin: 1rem 0;             /* Vertical spacing */
    }
</style>
""", unsafe_allow_html=True)
# unsafe_allow_html=True is required because we're injecting HTML/CSS
# Normally Streamlit escapes HTML for security, but we need it for styling

# ============================================================================
# MAIN APPLICATION FUNCTION
# ============================================================================
def main():
    """
    Main function that defines the core application layout and logic.

    This function demonstrates:
    - Streamlit's declarative UI approach
    - Conditional rendering based on state
    - Column-based layouts for responsive design
    - Integration between frontend UI and backend logic

    Streamlit Execution Model:
    - This function runs every time the user interacts with the app
    - Streamlit re-runs the entire script from top to bottom
    - State is maintained between runs using Streamlit's session state
    """

    # ========================================================================
    # HEADER SECTION
    # ========================================================================
    # Create the main header using our custom CSS class
    # st.markdown() with HTML allows us to use our custom styles
    st.markdown('<h1 class="main-header">🐱 Cat Tagline Generator</h1>', unsafe_allow_html=True)

    # Create subtitle with description of the app's purpose
    st.markdown('<p class="subtitle">AI-powered funny taglines for random cat images!</p>', unsafe_allow_html=True)

    # ========================================================================
    # API KEY CONFIGURATION SECTION
    # ========================================================================
    api_key = get_api_key()
    user_provided_key = None

    if is_running_locally():
        # Running locally - check for .env file
        if not api_key:
            st.markdown('<div class="api-key-section">', unsafe_allow_html=True)
            st.error("🔑 Please set your OPENAI_API_KEY in the .env file to use this app!")
            st.info("💡 Copy .env.example to .env and add your OpenAI API key")
            st.markdown('</div>', unsafe_allow_html=True)
            return
        else:
            st.success("✅ Running locally with API key from .env file")
    else:
        # Running deployed - check secrets or ask for user input
        if not api_key:
            st.markdown('<div class="api-key-section">', unsafe_allow_html=True)
            st.warning("🔑 OpenAI API Key Required")
            st.info("This app is running on Streamlit Community Cloud. Please enter your OpenAI API key below:")

            user_provided_key = st.text_input(
                "Enter your OpenAI API Key:",
                type="password",
                help="Your API key will not be stored and is only used for this session."
            )

            if not user_provided_key:
                st.info("👆 Please enter your OpenAI API key above to continue")
                st.markdown('</div>', unsafe_allow_html=True)
                return
            else:
                api_key = user_provided_key
                st.success("✅ API key provided - ready to generate cat content!")
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.success("✅ Running deployed with API key from Streamlit secrets")

    # ========================================================================
    # MAIN INTERFACE SECTION
    # ========================================================================
    # Create a three-column layout for better visual balance
    # The middle column (col2) will be twice as wide as the side columns
    col1, col2, col3 = st.columns([1, 2, 1])

    # Use the middle column for our main button
    # This centers the button and makes it prominent
    with col2:
        # st.button() creates an interactive button
        # When clicked, it returns True and triggers the condition
        if st.button("🎲 Generate Cat Content!", type="primary", use_container_width=True):
            # type="primary" makes it a prominent blue button
            # use_container_width=True makes it fill the column width
            generate_cat_content(api_key)

    # ========================================================================
    # EXISTING CONTENT DISPLAY SECTION (COMMENTED OUT FOR CLEANER UI)
    # ========================================================================
    # Check if there's already a cat image from a previous run
    # This demonstrates state persistence using the file system
    # if os.path.exists("current_cat.jpg"):
    #     # st.markdown("---") creates a horizontal line separator
    #     st.markdown("---")
    #     display_current_cat()

def generate_cat_content(api_key: str):
    """
    Generate new cat content using the AI pipeline.

    This function demonstrates:
    - Integration between Streamlit frontend and custom backend
    - Loading states and user feedback
    - Error handling in web applications
    - Calling external functions from Streamlit

    Args:
        api_key: The OpenAI API key to use for generation

    Key Streamlit Concepts:
    - st.spinner(): Shows loading animation
    - st.success(): Shows green success message
    - st.error(): Shows red error message
    - Exception handling in web context
    """

    # Show a loading spinner while the AI pipeline runs
    # This provides immediate user feedback that something is happening
    # The context manager automatically removes the spinner when done
    with st.spinner("🐱 Fetching a random cat..."):
        try:
            # Create an instance of our backend class with the API key
            # This demonstrates separation of concerns - UI vs business logic
            generator = CatTaglineGenerator(api_key=api_key)

            # Run the complete AI pipeline
            # This can take several seconds due to API calls
            result = generator.run_full_pipeline()

            # Check if the pipeline succeeded
            if result.get("success"):
                # Show success message with green checkmark
                st.success("🎉 Generated new cat content!")

                # Display the results to the user
                display_results(result)
            else:
                # Show error message with details
                error_msg = result.get("error", "Unknown error occurred")
                st.error(f"❌ Error: {error_msg}")

        except Exception as e:
            # Catch any unexpected errors and show user-friendly message
            st.error(f"❌ Unexpected error: {str(e)}")
            # In production, you might want to log this error for debugging
            print(f"Error in generate_cat_content: {e}")

def display_results(result):
    """
    Display the generated cat content in a beautiful, organized way.

    This function demonstrates:
    - Image display in Streamlit
    - Custom HTML/CSS styling within Streamlit
    - Responsive image handling
    - Structured content presentation

    Args:
        result (dict): Dictionary containing image_path, description, and tagline

    Key Streamlit Concepts:
    - st.image(): Display images with automatic formatting
    - use_container_width: Makes images responsive
    - Custom HTML injection for advanced styling
    """

    # ========================================================================
    # IMAGE DISPLAY SECTION
    # ========================================================================
    # Check if the image file exists before trying to display it
    if os.path.exists(result["image_path"]):
        # Load the image using PIL (Pillow)
        image = Image.open(result["image_path"])

        # Display the image using Streamlit's built-in image widget
        st.image(
            image,                           # The PIL Image object
            caption="Your Random Cat",      # Caption appears below image
            use_container_width=True        # Makes image responsive to container width
        )

    # ========================================================================
    # DESCRIPTION DISPLAY SECTION (COMMENTED OUT)
    # ========================================================================
    # # Use simple Streamlit components instead of custom HTML to avoid rendering issues
    # st.subheader("🔍 AI Description:")
    # st.write(result["description"])

    # ========================================================================
    # TAGLINE DISPLAY SECTION
    # ========================================================================
    # Display the funny tagline using simple Streamlit components
    st.subheader("😸 Funny Tagline:")

    if "tagline" in result and result["tagline"]:
        # Remove any existing quotes from the tagline to prevent double quotes
        clean_tagline = result["tagline"].strip('"')
        st.write(f'"{clean_tagline}"')
    else:
        st.error("❌ No tagline found in results!")
    # The tagline-box class uses different colors to distinguish from description

def display_current_cat():
    """
    Display the current cat image and instructions for getting a new one.

    This function demonstrates:
    - Conditional content display
    - File existence checking
    - User guidance and instructions
    - State management using files

    This function is called when there's already a cat image saved,
    showing the user what they have and how to get a new one.
    """

    # Create a section header
    st.subheader("🐱 Current Cat")

    # Display the existing image
    image = Image.open("current_cat.jpg")
    st.image(image, caption="Current Cat Image", use_container_width=True)

    # Provide user guidance
    # st.info() creates a blue informational box
    st.info("💡 Click 'Generate Cat Content!' to get a new cat with AI-generated description and tagline!")

# ============================================================================
# SIDEBAR INFORMATION PANEL
# ============================================================================
# The sidebar provides additional information without cluttering the main interface
# This demonstrates good UX design - keep main area focused, details in sidebar
with st.sidebar:
    # ========================================================================
    # ABOUT SECTION
    # ========================================================================
    st.header("ℹ️ About")
    st.write("""
    This app uses:
    - **Cat As A Service API** for random cat images
    - **OpenAI GPT-4 Vision** to describe images
    - **OpenAI GPT-4** to generate funny taglines
    """)
    # st.write() supports Markdown formatting (**bold**, bullet points, etc.)

    # ========================================================================
    # SETUP INSTRUCTIONS SECTION
    # ========================================================================
    st.header("🛠️ Setup")
    st.write("""
    1. Get an OpenAI API key
    2. Copy `.env.example` to `.env`
    3. Add your API key to `.env`
    4. Run: `streamlit run streamlit_app.py`
    """)
    # Numbered lists help users follow setup steps

    # ========================================================================
    # FEATURES SECTION
    # ========================================================================
    st.header("🎯 Features")
    st.write("""
    - Random cat image fetching
    - AI-powered image analysis
    - Witty tagline generation
    - Beautiful web interface
    """)
    # Bullet points make features easy to scan

# ============================================================================
# SCRIPT ENTRY POINT
# ============================================================================
# This ensures main() only runs when the script is executed directly
# When Streamlit runs this file, __name__ will be "__main__"
if __name__ == "__main__":
    main()

# ============================================================================
# STREAMLIT EXECUTION NOTES (COMMENTED OUT FOR CLEANER CODE)
# ============================================================================
# """
# How Streamlit Works:

# 1. **Script Execution**: Streamlit runs your Python script from top to bottom
# 2. **Widget Interaction**: When users interact with widgets (buttons, sliders, etc.)
# 3. **Re-execution**: Streamlit re-runs the entire script with new widget values
# 4. **State Management**: Streamlit remembers widget states between runs
# 5. **Caching**: Use @st.cache_data for expensive operations
# 6. **Session State**: Use st.session_state for custom state management

# Key Streamlit Concepts:

# - **Declarative**: You describe what you want, Streamlit figures out how
# - **Reactive**: UI automatically updates when data changes
# - **Pythonic**: Write web apps using only Python, no HTML/CSS/JS required
# - **Fast Development**: Changes appear immediately when you save the file

# Performance Tips:

# - Use st.spinner() for long-running operations
# - Cache expensive computations with @st.cache_data
# - Minimize API calls by storing results
# - Use st.session_state for persistent data across runs
# """