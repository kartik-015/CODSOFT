from flask import Flask, request, jsonify, render_template_string
import random
import datetime

app = Flask(__name__)

def time_based_greeting():
    hour = datetime.datetime.now().hour
    if hour < 12:
        return "Good morning! I hope your day is off to a wonderful start."
    elif 12 <= hour < 17:
        return "Good afternoon! I hope you're having a fantastic day so far."
    else:
        return "Good evening! I hope your day has been pleasant and relaxing."

responses = {
    "greeting": [
        "Hello! It's great to see you. How can I assist you today?",
        "Hi there! I'm here to help you with anything you need.",
        "Hey! What can I do for you today?",
        "Greetings! How's your day going so far?"
    ],
    "how_are_you": [
        "I'm just a bunch of code, but if I had feelings, I'd say I'm doing fantastic! How about you?",
        "All systems are running smoothly, thank you for asking! How are you feeling today?"
    ],
    "name": [
        "I'm ChatBot, your friendly virtual assistant, always here to chat and help.",
        "You can call me ChatBot. I'm here to make your day easier and more enjoyable."
    ],
    "help": [
        "You can ask me about the current time, today's date, the day of the week, how I'm doing, or just say hello to start a conversation.",
        "Feel free to ask me about the time, date, day, or anything you'd like to chat about. I'm all ears!"
    ],
    "thanks": [
        "You're very welcome! I'm glad I could assist you.",
        "No problem at all! Happy to help anytime.",
        "I'm delighted to be of service!"
    ],
    "bye": [
        "Goodbye! Wishing you a wonderful day ahead.",
        "See you later! Take care and stay safe.",
        "Take care! Looking forward to our next chat."
    ],
    "sad": [
        "I'm really sorry to hear that you're feeling down. Remember, it's okay to have tough days. If you'd like, I'm here to listen.",
        "It sounds like you're going through a hard time. You're not alone, and talking about it might help. I'm here for you."
    ],
    "happy": [
        "That's fantastic to hear! Your happiness brightens my circuits.",
        "I'm so glad you're feeling great! Keep that positive energy flowing."
    ],
    "fallback": [
        "Hmm, I'm not quite sure how to respond to that. Maybe try asking for 'help' to see what I can do.",
        "That's interesting! Could you please rephrase or ask something else? I'm eager to assist."
    ]
}

general_knowledge = {
    "what is your purpose": "I'm here to assist you with general questions, keep you company, and provide useful information.",
    "who created you": "I was created by a skilled developer to help you with your queries and chat with you.",
    "what can you do": "I can tell you the time, date, day, remember your name, and chat about various topics.",
    "how old are you": "I don't have an age like humans, but I was created recently to assist you.",
    "what is the meaning of life": "That's a profound question! Many say it's to find happiness and help others.",
    "who is the PM of India": "Narendra Modi is the PM of India",
    "who is the CEO of Google": "Sundar Pichai is the CEO of Google",
    "i need your help" : "Yeaa...tell naa...I am here to solve all your doubts",
    "what is the capital of India" : "Delhi is the capital of India"
}

user_name = None

