export default {
  async fetch(request) {
    const url = new URL(request.url);

    // Proxy /bot... (API calls) and /file/bot... (file downloads)
    if (url.pathname.startsWith('/bot') || url.pathname.startsWith('/file/bot')) {
      const telegramUrl = 'https://api.telegram.org' + url.pathname + url.search;

      // Rebuild headers, stripping 'host' so Telegram accepts the request
      const headers = new Headers(request.headers);
      headers.delete('host');

      const newRequest = new Request(telegramUrl, {
        method: request.method,
        headers,
        body: request.method !== 'GET' && request.method !== 'HEAD' ? request.body : undefined,
        redirect: 'follow',
      });

      const response = await fetch(newRequest);

      // Return response with CORS headers so the browser doesn't block it
      const newHeaders = new Headers(response.headers);
      newHeaders.set('Access-Control-Allow-Origin', '*');

      return new Response(response.body, {
        status: response.status,
        statusText: response.statusText,
        headers: newHeaders,
      });
    }

    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
          'Access-Control-Allow-Headers': '*',
        },
      });
    }

    return new Response('Telegram API Proxy Worker is running smoothly.', { status: 200 });
  },
};
