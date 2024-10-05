# DC-Comic-Agent
This repository contains code to create a 12-block comic featuring Sylendran(Me), Joker, and Superman using fine-tuned image generation models and text-to-speech capabilities. The project integrates OpenAI's GPT for script generation, FLUX for comic image generation, and gTTS for audio narration.

# AI Comic Generator

This project is an experiment in creating a comic book using various AI technologies. The pipeline generates a script, turns it into images, assembles a comic page, and even narrates the story.

### Features
- **Script Generation:** Uses OpenAI's GPT to generate a fun and action-packed comic script involving Sylendran, Joker, and Superman.
- **Image Generation:** Fine-tunes the FLUX model via Replicate to generate comic frames from the script.
- **Comic Page Creation:** Assembles the generated images into a full comic page.
- **Narration:** Uses text-to-speech (gTTS) to create an engaging audio version of the story.

### Setup
1. Clone the repository.
2. Set up environment variables for `OPENAI_API_KEY` and `FLUX_API_KEY` by creating a `.env` file.
3. Install required Python packages:
   ```bash
   pip install openai pillow gtts python-dotenv replicate
   ```

### Running the Project
Run the main script to generate the comic:
```bash
python main.py
```

### Notes
- The script involves generating a 12-block comic with a creative story, and each block's image is created using the FLUX image generation model.
- The generated comic includes Sylendran in a superhero role, making this a fun personal project!
