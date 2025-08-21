#!/usr/bin/env python

import json
import os

import requests
from flask import Flask, render_template_string, request

app = Flask(__name__)

FORM_HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Telegram File Uploader</title>
  <style>
    body{font-family:system-ui,-apple-system,Segoe UI,Roboto,'Helvetica Neue',Arial;
         max-width:700px;margin:40px auto;padding:18px}
    h1{font-size:20px;margin-bottom:10px}
    label{display:block;margin-top:12px;font-weight:600}
    input[type=text], input[type=file], textarea{
         width:100%;padding:8px;margin-top:6px;border:1px solid #ddd;border-radius:6px}
    button{margin-top:16px;padding:10px 14px;border-radius:8px;border:0;
           background:#2469f2;color:white;font-weight:600;cursor:pointer}
    button:active{transform:translateY(1px)}
    #copyUrl{background:#28a745}
  </style>
</head>
<body>
  <h1>Telegram File Uploader</h1>
  <form action="{{ url_for('upload') }}" method="post" enctype="multipart/form-data">
    <label>Bot token</label>
    <input id="token" name="token" type="text" placeholder="123456789:AAH..." value="{{ token|default('') }}" required>

    <label>Chat ID</label>
    <input id="chatid" name="chatid" type="text" placeholder="-1001234567890" value="{{ chatid|default('') }}" required>

    <label>Caption (optional)</label>
    <textarea name="caption" rows="2" placeholder="Write a caption...">{{ caption|default('') }}</textarea>

    <label>File</label>
    <input name="file" type="file" required>

    <button type="submit">Upload</button>
    <button id="copyUrl" type="button" style="display:none">Copy Link</button>
  </form>

  <script>
    const tokenInput = document.getElementById("token");
    const chatInput = document.getElementById("chatid");
    const copyBtn = document.getElementById("copyUrl");
    let linkShown = false;

    function updateCopyButton() {
      if (tokenInput.value && chatInput.value) {
        copyBtn.style.display = "inline-block";
        linkShown = true;
      } else {
        copyBtn.style.display = "none";
        linkShown = false;
      }
    }

    tokenInput.addEventListener("input", updateCopyButton);
    chatInput.addEventListener("input", updateCopyButton);

    copyBtn.addEventListener("click", () => {
      const url = window.location.origin + "/?token=" + encodeURIComponent(tokenInput.value) +
                  "&chatid=" + encodeURIComponent(chatInput.value);
      navigator.clipboard.writeText(url).then(() => {
        copyBtn.textContent = "Copied!";
        setTimeout(() => copyBtn.textContent = "Copy Link", 2000);
      });
    });

    updateCopyButton();
  </script>
</body>
</html>
"""

RESULT_HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Telegram Upload Result</title>
  <style>
    body{font-family:system-ui,-apple-system,Segoe UI,Roboto,'Helvetica Neue',Arial;
         max-width:700px;margin:40px auto;padding:18px}
    h1{font-size:20px;margin-bottom:10px}
    .result{margin-top:20px;padding:10px;border-radius:6px;background:#f6f6f6}
    pre{white-space:pre-wrap;word-break:break-word}
    a{display:inline-block;margin-top:14px;color:#2469f2;text-decoration:none;font-weight:600}
  </style>
</head>
<body>
  <h1>Telegram API Response</h1>
  <div class="result">
    <pre>{{ result }}</pre>
  </div>
  <a href="{{ url_for('index', token=token, chatid=chatid, caption=caption) }}">⬅ Back to upload</a>
</body>
</html>
"""


@app.route("/", methods=["GET"])
def index():
    token = request.args.get("token") or os.getenv("BOT_TOKEN", "")
    chatid = request.args.get("chatid") or os.getenv("CHAT_ID", "")
    caption = request.args.get("caption", "")
    return render_template_string(FORM_HTML, token=token, chatid=chatid, caption=caption)


@app.route("/upload", methods=["POST"])
def upload():
    token = request.form["token"].strip()
    chat_id = request.form["chatid"].strip()
    caption = request.form.get("caption", "").strip()
    file = request.files["file"]

    url = f"https://api.telegram.org/bot{token}/sendDocument"
    resp = requests.post(
        url,
        data={"chat_id": chat_id, "caption": caption},
        files={"document": (file.filename, file.stream, file.mimetype)},
    )

    try:
        data = resp.json()
        if data.get("ok"):
            msg = data["result"]
            result = (
                f"✅ Upload successful!\n\n"
                f"Message ID: {msg['message_id']}\n"
                f"Chat ID: {msg['chat']['id']}\n"
                f"File ID: {msg['document']['file_id']}\n"
                f"File Name: {msg['document']['file_name']}\n"
                f"File Size: {msg['document']['file_size']} bytes"
            )
            if caption:
                result += f"\nCaption: {caption}"
        else:
            result = f"❌ Error: {data.get('description', 'Unknown error')}"
    except json.JSONDecodeError:
        result = f"❌ Failed to parse response:\n{resp.text}"

    return render_template_string(
        RESULT_HTML, result=result, token=token, chatid=chat_id, caption=caption
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv("PORT"))
