import openai
import os

# Inicializa la clave de la API de OpenAI
openai.api_key = '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'


class ChatBot:
    def __init__(self, chat_model="gpt-3.5-turbo"):
        self.chat_model = chat_model
        self.reset_conversation()

    def reset_conversation(self):
        self.messages = [{"role": "system", "content": "start"}]

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})

    def get_response(self, message):
        self.add_message("user", message)
        try:
            response = openai.ChatCompletion.create(
                model=self.chat_model,
                messages=self.messages
            )
            self.messages.append({
                "role": "assistant",
                "content": response['choices'][0]['message']['content']
            })
            return response['choices'][0]['message']['content']
        except Exception as e:
            print(f"Hubo un error al obtener la respuesta: {e}")
            return None


# Crear una instancia del chatbot
bot = ChatBot()

# Conversar con el bot
while True:
    message = input("Tú: ")

    if message.lower() == "reiniciar":
        bot.reset_conversation()
        print("La conversación se ha reiniciado.")
    else:
        response = bot.get_response(message)
        if response:
            print(f"Jarvis: {response}")
