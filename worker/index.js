/**
 * SharpPages Site Audit — Cloudflare Worker
 *
 * Proxies Google PageSpeed Insights API and parses basic SEO signals
 * from the target page HTML. Returns a combined JSON response.
 *
 * Environment variables (set in wrangler.toml or dashboard):
 *   PSI_API_KEY  — Google PageSpeed Insights API key
 *   ALLOWED_ORIGIN — e.g. https://sharppages.com (or * for dev)
 */

const CORS_HEADERS = {
  "Access-Control-Allow-Methods": "GET, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
  "Access-Control-Max-Age": "86400",
};

function corsHeaders(origin, env) {
  const allowed = env.ALLOWED_ORIGIN || "*";
  return {
    ...CORS_HEADERS,
    "Access-Control-Allow-Origin": allowed === "*" ? "*" : origin,
  };
}

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin") || "";

    // Handle CORS preflight
    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: corsHeaders(origin, env) });
    }

    if (request.method !== "GET") {
      return jsonResponse({ error: "Method not allowed" }, 405, corsHeaders(origin, env));
    }

    const url = new URL(request.url);
    const targetUrl = url.searchParams.get("url");

    if (!targetUrl) {
      return jsonResponse({ error: "Missing ?url= parameter" }, 400, corsHeaders(origin, env));
    }

    // Validate URL format
    let parsedUrl;
    try {
      parsedUrl = new URL(targetUrl);
      if (!["http:", "https:"].includes(parsedUrl.protocol)) {
        throw new Error("Invalid protocol");
      }
    } catch {
      return jsonResponse({ error: "Invalid URL. Include https://" }, 400, corsHeaders(origin, env));
    }

    try {
      // Run PSI API call and HTML fetch in parallel
      const [psiResult, seoResult] = await Promise.allSettled([
        fetchPageSpeedInsights(targetUrl, env.PSI_API_KEY),
        fetchSeoChecks(targetUrl),
      ]);

      const response = {
        url: targetUrl,
        timestamp: new Date().toISOString(),
      };

      // PageSpeed data
      if (psiResult.status === "fulfilled") {
        response.pagespeed = psiResult.value;
      } else {
        response.pagespeed = { error: psiResult.reason?.message || "PageSpeed API failed" };
      }

      // SEO checks
      if (seoResult.status === "fulfilled") {
        response.seo = seoResult.value;
      } else {
        response.seo = { error: seoResult.reason?.message || "SEO check failed" };
      }

      return jsonResponse(response, 200, corsHeaders(origin, env));
    } catch (err) {
      return jsonResponse({ error: err.message }, 500, corsHeaders(origin, env));
    }
  },
};

async function fetchPageSpeedInsights(targetUrl, apiKey) {
  const psiUrl = new URL("https://www.googleapis.com/pagespeedonline/v5/runPagespeed");
  psiUrl.searchParams.set("url", targetUrl);
  psiUrl.searchParams.set("strategy", "mobile");
  psiUrl.searchParams.append("category", "performance");
  psiUrl.searchParams.append("category", "accessibility");
  psiUrl.searchParams.append("category", "best-practices");
  psiUrl.searchParams.append("category", "seo");

  if (apiKey) {
    psiUrl.searchParams.set("key", apiKey);
  }

  const res = await fetch(psiUrl.toString(), { cf: { cacheTtl: 300 } });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`PSI API returned ${res.status}: ${text.slice(0, 200)}`);
  }

  const data = await res.json();
  const cats = data.lighthouseResult?.categories || {};
  const audits = data.lighthouseResult?.audits || {};

  return {
    scores: {
      performance: Math.round((cats.performance?.score || 0) * 100),
      accessibility: Math.round((cats.accessibility?.score || 0) * 100),
      bestPractices: Math.round((cats["best-practices"]?.score || 0) * 100),
      seo: Math.round((cats.seo?.score || 0) * 100),
    },
    metrics: {
      speedIndex: audits["speed-index"]?.displayValue || null,
      lcp: audits["largest-contentful-paint"]?.displayValue || null,
      cls: audits["cumulative-layout-shift"]?.displayValue || null,
      tbt: audits["total-blocking-time"]?.displayValue || null,
    },
  };
}

async function fetchSeoChecks(targetUrl) {
  const res = await fetch(targetUrl, {
    headers: { "User-Agent": "SharpPages-Audit/1.0" },
    redirect: "follow",
    cf: { cacheTtl: 300 },
  });

  if (!res.ok) {
    throw new Error(`Failed to fetch page: ${res.status}`);
  }

  const html = await res.text();
  const checks = {};

  // Title tag
  const titleMatch = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
  checks.title = {
    exists: !!titleMatch,
    value: titleMatch ? titleMatch[1].trim().slice(0, 120) : null,
    length: titleMatch ? titleMatch[1].trim().length : 0,
    status: !titleMatch ? "red" : titleMatch[1].trim().length > 60 ? "yellow" : "green",
  };

  // Meta description
  const descMatch = html.match(/<meta[^>]+name=["']description["'][^>]+content=["']([^"']*)["']/i)
    || html.match(/<meta[^>]+content=["']([^"']*)["'][^>]+name=["']description["']/i);
  const descValue = descMatch ? descMatch[1].trim() : null;
  checks.metaDescription = {
    exists: !!descMatch,
    value: descValue ? descValue.slice(0, 200) : null,
    length: descValue ? descValue.length : 0,
    status: !descMatch ? "red" : (descValue.length < 120 || descValue.length > 160) ? "yellow" : "green",
  };

  // H1
  const h1Match = html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i);
  checks.h1 = {
    exists: !!h1Match,
    value: h1Match ? h1Match[1].replace(/<[^>]+>/g, "").trim().slice(0, 120) : null,
    status: h1Match ? "green" : "red",
  };

  // Viewport meta
  const viewportMatch = html.match(/<meta[^>]+name=["']viewport["']/i);
  checks.viewport = {
    exists: !!viewportMatch,
    status: viewportMatch ? "green" : "red",
  };

  // Canonical URL
  const canonicalMatch = html.match(/<link[^>]+rel=["']canonical["'][^>]+href=["']([^"']*)["']/i);
  checks.canonical = {
    exists: !!canonicalMatch,
    value: canonicalMatch ? canonicalMatch[1] : null,
    status: canonicalMatch ? "green" : "yellow",
  };

  // OG tags
  const ogTitle = html.match(/<meta[^>]+property=["']og:title["']/i);
  const ogDesc = html.match(/<meta[^>]+property=["']og:description["']/i);
  const ogImage = html.match(/<meta[^>]+property=["']og:image["']/i);
  checks.ogTags = {
    title: !!ogTitle,
    description: !!ogDesc,
    image: !!ogImage,
    status: ogTitle && ogDesc && ogImage ? "green" : ogTitle || ogDesc ? "yellow" : "red",
  };

  // Schema markup
  const schemaMatch = html.match(/application\/ld\+json/i);
  checks.schema = {
    exists: !!schemaMatch,
    status: schemaMatch ? "green" : "yellow",
  };

  return checks;
}

function jsonResponse(data, status, headers) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      "Content-Type": "application/json",
      ...headers,
    },
  });
}
