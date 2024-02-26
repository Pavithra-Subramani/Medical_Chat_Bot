import tkinter as tk
from PIL import Image, ImageTk
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Dictionary with medical-related responses
medical_responses = {
    "headache": ["You might be experiencing a tension headache. Have you been stressed lately?", 
                 "Drink plenty of water and try to relax. If it persists, consult a doctor."],
    "fever": ["Rest is essential. Monitor your temperature and take a fever reducer like acetaminophen.",
              "Stay hydrated and get adequate rest. Seek medical attention if the fever is high or persists."],
    "cough": ["A cough might be due to a cold or allergies. Try honey in warm water or lozenges for relief.",
              "If the cough persists for more than a week or is accompanied by other symptoms, consult a doctor."],
    "sore throat": ["Gargle with warm salt water and drink soothing liquids like tea with honey.",
                    "If the sore throat persists for more than a few days, consider seeing a doctor."],
    "stomach ache": ["Avoid heavy or spicy foods. Stick to bland, easy-to-digest foods.",
                     "If the stomach ache continues or worsens, consult a healthcare professional."],
    "fatigue": ["Make sure you're getting enough sleep and maintaining a balanced diet.",
                "If fatigue persists despite adequate rest, consider consulting a healthcare provider."],
    "rash": ["Apply a mild, unscented moisturizer and avoid scratching to prevent infection.",
             "If the rash spreads or is accompanied by other symptoms, seek medical advice."],
    "dizziness": ["Sit or lie down and take deep breaths. Avoid sudden movements.",
                  "If dizziness is recurrent or severe, consult a doctor to rule out underlying causes."],
    "back pain": ["Apply a cold pack or heating pad and try gentle stretches. Avoid heavy lifting.",
                  "If back pain persists or worsens, consult a healthcare professional for further evaluation."],
    "default": ["I'm not sure I understand. Please consult a medical professional for better assistance.",
                "I'm not trained to diagnose. It's best to see a doctor for a proper evaluation."]
}
symptoms = [
    "headache",
    "fever",
    "cough",
    "sore throat",
    "stomach ache",
    "fatigue",
    "rash",
    "dizziness",
    "back pain"
]

# Convert symptoms to vectors
vectorizer = CountVectorizer()
symptom_vectors = vectorizer.fit_transform(symptoms).toarray()

def get_bot_response(user_input):
    

    symptoms = []
    for key in medical_responses:
        if key in user_input:
            symptoms.append(key)
            return random.choice(medical_responses[key])

    if symptoms:
        diseases = identify_disease(symptoms)  # Assuming you have a function to identify diseases
        if diseases:
            return f"Based on your symptoms, possible diseases include: {', '.join(diseases)}"

    return random.choice(medical_responses["default"])




def get_bot_response(user_input):
    user_input = user_input.lower()
   
    
    symptoms = []
    for key in medical_responses:
        if key in user_input:
            symptoms.append(key)
            return random.choice(medical_responses[key])
    
    if symptoms:
        diseases = identify_disease(symptoms)
        if diseases:
            return f"Based on your symptoms, possible diseases include: {', '.join(diseases)}"
    
    return random.choice(medical_responses["default"])




# Function to handle  user sending messages and getting responses
def send():
    user_input = entry_field.get()
    display_user_message(user_input)
    response = get_bot_response(user_input)
    display_bot_message(response)
    entry_field.delete(0, tk.END)
    messages_frame.yview(tk.END)

# Display user's message with user icon
def display_user_message(message):
    user_icon = Image.open("user.jpeg")  # Replace "user.jpeg" with your user icon file
    user_icon = user_icon.resize((30, 30))  # Adjust the size of the icon as needed
    user_icon = ImageTk.PhotoImage(user_icon)
    
    label = tk.Label(messages_frame, image=user_icon, text="You: " + message, compound=tk.LEFT, bg="#10bee0",font=("Arial", 12))
    label.image = user_icon
    label.pack(anchor="e", padx=10, pady=5, fill=tk.X)

# Display bot's message with bot icon
def display_bot_message(message):
    bot_icon = Image.open("bot.jpeg")  # Replace "bot.jpeg" with your bot icon file
    bot_icon = bot_icon.resize((30, 30))  # Adjust the size of the icon as needed
    bot_icon = ImageTk.PhotoImage(bot_icon)
    
    label = tk.Label(messages_frame, image=bot_icon, text="Bot: " + message, compound=tk.LEFT, bg="#9fdbf5",font=("Arial", 12))
    label.image = bot_icon
    label.pack(anchor="w", padx=10, pady=5, fill=tk.X)
chat_counter = 0

# Function to handle sending messages and getting responses
def send():
    global chat_counter
    if chat_counter < 5:  # Limiting chat to 5 exchanges
        user_input = entry_field.get()
        display_user_message(user_input)
        response = get_bot_response(user_input)
        display_bot_message(response)
        entry_field.delete(0, tk.END)
        messages_frame.yview(tk.END)
        chat_counter += 1
    else:
        display_bot_message("This chat session has ended. If you have more questions, please start a new session.")
        entry_field.config(state='disabled') 

# Create a GUI window
root = tk.Tk()
root.title("Medical Chatbot")
root.geometry()
window_width = 800  # Adjust the width as needed
window_height = 600  # Adjust the height as needed
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width // 2) - (window_width // 2)
y_position = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Set background image
background_image = Image.open("backgroundd.png")  # Replace "backgroundd.png" with your image file
resized_bg_image = background_image.resize((window_width, window_height))
background_image = ImageTk.PhotoImage(resized_bg_image)
background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)


# Greet the user
greeting_label = tk.Label(root, text="Hi! I'm your Medical Chatbot. How can I assist you today?", font=("Arial", 16))
greeting_label.pack(padx=15, pady=15)

# Chat display area with scrollbar
messages_frame = tk.Frame(root)
messages_frame.pack(padx=10, pady=(0, 10), fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(messages_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

messages_canvas = tk.Canvas(messages_frame)
messages_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

messages_frame = tk.Frame(messages_canvas)
messages_canvas.create_window((0, 0), window=messages_frame, anchor="nw")

scrollbar.config(command=messages_canvas.yview)

# User input field and send button
entry_field = tk.Entry(root, font=("Arial", 12))  # Increase font size of the entry field
entry_field.pack(padx=10, pady=10, side=tk.LEFT, expand=True, fill=tk.X, ipady=10)  # Increase ipady for a taller text box

send_button = tk.Button(root, text="Send", command=send, font=("Arial", 12), width=10, height=2)  # Increase width and height of the button
send_button.pack(padx=10, pady=10, side=tk.RIGHT)
root.mainloop()


