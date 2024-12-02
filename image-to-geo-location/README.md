# Image to Geo Location 🌍

A Streamlit web application that uses OpenAI's gpt-4o-mini model to analyze photos and determine their geographical location. The app provides detailed location analysis with explanations using OSINT (Open Source Intelligence) investigation techniques.

## Demo

![Demo of the application](demo.gif)

## Features

- Upload and analyze photos to determine their geographical location
- Get detailed OSINT analysis including:
  - Country, region, and city identification
  - Possible exact coordinates (latitude/longitude)
  - Confidence level of the prediction
  - Detailed reasoning and methodology behind the location identification
- User-friendly interface with clear instructions
- Support for JPG image format
- Image size limit of 2MB to ensure optimal performance

## Requirements

- Python 3.6+
- OpenAI API key
- Required Python packages:
  - streamlit
  - openai

## Installation

1. Clone the repository:

```bash
git clone https://github.com/manjurulhoque/image-to-geo-location.git
cd image-to-geo-location

```

2. Install required packages:

```bash
pip install streamlit openai
```

3. Set up your OpenAI API key as an environment variable:
   ```bash
   export OPENAI_API_KEY=your_api_key_here
   ```

## Usage

1. Run the Streamlit app:

```bash
streamlit run main.py
```

2. Open your web browser and navigate to the provided local URL (typically http://localhost:8501)

3. Follow the on-screen instructions:
   - Upload a JPG image (max 2MB)
   - Click "Guess the Location!" button
   - Wait for the AI analysis
   - Review the detailed location prediction and explanation

## Limitations

- Only supports JPG image format
- Maximum image size of 2MB
- Requires an OpenAI API key
- Accuracy depends on the clarity and distinctive features in the uploaded image

## Contributing

Contributions are welcome! Feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.
