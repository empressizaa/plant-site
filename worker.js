export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    // Route traffic specifically for your RSS feed
    if (url.pathname === "/feed.xml") {
      try {
        // Fetch your generated feed file from your assets or binding
        const response = await env.ASSETS.fetch(request);
        const feedText = await response.text();

        return new Response(feedText, {
          headers: {
            "Content-Type": "application/xml; charset=utf-8",
            "Cache-Control": "no-cache"
          }
        });
      } catch (err) {
        return new Response("Feed generation error", { status: 500 });
      }
    }

    // Default: Fallback and serve all other regular static site files
    return env.ASSETS.fetch(request);
  }
};
