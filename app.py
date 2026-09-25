from flask import Flask, request
from html import escape
from pathlib import Path
from uuid import uuid4
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = Path(app.root_path) / "uploads"
UPLOAD_FOLDER.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024


def allowed_photo(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def ai_reply(message, name):
    text = message.lower().strip()

    if "hello" in text or "hey" in text or "hi" in text:
        return "Hello, " + name + "!"
    elif "how are you" in text:
        return "I am doing great! Thanks for asking."
    elif "what is your name" in text or "who are you" in text:
        return "My name is Orbit AI!"
    elif "what can you do" in text:
        return "I can chat with you and receive images."
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
    name = request.form.get("name", "Friend").strip() or "Friend"

    if request.method == "POST":
        message = request.form.get("message", "")
        photo = request.files.get("photo")

        if photo and photo.filename:
            if allowed_photo(photo.filename):
                filename = secure_filename(photo.filename)
                saved_filename = f"{uuid4().hex}_{filename}"
                saved_path = UPLOAD_FOLDER / saved_filename
                photo.save(saved_path)
                photo_status = f"Image received: {filename}"
            else:
                photo_status = "Please choose a PNG, JPG, JPEG, GIF, or WEBP image."

        answer = ai_reply(message, name)

    safe_name = escape(name)
    safe_answer = escape(answer)
    safe_photo_status = escape(photo_status)

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Orbit AI — Your curious companion</title>
    <style>
        :root {{
            --ink: #eaf0ff;
            --muted: #a9b4d0;
            --card: rgba(18, 25, 58, 0.78);
            --line: rgba(153, 172, 255, 0.18);
            --violet: #8b5cf6;
            --cyan: #22d3ee;
        }}

        * {{ box-sizing: border-box; }}

        body {{
            min-height: 100vh;
            margin: 0;
            color: var(--ink);
            font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            background:
                radial-gradient(circle at 15% 12%, rgba(34, 211, 238, 0.18), transparent 25rem),
                radial-gradient(circle at 85% 90%, rgba(139, 92, 246, 0.22), transparent 28rem),
                #070b1c;
        }}

        .shell {{
            width: min(720px, calc(100% - 32px));
            margin: 0 auto;
            padding: 56px 0;
        }}

        .brand {{
            display: flex;
            align-items: center;
            gap: 14px;
            margin-bottom: 24px;
        }}

        .orbit-mark {{
            position: relative;
            width: 52px;
            height: 52px;
            border: 2px solid var(--cyan);
            border-radius: 50%;
            box-shadow: 0 0 28px rgba(34, 211, 238, 0.45);
        }}

        .orbit-mark::after {{
            content: "";
            position: absolute;
            width: 64px;
            height: 20px;
            top: 14px;
            left: -8px;
            border: 2px solid var(--violet);
            border-radius: 50%;
            transform: rotate(-22deg);
        }}

        h1 {{ margin: 0; font-size: clamp(2rem, 7vw, 3rem); letter-spacing: -0.06em; }}
        .tagline {{ margin: 4px 0 0; color: var(--muted); }}

        .card {{
            padding: clamp(22px, 5vw, 36px);
            background: var(--card);
            border: 1px solid var(--line);
            border-radius: 24px;
            box-shadow: 0 24px 65px rgba(0, 0, 0, 0.32);
            backdrop-filter: blur(16px);
        }}

        .intro {{ margin: 0 0 26px; color: var(--muted); line-height: 1.55; }}
        .field {{ margin-bottom: 16px; }}
        label {{ display: block; margin-bottom: 8px; font-size: 0.92rem; font-weight: 650; }}

        input {{
            width: 100%;
            border: 1px solid var(--line);
            border-radius: 13px;
            padding: 14px 15px;
            color: var(--ink);
            background: rgba(7, 11, 28, 0.62);
            font: inherit;
            outline: none;
        }}

        input:focus {{ border-color: var(--cyan); box-shadow: 0 0 0 3px rgba(34, 211, 238, 0.12); }}
        input::file-selector-button {{
            margin-right: 12px;
            border: 0;
            border-radius: 8px;
            padding: 8px 10px;
            color: #06111a;
            background: var(--cyan);
            font: inherit;
            font-weight: 700;
            cursor: pointer;
        }}

        .upload-help {{ margin: 8px 0 0; color: var(--muted); font-size: 0.84rem; }}

        button {{
            width: 100%;
            margin-top: 8px;
            border: 0;
            border-radius: 13px;
            padding: 15px;
            color: #fff;
            background: linear-gradient(100deg, var(--violet), #4f46e5 55%, var(--cyan));
            box-shadow: 0 12px 26px rgba(79, 70, 229, 0.28);
            cursor: pointer;
            font: inherit;
            font-weight: 750;
            font-size: 1rem;
        }}

        button:hover {{ filter: brightness(1.1); transform: translateY(-1px); }}

        .answer {{
            min-height: 72px;
            margin-top: 24px;
            padding: 17px 18px;
            border: 1px solid rgba(34, 211, 238, 0.23);
            border-radius: 16px;
            background: rgba(34, 211, 238, 0.06);
        }}

        .answer-label {{ display: block; margin-bottom: 6px; color: var(--cyan); font-size: 0.78rem; font-weight: 800; letter-spacing: 0.1em; text-transform: uppercase; }}
        .answer p {{ margin: 0; line-height: 1.55; }}
        .empty {{ color: var(--muted); }}
        .photo-status {{ margin: 14px 0 0; color: #86efac; font-size: 0.92rem; }}

        footer {{ margin-top: 20px; color: var(--muted); font-size: 0.82rem; text-align: center; }}
    </style>
</head>
<body>
    <main class="shell">
        <header class="brand">
            <div class="orbit-mark" aria-hidden="true"></div>
            <div>
                <h1>Orbit AI</h1>
                <p class="tagline">Your curious companion</p>
            </div>
        </header>

        <section class="card">
            <p class="intro">Ask a question, share a thought, or add an image for Orbit to receive. Image understanding is coming next.</p>

            <form method="post" enctype="multipart/form-data">
                <div class="field">
                    <label for="name">Your name</label>
                    <input id="name" name="name" placeholder="How should Orbit call you?" value="{safe_name}">
                </div>

                <div class="field">
                    <label for="message">Message</label>
                    <input id="message" name="message" placeholder="Ask Orbit anything..." autocomplete="off">
                </div>

                <div class="field">
                    <label for="photo">Add an image</label>
                    <input id="photo" name="photo" type="file" accept=".png,.jpg,.jpeg,.gif,.webp">
                    <p class="upload-help">PNG, JPG, GIF, or WEBP · up to 5 MB</p>
                </div>

                <button type="submit">Send to Orbit ✦</button>
            </form>

            <div class="answer" aria-live="polite">
                <span class="answer-label">Orbit says</span>
                <p class="{'empty' if not safe_answer else ''}">{safe_answer or 'I’m ready when you are.'}</p>
            </div>

            <p class="photo-status">{safe_photo_status}</p>
        </section>

        <footer>Orbit AI · Explore, ask, discover.</footer>
    </main>
</body>
</html>
"""


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
