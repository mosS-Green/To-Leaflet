# Telegram Uploader (React)

A modern, pure React single-page application that allows you to seamlessly upload and download files to/from a Telegram chat using a Bot Token directly from your browser.

## Features

- **Multiple File Upload**: Select multiple files via the file dialog, drag-and-drop them onto the drop zone, or paste multiple images/files directly from your clipboard.
- **Sequential Sending**: Files are queued and uploaded one-by-one sequentially, displaying clear real-time progress indicators.
- **Image Previews**: Received images are loaded lazily from Telegram's API as inline thumbnails in the recent files list.
- **Copy Image to Clipboard**: Copy received images directly to your system's clipboard with a single click.
- **File Size Restrictions (Max 25 MB)**: Automatic validation restricts uploads to a maximum of 25 MB per file, providing instant feedback via animated toast notifications.
- **Secure Storage**: Your Bot Token and Chat ID are saved securely in your browser's local storage.
- **Dismiss/Hide Files**: Manually hide any items from the "Recent Files" list in the UI, with automatic garbage collection on refresh to keep local storage clean.

## Hosting

This application is built with Vite and features an automated GitHub Actions deployment to GitHub Pages on every commit.

### How to use GitHub Pages Deployment
1. Go to your GitHub repository **Settings**.
2. Navigate to the **Pages** section on the left sidebar.
3. Under **Build and deployment > Source**, select **Deploy from a branch**.
4. Set the branch to **gh-pages** and save.
5. The GitHub Actions workflow (`.github/workflows/deploy.yml`) will automatically build and publish to the `gh-pages` branch every time you push to `main` or `master`.

