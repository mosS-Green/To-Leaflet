#!/usr/bin/env python

import json
import os

import requests
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Cache environment values globally so we don’t repeatedly query os.getenv
ENV_BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
ENV_CHAT_ID = os.getenv("CHAT_ID", "").strip()
ENV_PORT = os.getenv("PORT")

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
    .hint{font-size:13px;color:#555;margin-top:6px}
    .env-warning{font-size:13px;color:#0a66ff;margin-top:6px}
    .disabled{opacity:0.6}
  </style>
</head>
<body>
  <h1>Telegram File Uploader</h1>
  <form id="uploadForm" action="{{ url_for('upload') }}" method="post" enctype="multipart/form-data">
    <label>Bot token</label>
    <input id="token" name="token" type="text" placeholder="123456789:AAH..." value="{{ url_token|default('') }}">
    <div id="envTokenMsg" class="env-warning" style="display:none">Default server value will be used for Bot Token.</div>

    <label>Chat ID</label>
    <input id="chatid" name="chatid" type="text" placeholder="-1001234567890" value="{{ url_chatid|default('') }}">
    <div id="envChatMsg" class="env-warning" style="display:none">Default server value will be used for Chat ID.</div>

    <label>Caption (optional)</label>
    <textarea name="caption" rows="2" placeholder="Write a caption...">{{ caption|default('') }}</textarea>

    <label>File</label>
    <input name="file" type="file" required>

    <button id="uploadBtn" type="submit" disabled>Upload</button>
    <button id="copyUrl" type="button" style="display:none">Copy Link</button>
  </form>

  <script>
    const envToken = {{ env_token|tojson }};
    const envChat = {{ env_chatid|tojson }};

    const tokenInput = document.getElementById("token");
    const chatInput = document.getElementById("chatid");
    const copyBtn = document.getElementById("copyUrl");
    const uploadBtn = document.getElementById("uploadBtn");
    const envTokenMsg = document.getElementById("envTokenMsg");
    const envChatMsg = document.getElementById("envChatMsg");

    function hasTokenValue() {
      return tokenInput.value && tokenInput.value.trim().length > 0;
    }
    function hasChatValue() {
      return chatInput.value && chatInput.value.trim().length > 0;
    }

    function updateEnvMessages() {
      envTokenMsg.style.display = (!hasTokenValue() && envToken) ? 'block' : 'none';
      envChatMsg.style.display = (!hasChatValue() && envChat) ? 'block' : 'none';
    }

    function updateCopyButton() {
      if (hasTokenValue() && hasChatValue()) {
        copyBtn.style.display = 'inline-block';
      } else {
        copyBtn.style.display = 'none';
      }
    }

    function updateUploadButton() {
      const okToken = hasTokenValue() || envToken;
      const okChat = hasChatValue() || envChat;
      if (okToken && okChat) {
        uploadBtn.disabled = false;
        uploadBtn.classList.remove('disabled');
      } else {
        uploadBtn.disabled = true;
        uploadBtn.classList.add('disabled');
      }
    }

    tokenInput.addEventListener('input', () => { updateEnvMessages(); updateCopyButton(); updateUploadButton(); });
    chatInput.addEventListener('input', () => { updateEnvMessages(); updateCopyButton(); updateUploadButton(); });

    copyBtn.addEventListener('click', () => {
      const url = window.location.origin + "/?token=" + encodeURIComponent(tokenInput.value) +
                  "&chatid=" + encodeURIComponent(chatInput.value);
      navigator.clipboard.writeText(url).then(() => {
        copyBtn.textContent = "Copied!";
        setTimeout(() => copyBtn.textContent = "Copy Link", 2000);
      });
    });

    updateEnvMessages();
    updateCopyButton();
    updateUploadButton();

    document.getElementById('uploadForm').addEventListener('submit', function (e) {
      const okToken = hasTokenValue() || envToken;
      const okChat = hasChatValue() || envChat;
      if (!(okToken && okChat)) {
        e.preventDefault();
        alert('Missing Bot Token or Chat ID. Provide them or set server defaults.');
      }
    });
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
    .info{margin-top:12px;font-size:14px;color:#0a66ff}
  </style>
</head>
<body>
  <h1>Telegram API Response</h1>
  <div class="result">
    <pre>{{ result }}</pre>
  </div>
  {% if used_env %}
    <div class="info">ℹ️ Some values were taken from server defaults.</div>
  {% endif %}
  <a href="{{ url_for('index', caption=caption) }}">⬅ Back to upload</a>
</body>
</html>
"""


@app.route("/", methods=["GET"])
def index():
    env_token_present = bool(ENV_BOT_TOKEN)
    env_chatid_present = bool(ENV_CHAT_ID)

    url_token = request.args.get("token", "")
    url_chatid = request.args.get("chatid", "")
    caption = request.args.get("caption", "")

    return render_template_string(
        FORM_HTML,
        env_token=env_token_present,
        env_chatid=env_chatid_present,
        url_token=url_token,
        url_chatid=url_chatid,
        caption=caption,
    )


@app.route("/upload", methods=["POST"])
def upload():
    token = request.form.get("token", "").strip()
    chat_id = request.form.get("chatid", "").strip()
    caption = request.form.get("caption", "").strip()
    file = request.files.get("file")

    used_env = False

    if not token and ENV_BOT_TOKEN:
        token = ENV_BOT_TOKEN
        used_env = True
    if not chat_id and ENV_CHAT_ID:
        chat_id = ENV_CHAT_ID
        used_env = True

    if not token or not chat_id:
        result = "❌ Missing Bot token or Chat ID. Provide them in the form, URL params, or set server environment variables."
        return render_template_string(RESULT_HTML, result=result, caption=caption, used_env=False)

    if not file:
        result = "❌ No file uploaded."
        return render_template_string(
            RESULT_HTML, result=result, caption=caption, used_env=used_env
        )

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
                f"File Name: {msg['document'].get('file_name', file.filename)}\n"
                f"File Size: {msg['document'].get('file_size', 'unknown')} bytes"
            )
            if caption:
                result += f"\nCaption: {caption}"
        else:
            result = f"❌ Error: {data.get('description', 'Unknown error')}"
    except json.JSONDecodeError:
        result = f"❌ Failed to parse response:\n{resp.text}"

    return render_template_string(RESULT_HTML, result=result, caption=caption, used_env=used_env)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=ENV_PORT)
