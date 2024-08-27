import os

import gradio as gr
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
# Use environment variables for API keys
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)


def generate_email(description):
    prompt = f"Given the following description of a person, write a professional email to them:\n\n{description}\n\nEmail:"
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional email writer.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=300,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error in generating response: {e}")
        return None


# Create the Gradio interface
iface = gr.Interface(
    fn=generate_email,
    inputs=gr.Textbox(lines=5, label="Describe the person:"),
    outputs=gr.Textbox(label="Generated Email:"),
    title="Personalized Email Generator",
    description="Enter a description of the person, and I'll generate a personalized email for you.",
)

# Launch the interface
iface.launch()
