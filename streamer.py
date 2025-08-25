#!/usr/bin/env python3
import os
from urllib.parse import unquote
from mimetypes import guess_type
import logging

from aiohttp import web
from pyrogram import Client
from pyrogram.file_id import FileId

# --- Configuration ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("PYROGRAM_BOT_TOKEN")
STREAM_PORT = int(os.environ.get("STREAM_PORT", 8081))

# Initialize Pyrogram Client
app = Client("streamer_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- Web Server Logic ---
async def stream_file(request: web.Request):
    """
    Streams a file from Telegram using file_id.
    URL format: /stream?file_id=...&name=...&size=...&mime=...
    """
    params = request.query
    try:
        file_id = unquote(params.get("file_id", ""))
        media_name = unquote(params.get("name", "file"))
        media_size = int(params.get("size", 0))
        media_mime = unquote(params.get("mime", guess_type(media_name)[0] or "application/octet-stream"))
        
        if not all([file_id, media_name, media_size]):
            raise ValueError("Missing one or more required query parameters: file_id, name, size")

    except (ValueError, TypeError) as e:
        log.error(f"Bad Request from {request.remote}: {e}")
        return web.Response(status=400, text=f"Bad Request: {e}")

    log.info(f"Streaming request for: {media_name} ({file_id})")

    try:
        # Prepare response headers
        response_headers = {
            "Content-Type": media_mime,
            "Content-Disposition": f'attachment; filename="{media_name}"',
            "Content-Length": str(media_size),
            "Accept-Ranges": "bytes",
        }
        
        # Handle range requests for seeking/resuming
        offset = 0
        length = media_size
        if "Range" in request.headers:
            ran = request.headers.get("Range")
            start_str, _, end_str = ran.replace("bytes=", "").partition("-")
            offset = int(start_str) if start_str else 0
            end = int(end_str) if end_str else media_size - 1
            length = end - offset + 1
            
            response_headers["Content-Range"] = f"bytes {offset}-{end}/{media_size}"
        
        # Create StreamResponse
        status_code = 206 if "Range" in request.headers else 200
        stream_response = web.StreamResponse(status=status_code, headers=response_headers)
        await stream_response.prepare(request)

        # Stream the file chunk by chunk
        async for chunk in app.stream_media(file_id, offset=offset, limit=length):
            if chunk:
                await stream_response.write(chunk)
        
        await stream_response.write_eof()
        return stream_response

    except Exception as e:
        log.exception(f"Error streaming file {file_id}: {e}")
        return web.Response(status=500, text=f"Internal Server Error: {e}")

async def health_check(request):
    return web.Response(text="Streamer is alive!")

async def start_server():
    """Initializes the Pyrogram client and starts the web server."""
    log.info("Starting Pyrogram client...")
    await app.start()
    log.info("Client started. Starting web server...")
    
    web_app = web.Application()
    web_app.router.add_get("/stream", stream_file)
    web_app.router.add_get("/health", health_check)

    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', STREAM_PORT)
    await site.start()
    log.info(f"Streamer service running on http://0.0.0.0:{STREAM_PORT}")

async def stop_server():
    """Stops the Pyrogram client."""
    log.info("Stopping Pyrogram client...")
    await app.stop()

if __name__ == "__main__":
    loop = app.loop
    try:
        loop.run_until_complete(start_server())
        loop.run_forever()
    except KeyboardInterrupt:
        log.info("Shutdown signal received.")
    finally:
        loop.run_until_complete(stop_server())
        log.info("Services shut down gracefully.")
