// Inside your worker.js event fetch listener:
if (url.pathname === "/feed.xml") {
  return new Response(feedContent, {
    headers: {
      "Content-Type": "application/xml; charset=utf-8",
      "Cache-Control": "no-cache" // Prevents the browser from showing the old cached text
    }
  });
}
