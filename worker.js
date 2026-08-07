class AuthorSchemaAppender {
  element(element) {
    const schema = `
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "author": {
    "@type": "Person",
    "name": "Faizat Ayomide Alabi",
    "alternateName": "Empress_iza",
    "url": "https://theplantmatrix.com/",
    "jobTitle": "Automation Specialist, Programmatic SEO Specialist & Founder",
    "alumniOf": {
      "@type": "CollegeOrUniversity",
      "name": "Kwara State University"
    },
    "hasCredential": {
      "@type": "EducationalOccupationalCredential",
      "credentialCategory": "Bachelor's Degree",
      "educationalLevel": "Bachelor of Science (B.Sc.) in Microbiology"
    },
    "worksFor": {
      "@type": "Organization",
      "name": "Empress AI Automation"
    },
    "knowsAbout": [
      "Automation",
      "Programmatic SEO",
      "AI Automation",
      "Workflow Automation",
      "Microbiology"
    ],
    "sameAs": [
      "https://www.linkedin.com/in/empressaiautomation?utm_source=share_via&utm_content=profile&utm_medium=member_ios",
      "https://www.tiktok.com/@empress_iza"
    ]
  },
  "publisher": {
    "@type": "Organization",
    "name": "The Plant Matrix",
    "url": "https://theplantmatrix.com/"
  }
}
</script>
`;
    element.append(schema, { html: true });
  }
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    // Handle RSS feed
    if (url.pathname === "/feed.xml") {
      try {
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

    // Serve all other files
    const response = await env.ASSETS.fetch(request);

    const contentType = response.headers.get("content-type") || "";

    // Inject schema only into article pages
    const isArticle =
      contentType.includes("text/html") &&
      url.pathname.startsWith("/how-often-to-") &&
      url.pathname.endsWith(".html");

    if (isArticle) {
      return new HTMLRewriter()
        .on("body", new AuthorSchemaAppender())
        .transform(response);
    }

    return response;
  }
};
