export default {
async fetch(request, env, ctx) {
const url = new URL(request.url);
// Securely routes all worker traffic directly to your live GitHub Pages hosting layout
return fetch(`https://github.io{url.pathname}${url.search}`);
},
};
