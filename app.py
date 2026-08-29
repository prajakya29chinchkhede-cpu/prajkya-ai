from flask import Flask, request
from pathlib import Path
from uuid import uuid4

from werkzeug.utils import secure_filename


app = Flask(__name__)

UPLOAD_FOLDER = Path(app.root_path) / "uploads"
UPLOAD_FOLDER.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024


def allowed_photo(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


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
    photo_status = ""
    name = request.form.get("name", "Friend")


    if request.method == "POST":
        message = request.form.get("message", "")
        photo = request.files.get("photo")

        if photo and photo.filename:
            if allowed_photo(photo.filename):
                filename = secure_filename(photo.filename)
                saved_filename = f"{uuid4().hex}_{filename}"
                saved_path = UPLOAD_FOLDER / saved_filename
                photo.save(saved_path)
                photo_status = f"Photo received: {filename} ({saved_path.stat().st_size} bytes)."
            else:
                photo_status = "Please upload a PNG, JPG, JPEG, GIF, or WEBP image."

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
            .photo-status {{
                color: #176b3a;
            }}
        </style>
    </head>
    <body>
        <h1>🤖 MyAI</h1>
        <form method="post" enctype="multipart/form-data">
            <input name="name" placeholder="Your name" value="{name}">
            <input name="message" placeholder="Talk to MyAI">
            <input name="photo" type="file" accept=".png,.jpg,.jpeg,.gif,.webp">
            <button type="submit">Send</button>
        </form>
        <h3>AI: {answer}</h3>
        <p class="photo-status">{photo_status}</p>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
