export default {
  async fetch(request) {
    const url = new URL(request.url);
    
    // Only proxy paths starting with /bot or /file/bot (for downloads)
    if (url.pathname.startsWith('/bot') || url.pathname.startsWith('/file/bot')) {
      const telegramUrl = new URL('https://api.telegram.org' + url.pathname + url.search);
      
      // Create a new request to forward to Telegram
      const newRequest = new Request(telegramUrl, request);
      
      // Fetch and return the response from the Telegram API
      return fetch(newRequest);
    }

    // Default response for all other paths
    return new Response("Telegram API Proxy Worker is running smoothly.", { status: 200 });
  }
};
