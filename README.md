# 🐱 Cat Tagline Generator

An AI-powered application that fetches random cat images and generates funny taglines for them using OpenAI's APIs.

## Features

- 🎲 **Random Cat Images**: Fetches images from the Cat As A Service API
- 🔍 **AI Image Analysis**: Uses OpenAI's GPT-4 Vision to describe cat images
- 😸 **Funny Tagline Generation**: Creates witty, pun-filled taglines using GPT-4
- 🖥️ **Web Interface**: Beautiful Streamlit web app for easy interaction
- 💻 **Command Line**: Simple CLI script for quick usage

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get OpenAI API Key

1. Go to [OpenAI's API platform](https://platform.openai.com/api-keys)
2. Create a new API key
3. Copy the key for the next step

### 3. Configure API Key

#### For Local Development

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=your_actual_api_key_here
```

#### For Streamlit Community Cloud Deployment

You have two options:

**Option 1: Use Streamlit Secrets (Recommended)**
1. In your Streamlit Community Cloud dashboard, go to your app settings
2. Add a secret: `OPENAI_API_KEY = "your_actual_api_key_here"`

**Option 2: User Input**
- If no API key is configured, the app will prompt users to enter their API key
- The key is only used for that session and is not stored

## Usage

### Web Interface (Recommended)

Launch the beautiful Streamlit web interface:

```bash
streamlit run streamlit_app.py
```

Then open your browser to `http://localhost:8501`

### Command Line

Run the CLI version:

```bash
python cat_tagline_generator.py
```

## How It Works

1. **Fetch**: Gets a random cat image from the Cat As A Service API
2. **Analyze**: Uses OpenAI's GPT-4 Vision to describe the image in detail
3. **Generate**: Creates a funny tagline based on the description using GPT-4
4. **Display**: Shows the image, description, and tagline

### API Key Detection

The app automatically detects whether it's running locally or deployed:

- **Local Development**: Loads API key from `.env` file
- **Deployed (Streamlit Community Cloud)**:
  - First tries to load from Streamlit secrets
  - If not found, prompts user to enter API key
  - User-provided keys are only used for that session

## Example Output

```
🐱 Starting Cat Tagline Generator...
✅ Successfully fetched cat image (45231 bytes)
💾 Saved image as current_cat.jpg
🔍 Image description: A fluffy orange tabby cat sitting in a cardboard box, looking directly at the camera with bright green eyes and a slightly confused expression.
😸 Generated tagline: "When you order confidence online but get anxiety instead"
```

## Project Structure

```
cat-project/
├── cat_tagline_generator.py    # Main CLI application
├── streamlit_app.py           # Web interface
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── .env                      # Your API keys (create this)
├── current_cat.jpg           # Latest cat image (auto-generated)
└── README.md                 # This file
```

## API Usage

### Cat As A Service API
- **Endpoint**: `https://cataas.com/cat`
- **Usage**: Fetches random cat images
- **No API key required**

### OpenAI API
- **Models Used**:
  - `gpt-4o-mini` for image analysis
  - `gpt-4o-mini` for tagline generation
- **API Key Required**: Yes

## Troubleshooting

### Common Issues

1. **"Please set your OPENAI_API_KEY in the .env file"** (Local)
   - Make sure you've created a `.env` file with your API key
   - Copy `.env.example` to `.env` and add your key

2. **"OpenAI API Key Required"** (Deployed)
   - Either configure the API key in Streamlit secrets
   - Or enter your API key when prompted in the web interface

3. **"Error fetching cat image"**
   - Check your internet connection
   - The Cat As A Service API might be temporarily down

4. **"Error describing image" or "Error generating tagline"**
   - Check your OpenAI API key is valid
   - Ensure you have sufficient API credits

### Dependencies

- `requests`: For API calls
- `openai`: OpenAI Python client
- `pillow`: Image processing
- `python-dotenv`: Environment variables
- `streamlit`: Web interface

## Contributing

Feel free to fork this project and add your own improvements! Some ideas:

- Add support for other AI providers (Anthropic, Google Vision, etc.)
- Implement different tagline styles (professional, poetic, etc.)
- Add image filters or effects
- Save favorite combinations
- Share generated content on social media

## License

MIT License - feel free to use this code for your own projects!

---

Made with ❤️ and lots of cat photos