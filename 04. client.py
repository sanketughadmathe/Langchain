import gradio as gr
import requests


def get_openai_response(input_text, history):
    response = requests.post(
        "http://localhost:8000/essay/invoke", json={"input": {"topic": input_text}}
    )

    return response.json()["output"]["content"]


def get_ollama_response(input_text, history):
    response = requests.post(
        "http://localhost:8000/poem/invoke", json={"input": {"topic": input_text}}
    )

    return response.json()["output"]["content"]


# Gradio Interface
iface = gr.ChatInterface(
    get_ollama_response,
    chatbot=gr.Chatbot(height=400),
    textbox=gr.Textbox(
        placeholder="Ask me anything about the wizarding world!", container=False
    ),
    title="Harry Potter Chatbot",
    description="Chat with a Harry Potter themed bot. Try asking about Hogwarts, Quidditch, or magic! You can also ask to be sorted into a house or introduce yourself!",
    theme="soft",
)

iface.launch()
