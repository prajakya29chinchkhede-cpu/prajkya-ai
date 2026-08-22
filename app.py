from flask import Flask, request

app = Flask(__name__)

def ai_reply(message, name):
    text = message.lower().strip()

    if "hello" in text or "hey" in text or "hi" in text:
        return "Hello, " + name + "!"

    elif "how are you" in text:
        return "I am doing great! Thanks for asking."

    elif "what is your name" in text or "who are you" in text:
        return "My name is MyAI!"

    elif "what can you do" in text:
        return "I can chat with you and answer simple questions."

    elif "who made you" in text or "who created you" in text:
        return "You are building me!"

    elif "good morning" in text:
        return "Good morning, " + name + "!"

    elif "good night" in text:
        return "Good night, " + name + "!"

    elif "thank" in text:
        return "You're welcome!"

    elif "sorry" in text:
        return "That's okay!"

    elif text in ["yes", "yeah", "yep"]:
        return "Great! 😄"

    elif text in ["no", "nope"]:
        return "Okay!"

    elif "what is python" in text:
        return "Python is a programming language used to build software."

    elif "what is ai" in text:
        return "AI means Artificial Intelligence."

    elif "help" in text:
        return "Sure! Tell me what you need help with."

    elif "how old are you" in text:
        return "I don't have a human age. I am software!"

    elif "where are you" in text:
        return "I am running as a web application!"

    elif "bye" in text or "goodbye" in text:
        return "Goodbye, " + name + "!"

    else:
        return "I don't understand that yet, but I'm learning!"


@app.route("/", methods=["GET", "POST"])
def home():
    answer = ""
    name = request.form.get("name", "Friend")

    if request.method == "POST":
        message = request.form.get("message", "")
        answer = ai_reply(message, name)

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>MyAI</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{
                font-family: Arial;
                max-width: 600px;
                margin: 40px auto;
                padding: 20px;
            }}
            input, button {{
                padding: 12px;
                margin: 5px 0;
                width: 100%;
                box-sizing: border-box;
            }}
            button {{
                cursor: pointer;
            }}
        </style>
    </head>

    <body>
        <h1>🤖 MyAI</h1>

        <form method="post">
            <input name="name" placeholder="Your name" value="{name}">
            <input name="message" placeholder="Talk to MyAI">
            <button type="submit">Send</button>
        </form>

        <h3>AI: {answer}</h3>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
