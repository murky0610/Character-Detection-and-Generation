import requests
import json

url = "http://demo.zktech.solutions:11434/api/chat"

# Load the input text from a file
with open('input_text.txt', 'r', encoding='utf-8') as file:
    text_input = file.read()

# Clean up the input text to remove excessive whitespaces
text_input = ' '.join(text_input.split())

# Check word count and ensure it doesn't exceed the 1000-word limit
if len(text_input.split()) > 1500:
    print("Error: Input exceeds the 1500-word limit. Please reduce the length.")
else:
    # Define the payload for extracting and describing main characters
    payload = {
        "model": "llama3",
        "messages": [
            {
                "role": "system",
                "content": (
                     """You are a highly skilled assistant specialized in main character analysis 
                     from novel texts. Please list the main characters from the given text and provide 
                     a detailed analysis of each character in paragraph form. Your analysis should 
                     include the character's name, role in the story, physical traits, personality 
                     traits, motivations, relationships, growth or change throughout the story, and 
                     any symbolism or themes they represent. Ensure that the descriptions are cohesive 
                     and well-structured. 
                    
                      Make the answer in one paragraph form for each character and detail as possible.
                    Follow this format: "
                    1. Character Name: Description of the character.
                    2. Character Name: Description of the character.
"""
# For each character, generate a creative prompt for illustrating or generating their image.
                )
            },

            {
                "role": "user",
                "content": (
                
                    f"Here is the text:\n{text_input} and make sure the output to be in only one paragraph form for each character."
                )
            },

        ],
     "options": {
            "temperature": 0.43,
            "num_ctx": 8192,  # Increase context window size for longer texts
            # "seed": 42,  # Set a seed for repeatable outputs
            # "repeat_penalty": 1.1  # Penalty for repetitions
        },
        "stream": False  # Single complete response, no streaming
    }

    # Make the request to the API
    response = requests.post(url, data=json.dumps(payload), headers={"Content-Type": "application/json"})

    try:
        # Parse the JSON response
        response_json = response.json()
        character_descriptions = response_json['message']['content']
        
        # Clean the output text
        cleaned_descriptions = character_descriptions.replace('**', '').strip()

        # Display or save the cleaned descriptions of the content only
        print(cleaned_descriptions)
        with open('character_descriptions.txt', 'w', encoding='utf-8') as output_file:
            output_file.write(cleaned_descriptions)
    except json.JSONDecodeError as e:
        print(f"JSON decoding failed: {e}")
        print(f"Raw response: {response.text}")
