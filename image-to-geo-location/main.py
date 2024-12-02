import json
import streamlit as st
import asyncio
from openai import AsyncOpenAI
import io
import os
import base64
import folium
from streamlit_folium import st_folium

# Set your OpenAI client
try:
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except:
    client = AsyncOpenAI()

# Set page configuration
st.set_page_config(
    page_title="Photo to Geo location guesser",
    page_icon="🌍",
)

# Center the entire app
st.markdown("<h1 style='text-align: center;'>Guess location from image</h1>", unsafe_allow_html=True)

# Instructions for Using the App
st.markdown("<h2 style='text-align: center;'>Instructions for Using the App</h2>", unsafe_allow_html=True)
st.write("1. Upload a photo - only jpg format (maximum size: 2 MB)")
st.write("2. Scroll down and click the 'Guess the Location!' button")
st.write("3. Wait a moment, and the result will be displayed below the button")

# Upload image
image = st.file_uploader(
    "Choose an Image file", accept_multiple_files=False, type=["jpg"]
)

# Convert the main function to an async function
async def main():
    # Initialize session state for map_location if not already done
    if "map_location" not in st.session_state:
        st.session_state.map_location = None
        st.session_state.markdown_content = ""
        
    # Process the uploaded image
    if image is not None:
        # Check file size
        if image.size > 2 * 1024 * 1024:  # 2 MB limit
            st.error("File size exceeds 2 MB. Please upload a smaller image.")
        else:
            # Display the uploaded image
            st.image(image, caption="Uploaded Image", use_container_width=False, width=400)

            generate = st.button(
                "Guess the location!", type="primary", use_container_width=True, disabled=False
            )

            if generate:
                st.write("Guessing the location. Please wait...")

                # Prepare the prompt for OpenAI
                prompt = """You are an Open Source Intelligence (OSINT) investigator. Your role is to determine the geographical location where a photo was taken. Identify the country, region, and city, and, if possible, specify the exact latitude and longitude of the location.

                    Thoroughly explain your methodology and reasoning behind your conclusion. Include detailed steps to verify your findings and indicate the confidence level (in percentage) of the location you have identified with steps and points in html format.
                    Return in json format like this only. Not in plain text and just plain json without without any code snippet like 'json' text: {text: "explanation", latitude: 0.0, longitude: 0.0, confidence: 0.0}"""

                # Convert the image to bytes
                image_bytes = io.BytesIO(image.read())
                image_bytes.seek(0)

                # Encode the image to base64
                image_base64 = base64.b64encode(image_bytes.getvalue()).decode("utf-8")

                # Call OpenAI API to analyze the image and generate a response
                response = await client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{image_base64}"
                                    },
                                },
                            ],
                        },
                    ],
                    max_tokens=8192,  # Maximum number of tokens in the response
                    temperature=1,    # Controls randomness; 1 for more creativity
                    top_p=0.95,       # Nucleus sampling; considers top 95% probability mass
                    # stream=True  # Enable streaming of responses
                )

                try:
                    content = response.choices[0].message.content
                    json_content = json.loads(content)
                    
                    # After processing the response and extracting latitude and longitude
                    latitude = json_content["latitude"]
                    longitude = json_content["longitude"]

                    # Create a map centered around the guessed location
                    map_location = folium.Map(location=[latitude, longitude], zoom_start=14)

                    # Add a marker for the guessed location
                    folium.Marker(
                        location=[latitude, longitude],
                        popup="Guessed Location",
                        icon=folium.Icon(color="blue")
                    ).add_to(map_location)

                    # Store the map and markdown content in session state
                    st.session_state.map_location = map_location
                    st.session_state.markdown_content = json_content["text"]
                    
                except Exception as e:
                    st.error(f"Failed to parse the JSON response. Please try again. Error: {str(e)}")
                    
                
                # Could not stream the JSON response
                # async for chunk in response:
                #     print(chunk)
                #     if chunk.choices[0].delta.content is not None:
                #         response_stream.empty()
                #         streamed_text += chunk.choices[0].delta.content
                #         response_stream.markdown(streamed_text)
    
    # Display the markdown content if it exists in session state
    if st.session_state.markdown_content:
        st.markdown(st.session_state.markdown_content)

    # Display the map if it exists in session state
    if st.session_state.map_location is not None:
        st_folium(st.session_state.map_location, width=700, height=500)


# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