def get_response(user_input):
    global user_name
    user_input_lower = user_input.lower()

    if any(phrase in user_input_lower for phrase in ["my name is", "i am called", "call me"]):
        for phrase in ["my name is", "i am called", "call me"]:
            if phrase in user_input_lower:
                name = user_input_lower.split(phrase)[-1].strip().split(" ")[0]
                user_name = name.capitalize()
                return f"Nice to meet you, {user_name}! How can I assist you today?"

    # Ask for user's name if not known
    if user_name is None and any(word in user_input_lower for word in ["hi", "hello", "hey", "greetings"]):
        return "Hello! Before we start, may I know your name?"

    if any(word in user_input_lower for word in ["hi", "hello", "hey", "greetings"]):
        if user_name:
            return f"Hello again, {user_name}! How can I assist you today?"
        else:
            return random.choice(responses["greeting"])

    elif "how are you" in user_input_lower:
        return random.choice(responses["how_are_you"])

    elif "your name" in user_input_lower or "who are you" in user_input_lower:
        return random.choice(responses["name"])

    elif "what is my name" in user_input_lower or "do you know my name" in user_input_lower:
        if user_name:
            return f"Your name is {user_name}, of course!"
        else:
            return "I don't know your name yet. What should I call you?"

    elif "help" in user_input_lower:
        return random.choice(responses["help"])

    elif "thank" in user_input_lower:
        return random.choice(responses["thanks"])

    elif "time" in user_input_lower:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}. Is there anything else you'd like to know?"

    elif "date" in user_input_lower:
        current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        return f"Today's date is {current_date}. How can I assist you further?"

    elif "day" in user_input_lower:
        current_day = datetime.datetime.now().strftime("%A")
        return f"Today is {current_day}. What else can I help you with?"

    elif "sad" in user_input_lower or "depressed" in user_input_lower or "unhappy" in user_input_lower:
        return random.choice(responses["sad"])

    elif "happy" in user_input_lower or "great" in user_input_lower or "good" in user_input_lower:
        return random.choice(responses["happy"])

    elif "bye" in user_input_lower or "exit" in user_input_lower or "quit" in user_input_lower:
        return "exit"

    import string

    def normalize(text):
        return text.lower().translate(str.maketrans('', '', string.punctuation)).strip()

    normalized_input = normalize(user_input)

    for question, answer in general_knowledge.items():
        normalized_question = normalize(question)
        if normalized_question in normalized_input:
            return answer

    else:
        return random.choice(responses["fallback"])

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>AI Chatbot</title>
<style>
  body {
    font-family: Arial, sans-serif;
    background: #f4f7f9;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    height: 100vh;
  }
  #chatbox {
    flex: 1;
    padding: 20px;
    overflow-y: auto;
    background: white;
    border-bottom: 1px solid #ccc;
  }
  .message {
    margin: 10px 0;
    max-width: 70%;
    padding: 10px 15px;
    border-radius: 15px;
    clear: both;
  }
  .user {
    background: #007bff;
    color: white;
    float: right;
    text-align: right;
  }
  .bot {
    background: #e4e6eb;
    color: black;
    float: left;
    text-align: left;
  }
  #input-area {
    display: flex;
    padding: 10px;
    background: #fff;
  }
  #input-area input[type="text"] {
    flex: 1;
    padding: 10px;
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 20px;
    outline: none;
  }
  #input-area button {
    margin-left: 10px;
    padding: 10px 20px;
    font-size: 16px;
    background: #007bff;
    color: white;
    border: none;
    border-radius: 20px;
    cursor: pointer;
  }
  #input-area button:hover {
    background: #0056b3;
  }
  /* Thinking indicator style */
  .thinking {
    font-style: italic;
    color: #888;
    margin-left: 10px;
  }
  /* Typing dots animation */
  .typing-dots span {
    display: inline-block;
    width: 6px;
    height: 6px;
    margin: 0 2px;
    background-color: #888;
    border-radius: 50%;
    animation: blink 1.4s infinite both;
  }
  .typing-dots span:nth-child(1) {
    animation-delay: 0s;
  }
  .typing-dots span:nth-child(2) {
    animation-delay: 0.2s;
  }
  .typing-dots span:nth-child(3) {
    animation-delay: 0.4s;
  }
  @keyframes blink {
    0%, 80%, 100% {
      opacity: 0;
    }
    40% {
      opacity: 1;
    }
  }
</style>
</head>
<body>
<div id="chatbox"></div>
<div id="input-area">
  <input type="text" id="user-input" placeholder="Type your message here..." autocomplete="off" />
  <button onclick="sendMessage()">Send</button>
</div>
<script>
  const chatbox = document.getElementById('chatbox');
  const userInput = document.getElementById('user-input');

  function appendMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender);
    messageDiv.textContent = text;
    chatbox.appendChild(messageDiv);
    chatbox.scrollTop = chatbox.scrollHeight;
  }

  function appendThinkingIndicator() {
    const thinkingDiv = document.createElement('div');
    thinkingDiv.classList.add('message', 'bot', 'thinking');
    thinkingDiv.id = 'thinking-indicator';
    thinkingDiv.innerHTML = 'Bot is thinking<span class="typing-dots"><span></span><span></span><span></span></span>';
    chatbox.appendChild(thinkingDiv);
    chatbox.scrollTop = chatbox.scrollHeight;
  }

  function removeThinkingIndicator() {
    const thinkingDiv = document.getElementById('thinking-indicator');
    if (thinkingDiv) {
      chatbox.removeChild(thinkingDiv);
    }
  }

  function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;
    appendMessage(text, 'user');
    userInput.value = '';
    appendThinkingIndicator();
    fetch('/chat', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({message: text})
    })
    .then(response => response.json())
    .then(data => {
      removeThinkingIndicator();
      // Delay the bot response to simulate thinking
      setTimeout(() => {
        appendMessage(data.response, 'bot');
      }, 1500);
    })
    .catch(() => {
      removeThinkingIndicator();
      appendMessage("Sorry, there was an error processing your message.", 'bot');
    });
  }

  userInput.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
      sendMessage();
    }
  });

  // Initial greeting from bot
  window.onload = function() {
    fetch('/chat', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({message: '__init__'})
    })
    .then(response => response.json())
    .then(data => {
      appendMessage(data.response, 'bot');
    });
  };
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    if user_message == '__init__':
        response_text = f"{time_based_greeting()} I'm ChatBot, your virtual assistant. Feel free to chat with me!"
    else:
        response_text = get_response(user_message)
        if response_text == "exit":
            response_text = "Goodbye! Have a wonderful day. Looking forward to chatting with you again soon."
    return jsonify({'response': response_text})

if __name__ == '__main__':
    app.run(debug=True)
