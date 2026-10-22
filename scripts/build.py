"""Baut aus src/app.html (1) die Artifact-Fassung und (2) die installierbare PWA in dist/."""
import base64, pathlib, re, shutil

root = pathlib.Path(__file__).resolve().parent.parent
src = (root / "src" / "app.html").read_text(encoding="utf-8")
assets = root / "assets"

def inline(m):
    data = base64.b64encode((assets / f"{m.group(1)}.webp").read_bytes()).decode()
    return f"data:image/webp;base64,{data}"

app = re.sub(r"\{\{IMG:([a-z-]+)\}\}", inline, src)
(root / "korrekturleitfaden.html").write_text(app, encoding="utf-8")

dist = root / "dist"
dist.mkdir(exist_ok=True)
head = """<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#F3F5F9">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Korrektur">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon-192.png">
<link rel="apple-touch-icon" href="icon-192.png">
<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>
"""
tail = """
<script>if ("serviceWorker" in navigator) navigator.serviceWorker.register("sw.js").catch(() => {});</script>
</body>
</html>
"""
# <title>, <meta>, <link>, <style> des Fragments gehören in den <head>, der Rest in den <body>
split = app.index("</style>") + len("</style>")
(dist / "index.html").write_text(head + app[:split] + "\n</head>\n<body>\n" + app[split:] + tail, encoding="utf-8")

(dist / "manifest.webmanifest").write_text("""{
  "name": "Korrekturleitfaden",
  "short_name": "Korrektur",
  "lang": "de",
  "start_url": "./",
  "scope": "./",
  "display": "standalone",
  "orientation": "any",
  "background_color": "#F3F5F9",
  "theme_color": "#F3F5F9",
  "icons": [
    { "src": "icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any" },
    { "src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable" }
  ]
}
""", encoding="utf-8")

(dist / "sw.js").write_text("""const CACHE = "korrekturleitfaden-v1";
const CORE = ["./", "index.html", "manifest.webmanifest", "icon-192.png", "icon-512.png"];
self.addEventListener("install", (e) => { e.waitUntil(caches.open(CACHE).then((c) => c.addAll(CORE)).then(() => self.skipWaiting())); });
self.addEventListener("activate", (e) => {
  e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== CACHE).map((k) => caches.delete(k)))).then(() => self.clients.claim()));
});
// Eigene Dateien: erst Netz (Aktualisierung), sonst Cache. Schriften: Cache, im Hintergrund auffrischen.
self.addEventListener("fetch", (e) => {
  const url = new URL(e.request.url);
  if (e.request.method !== "GET") return;
  if (url.origin === location.origin) {
    e.respondWith(fetch(e.request).then((r) => { const copy = r.clone(); caches.open(CACHE).then((c) => c.put(e.request, copy)); return r; })
      .catch(() => caches.match(e.request).then((r) => r || caches.match("index.html"))));
  } else if (/fonts\\.(googleapis|gstatic)\\.com$/.test(url.hostname)) {
    e.respondWith(caches.open(CACHE).then((c) => c.match(e.request).then((hit) => {
      const net = fetch(e.request).then((r) => { c.put(e.request, r.clone()); return r; }).catch(() => hit);
      return hit || net;
    })));
  }
});
""", encoding="utf-8")

for s in (192, 512):
    shutil.copy(assets / f"icon-{s}.png", dist / f"icon-{s}.png")
print("ok", len(app) // 1024, "KB")
