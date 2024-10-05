import openai
from PIL import Image
from io import BytesIO
from gtts import gTTS
import os
from dotenv import load_dotenv
import replicate

load_dotenv()
# Set up OpenAI and FLUX API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FLUX_API_KEY = os.getenv("FLUX_API_KEY")
os.environ["REPLICATE_API_TOKEN"] = os.getenv("FLUX_API_KEY")

# 1. Generate Script Using LLM

def generate_comic_script():
    openai.api_key = OPENAI_API_KEY
    prompt = (
        "Write a creative script for a 12-block comic featuring Sylendran, Joker, and Superman. "
        "The story should be fun and action-packed, with a clear beginning, middle, and end. "
        "Sylendran is a 28-year-old fit man. His images have been used to fine-tune the FLUX image generation model. "
        "The trigger word to create images of Sylendran using the FLUX model is 'sylendran'. "
        "The comic should give an interesting superhero role to Sylendran and come up with a creative and interesting 12-block comic chapter. "
        "It should be a short and complete story with an ending."
    )
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=800,
        temperature=0.9
    )
    script = response.choices[0].message.content.strip()

    # Save script to a local text file
    with open("comic_script.txt", "w") as script_file:
        script_file.write(script)
    return script

# 2. Generate Prompts for Each Comic Block

def generate_comic_prompts(script):
    # Split the script into 12 blocks
    blocks = script.split('\n')
    prompts = []
    for i, block in enumerate(blocks):
        if block.strip():
            prompt = f"sylendran: {block.strip()}"
            prompts.append(prompt)
    return prompts

# 3. Call the FLUX Model for Comic Image Generation

def generate_comic_images(prompts):
    #headers = {'Authorization': f'Bearer {FLUX_API_KEY}'}
    images = []
    #deployment = replicate.deployments.get("sylendran/my-comic-image-generator")
    for i, prompt in enumerate(prompts):
        response = replicate.run("sylendran/myimagemodel:e3ac779cfdf5f0638e147021be139c67289767e3621cc268d740c96888aa81b0", input={"prompt": prompt})
        if response and response.status == "succeeded":
            image = Image.open(BytesIO(response.output))
            image_path = f"comic_frame_{i + 1}.png"
            image.save(image_path)
            images.append(image_path)
        else:
            print(f"Failed to generate image for prompt: {prompt}")
    return images

# 4. Combine Images into a Comic Page

def create_comic_page(images):
    # Create a blank comic page
    page_width = 800
    page_height = 1200
    comic_page = Image.new("RGB", (page_width, page_height), "white")

    # Load each image and place it in a 3x4 grid
    block_width = page_width // 3
    block_height = page_height // 4
    for i, image_path in enumerate(images):
        image = Image.open(image_path)
        image = image.resize((block_width, block_height))
        x = (i % 3) * block_width
        y = (i // 3) * block_height
        comic_page.paste(image, (x, y))

    # Save the final comic page
    comic_page_path = "comic_page.png"
    comic_page.save(comic_page_path)
    print(f"Comic page saved as {comic_page_path}")

# 5. Use TTS to Narrate the Story

def narrate_story(script):
    openai.api_key = OPENAI_API_KEY
    prompt = (
        "Summarize the following comic script into a cohesive, fun narrative about the characters Sylendran, Joker, and Superman. "
        "Make it engaging and concise, highlighting the key events and interactions between the characters."
        f"\n\n{script}"
    )
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=800,
        temperature=0.9
    )
    story_narrative = response.choices[0].message.content.strip()

    # Use TTS to generate the narration
    tts = gTTS(text=story_narrative, lang='en')
    tts.save("comic_narration.mp3")
    print("Narration saved as comic_narration.mp3")
    os.system("start comic_narration.mp3")

# Main function to tie everything together
def main():
    # Step 1: Generate Script
    script = generate_comic_script()
    print("Generated Script:\n", script)

    # Step 2: Generate Prompts for Each Comic Block
    prompts = generate_comic_prompts(script)
    print("Generated Prompts:", prompts)

    # Step 3: Generate Comic Images
    images = generate_comic_images(prompts)
    print("Generated Images:", images)

    # Step 4: Create Comic Page
    create_comic_page(images)

    # Step 5: Narrate the Story
    narrate_story(script)

if __name__ == "__main__":
    main()