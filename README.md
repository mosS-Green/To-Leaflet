# Telegram Uploader (React)

A pure React single-page application that allows you to upload and download files to/from a Telegram chat using a Bot Token directly from the browser. 

The Bot Token and Chat ID are saved securely in your browser's local storage.

## Hosting

This application is built with Vite and features an automated GitHub Actions deployment to GitHub Pages on every commit.

### How to use GitHub Pages Deployment
1. Go to your GitHub repository **Settings**.
2. Navigate to the **Pages** section on the left sidebar.
3. Under **Build and deployment > Source**, select **Deploy from a branch**.
4. Set the branch to **gh-pages** and save.
5. The Github Actions workflow (`.github/workflows/deploy.yml`) will automatically build and publish to the `gh-pages` branch every time you push to `main` or `master`.
