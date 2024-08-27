import os
import random

import gradio as gr
from langchain.schema import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

## Langmith tracking
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

# Predefined responses for fallback
responses = {
    "how is hogwarts": [
        "Hogwarts is as magical as ever! The castle is bustling with students and enchantments.",
        "Ah, Hogwarts! A place full of mystery and wonder. Anything specific you'd like to know?",
        "Hogwarts is always full of surprises. What part of it intrigues you the most?",
    ],
    "hello harry": [
        "Hello! I'm Harry Potter. What can I help you with?",
        "Hi there! Harry here, ready to answer your questions.",
        "You can count on me, Harry Potter, to assist you. What do you need?",
    ],
    "what is quidditch": [
        "Quidditch is a magical sport played on broomsticks. It's thrilling and dangerous! Any particular aspect you want to know about?",
        "In Quidditch, players fly on broomsticks and try to score points by getting the Quaffle through hoops. Interested in the rules or positions?",
        "Quidditch is the most popular sport in the wizarding world. What about it interests you?",
    ],
    "what spells can i learn": [
        "There are countless spells you can learn, from basic charms to advanced hexes. Any spell in particular?",
        "Spells at Hogwarts range from simple Lumos to complex Patronus charms. What are you looking to master?",
        "Learning spells is an essential part of being a wizard. Which spell do you want to start with?",
    ],
    "how to make a potion": [
        "Potion-making requires precise ingredients and careful brewing. What potion are you interested in?",
        "From Polyjuice Potion to Felix Felicis, potion-making is an art. Do you need help with a specific recipe?",
        "Brewing potions is a skillful craft. What kind of potion are you looking to create?",
    ],
    "where is dumbledore": [
        "Professor Dumbledore is usually in his office, behind the statue of the phoenix.",
        "You can find Dumbledore at Hogwarts, always ready to guide and protect the students.",
        "Dumbledore is the headmaster of Hogwarts, often found in his office or around the castle.",
    ],
    "default": [
        "The wizarding world is vast and magical. What else would you like to know?",
        "There's always something fascinating about Hogwarts. Any other questions?",
        "I'm here to help you explore the magical world. What else can I assist you with?",
    ],
}
# User info storage
user_info = {"name": None, "house": None}


def sort_into_house():
    houses = ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]
    return random.choice(houses)


# LangChain setup
llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0,
)

prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a Harry Potter themed chatbot. Respond in character as if you are Harry Potter himself. Current context:\n{context}",
        ),
        ("human", "{input}"),
    ]
)

output_parser = StrOutputParser()

chain = prompt_template | llm | output_parser


def generate_response(prompt, context):
    try:
        output = chain.invoke({"input": prompt, "context": context})
        return output.strip()
    except Exception as e:
        print(f"Error in generating response: {e}")
        return None


def chatbot(message, history):
    message = message.lower()

    # Construct a context string from history
    context = "\n".join(
        [f"User: {h[0]}\nHarry: {h[1]}" for h in history[-5:]]
    )  # Last 5 exchanges

    if "my name is" in message:
        name = message.split("my name is")[-1].strip()
        user_info["name"] = name
        return f"Nice to meet you, {name}! Welcome to Hogwarts!"

    elif "sort me" in message:
        if user_info["house"] is None:
            user_info["house"] = sort_into_house()
            return f"Let's see... I think you belong in... {user_info['house']}!"
        else:
            return f"You've already been sorted into {user_info['house']}!"

    else:
        # Fallback to predefined responses if Llama 3 fails
        for key in responses:
            if key in message:
                return random.choice(responses[key])

        # Include context in the prompt for Llama 3
        prompt = f"{context}\nUser: {message}\nHarry:"
        llm_response = generate_response(message, context)
        if llm_response:
            return llm_response

        return random.choice(responses["default"])
        # # Include context in the prompt for LangChain
        # llm_response = generate_response(message, context)
        # return llm_response


# Example interactions
examples = [
    ["How is Hogwarts?"],
    ["Hello Harry"],
    ["What is Quidditch?"],
    ["Sort me into a house"],
    ["My name is Hermione"],
    ["Where is Dumbledore?"],
    ["What spells can I learn"],
    ["How to make a potion"],
]

# Gradio Interface
iface = gr.ChatInterface(
    chatbot,
    chatbot=gr.Chatbot(height=400),
    textbox=gr.Textbox(
        placeholder="Ask me anything about the wizarding world!", container=False
    ),
    title="Harry Potter Chatbot",
    description="Chat with a Harry Potter themed bot. Try asking about Hogwarts, Quidditch, or magic! You can also ask to be sorted into a house or introduce yourself!",
    theme="soft",
    examples=examples,
)

iface.launch()
