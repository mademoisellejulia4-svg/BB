#!/usr/bin/env python3
import base64, io, json, re, os
from PIL import Image

ROOT = "/home/user/BB"
PUB = os.path.join(ROOT, "public")

def data_uri(path, max_w=1100, quality=82):
    img = Image.open(path).convert("RGB")
    if img.width > max_w:
        h = round(img.height * max_w / img.width)
        img = img.resize((max_w, h), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=quality, optimize=True)
    b = buf.getvalue()
    return "data:image/jpeg;base64," + base64.b64encode(b).decode(), len(b)

# --- compress images, map relative path -> data uri ---
img_files = {
    "images/black-tea.png": ("images/black-tea.png", 1100),
    "images/hero-poster.jpg": ("images/hero-poster.jpg", 1280),
    "images/storefront.jpg": ("images/storefront.jpg", 1400),
    "images/brew-brewer.jpg": ("images/brew-brewer.jpg", 560),
    "images/brew-infuser.jpg": ("images/brew-infuser.jpg", 560),
    "images/brew-water.jpg": ("images/brew-water.jpg", 560),
    "images/brew-tea.jpg": ("images/brew-tea.jpg", 560),
    "images/name-1.jpg": ("images/name-1.jpg", 900),
    "images/name-2.jpg": ("images/name-2.jpg", 900),
    "images/name-3.jpg": ("images/name-3.jpg", 760),
    "images/caffeine-hero.jpg": ("images/caffeine-hero.jpg", 1280),
    "images/caffeine-cups.jpg": ("images/caffeine-cups.jpg", 1000),
    "images/pear-pistachio.jpg": ("images/pear-pistachio.jpg", 800),
    "images/lull.jpg": ("images/lull.jpg", 800),
    "images/watermelon-sugar.jpg": ("images/watermelon-sugar.jpg", 800),
    "images/robin-hood-1.jpg": ("images/robin-hood-1.jpg", 800),
    "images/robin-hood-2.jpg": ("images/robin-hood-2.jpg", 800),
    "images/deep-breath.jpg": ("images/deep-breath.jpg", 800),
    "images/strawberry-fields-forever.jpg": ("images/strawberry-fields-forever.jpg", 800),
    "images/cherry-kiss.jpg": ("images/cherry-kiss.jpg", 800),
    "images/little-picture.jpg": ("images/little-picture.jpg", 800),
    "images/raspberry-rose.jpg": ("images/raspberry-rose.jpg", 800),
    "images/jaffa-cake.jpg": ("images/jaffa-cake.jpg", 800),
    "images/french-toast.jpg": ("images/french-toast.jpg", 800),
    "images/plum-tart.jpg": ("images/plum-tart.jpg", 800),
    "images/battenberg.jpg": ("images/battenberg.jpg", 800),
    "images/rhubarb-custard.jpg": ("images/rhubarb-custard.jpg", 800),
    "images/hound-on-the-hunt.jpg": ("images/hound-on-the-hunt.jpg", 800),
    "images/newsletter-bg.jpg": ("images/newsletter-bg.jpg", 1400),
    "images/fav-caramel-apple-betty.jpg": ("images/fav-caramel-apple-betty.jpg", 500),
    "images/fav-battenberg.jpg": ("images/fav-battenberg.jpg", 500),
    "images/fav-biscuit-brew.jpg": ("images/fav-biscuit-brew.jpg", 500),
    "images/fav-lull.jpg": ("images/fav-lull.jpg", 500),
    "images/best-seller.jpg": ("images/best-seller.jpg", 800),
    "images/green-tea.png": ("images/green-tea.png", 1100),
    "images/fruit-herbal.png": ("images/fruit-herbal.png", 1100),
    "images/matcha-kit.png": ("images/matcha-kit.png", 1000),
    "images/matcha.png": ("images/matcha.png", 1000),
    "images/matcha-whisk.png": ("images/matcha-whisk.png", 1000),
    "images/starter-loose-leaf.png": ("images/starter-loose-leaf.png", 1000),
    "images/starter-matcha.png": ("images/starter-matcha.png", 1000),
    "images/story-owners.png": ("images/story-owners.png", 800),
    "images/story-1.jpg": ("images/story-1.jpg", 760),
    "images/story-2.jpg": ("images/story-2.jpg", 760),
    "images/instagram-1.jpg": ("images/instagram-1.jpg", 540),
    "images/instagram-2.jpg": ("images/instagram-2.jpg", 540),
    "images/review-teapot.jpg": ("images/review-teapot.jpg", 560),
    "images/review-food.jpg": ("images/review-food.jpg", 640),
    "images/book-afternoon-tea.jpg": ("images/book-afternoon-tea.jpg", 1100),
    "images/cherry-bakewell.jpg": ("images/cherry-bakewell.jpg", 760),
    "images/biscuit-brew.jpg": ("images/biscuit-brew.jpg", 760),
    "images/caramel-apple-betty.jpg": ("images/caramel-apple-betty.jpg", 760),
    "images/english-breakfast.jpg": ("images/english-breakfast.jpg", 760),
    "images/moonbeam.jpg": ("images/moonbeam.jpg", 760),
    "images/james-giant-peach.jpg": ("images/james-giant-peach.jpg", 760),
    "images/mango-tchai.jpg": ("images/mango-tchai.jpg", 760),
    "images/banana-fudge.jpg": ("images/banana-fudge.jpg", 760),
    "images/salted-caramel.jpg": ("images/salted-caramel.jpg", 760),
    "images/bucket-brewer.jpg": ("images/bucket-brewer.jpg", 900),
    "images/cast-iron-teapot.jpg": ("images/cast-iron-teapot.jpg", 760),
    "images/essential-bundle.jpg": ("images/essential-bundle.jpg", 1000),
    "images/rooibos.png": ("images/rooibos.png", 1100),
    "images/vouchers.png": ("images/vouchers.png", 1100),
    "images/accessories.png": ("images/accessories.png", 1100),
    "images/tea-taster-box.jpg": ("images/tea-taster-box.jpg", 760),
    "images/loose-leaf-bundle.jpg": ("images/loose-leaf-bundle.jpg", 900),
    "images/tea-tube.jpg": ("images/tea-tube.jpg", 760),
    "images/studio-chocolate.jpg": ("images/studio-chocolate.jpg", 760),
    "images/strawberry-jam.jpg": ("images/strawberry-jam.jpg", 760),
    "images/essentially-giftset.jpg": ("images/essentially-giftset.jpg", 760),
    "images/rv-battenburg.jpg": ("images/rv-battenburg.jpg", 300),
    "images/rv-taster.jpg": ("images/rv-taster.jpg", 300),
    "images/rv-biscuitbrew.jpg": ("images/rv-biscuitbrew.jpg", 300),
    "images/rv-cherrybakewell.jpg": ("images/rv-cherrybakewell.jpg", 300),
}
uri_map = {}
total = 0
for rel, (p, mw) in img_files.items():
    uri, n = data_uri(os.path.join(PUB, p), max_w=mw)
    uri_map[rel] = uri
    total += n
    print(f"  {rel}: {n//1024} KB")
print(f"  images total: {total//1024} KB")

# hero background = black tea tin (already a cinematic dark shot)
hero_uri = uri_map["images/black-tea.png"]

# --- load catalog, replace image paths with data URIs ---
with open(os.path.join(PUB, "data/products.json")) as f:
    store = json.load(f)
store.pop("_comment", None)
for cat in store["categories"]:
    if cat.get("image") in uri_map:
        cat["image"] = uri_map[cat["image"]]
    for prod in cat["products"]:
        if prod.get("image") in uri_map:
            prod["image"] = uri_map[prod["image"]]
store_json = json.dumps(store, ensure_ascii=False)

# --- reuse the CSS block from the served site for visual parity ---
with open(os.path.join(PUB, "index.html")) as f:
    page = f.read()
css = re.search(r"<style>(.*?)</style>", page, re.S).group(1)

HERO_CSS = """
  /* standalone reuses the scroll-scrubbed video hero CSS from index.html */
  /* Instagram tiles use poster thumbnails + play overlay (reels removed) */
  .ig-tile .ig-play{ position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); width:54px; height:54px; border-radius:50%; background:rgba(0,0,0,0.4); border:1.5px solid rgba(255,255,255,0.85); display:flex; align-items:center; justify-content:center; transition:transform .3s var(--ease), background .3s var(--ease); }
  .ig-tile:hover .ig-play{ transform:translate(-50%,-50%) scale(1.08); background:rgba(var(--amber-rgb),0.85); }
  .ig-tile .ig-play::after{ content:""; margin-left:4px; border-style:solid; border-width:9px 0 9px 15px; border-color:transparent transparent transparent #fff; }
  #promoMsg{ transition:opacity .4s ease; }
  #favourites{ position:relative; z-index:2; background:linear-gradient(to bottom, #0a0a1a, #050510); padding:clamp(70px,11vh,140px) clamp(20px,6vw,90px); text-align:center; }
  .fav-grid{ max-width:1100px; margin:46px auto 0; display:grid; gap:30px; grid-template-columns:repeat(auto-fit, minmax(210px, 1fr)); }
  .fav-card{ cursor:pointer; display:flex; flex-direction:column; align-items:center; }
  .fav-medal{ position:relative; width:180px; height:180px; border-radius:50%; background-size:cover; background-position:center; background-color:#0c0c14; border:1px solid rgba(var(--amber-rgb),0.25); box-shadow:0 20px 40px -20px rgba(0,0,0,0.7); transition:transform .4s var(--ease), box-shadow .4s var(--ease), border-color .4s var(--ease); }
  .fav-card:hover .fav-medal{ transform:translateY(-8px) scale(1.03); border-color:rgba(255,170,0,0.6); box-shadow:0 30px 50px -20px rgba(0,0,0,0.8), 0 0 30px -8px rgba(255,170,0,0.3); }
  .fav-badge{ position:absolute; top:12px; left:50%; transform:translateX(-50%); background:#3a4a3a; color:#fff; font-size:9px; letter-spacing:.12em; text-transform:uppercase; padding:4px 10px; border-radius:30px; white-space:nowrap; }
  .fav-name{ margin-top:18px; font-family:'Cormorant Garamond',serif; font-size:21px; color:#fff; letter-spacing:.02em; }
  .fav-price{ margin-top:5px; font-size:12px; color:rgba(var(--amber-rgb),0.85); letter-spacing:.04em; }
  .fav-shop{ margin-top:44px; cursor:pointer; background:none; border:1px solid rgba(var(--amber-rgb),0.5); color:var(--amber); border-radius:40px; padding:13px 30px; font-family:'Inter',sans-serif; font-size:11px; text-transform:uppercase; letter-spacing:.22em; transition:all .3s var(--ease); }
  .fav-shop:hover{ background:rgba(var(--amber-rgb),0.1); transform:translateY(-2px); }
  .nl-club{ margin:38px auto 0; max-width:440px; display:flex; flex-direction:column; gap:16px; }
  .nlc-two{ display:flex; gap:16px; }
  .nl-club input{ flex:1; width:100%; background:transparent; border:none; border-bottom:1px solid rgba(var(--amber-rgb),0.5); color:#fff; padding:12px 4px; font-family:'Inter',sans-serif; font-size:14px; letter-spacing:.04em; }
  .nl-club input::placeholder{ color:rgba(255,255,255,0.4); }
  .nl-club input:focus{ outline:none; border-color:var(--amber); }
  .nl-club-btn{ margin-top:10px; cursor:pointer; background:var(--amber); color:#0a0a0a; border:none; border-radius:40px; padding:15px; font-family:'Inter',sans-serif; font-size:11px; font-weight:500; text-transform:uppercase; letter-spacing:.22em; transition:transform .3s var(--ease), filter .3s var(--ease); }
  .nl-club-btn:hover{ filter:brightness(1.08); transform:translateY(-2px); }
  @media (max-width:440px){ .nlc-two{ flex-direction:column; } }
  #promoModal{ position:fixed; inset:0; z-index:900; display:none; align-items:center; justify-content:center; padding:24px; background:rgba(3,3,5,0.80); backdrop-filter:blur(6px); opacity:0; transition:opacity .5s var(--ease); }
  #promoModal.open{ display:flex; }
  .pm-card{ position:relative; width:min(460px, 94vw); max-height:92vh; overflow:auto; background:radial-gradient(120% 90% at 50% 18%, #fbf7ef, #f1e8d8); border:1px solid rgba(var(--amber-rgb),0.35); border-radius:50% / 42%; padding:clamp(54px,8vw,74px) clamp(40px,8vw,64px); text-align:center; box-shadow:0 50px 120px -40px rgba(0,0,0,0.85), inset 0 0 0 1px rgba(255,255,255,0.5); transform:scale(.92) translateY(14px); transition:transform .55s var(--ease); }
  #promoModal.open .pm-card{ transform:scale(1) translateY(0); }
  .pm-close{ position:absolute; top:18px; right:22px; width:34px; height:34px; border-radius:50%; background:none; border:1px solid rgba(58,74,58,0.35); color:#3a4a3a; font-size:18px; line-height:1; cursor:pointer; transition:all .3s var(--ease); }
  .pm-close:hover{ background:#3a4a3a; color:#fff; border-color:#3a4a3a; }
  .pm-eyebrow{ font-size:10px; letter-spacing:.4em; text-transform:uppercase; color:#9a7b3a; margin-bottom:12px; }
  .pm-card h2{ font-family:'Cormorant Garamond', serif; font-weight:600; font-size:clamp(28px,7vw,40px); line-height:1.1; letter-spacing:.02em; color:#2f3a2f; }
  .pm-card h2 .pm-amber{ color:#b8860b; }
  .pm-card p{ margin:16px auto 24px; max-width:300px; font-size:13px; line-height:1.6; color:rgba(47,58,47,0.7); }
  .pm-card form{ display:flex; flex-direction:column; gap:18px; max-width:300px; margin:0 auto; }
  .pm-card .pm-field{ text-align:left; }
  .pm-card label{ display:block; font-size:10px; text-transform:uppercase; letter-spacing:.2em; color:rgba(47,58,47,0.6); margin-bottom:6px; }
  .pm-card input{ width:100%; background:transparent; border:none; border-bottom:1px solid rgba(58,74,58,0.4); color:#2f3a2f; padding:8px 2px; font-family:'Inter',sans-serif; font-size:15px; }
  .pm-card input:focus{ outline:none; border-color:#b8860b; }
  .pm-btn{ margin-top:8px; cursor:pointer; align-self:center; background:none; border:1px solid #3a4a3a; color:#3a4a3a; border-radius:40px; padding:13px 40px; font-family:'Inter',sans-serif; font-size:11px; font-weight:500; text-transform:uppercase; letter-spacing:.24em; transition:all .3s var(--ease); }
  .pm-btn:hover{ background:#3a4a3a; color:#fbf7ef; }
  @media (max-width:520px){ .pm-card{ border-radius:30px; padding:54px 30px; } }
  #book{ position:relative; z-index:2; background:#0a0a14; padding:clamp(80px,12vh,150px) clamp(20px,6vw,90px); border-top:1px solid rgba(255,255,255,0.06); }
  .book-banner{ max-width:1100px; margin:0 auto 48px; height:clamp(220px,34vh,380px); border-radius:18px; overflow:hidden; border:1px solid rgba(255,255,255,0.08); }
  .book-banner img{ width:100%; height:100%; object-fit:cover; display:block; }
  .book-grid{ max-width:1100px; margin:0 auto; display:grid; gap:54px; grid-template-columns:1.25fr 1fr; }
  @media (max-width:820px){ .book-grid{ grid-template-columns:1fr; } }
  .book-form{ display:flex; flex-direction:column; gap:18px; }
  .bf-row{ display:flex; flex-direction:column; gap:7px; }
  .bf-row label{ font-size:10px; text-transform:uppercase; letter-spacing:.22em; color:rgba(255,255,255,0.5); }
  .bf-row input, .bf-row select, .bf-row textarea{ background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.12); border-radius:10px; padding:13px 14px; color:#fff; font-family:'Inter',sans-serif; font-size:14px; letter-spacing:.02em; }
  .bf-row textarea{ resize:vertical; min-height:84px; }
  .bf-row input:focus, .bf-row select:focus, .bf-row textarea:focus{ outline:none; border-color:rgba(var(--amber-rgb),0.6); }
  .bf-row select option{ background:#0c0c16; color:#fff; }
  .bf-two{ display:grid; grid-template-columns:1fr 1fr; gap:16px; }
  @media (max-width:480px){ .bf-two{ grid-template-columns:1fr; } }
  .book-submit{ margin-top:6px; cursor:pointer; background:var(--amber); color:#0a0a0a; border:none; border-radius:12px; padding:16px; font-family:'Inter',sans-serif; font-size:11px; font-weight:500; text-transform:uppercase; letter-spacing:.22em; transition:transform .3s var(--ease), filter .3s var(--ease); }
  .book-submit:hover{ filter:brightness(1.08); transform:translateY(-2px); }
  .book-note{ font-size:11px; color:rgba(255,255,255,0.4); letter-spacing:.03em; text-align:center; }
  .book-aside .ba-block{ margin-bottom:40px; }
  .book-aside h3{ font-family:'Cormorant Garamond',serif; font-size:26px; font-weight:500; color:#fff; margin-bottom:16px; letter-spacing:.03em; }
  .hours-row{ display:flex; justify-content:space-between; max-width:320px; font-size:13px; padding:8px 0; border-bottom:1px solid rgba(255,255,255,0.07); color:rgba(255,255,255,0.7); }
  .hours-row span:last-child{ color:rgba(255,255,255,0.45); }
  .book-aside p{ font-size:13px; font-weight:300; line-height:1.8; color:rgba(255,255,255,0.6); }
  .maps-btn{ display:inline-flex; align-items:center; gap:9px; margin-top:16px; border:1px solid rgba(var(--amber-rgb),0.5); color:var(--amber); text-decoration:none; border-radius:40px; padding:11px 22px; font-size:11px; text-transform:uppercase; letter-spacing:.2em; transition:all .3s var(--ease); }
  .maps-btn:hover{ background:rgba(var(--amber-rgb),0.1); transform:translateY(-2px); }
  #reviews{ position:relative; z-index:2; background:#08080f; padding:clamp(80px,12vh,150px) clamp(20px,6vw,90px); border-top:1px solid rgba(255,255,255,0.06); text-align:center; }
  .rv-score{ display:inline-flex; align-items:center; gap:14px; margin-top:8px; flex-wrap:wrap; justify-content:center; }
  .rv-score .rv-num{ font-family:'Cormorant Garamond',serif; font-size:44px; color:#fff; line-height:1; }
  .rv-stars{ color:var(--amber); font-size:18px; letter-spacing:2px; }
  .rv-count{ font-size:12px; color:rgba(255,255,255,0.5); letter-spacing:.04em; }
  .rv-marquee{ margin:46px auto 0; overflow:hidden; text-align:center; -webkit-mask:linear-gradient(90deg, transparent, #000 6%, #000 94%, transparent); mask:linear-gradient(90deg, transparent, #000 6%, #000 94%, transparent); }
  .rv-track{ display:flex; align-items:stretch; gap:22px; width:max-content; animation:rv-scroll 48s linear infinite; }
  .rv-marquee:hover .rv-track{ animation-play-state:paused; }
  @keyframes rv-scroll{ from{ transform:translateX(0); } to{ transform:translateX(-50%); } }
  @media (prefers-reduced-motion:reduce){ .rv-marquee{ overflow-x:auto; } .rv-track{ animation:none; } }
  .rv-card{ flex:0 0 300px; max-width:300px; border:1px solid rgba(255,255,255,0.08); border-radius:16px; background:linear-gradient(160deg, rgba(255,255,255,0.045), rgba(255,255,255,0.015)); padding:30px 24px 26px; display:flex; flex-direction:column; align-items:center; gap:14px; }
  .rv-card .rv-s{ color:var(--amber); font-size:13px; letter-spacing:2px; }
  .rv-card .rv-q{ font-size:14px; font-weight:300; line-height:1.7; color:rgba(255,255,255,0.78); flex:1; }
  .rv-card .rv-by{ font-size:11px; letter-spacing:.06em; color:rgba(255,255,255,0.45); }
  .rv-card .rv-by b{ color:rgba(255,255,255,0.7); font-weight:500; }
  .rv-cta{ display:inline-block; margin-top:36px; cursor:pointer; text-decoration:none; border:1px solid rgba(255,255,255,0.16); color:rgba(255,255,255,0.8); border-radius:40px; padding:13px 28px; font-size:11px; text-transform:uppercase; letter-spacing:.2em; transition:all .3s var(--ease); }
  .rv-cta:hover{ border-color:rgba(var(--amber-rgb),0.6); color:var(--amber); }
  .fc-social{ margin-top:22px; display:flex; gap:14px; }
  .fc-social a{ width:34px; height:34px; border:1px solid rgba(255,255,255,0.15); border-radius:50%; display:flex; align-items:center; justify-content:center; color:rgba(255,255,255,0.6); text-decoration:none; transition:all .3s var(--ease); }
  .fc-social a:hover{ border-color:var(--amber); color:var(--amber); }
  .fc-pay{ max-width:1180px; margin:30px auto 0; padding-top:22px; border-top:1px solid rgba(255,255,255,0.06); display:flex; flex-wrap:wrap; gap:9px; align-items:center; }
  .fc-pay .pay{ font-size:9px; letter-spacing:.06em; color:rgba(255,255,255,0.5); border:1px solid rgba(255,255,255,0.14); border-radius:5px; padding:5px 8px; background:rgba(255,255,255,0.03); }
  .fc-pay svg{ height:28px; width:auto; display:block; }

  #cafemenu{ position:relative; z-index:2; background:#08080f; padding:clamp(80px,12vh,150px) clamp(20px,6vw,90px); border-top:1px solid rgba(255,255,255,0.06); }
  .cm-grid{ max-width:1180px; margin:0 auto; display:grid; gap:34px 48px; grid-template-columns:repeat(auto-fit, minmax(300px, 1fr)); }
  .cm-group h3{ font-family:'Cormorant Garamond',serif; font-size:26px; font-weight:500; color:#fff; letter-spacing:.04em; margin-bottom:6px; }
  .cm-group .cm-note{ font-size:11px; color:rgba(255,255,255,0.4); letter-spacing:.04em; margin-bottom:16px; }
  .cm-row{ display:flex; align-items:baseline; gap:12px; padding:9px 0; border-bottom:1px dashed rgba(255,255,255,0.08); }
  .cm-row .cm-name{ color:rgba(255,255,255,0.82); font-size:14px; }
  .cm-row .cm-dots{ flex:1; border-bottom:1px dotted rgba(255,255,255,0.18); transform:translateY(-3px); }
  .cm-row .cm-price{ font-family:'Cormorant Garamond',serif; color:var(--amber); font-size:16px; white-space:nowrap; }
  .cm-sub{ font-size:11.5px; font-weight:300; color:rgba(255,255,255,0.4); margin-top:6px; line-height:1.6; }
  .kids-free{ max-width:1180px; margin:46px auto 0; text-align:center; border:1px solid rgba(var(--amber-rgb),0.3); border-radius:14px; padding:24px 28px; background:rgba(var(--amber-rgb),0.06); }
  .kids-free b{ color:var(--amber); font-weight:500; letter-spacing:.06em; }
  .kids-free span{ display:block; margin-top:8px; font-size:12px; font-weight:300; color:rgba(255,255,255,0.55); }

  #refer{ position:relative; z-index:2; background:linear-gradient(160deg, #3a4a3a, #2a352a); padding:clamp(70px,11vh,130px) 24px; text-align:center; }
  #refer .r-eyebrow{ font-size:11px; letter-spacing:.4em; text-transform:uppercase; color:var(--amber); margin-bottom:16px; }
  #refer h2{ font-family:'Cormorant Garamond',serif; font-size:clamp(34px,6vw,54px); font-weight:500; color:#fff; }
  #refer p{ margin-top:14px; font-size:14px; font-weight:300; color:rgba(255,255,255,0.7); }
  .r-cards{ margin-top:40px; display:flex; gap:20px; justify-content:center; flex-wrap:wrap; }
  .r-card{ background:rgba(0,0,0,0.25); border:1px solid rgba(255,255,255,0.12); border-radius:14px; padding:26px 32px; min-width:200px; }
  .r-card .r-amt{ font-family:'Cormorant Garamond',serif; font-size:34px; color:var(--amber); }
  .r-card .r-lbl{ margin-top:6px; font-size:12px; letter-spacing:.06em; color:rgba(255,255,255,0.65); }
  .r-cta{ margin-top:40px; display:inline-block; cursor:pointer; background:var(--amber); color:#0a0a0a; border:none; border-radius:12px; padding:15px 38px; font-family:'Inter',sans-serif; font-size:11px; font-weight:500; text-transform:uppercase; letter-spacing:.22em; transition:transform .3s var(--ease), filter .3s var(--ease); }
  .r-cta:hover{ filter:brightness(1.08); transform:translateY(-2px); }
"""

JS = """
(function(){
  "use strict";
  const $ = (s,r=document)=>r.querySelector(s);
  const STORE = __STORE__;
  const symbol = ()=> (STORE.store && STORE.store.currencySymbol) || '\\u00a3';
  const fmt = n => symbol() + Number(n).toFixed(2);
  const fromPrice = p => Math.min.apply(null, p.variants.map(v=>v.price));
  const CAT = {}; (STORE.categories||[]).forEach(c=>CAT[c.id]=c);
  const FAVS=[['black','caramel-apple-betty','images/fav-caramel-apple-betty.jpg'],['rooibos','battenburg','images/fav-battenberg.jpg'],['black','biscuit-brew','images/fav-biscuit-brew.jpg'],['green','lull','images/fav-lull.jpg']];
  function buildFavourites(){
    const grid=$('#favGrid'); if(!grid) return; grid.innerHTML='';
    FAVS.forEach(([cid,pid,img])=>{
      const c=CAT[cid]; if(!c) return; const p=(c.products||[]).find(x=>x.id===pid); if(!p) return;
      const bg=img||c.image;
      const card=document.createElement('div'); card.className='fav-card';
      card.innerHTML='<div class="fav-medal"'+(bg?' style="background-image:url(\\''+bg+'\\')"':'')+'><span class="fav-badge">'+c.name+'</span></div>'+
        '<div class="fav-name">'+p.name+'</div>'+
        '<div class="fav-price">From '+fmt(fromPrice(p))+'</div>';
      card.addEventListener('click',()=>openModal(c,p));
      grid.appendChild(card);
    });
  }

  /* ---- categories ---- */
  const catGrid = $('#catGrid');
  function buildCategories(){
    catGrid.innerHTML='';
    const bcard=document.createElement('div'); bcard.className='cat-card cat-best';
    bcard.innerHTML='<div class="cc-img" style="background-image:url(\\'images/best-seller.jpg\\')"></div>'+
      '<div class="cc-index cc-star">\\u2605</div>'+
      '<div class="cc-name">Best Sellers</div>'+
      '<div class="cc-meta">The blends everyone loves</div>'+
      '<div class="cc-cta">Explore \\u2192</div>';
    bcard.addEventListener('click',openBestSellers);
    catGrid.appendChild(bcard);
    STORE.categories.forEach((c,i)=>{
      const card=document.createElement('div'); card.className='cat-card';
      const count=(c.products&&c.products.length)||0;
      const img=c.image?'<div class="cc-img" style="background-image:url(\\''+c.image+'\\')"></div>':'';
      card.innerHTML=img+
        '<div class="cc-index">'+(i<9?'0':'')+(i+1)+'</div>'+
        '<div class="cc-name">'+c.name+'</div>'+
        '<div class="cc-meta">'+(c.meta||(count+' blends'))+'</div>'+
        '<div class="cc-cta">Explore \\u2192</div>';
      card.addEventListener('click',()=>openCategory(c.id));
      catGrid.appendChild(card);
    });
  }
  const catView=$('#catView'), detailView=$('#detailView'), prodGrid=$('#prodGrid');
  function renderDetail(title, items, medals){
    $('#detailTitle').textContent=title; prodGrid.innerHTML='';
    prodGrid.classList.toggle('medals', !!medals);
    items.forEach(({c,p})=>{
      const card=document.createElement('div');
      if(medals){
        card.className='fav-card';
        const bg=p.image||c.image;
        card.innerHTML='<div class="fav-medal"'+(bg?' style="background-image:url(\\''+bg+'\\')"':'')+'><span class="fav-badge">'+c.name+'</span></div>'+
          '<div class="fav-name">'+p.name+'</div>'+
          '<div class="fav-price">From '+fmt(fromPrice(p))+'</div>';
      } else {
        card.className='prod-card';
        const chips=p.variants.map(v=>'<span class="pc-chip">'+v.size+' <b>'+fmt(v.price)+'</b></span>').join('');
        const pimg=p.image?'<div class="pc-img" style="background-image:url(\\''+p.image+'\\')"></div>':'';
        card.innerHTML=pimg+
          '<div class="pc-cat">'+c.name+'</div>'+
          '<div class="pc-name">'+p.name+'</div>'+
          (p.rating?'<div class="pc-stars">'+('★★★★★'.slice(0,p.rating))+' <span>'+(p.reviews||'')+(p.reviews?' reviews':'')+'</span></div>':'')+
          '<div class="pc-desc">'+(p.description||'')+'</div>'+
          '<div class="pc-variants">'+chips+'</div>'+
          '<div class="pc-from"><span><span class="lbl">From&nbsp;</span><span class="val">'+fmt(fromPrice(p))+'</span></span><span class="pc-view">View \\u2192</span></div>';
      }
      card.addEventListener('click',()=>openModal(c,p));
      prodGrid.appendChild(card);
    });
    catView.classList.remove('active'); detailView.classList.add('active');
    window.scrollTo({top:$('#products').offsetTop-10,behavior:'smooth'});
  }
  const BEST=[['black','biscuit-brew'],['black','moonbeam'],['black','caramel-apple-betty'],['black','cherry-bakewell'],['herbal','strawberry-fields-forever'],['herbal','raspberry-rose'],['black','english-breakfast'],['green','robin-hood']];
  function openBestSellers(){ renderDetail('Best Sellers', BEST.map(([cid,pid])=>findProd(cid,pid)).filter(Boolean), true); }
  function openCategory(id){ const c=CAT[id]; if(!c) return; renderDetail(c.name,(c.products||[]).map(p=>({c,p}))); }
  function backToCats(){ detailView.classList.remove('active'); catView.classList.add('active'); }
  $('#backBtn').addEventListener('click',backToCats);

  /* ---- recommendations: "You may also like" + "Recently viewed" ---- */
  const RECENT_KEY='bb_recent_v1';
  function allProducts(){ const out=[]; (STORE.categories||[]).forEach(c=>(c.products||[]).forEach(p=>out.push({c,p}))); return out; }
  function findProd(cid,pid){ const c=CAT[cid]; if(!c) return null; const p=(c.products||[]).find(x=>x.id===pid); return p?{c,p}:null; }
  function getRecent(){ try{ return JSON.parse(localStorage.getItem(RECENT_KEY))||[]; }catch(e){ return []; } }
  function pushRecent(cid,pid){ let r=getRecent().filter(x=>!(x.cid===cid&&x.pid===pid)); r.unshift({cid,pid}); try{ localStorage.setItem(RECENT_KEY,JSON.stringify(r.slice(0,12))); }catch(e){} }
  function recCard(c,p){
    const card=document.createElement('div'); card.className='rec-card';
    const img=p.image||c.image||'';
    card.innerHTML='<div class="rec-img"'+(img?' style="background-image:url(\\''+img+'\\')"':'')+'><span class="rec-badge">'+c.name+'</span></div>'+
      '<div class="rec-name">'+p.name+'</div>'+
      '<div class="rec-price">From '+fmt(fromPrice(p))+'</div>';
    card.addEventListener('click',()=>openModal(c,p));
    return card;
  }
  function renderAlsoLike(c,p){
    const row=$('#mAlsoRow'); row.innerHTML='';
    const picks=[];
    (c.products||[]).forEach(x=>{ if(x.id!==p.id) picks.push({c,p:x}); });
    if(picks.length<4){ allProducts().forEach(({c:cc,p:pp})=>{ if(picks.length>=8||cc.id===c.id) return; picks.push({c:cc,p:pp}); }); }
    picks.slice(0,4).forEach(({c:cc,p:pp})=>row.appendChild(recCard(cc,pp)));
    $('#mAlso').classList.toggle('show', row.children.length>0);
  }
  function renderRecent(c,p){
    const row=$('#mRecentRow'); row.innerHTML='';
    getRecent().map(x=>findProd(x.cid,x.pid)).filter(Boolean)
      .filter(({c:cc,p:pp})=>!(cc.id===c.id&&pp.id===p.id))
      .slice(0,8).forEach(({c:cc,p:pp})=>row.appendChild(recCard(cc,pp)));
    $('#mRecent').classList.toggle('show', row.children.length>0);
  }

  /* ---- swipeable image gallery ---- */
  let galIdx=0, galCount=0;
  function setGal(i){ if(!galCount) return; galIdx=(i%galCount+galCount)%galCount; $('#mGalTrack').style.transform='translateX(-'+(galIdx*100)+'%)'; $('#mGalDots').querySelectorAll('i').forEach((d,k)=>d.classList.toggle('on',k===galIdx)); }
  function buildGallery(imgs){
    const gal=$('#mGal'), track=$('#mGalTrack'), dots=$('#mGalDots');
    track.innerHTML=''; dots.innerHTML=''; galIdx=0; galCount=imgs.length;
    if(!galCount){ gal.classList.remove('show','multi'); return; }
    imgs.forEach((src,k)=>{ const s=document.createElement('div'); s.className='mgal-slide'; s.style.backgroundImage=\"url('\"+src+\"')\"; track.appendChild(s);
      const dot=document.createElement('i'); if(k===0) dot.classList.add('on'); dot.addEventListener('click',()=>setGal(k)); dots.appendChild(dot); });
    track.style.transform='translateX(0)'; gal.classList.add('show'); gal.classList.toggle('multi', galCount>1);
  }
  $('#mGalPrev').addEventListener('click',()=>setGal(galIdx-1));
  $('#mGalNext').addEventListener('click',()=>setGal(galIdx+1));
  (function(){ let x0=null; const t=$('#mGalTrack'); t.addEventListener('pointerdown',e=>{x0=e.clientX;}); t.addEventListener('pointerup',e=>{ if(x0==null)return; const dx=e.clientX-x0; if(Math.abs(dx)>40) setGal(galIdx+(dx<0?1:-1)); x0=null; }); })();

  /* ---- modal ---- */
  const modal=$('#modal'); let mProduct=null,mCat=null,mVarIdx=0,mQty=1;
  function openModal(c,p){
    mProduct=p; mCat=c; mVarIdx=0; mQty=1;
    buildGallery((p.images&&p.images.length)?p.images:(p.image?[p.image]:[]));
    $('#mCat').textContent=c.name; $('#mName').textContent=p.name;
    $('#mDesc').textContent=p.description||'';
    $('#mVlabel').textContent=c.variantLabel||'Select size';
    const rEl=$('#mRating');
    if(p.rating){ $('#mStars').textContent='★★★★★'.slice(0,p.rating)+'☆☆☆☆☆'.slice(0,5-p.rating); $('#mReviews').textContent=(p.reviews?p.reviews+' review'+(p.reviews>1?'s':''):''); rEl.classList.add('show'); }
    else { rEl.classList.remove('show'); }
    $('#qVal').textContent='1';
    const w=$('#mVariants'); w.innerHTML='';
    p.variants.forEach((v,idx)=>{
      const b=document.createElement('button'); b.className='vbtn'+(idx===0?' sel':'');
      b.innerHTML='<span class="vs">'+v.size+'</span>'+(v.cups?'<span class="vc">'+v.cups+'</span>':'')+'<span class="vp">'+fmt(v.price)+'</span>';
      b.addEventListener('click',()=>{ mVarIdx=idx; w.querySelectorAll('.vbtn').forEach(x=>x.classList.remove('sel')); b.classList.add('sel'); });
      w.appendChild(b);
    });
    const setExtra=(rowId,valId,val)=>{ const row=$('#'+rowId), el=$('#'+valId); if(val){ el.textContent=val; row.classList.add('show'); } else row.classList.remove('show'); };
    setExtra('mTasteRow','mTaste',p.taste); setExtra('mIngRow','mIng',p.ingredients); setExtra('mBrewRow','mBrew',p.brew); setExtra('mPairRow','mPair',p.pairing);
    renderAlsoLike(c,p); renderRecent(c,p); pushRecent(c.id,p.id);
    modal.classList.add('open');
    const mCardEl=$('.modal-card'); if(mCardEl) mCardEl.scrollTop=0;
    requestAnimationFrame(()=>modal.style.opacity='1');
  }
  function closeModal(){ modal.style.opacity='0'; setTimeout(()=>modal.classList.remove('open'),350); }
  $('#modalClose').addEventListener('click',closeModal);
  modal.addEventListener('click',e=>{ if(e.target===modal) closeModal(); });
  document.addEventListener('keydown',e=>{ if(e.key==='Escape'){ closeModal(); closeCart(); } });
  $('#qMinus').addEventListener('click',()=>{ mQty=Math.max(1,mQty-1); $('#qVal').textContent=mQty; });
  $('#qPlus').addEventListener('click',()=>{ mQty=Math.min(99,mQty+1); $('#qVal').textContent=mQty; });

  const toast=$('#toast'); let tt;
  function showToast(h){ toast.innerHTML=h; toast.classList.add('show'); clearTimeout(tt); tt=setTimeout(()=>toast.classList.remove('show'),2600); }
  $('#addBtn').addEventListener('click',()=>{
    const v=mProduct.variants[mVarIdx];
    addToCart({ sku:v.sku||(mProduct.id+'|'+v.size), name:mProduct.name, size:v.size, price:v.price, qty:mQty });
    showToast('Added <b>'+mQty+' \\u00d7 '+mProduct.name+'</b> ('+v.size+')'); closeModal();
  });

  /* ---- cart (localStorage) ---- */
  const KEY='bb_cart_v1';
  let cart=(()=>{ try{ return JSON.parse(localStorage.getItem(KEY))||[]; }catch(e){ return []; } })();
  const save=()=>{ try{ localStorage.setItem(KEY,JSON.stringify(cart)); }catch(e){} };
  const count=()=>cart.reduce((s,i)=>s+i.qty,0);
  const total=()=>cart.reduce((s,i)=>s+i.qty*i.price,0);
  const bag=$('#bagCount');
  function addToCart(it){ const e=cart.find(i=>i.sku===it.sku); if(e) e.qty=Math.min(99,e.qty+it.qty); else cart.push(Object.assign({},it)); save(); renderCart(); bag.classList.add('pop'); setTimeout(()=>bag.classList.remove('pop'),300); }
  function setQty(sku,q){ const it=cart.find(i=>i.sku===sku); if(!it) return; it.qty=q; if(it.qty<=0) cart=cart.filter(i=>i.sku!==sku); save(); renderCart(); }
  const items=$('#cartItems'), empty=$('#cartEmpty'), foot=$('#cartFoot');
  function renderCart(){
    bag.textContent=count(); $('#cartTotal').textContent=fmt(total());
    const e=cart.length===0; empty.style.display=e?'flex':'none'; foot.style.display=e?'none':'block';
    items.innerHTML='';
    cart.forEach(i=>{
      const row=document.createElement('div'); row.className='cart-item';
      row.innerHTML='<div class="ci-main"><div class="ci-name">'+i.name+'</div>'+
        '<div class="ci-meta">'+i.size+' \\u00b7 '+fmt(i.price)+'</div>'+
        '<div class="ci-row"><div class="ci-qty"><button data-a="d">\\u2212</button><span>'+i.qty+'</span><button data-a="i">+</button></div>'+
        '<div class="ci-price">'+fmt(i.price*i.qty)+'</div></div>'+
        '<button class="ci-remove">Remove</button></div>';
      row.querySelector('[data-a="d"]').addEventListener('click',()=>setQty(i.sku,i.qty-1));
      row.querySelector('[data-a="i"]').addEventListener('click',()=>setQty(i.sku,Math.min(99,i.qty+1)));
      row.querySelector('.ci-remove').addEventListener('click',()=>setQty(i.sku,0));
      items.appendChild(row);
    });
  }
  const cartEl=$('#cart'), ov=$('#cartOverlay');
  function openCart(){ renderCart(); cartEl.classList.add('open'); ov.classList.add('open'); }
  function closeCart(){ cartEl.classList.remove('open'); ov.classList.remove('open'); }
  $('#bagBtn').addEventListener('click',openCart);
  $('#cartClose').addEventListener('click',closeCart);
  ov.addEventListener('click',closeCart);
  $('#checkoutBtn').addEventListener('click',()=>showToast('Checkout is a demo \\u2014 <b>'+count()+'</b> item(s), '+fmt(total())));
  $('#shopLink').addEventListener('click',()=>$('#products').scrollIntoView({behavior:'smooth'}));
  $('#nlForm').addEventListener('submit',e=>{ e.preventDefault(); const v=$('#nlEmail').value.trim(); if(v){ showToast('Welcome to the <b>Tea Club</b> \\u2014 check your inbox.'); $('#nlEmail').value=''; } });
  const rvTrack=$('#rvTrack'); if(rvTrack) rvTrack.innerHTML += rvTrack.innerHTML;
  document.querySelectorAll('#faq .faq-item').forEach((item)=>{
    const q=item.querySelector('.faq-q'), a=item.querySelector('.faq-a');
    q.addEventListener('click',()=>{
      const isOpen=item.classList.contains('open');
      document.querySelectorAll('#faq .faq-item.open').forEach((o)=>{ if(o!==item){ o.classList.remove('open'); o.querySelector('.faq-a').style.maxHeight=null; } });
      if(isOpen){ item.classList.remove('open'); a.style.maxHeight=null; }
      else { item.classList.add('open'); a.style.maxHeight=a.scrollHeight+'px'; }
    });
  });
  const contactForm=$('#contactForm'); if(contactForm) contactForm.addEventListener('submit',(e)=>{ e.preventDefault(); showToast('Thanks for your message \\u2014 we\\'ll be in touch soon.'); contactForm.reset(); });
  const wholesaleForm=$('#wholesaleForm'); if(wholesaleForm) wholesaleForm.addEventListener('submit',(e)=>{ e.preventDefault(); showToast('Thanks for your wholesale enquiry \\u2014 we\\'ll be in touch soon.'); wholesaleForm.reset(); });
  const referBtn=$('#referBtn'); if(referBtn) referBtn.addEventListener('click',()=>showToast('Referral is a demo \\u2014 share your <b>£5</b> link.'));
  const storyVisit=$('#storyVisit'); if(storyVisit) storyVisit.addEventListener('click',()=>$('#visit').scrollIntoView({behavior:'smooth'}));
  const bookForm=$('#bookForm'); if(bookForm) bookForm.addEventListener('submit',(e)=>{ e.preventDefault(); showToast('Booking enquiry sent \\u2014 we\\'ll confirm by <b>email</b>.'); bookForm.reset(); });

  const promoModal=$('#promoModal');
  if(promoModal){
    const SEEN='bb_promo_seen_v1';
    const openPromo=()=>{ promoModal.classList.add('open'); requestAnimationFrame(()=>promoModal.style.opacity='1'); };
    const closePromo=()=>{ promoModal.style.opacity='0'; setTimeout(()=>promoModal.classList.remove('open'),500); try{ localStorage.setItem(SEEN,'1'); }catch(e){} };
    let seen=false; try{ seen=localStorage.getItem(SEEN)==='1'; }catch(e){}
    if(!seen) setTimeout(openPromo,1400);
    $('#pmClose').addEventListener('click',closePromo);
    promoModal.addEventListener('click',(e)=>{ if(e.target===promoModal) closePromo(); });
    document.addEventListener('keydown',(e)=>{ if(e.key==='Escape'&&promoModal.classList.contains('open')) closePromo(); });
    $('#pmForm').addEventListener('submit',(e)=>{ e.preventDefault(); closePromo(); showToast('Welcome to the <b>Tea Club</b> \\u2014 your <b>20% off</b> code is on its way.'); });
  }

  /* promo banner */
  document.body.classList.add('promo-on');
  $('#promoX').addEventListener('click',()=>{ document.body.classList.remove('promo-on'); $('#promo').style.display='none'; });
  (function(){ const el=$('#promoMsg'); if(!el) return; const msgs=["Hello! Is it tea you're looking for?","Free Delivery on all orders over &pound;30","<b>20% off</b> when you subscribe to the mail list"]; let i=0; setInterval(()=>{ el.style.opacity='0'; setTimeout(()=>{ i=(i+1)%msgs.length; el.innerHTML=msgs[i]; el.style.opacity='1'; },400); },4200); })();
  const favShop=$('#favShop'); if(favShop) favShop.addEventListener('click',()=>{ backToCats(); $('#products').scrollIntoView({behavior:'smooth'}); });
  const brandLogo=$('#brandLogo'); if(brandLogo) brandLogo.addEventListener('click',(e)=>{ e.preventDefault(); window.scrollTo({top:0,behavior:'smooth'}); });

  /* nav drawer */
  const nav=$('#nav'), navOv=$('#navOverlay');
  function openNav(){ nav.classList.add('open'); navOv.classList.add('open'); }
  function closeNav(){ nav.classList.remove('open'); navOv.classList.remove('open'); }
  $('#menuBtn').addEventListener('click',openNav);
  $('#navClose').addEventListener('click',closeNav);
  navOv.addEventListener('click',closeNav);
  const MENU_OVERLAYS={ cafemenu:1, kidsmenu:1 };
  function openMenuOverlay(id){ const el=document.getElementById(id); if(!el) return; el.classList.add('open'); el.scrollTop=0; document.body.style.overflow='hidden'; }
  function closeMenuOverlay(id){ const el=document.getElementById(id); if(el) el.classList.remove('open'); document.body.style.overflow=''; }
  document.querySelectorAll('[data-close]').forEach(b=>b.addEventListener('click',()=>closeMenuOverlay(b.getAttribute('data-close'))));
  function goTo(go){
    if(go==='products'){ backToCats(); $('#products').scrollIntoView({behavior:'smooth'}); }
    else if(MENU_OVERLAYS[go]){ openMenuOverlay(go); }
    else if(CAT[go]){ $('#products').scrollIntoView({behavior:'smooth'}); setTimeout(()=>openCategory(go),420); }
    else { const el=document.getElementById(go); if(el) el.scrollIntoView({behavior:'smooth'}); else { backToCats(); $('#products').scrollIntoView({behavior:'smooth'}); } }
  }
  document.querySelectorAll('[data-go]').forEach(a=>{
    a.addEventListener('click',()=>{ closeNav(); goTo(a.getAttribute('data-go')); });
  });
  const navLogin=$('#navLogin'); if(navLogin) navLogin.addEventListener('click',()=>{ closeNav(); showToast('Accounts are a demo \\u2014 sign-in coming soon.'); });

  /* horizontal mega-menu (wide screens) */
  const megaItems=Array.from(document.querySelectorAll('.megabar .mega-item'));
  function closeMega(){ megaItems.forEach(i=>i.classList.remove('open')); }
  megaItems.forEach(item=>{
    const trig=item.querySelector('.mega-trig');
    trig.addEventListener('click',(e)=>{ e.stopPropagation(); const wasOpen=item.classList.contains('open'); closeMega(); if(!wasOpen) item.classList.add('open'); });
    item.querySelectorAll('[data-go]').forEach(a=>a.addEventListener('click',()=>{ closeMega(); if(document.activeElement) document.activeElement.blur(); }));
  });
  document.addEventListener('click',(e)=>{ if(!e.target.closest('.mega-item')) closeMega(); });
  document.addEventListener('keydown',e=>{ if(e.key==='Escape'){ closeNav(); closeMega(); closeMenuOverlay('cafemenu'); closeMenuOverlay('kidsmenu'); } });

  /* hero: scroll-scrub the whole clip across ~3 viewport scrolls */
  (function(){
    const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
    const ramp=(p,a,b)=>clamp((p-a)/(b-a),0,1);
    const band=(p,a,b,c,d)=>Math.min(ramp(p,a,b),1-ramp(p,c,d));
    const hero=$('#hero'), v=$('#heroVideo'), center=$('#sticky .hero-center');
    const hl1=$('#heroLine1'), hl2=$('#heroLine2');
    const reveal=(el,val)=>{ if(!el) return; el.style.opacity=val.toFixed(3); el.firstElementChild.style.transform='translateY('+((1-val)*26).toFixed(1)+'px)'; };
    if(!hero||!v) return;
    let dur=0, targetT=0, curT=0, primed=false;
    v.muted=true; v.playsInline=true; v.setAttribute('webkit-playsinline','');
    v.addEventListener('loadedmetadata',()=>{ dur=v.duration||0; });
    const prime=()=>{ if(primed) return; primed=true; const pr=v.play(); if(pr&&pr.then) pr.then(()=>v.pause()).catch(()=>{}); else { try{v.pause();}catch(e){} } };
    v.addEventListener('canplay',prime);
    window.addEventListener('touchstart',prime,{once:true,passive:true});
    window.addEventListener('wheel',prime,{once:true,passive:true});
    v.load();
    function prog(){ const t=hero.offsetHeight-window.innerHeight; return t<=0?0:clamp(-hero.getBoundingClientRect().top/t,0,1); }
    function onScroll(){ const p=prog(); const d=dur||v.duration||0; targetT=p*Math.max(0,d-0.05); if(center) center.style.opacity=(1-ramp(p,0.04,0.32)).toFixed(3); reveal(hl1,band(p,0.34,0.45,0.55,0.64)); reveal(hl2,band(p,0.66,0.77,0.88,0.97)); }
    function loop(){ curT+=(targetT-curT)*0.22; if(Math.abs(targetT-curT)<0.008) curT=targetT; if((dur||v.duration)&&Math.abs(v.currentTime-curT)>0.02){ try{v.currentTime=curT;}catch(e){} } requestAnimationFrame(loop); }
    requestAnimationFrame(loop);
    window.addEventListener('scroll',onScroll,{passive:true});
    window.addEventListener('resize',onScroll);
    onScroll();
  })();

  buildCategories(); buildFavourites(); renderCart();
})();
"""
JS = JS.replace("__STORE__", store_json)

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>BISCUIT &amp; BREW</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Inter:wght@300;400;500&display=swap" rel="stylesheet" />
<style>
__CSS__
__HEROCSS__
</style>
</head>
<body>
<div id="promo">
  <span id="promoMsg">Hello! Is it tea you're looking for?</span>
  <button class="promo-x" id="promoX" aria-label="Dismiss">&times;</button>
</div>

<header>
  <div class="hleft">
    <button class="menu-btn" id="menuBtn"><span class="bars"><i></i><i></i><i></i></span> MENU</button>
    <nav class="megabar" aria-label="Primary">
      <div class="mega-item">
        <button class="mega-trig">Shop <span class="car">&#9660;</span></button>
        <div class="mega-panel">
          <div class="mega-col">
            <div class="mega-h">Tea</div>
            <a data-go="products">All Tea</a>
            <a data-go="favourites">Best Sellers</a>
            <a data-go="black">Black Tea</a>
            <a data-go="matcha">Matcha</a>
            <a data-go="green">Green Tea</a>
            <a data-go="herbal">Fruit Infusions</a>
            <a data-go="rooibos">Rooibos</a>
          </div>
          <div class="mega-col">
            <div class="mega-h">Gifts &amp; More</div>
            <a data-go="vouchers">Gifts &amp; Bundles</a>
            <a data-go="starter-kits">Starter Kits</a>
            <a data-go="accessories">Accessories</a>
            <a data-go="vouchers">Gift Vouchers</a>
          </div>
        </div>
      </div>
      <div class="mega-item">
        <button class="mega-trig">Cafe &amp; Lounge <span class="car">&#9660;</span></button>
        <div class="mega-panel">
          <div class="mega-col">
            <div class="mega-h">Cafe &amp; Lounge</div>
            <a data-go="book">Book A Table</a>
            <a data-go="cafemenu">Menu</a>
            <a data-go="kidsmenu">Kids Menu</a>
            <a data-go="visit">Visit Us</a>
            <a data-go="vouchers">Gift Vouchers</a>
          </div>
          <div class="mega-col">
            <div class="mega-h">Experiences</div>
            <a data-go="book">Afternoon Tea</a>
            <a data-go="book">Tea Tasting</a>
            <a data-go="book">Cream Tea</a>
          </div>
          <div class="mega-col">
            <div class="mega-h">Events</div>
            <a data-go="book">Summer Paint &amp; Brew</a>
            <a data-go="book">A Court of Thorns and Roses Book Club</a>
          </div>
        </div>
      </div>
      <div class="mega-item">
        <button class="mega-trig">About Us <span class="car">&#9660;</span></button>
        <div class="mega-panel">
          <div class="mega-col">
            <div class="mega-h">About Us</div>
            <a data-go="story">Our Story</a>
            <a data-go="visit">Visit Us</a>
            <a data-go="reviews">Reviews</a>
            <a data-go="instagram">Find Us On Instagram</a>
            <a data-go="faq">FAQ</a>
            <a data-go="contact">Contact Us</a>
            <a data-go="refer">Refer a Friend</a>
          </div>
        </div>
      </div>
    </nav>
  </div>
  <div class="hnav">
    <button class="shop" id="shopLink">SHOP</button>
    <button class="shop bag" id="bagBtn">BAG <span id="bagCount" class="bag-count">0</span></button>
  </div>
</header>

<div id="navOverlay"></div>
<nav id="nav" aria-label="Main menu">
  <div class="nav-head">
    <button class="nav-close" id="navClose">&times;</button>
    <span class="brand-logo"><img src="images/logo-mark.png" alt="Biscuit &amp; Brew" /></span>
    <span style="width:24px"></span>
  </div>
  <div class="nav-body nav-flat">
    <a data-go="products">All Tea</a>
    <a data-go="favourites">Best Sellers</a>
    <a data-go="black">Black Tea</a>
    <a data-go="matcha">Matcha</a>
    <a data-go="green">Green Tea</a>
    <a data-go="herbal">Fruit Infusions</a>
    <a data-go="rooibos">Rooibos</a>
    <a data-go="black">Chai</a>
    <a data-go="green">White Tea</a>
    <a data-go="rooibos">Caffeine Free</a>
    <a data-go="products">Music Blends</a>
    <a data-go="cafemenu">Cafe &amp; Lounge Menu</a>
    <a data-go="kidsmenu">Kids Menu</a>
  </div>
  <div class="nav-foot">
    <a class="nav-login" id="navLogin">&#9711;&nbsp; Log In</a>
  </div>
</nav>

<section id="hero">
  <a class="hero-logo" id="brandLogo" href="#" aria-label="Biscuit &amp; Brew — home"><img src="images/logo-mark.png" alt="Biscuit &amp; Brew" /></a>
  <div id="sticky">
    <video id="heroVideo" src="videos/hero.mp4" muted playsinline preload="auto" poster="images/hero-poster.jpg"></video>
    <div class="hero-veil"></div>
    <div class="hero-center">
      <div class="hero-title">BISCUIT &amp; BREW</div>
      <div class="hero-tag">Rooted in the hills</div>
    </div>
    <div class="hero-line left" id="heroLine1"><div class="hl-in"><span>An Everyday Brew, <em>But Better</em></span><span class="hl-rule"></span></div></div>
    <div class="hero-line right" id="heroLine2"><div class="hl-in"><span>Cosy Cafe &amp; <em>The Hidden Lounge</em></span><span class="hl-rule"></span></div></div>
    <div class="scroll-hint">Scroll to explore</div>
  </div>
</section>

<section id="products">
  <div class="sec-head">
    <div class="sec-eyebrow">The Collection</div>
    <h2 class="sec-title">Choose your ritual</h2>
    <p class="sec-sub">Small-batch loose leaf, blended in the British hills.</p>
  </div>
  <div class="view active" id="catView"><div class="cat-grid" id="catGrid"></div></div>
  <div class="view" id="detailView">
    <div class="detail-top">
      <button class="back-btn" id="backBtn">&larr;&nbsp; Back to categories</button>
      <div class="detail-title" id="detailTitle"></div>
    </div>
    <div class="prod-grid" id="prodGrid"></div>
  </div>
</section>

<section id="cafemenu">
  <button class="menu-overlay-close" data-close="cafemenu" aria-label="Close menu">&times;</button>
  <div class="sec-head">
    <div class="sec-eyebrow">Cafe &amp; Lounge</div>
    <h2 class="sec-title">The Menu</h2>
    <p class="sec-sub">Served in our Nottingham tea house. Loose leaf tea brewed in a Japanese cast iron teapot.</p>
  </div>
  <div class="cm-grid">
    <div class="cm-group">
      <h3>Tea</h3>
      <div class="cm-note">Loose leaf, brewed in a cast iron teapot</div>
      <div class="cm-row"><span class="cm-name">Our Blends &mdash; Pot For One</span><span class="cm-dots"></span><span class="cm-price">£4.25</span></div>
      <div class="cm-row"><span class="cm-name">Our Blends &mdash; 65g Tea Pack</span><span class="cm-dots"></span><span class="cm-price">£6.95</span></div>
      <div class="cm-row"><span class="cm-name">Traditional Brews &mdash; Pot For One</span><span class="cm-dots"></span><span class="cm-price">£4.10</span></div>
      <div class="cm-row"><span class="cm-name">Traditional Brews &mdash; 65g Tea Pack</span><span class="cm-dots"></span><span class="cm-price">£5.95</span></div>
      <p class="cm-sub">English Breakfast &middot; Decaf Black &middot; Earl Grey &middot; Assam &middot; Darjeeling &middot; Ceylon &middot; Jasmine Green &middot; Black Dragon Oolong &middot; Chun Mee Green &middot; Rooibos &middot; Pure Peppermint &middot; Lapsang Souchong &middot; Lavender Flower</p>
    </div>
    <div class="cm-group">
      <h3>Coffee</h3>
      <div class="cm-note">Rich, smooth dark roast &middot; poured over ice +50p</div>
      <div class="cm-row"><span class="cm-name">Americano</span><span class="cm-dots"></span><span class="cm-price">£3.70</span></div>
      <div class="cm-row"><span class="cm-name">Cappuccino</span><span class="cm-dots"></span><span class="cm-price">£3.95</span></div>
      <div class="cm-row"><span class="cm-name">Latte</span><span class="cm-dots"></span><span class="cm-price">£3.95</span></div>
      <div class="cm-row"><span class="cm-name">Flat White</span><span class="cm-dots"></span><span class="cm-price">£3.85</span></div>
      <div class="cm-row"><span class="cm-name">Double Espresso</span><span class="cm-dots"></span><span class="cm-price">£2.95</span></div>
      <div class="cm-row"><span class="cm-name">Mocha / White Mocha</span><span class="cm-dots"></span><span class="cm-price">£4.45</span></div>
      <div class="cm-row"><span class="cm-name">Affogato</span><span class="cm-dots"></span><span class="cm-price">£4.45</span></div>
      <div class="cm-row"><span class="cm-name">250g Beans</span><span class="cm-dots"></span><span class="cm-price">£10.95</span></div>
      <p class="cm-sub">Upgrades: oat milk +50p &middot; over ice +50p &middot; extra shot +£1.45 &middot; flavouring syrups +50p (hazelnut, vanilla, caramel, salted caramel, Biscoff, cinnamon)</p>
    </div>
    <div class="cm-group">
      <h3>Chai</h3>
      <div class="cm-note">Served hot or poured over ice +50p</div>
      <div class="cm-row"><span class="cm-name">Chai Latte</span><span class="cm-dots"></span><span class="cm-price">£3.95</span></div>
      <div class="cm-row"><span class="cm-name">Dirty Chai</span><span class="cm-dots"></span><span class="cm-price">£5.25</span></div>
      <h3 style="margin-top:26px">Iced Brews</h3>
      <div class="cm-row"><span class="cm-name">Strawberry Fields Forever</span><span class="cm-dots"></span><span class="cm-price">£4.95</span></div>
      <div class="cm-row"><span class="cm-name">Cherry Kiss</span><span class="cm-dots"></span><span class="cm-price">£4.95</span></div>
    </div>
    <div class="cm-group">
      <h3>Matcha</h3>
      <div class="cm-note">Japanese ceremonial-grade green tea</div>
      <div class="cm-row"><span class="cm-name">Matcha Latte</span><span class="cm-dots"></span><span class="cm-price">£4.25</span></div>
      <div class="cm-row"><span class="cm-name">Iced Matcha Latte</span><span class="cm-dots"></span><span class="cm-price">£4.75</span></div>
      <div class="cm-row"><span class="cm-name">Matchagato</span><span class="cm-dots"></span><span class="cm-price">£4.45</span></div>
      <div class="cm-row"><span class="cm-name">Biscuit Brew Matcha</span><span class="cm-dots"></span><span class="cm-price">£5.45</span></div>
      <div class="cm-row"><span class="cm-name">30g Pack</span><span class="cm-dots"></span><span class="cm-price">£17.95</span></div>
    </div>
    <div class="cm-group">
      <h3>Hot Chocolate</h3>
      <div class="cm-note">Add flavouring syrups +50p</div>
      <div class="cm-row"><span class="cm-name">Belgian Hot Chocolate</span><span class="cm-dots"></span><span class="cm-price">£4.25</span></div>
      <div class="cm-row"><span class="cm-name">Italian White Hot Chocolate</span><span class="cm-dots"></span><span class="cm-price">£4.25</span></div>
      <div class="cm-row"><span class="cm-name">Luxury Hot Choc</span><span class="cm-dots"></span><span class="cm-price">£5.20</span></div>
    </div>
    <div class="cm-group">
      <h3>Cold Drinks</h3>
      <div class="cm-note">Chilled &amp; refreshing</div>
      <div class="cm-row"><span class="cm-name">Soft Drinks</span><span class="cm-dots"></span><span class="cm-price">£4.75</span></div>
      <p class="cm-sub">Cloudy Lemonade &middot; Dandelion &amp; Burdock &middot; Orange Juice &middot; Apple Juice</p>
    </div>
  </div>

  <div class="cm-divider">
    <span class="l"></span><h3>Our Loose Leaf Blends</h3><span class="l"></span>
    <p>We're loose leaf tea specialists and have been blending our own unique tea blends for nearly a decade. Blends marked <span class="cm-caff">*</span> contain caffeine.</p>
  </div>
  <div class="cm-grid">
    <div class="cm-group">
      <h3>Black Tea <span class="cm-caff">*</span></h3>
      <div class="cm-blend"><span class="bn">Biscuit Brew</span><p class="bd">Our signature chocolate digestive blend. Rich and malty with chocolate and oats.</p></div>
      <div class="cm-blend"><span class="bn">James &amp; The Giant Peach</span><p class="bd">Peach, ginger and cardamom. Based on the book by Roald Dahl. Sweet zesty fruits with subtle spice.</p></div>
      <div class="cm-blend"><span class="bn">Banana Fudge</span><p class="bd">Creamy banana flavoured, bold but fruity.</p></div>
      <div class="cm-blend"><span class="bn">Salted Caramel</span><p class="bd">Salted and caramelised. Robust with a warm, dark sweetness.</p></div>
      <div class="cm-blend"><span class="bn">Caramel Apple Betty</span><p class="bd">Spiced cinnamon apple pie. Rich and creamy with subtle fruity notes and aromatic undertones.</p></div>
      <div class="cm-blend"><span class="bn">Cherry Bakewell</span><p class="bd">A cherry amaretto blend. Rich and tangy with nutty tones.</p></div>
      <div class="cm-blend"><span class="bn">Mango T'Chai</span><p class="bd">Mango and coconut chai, pronounced with a soft T. Light and fruity with warming aromatic undertones.</p></div>
      <div class="cm-blend"><span class="bn">Moonbeam</span><p class="bd">Lavender flower and orange peel. Bright with floral undertones.</p></div>
    </div>
    <div class="cm-group">
      <h3>Fruit Infusions</h3>
      <div class="cm-blend"><span class="bn">Cherry Kiss</span><p class="bd">Cherry Cola flavoured fruit infusion. Fruity and aromatic.</p></div>
      <div class="cm-blend"><span class="bn">Little Picture</span><p class="bd">Zesty lime, mango, papaya and pineapple. Blended to 'Little Picture' by Arthur Dove. Citrussy tropical fruits.</p></div>
      <div class="cm-blend"><span class="bn">Hound on the Hunt <span class="cm-caff">*</span></span><p class="bd">Sweet, smokey and chilli flavoured bonfire blend. Smokey but sweet with a hot chilli kick.</p></div>
      <div class="cm-blend"><span class="bn">Strawberry Fields Forever</span><p class="bd">Zesty lime and lemon with strawberries. Blended to the music of The Beatles. Tastes a bit like a Twister lolly.</p></div>
      <div class="cm-blend"><span class="bn">Raspberry Rose <span class="cm-caff">*</span></span><p class="bd">Inspired by our wedding cake. Tart, floral and fruity.</p></div>
    </div>
    <div class="cm-group">
      <h3>Rooibos</h3>
      <div class="cm-blend"><span class="bn">Plum Tart</span><p class="bd">A springtime, fruity little tart. We use elderberries to make it plum-y with a bit of cinnamon.</p></div>
      <div class="cm-blend"><span class="bn">French Toast <span class="cm-caff">*</span></span><p class="bd">Tastes like spiced-vanilla toast.</p></div>
      <div class="cm-blend"><span class="bn">Jaffa Cake</span><p class="bd">Marmalade &amp; chocolate. Rich and creamy with fruit tones.</p></div>
      <div class="cm-blend"><span class="bn">Battenburg</span><p class="bd">Apricot jam &amp; marzipan flavoured rooibos. Cakey with fruity and nutty tones.</p></div>
    </div>
    <div class="cm-group">
      <h3>Green Tea <span class="cm-caff">*</span></h3>
      <div class="cm-blend"><span class="bn">Robin Hood</span><p class="bd">Inspired by the folklore legend, made with fruits and flowers from the forests of Nottingham. Tastes of elderberry, dandelion &amp; blackberries.</p></div>
      <div class="cm-blend"><span class="bn">Lull</span><p class="bd">Blueberry, almond &amp; cinnamon purple tea. Fruity and subtly spiced.</p></div>
      <div class="cm-blend"><span class="bn">Watermelon Sugar</span><p class="bd">Watermelon, lychee &amp; passionfruit. Blended to the music of Harry Styles. Soft, fruity with a slight tang.</p></div>
      <div class="cm-blend"><span class="bn">Pear &amp; Pistachio</span><p class="bd">Tastes as it sounds. One of the blends we made for our wedding. Fruity, earthy and nutty.</p></div>
      <div class="cm-blend"><span class="bn">Deep Breath</span><p class="bd">Cool, clarifying eucalyptus and peppermint with a greeny, blue hue.</p></div>
    </div>
  </div>

  <div class="kids-free" style="margin-top:48px">
    <b>Take the Biscuit &amp; Brew experience home</b>
    <p class="cm-sub" style="margin-top:10px">We make every loose leaf blend in house. Take a pack home, put the kettle on and fill your teapot. All blends available at the counter:</p>
    <p class="cm-sub" style="margin-top:8px;color:rgba(255,255,255,0.62)">65g Loose Leaf Tea from £6.95 &nbsp;&middot;&nbsp; Bucket Brewer Tea Infuser £8.50 &nbsp;&middot;&nbsp; Cast Iron Teapot £25</p>
  </div>
</section>

<section id="kidsmenu" style="background:#0a0a14">
  <button class="menu-overlay-close" data-close="kidsmenu" aria-label="Close menu">&times;</button>
  <div class="sec-head">
    <div class="sec-eyebrow">For the little ones</div>
    <h2 class="sec-title">Kids Menu</h2>
    <p class="sec-sub">Breakfast &amp; brunch served all day.</p>
  </div>
  <div class="cm-grid">
    <div class="cm-group">
      <h3>Cold Drinks</h3>
      <div class="cm-row"><span class="cm-name">Strawberry Fields</span><span class="cm-dots"></span><span class="cm-price">£4.50</span></div>
      <div class="cm-row"><span class="cm-name">Cherry Cola Bottle</span><span class="cm-dots"></span><span class="cm-price">£4.50</span></div>
      <div class="cm-row"><span class="cm-name">Soft Drinks</span><span class="cm-dots"></span><span class="cm-price">£4.50</span></div>
      <p class="cm-sub">Strawberry, lemon &amp; lime &middot; cherry cola &middot; Orange Juice &middot; Apple Juice</p>
    </div>
    <div class="cm-group">
      <h3>Breakfast &amp; Brunch</h3>
      <div class="cm-note">Served all day</div>
      <div class="cm-row"><span class="cm-name">Toast (v)</span><span class="cm-dots"></span><span class="cm-price">£2.25</span></div>
      <div class="cm-row"><span class="cm-name">Eggs on Toast (v)</span><span class="cm-dots"></span><span class="cm-price">£4.95</span></div>
      <div class="cm-row"><span class="cm-name">Mini English (v)</span><span class="cm-dots"></span><span class="cm-price">£5.95</span></div>
      <p class="cm-sub">Toast: add jam or chocolate spread +50p &middot; add beans +£1.50</p>
    </div>
    <div class="cm-group">
      <h3>Sandwiches</h3>
      <div class="cm-note">On white bread with fruit on the side &middot; toast it +50p</div>
      <div class="cm-row"><span class="cm-name">Ham</span><span class="cm-dots"></span><span class="cm-price">£4.95</span></div>
      <div class="cm-row"><span class="cm-name">Cheese</span><span class="cm-dots"></span><span class="cm-price">£4.95</span></div>
      <div class="cm-row"><span class="cm-name">Jam</span><span class="cm-dots"></span><span class="cm-price">£4.50</span></div>
    </div>
    <div class="cm-group">
      <h3>Little Hot Chocolate</h3>
      <div class="cm-note">Add flavouring syrups +50p</div>
      <div class="cm-row"><span class="cm-name">Belgian Hot Chocolate</span><span class="cm-dots"></span><span class="cm-price">£2.95</span></div>
      <div class="cm-row"><span class="cm-name">Italian White Hot Chocolate</span><span class="cm-dots"></span><span class="cm-price">£2.95</span></div>
      <div class="cm-row"><span class="cm-name">Luxury Hot Choc</span><span class="cm-dots"></span><span class="cm-price">£3.95</span></div>
    </div>
    <div class="cm-group">
      <h3>Desserts</h3>
      <div class="cm-row"><span class="cm-name">Ice Cream &mdash; one scoop</span><span class="cm-dots"></span><span class="cm-price">£1.50</span></div>
      <div class="cm-row"><span class="cm-name">Ice Cream &mdash; two scoops</span><span class="cm-dots"></span><span class="cm-price">£2.75</span></div>
      <div class="cm-row"><span class="cm-name">Mini Chocolate Brownie</span><span class="cm-dots"></span><span class="cm-price">£3.95</span></div>
      <p class="cm-sub">Madagascan vanilla ice cream &middot; brownie served warm with a scoop</p>
    </div>
  </div>
  <div class="kids-free">
    <b>KIDS EAT FREE</b> with adults eating a main meal
    <span>Choose any cold drink &amp; a breakfast or sandwich. Desserts and hot chocolates not included.</span>
  </div>
</section>

<section id="book">
  <div class="book-banner"><img src="images/book-afternoon-tea.jpg" alt="Afternoon tea at Biscuit &amp; Brew" /></div>
  <div class="sec-head">
    <div class="sec-eyebrow">Book A Table</div>
    <h2 class="sec-title">Book Your Experience</h2>
    <p class="sec-sub">Select your experience and preferred date to submit a booking enquiry.</p>
  </div>
  <div class="book-grid">
    <form class="book-form" id="bookForm">
      <div class="bf-row">
        <label for="bkExp">Choose your experience</label>
        <select id="bkExp" required>
          <option value="">Select an experience</option>
          <option>Afternoon Tea Experience</option>
          <option>Cream Tea Experience</option>
          <option>Tea Tasting Event</option>
          <option>Table Reservation</option>
        </select>
      </div>
      <div class="bf-two">
        <div class="bf-row"><label for="bkDate">Preferred date</label><input type="date" id="bkDate" required /></div>
        <div class="bf-row"><label for="bkTime">Preferred time</label><input type="time" id="bkTime" required /></div>
      </div>
      <div class="bf-row">
        <label for="bkGuests">Number of guests</label>
        <select id="bkGuests">
          <option>1 guest</option><option selected>2 guests</option><option>3 guests</option>
          <option>4 guests</option><option>5 guests</option><option>6 guests</option>
          <option>7 guests</option><option>8+ guests</option>
        </select>
      </div>
      <div class="bf-two">
        <div class="bf-row"><label for="bkName">Full name</label><input type="text" id="bkName" placeholder="Your name" required /></div>
        <div class="bf-row"><label for="bkEmail">Email</label><input type="email" id="bkEmail" placeholder="your@email.com" required /></div>
      </div>
      <div class="bf-row"><label for="bkPhone">Phone</label><input type="tel" id="bkPhone" placeholder="07xxx xxxxxx" /></div>
      <div class="bf-row">
        <label for="bkReq">Special requests or dietary requirements</label>
        <textarea id="bkReq" placeholder="Let us know about any allergies, dietary requirements, or special occasions…"></textarea>
      </div>
      <button type="submit" class="book-submit">Submit Booking Request</button>
      <p class="book-note">This is a booking enquiry. We'll confirm availability and send payment details via email.</p>
    </form>
    <aside class="book-aside">
      <div class="ba-block">
        <h3>Our Opening Hours</h3>
        <div class="hours-row"><span>Monday</span><span>9:00 &ndash; 5:00</span></div>
        <div class="hours-row"><span>Tuesday</span><span>9:00 &ndash; 5:00</span></div>
        <div class="hours-row"><span>Wednesday</span><span>9:00 &ndash; 5:00</span></div>
        <div class="hours-row"><span>Thursday</span><span>9:00 &ndash; 5:00</span></div>
        <div class="hours-row"><span>Friday</span><span>9:00 &ndash; 5:00</span></div>
        <div class="hours-row"><span>Saturday</span><span>9:30 &ndash; 5:00</span></div>
        <div class="hours-row"><span>Sunday</span><span>10:00 &ndash; 4:30</span></div>
      </div>
      <div class="ba-block">
        <h3>How To Find Us</h3>
        <p>5 Victoria Street<br/>Nottingham NG1 2EW</p>
        <a class="maps-btn" href="https://www.google.com/maps/search/?api=1&query=Biscuit%20%26%20Brew%205%20Victoria%20Street%20Nottingham%20NG1%202EW" target="_blank" rel="noopener">Open in Google Maps →</a>
      </div>
    </aside>
  </div>
</section>

<section id="story">
  <div class="story-wrap">
    <img class="story-portrait" src="images/story-owners.png" alt="Dee and Darren, owners of Biscuit &amp; Brew" />
    <div class="story-eyebrow">Our Story</div>
    <h2 class="story-title">Come in, get comfy</h2>
    <p>Hi! We're Dee and Darren, the owners of Biscuit and Brew. Welcome to our teahouse!</p>
    <p>We'd like to tell you a bit about who we are, how we got started, and what we aim to deliver for our customers.</p>
    <p>We established Biscuit and Brew in 2019, initially as something of a side hustle. We were both working in creative jobs &mdash; Darren as a musician and Dee as a dance teacher &mdash; when we started crafting tea blends inspired by Darren's music. We'd never encountered a music-inspired tea before, and pairing each song with its own tea felt like a fun way to make the music more memorable for people.</p>
    <p>We quickly got hooked on experimenting with new blends, and over the next couple of years we crafted flavours inspired by sweets, desserts and cocktails; books and music; different moods and different times of day. We even made a tea that tastes like our wedding cake.</p>
    <p>At this point we never thought we'd end up opening a tea house! But, when we started selling tea to our friends and inviting them over for tasting sessions called "biscuit and brews," we had an inkling this could be more than just a hobby. It was tough to find creative work after lockdown, and Darren was rejected from a job he really thought he would get. 24 hours later we were in Nottingham visiting what would become our first cafe on Hounds Gate. It really was that spontaneous!</p>
    <p>So, that's the story of Biscuit and Brew! But what can you expect if you come to visit us?</p>
    <p>We started out by having our friends over for cosy cups of tea, and really the goal hasn't changed. We want you to feel as though you've been welcomed into our home. This is why we focus on making your visit feel as personal as possible: our scones and cakes are freshly baked in-house, and we craft all the different tea flavours ourselves. We even use the same cast-iron Japanese teapots we have at home (because we think they're the best!)</p>
    <p>Giving friendly, attentive, and knowledgeable service is also super important to us. Greeting customers at the door and serving them at the table might have gone a little out of fashion, but we think it's the best way to make people feel special. We've noticed over the years that memorable dining experiences are often defined by great service &mdash; you're just as likely to remember a friendly waiter or waitress as a delicious meal. So, when you come to the tea house, you'll be welcomed warmly, invited in, and hosted properly: like you're visiting a friend.</p>
    <div class="story-images">
      <img src="images/story-1.jpg" alt="Enjoying a pot of tea at Biscuit &amp; Brew" />
      <img src="images/story-2.jpg" alt="Table service at Biscuit &amp; Brew" />
    </div>
    <p>Focussing on service also helps us to fulfil our role as tea experts, here to help you navigate the (sometimes overwhelming!) world of loose leaf. After all, there are so many different blends, it's not always clear how much tea to brew, how long to brew it for, whether it has caffeine in it, and so on. Our goal is to show that brewing a cup of tea shouldn't feel so complicated! When you visit us, we'll guide you through the process and answer any queries you might have. We keep scent bottles on our front counter so you can smell a blend before you try it, and our refillable afternoon teas are a great way to explore all the flavours on our menu. We're eager to tell the stories of our teas, so no question is too small to ask.</p>
    <p>While there's nothing wrong with sticking to what you know, we've also tried to challenge you a bit with our menu. You'll never blow someone's mind by giving them something they expect! Darren once had a burger with a donut on it, and it was so unexpectedly enjoyable that it stuck with him ever since. Our goal is to recreate that experience for you. Tea that tastes like Battenburg cake, banana bread with bacon and mascarpone on it, an eggy-bread toastie glazed with honey: all these experiments are designed to give you something you didn't know you needed. Don't worry though, if dippy eggs and English Breakfast is more your thing, we've got you. We still appreciate the classics.</p>
    <p>In short, we want you to feel welcomed and looked after, but also (if you fancy it!) encouraged to venture out of your comfort zone to try some new flavours. If we can make you feel at home and provide you with a memorable experience, we're doing our jobs properly!</p>
    <p>Thanks for visiting us, and we hope to see you soon.</p>
    <div class="story-sign">Dee &amp; Darren</div>
    <button class="story-cta" id="storyVisit">Visit Us</button>
  </div>
</section>

<section id="favourites">
  <div class="sec-head" style="margin-bottom:0">
    <div class="sec-eyebrow">Personal Favourites</div>
    <h2 class="sec-title">Our Personal Favourites</h2>
    <p class="sec-sub">Not sure where to start with our range? Here are a few of the team's favourite blends.</p>
  </div>
  <div class="fav-grid" id="favGrid"></div>
  <button class="fav-shop" id="favShop">Shop our favourites &rarr;</button>
</section>

<section id="instagram">
  <div class="sec-head" style="margin-bottom:0">
    <div class="sec-eyebrow">Follow along</div>
    <h2 class="sec-title">Find Us On Instagram</h2>
    <div class="ig-handle"><a href="https://www.instagram.com/biscuitandbrew_/" target="_blank" rel="noopener">@biscuitandbrew_</a></div>
  </div>
  <div class="ig-grid">
    <a class="ig-tile" href="https://www.instagram.com/reel/DZrpOSkNASV/" target="_blank" rel="noopener" style="background-image:url('images/instagram-1.jpg')">
      <span class="ig-veil"></span>
      <span class="ig-play"></span>
      <span class="ig-ico">▶ Reel</span>
    </a>
    <a class="ig-tile" href="https://www.instagram.com/reel/DY2JboxNfP-/" target="_blank" rel="noopener" style="background-image:url('images/instagram-2.jpg')">
      <span class="ig-veil"></span>
      <span class="ig-play"></span>
      <span class="ig-ico">▶ Reel</span>
    </a>
  </div>
</section>

<section id="refer">
  <div class="r-eyebrow">Rewards</div>
  <h2>Refer A Friend</h2>
  <p>You'll both love Biscuit &amp; Brew &mdash; so here's £5 each off your next order.</p>
  <div class="r-cards">
    <div class="r-card"><div class="r-amt">£5</div><div class="r-lbl">Your friend gets</div></div>
    <div class="r-card"><div class="r-amt">£5</div><div class="r-lbl">You get</div></div>
  </div>
  <button class="r-cta" id="referBtn">Start Earning</button>
</section>

<section id="visit">
  <div class="visit-wrap">
    <div class="visit-col">
      <div class="v-eyebrow">Cafe &amp; Lounge</div>
      <h3>Come and sit a while.</h3>
      <p>A family-run cafe and hidden lounge in the heart of Nottingham, pouring our handcrafted loose leaf blends since 2017. Breakfast, brunch, afternoon tea, cakes and hot chocolates &mdash; with gluten-free and vegan-friendly options, served at your table or tucked away in our cosy downstairs snug.</p>
    </div>
    <div class="visit-col">
      <div class="v-eyebrow">Find Us</div>
      <h3>Visit Us</h3>
      <p>5 Victoria Street<br/>Nottingham NG1 2EW</p>
      <div style="margin-top:18px">
        <div class="v-row"><span>Mon &ndash; Fri</span><span>9:00 &ndash; 5:00</span></div>
        <div class="v-row"><span>Saturday</span><span>9:30 &ndash; 5:00</span></div>
        <div class="v-row"><span>Sunday</span><span>10:00 &ndash; 4:30</span></div>
      </div>
    </div>
    <div class="visit-col">
      <div class="v-eyebrow">Experiences</div>
      <h3>Afternoon Tea</h3>
      <p>Book the full afternoon tea experience &mdash; scones, finger sandwiches, cake and a pot of loose leaf tea &mdash; or join one of our guided tea-tasting events. Booking online, or gift it with a voucher.</p>
    </div>
  </div>
</section>

<section id="reviews">
  <div class="sec-head" style="margin-bottom:8px">
    <div class="sec-eyebrow">Reviews</div>
    <h2 class="sec-title">Why people love our loose leaf tea</h2>
  </div>
  <div class="rv-ratings">
    <span class="rv-score"><span class="rv-num">4.98</span><span class="rv-stars">★★★★★</span><span class="rv-count">(42)</span></span>
    <span class="rv-verified">Verified reviews</span>
    <span class="rv-count">·&nbsp; Google 4.8 ★ · 155 reviews</span>
  </div>
  <div class="rv-marquee">
   <div class="rv-track" id="rvTrack">
    <div class="rv-card">
      <img class="rv-avatar" src="images/rv-battenburg.jpg" alt="Battenburg loose leaf tea" />
      <p class="rv-q">"Lovely tea"</p>
      <div class="rv-s">★★★★★</div>
      <div class="rv-name">Carl Farrell</div>
      <div class="rv-prod">Battenburg</div>
    </div>
    <div class="rv-card">
      <img class="rv-avatar" src="images/rv-taster.jpg" alt="Tea Taster Bundle Box" />
      <p class="rv-q">"Delicious teas, thank you!"</p>
      <div class="rv-s">★★★★★</div>
      <div class="rv-name">Emma Winterton</div>
      <div class="rv-prod">Tea Taster Bundle Box</div>
    </div>
    <div class="rv-card">
      <img class="rv-avatar" src="images/rv-biscuitbrew.jpg" alt="Biscuit Brew loose leaf tea" />
      <p class="rv-q">"Biscuit Brew is the perfect tea, great flavour, perfectly balanced. My new go-to!"</p>
      <div class="rv-s">★★★★★</div>
      <div class="rv-name">Nick W</div>
      <div class="rv-prod">Biscuit Brew</div>
    </div>
    <div class="rv-card">
      <img class="rv-avatar" src="images/rv-cherrybakewell.jpg" alt="Cherry Bakewell loose leaf tea" />
      <p class="rv-q">"Omg the Cherry Bakewell!"</p>
      <div class="rv-s">★★★★★</div>
      <div class="rv-name">Dina K</div>
      <div class="rv-prod">Cherry Bakewell</div>
    </div>
    <div class="rv-card">
      <img class="rv-avatar" src="images/review-teapot.jpg" alt="Customer's cast iron teapot" />
      <p class="rv-q">"I'm so happy with my new teapot. The loose teas are so nice, and the customer service was excellent."</p>
      <div class="rv-s">★★★★★</div>
      <div class="rv-name">Caroline Sutliffe</div>
      <div class="rv-prod">Loose Leaf Tea Starter Kit</div>
    </div>
    <div class="rv-card">
      <img class="rv-avatar" src="images/review-food.jpg" alt="Brunch at Biscuit &amp; Brew" />
      <p class="rv-q">"Delicious food, reasonably priced, with such wonderful friendly staff."</p>
      <div class="rv-s">★★★★★</div>
      <div class="rv-name">Daniel McDonald-Smith</div>
      <div class="rv-prod">Cafe &amp; Lounge</div>
    </div>
   </div>
  </div>
  <a class="rv-cta" href="https://www.google.com/maps/search/?api=1&query=Biscuit%20%26%20Brew%20Nottingham" target="_blank" rel="noopener">Read &amp; leave a review →</a>
</section>

<section id="faq">
  <div class="sec-head">
    <div class="sec-eyebrow">Good to know</div>
    <h2 class="sec-title">Frequently Asked Questions</h2>
    <p class="sec-sub">Everything you need to know about our tea, orders and the tea house.</p>
  </div>
  <div class="faq-wrap">
    <div class="faq-group">Questions About Our Products</div>
    <div class="faq-item">
      <button class="faq-q">How do I brew the perfect tea? <span class="faq-ic">+</span></button>
      <div class="faq-a"><p>Brewing instructions are written on the front of every packet of loose leaf tea we send out, and are also available to view on all tea blends — just search for your particular blend and see. Our <a data-go="brew">Brew Guide</a> also has loads of great tips on how to make the perfect loose leaf brew.</p></div>
    </div>
    <div class="faq-item">
      <button class="faq-q">Do I need an infuser? <span class="faq-ic">+</span></button>
      <div class="faq-a"><p>Pretty much. If you really do still need one, you can <a data-go="accessories">get one here</a>.</p></div>
    </div>
    <div class="faq-item">
      <button class="faq-q">What are natural flavourings? <span class="faq-ic">+</span></button>
      <div class="faq-a"><p>Natural flavourings are basically natural flavouring preparations which have been derived from only natural ingredients, as opposed to artificial flavours or nature-identical flavours, which are the chemical equivalent of natural flavourings but chemically synthesised rather than extracted from natural source materials.</p><p>Please be aware that flavourings are not necessarily made from the ingredients you would assume. For example, the natural almond flavour we use contains no actual nuts whatsoever! So whilst you can describe the resulting flavour from the taste, you wouldn't include it in the ingredient list. It's worth adding that none of our flavourings contain any allergens.</p></div>
    </div>

    <div class="faq-group">Delivery</div>
    <div class="faq-item">
      <button class="faq-q">How much is shipping? <span class="faq-ic">+</span></button>
      <div class="faq-a"><p>Our shipping costs are calculated based on our own packaging costs in addition to the couriers' own shipping prices. Most UK orders are shipped using Royal Mail or DPD. Couriers on international orders vary.</p></div>
    </div>
    <div class="faq-item">
      <button class="faq-q">When will my order arrive? <span class="faq-ic">+</span></button>
      <div class="faq-a"><p>Usually orders are fulfilled and shipped out within 1–2 days of being placed. Order times do vary depending on your location in the world, but our best efforts have been made to include this information when you're selecting your postage at checkout. If this isn't the case, <a data-go="contact">let us know here</a>.</p></div>
    </div>
    <div class="faq-item">
      <button class="faq-q">My order hasn't arrived <span class="faq-ic">+</span></button>
      <div class="faq-a"><p>There can be occasional delays on orders for reasons beyond us and exclusive to the particular couriers. In the rare cases this does happen it usually has something to do with processing or collection issues and damaged labels. Hang tight for a couple of days and if your order still hasn't arrived then <a data-go="contact">contact us here</a>.</p></div>
    </div>
    <div class="faq-item">
      <button class="faq-q">I've changed my mind on my order <span class="faq-ic">+</span></button>
      <div class="faq-a"><p>Unfortunately we're unable to make changes to your order once it has been placed (it makes it difficult to keep track of stock, and things are more easily lost and generally confused). That being said, if you have ordered something by mistake, or even if you've just changed your mind, <a data-go="contact">let us know</a> as soon as you can; if the order hasn't been packed we may be able to make it right.</p></div>
    </div>
    <div class="faq-item">
      <button class="faq-q">What do I do if something is wrong with my order? <span class="faq-ic">+</span></button>
      <div class="faq-a"><p>We want everyone to be happy with their tea. If you're unhappy with your order in any way — if something is incomplete, damaged or anything else — then please <a data-go="contact">reach out to us here</a>.</p></div>
    </div>
    <div class="faq-item">
      <button class="faq-q">What is your refund and returns policy? <span class="faq-ic">+</span></button>
      <div class="faq-a"><p>You can read our full <a data-go="returns">returns policy here</a>. In short: unopened tea can be returned, and if anything arrives damaged or wrong we'll put it right — just get in touch.</p></div>
    </div>
    <div class="faq-item">
      <button class="faq-q">Do you ship internationally? <span class="faq-ic">+</span></button>
      <div class="faq-a"><p>Yes! We currently ship worldwide, although this may not always be reflected in the checkout options (this is for quite boring reasons; we have to input the costs of shipping to each country manually and we just haven't gotten to yours yet). If your country is not on the list of possible shipping options then you can <a data-go="contact">contact us here</a>.</p></div>
    </div>
    <div class="faq-item">
      <button class="faq-q">Can you send my order quicker? <span class="faq-ic">+</span></button>
      <div class="faq-a"><p>In a rush? No problem! Just <a data-go="contact">get in touch</a> with us before you place your order to check.</p></div>
    </div>

    <div class="faq-group">Tea House</div>
    <div class="faq-item">
      <button class="faq-q">Can I reserve a table? <span class="faq-ic">+</span></button>
      <div class="faq-a"><p>We are walk-in only, but we do take bookings for Afternoon Tea. You can make a reservation enquiry <a data-go="book">here</a>.</p></div>
    </div>
    <div class="faq-item">
      <button class="faq-q">Do you have wheelchair access? <span class="faq-ic">+</span></button>
      <div class="faq-a"><p>We have access and space for wheelchairs. However, space is limited to the ground floor level, which can get very cosy, so please bear this in mind when attending. There is also a small step at the entrance of our shop, and our only toilet facilities are accessible from the shop exterior. If you have further concerns please <a data-go="contact">contact us here</a>.</p></div>
    </div>
    <div class="faq-item">
      <button class="faq-q">Do you allow dogs? <span class="faq-ic">+</span></button>
      <div class="faq-a"><p>We love dogs! If your dog is as well behaved as you are then we're happy to host them anytime.</p></div>
    </div>
    <div class="faq-item">
      <button class="faq-q">Do you serve any gluten free or dairy free foods? <span class="faq-ic">+</span></button>
      <div class="faq-a"><p>We can cater to gluten free and dairy free for much of our menu, depending on availability. As the cost of many gluten free ingredients can be, on average, up to four times as expensive as non-GF ingredients, there may be a small surcharge.</p></div>
    </div>

    <div class="faq-group">Allergens</div>
    <div class="faq-item">
      <button class="faq-q">Which allergens do you handle? <span class="faq-ic">+</span></button>
      <div class="faq-a"><p>We handle the following allergens in our kitchen: milk, eggs, wheat, peanuts, nuts, soybean, mustard &amp; sulphur dioxide. While we do our utmost to ensure cross contamination is avoided, please note that all of the food is prepared in a very small space. Those with strong food allergies should take this into consideration before attending.</p></div>
    </div>
  </div>
</section>

<section id="contact">
  <div class="sec-head">
    <div class="sec-eyebrow">Get in touch</div>
    <h2 class="sec-title">Contact Us</h2>
    <p class="sec-sub">Questions about an order, a booking or a blend? We'd love to hear from you.</p>
  </div>
  <div class="contact-info">
    <div class="ci-col">
      <div class="v-eyebrow">Visit</div>
      <p>5 Victoria Street<br/>Nottingham NG1 2EW</p>
    </div>
    <div class="ci-col">
      <div class="v-eyebrow">Opening Hours</div>
      <div class="v-row"><span>Mon – Fri</span><span>9:00 – 5:00</span></div>
      <div class="v-row"><span>Saturday</span><span>9:30 – 5:00</span></div>
      <div class="v-row"><span>Sunday</span><span>10:00 – 4:30</span></div>
    </div>
    <div class="ci-col">
      <div class="v-eyebrow">Say Hello</div>
      <p><a href="mailto:hello@biscuitandbrewteahouse.com">hello@biscuitandbrewteahouse.com</a><br/>
      <a href="https://www.instagram.com/biscuitandbrew_/" target="_blank" rel="noopener">@biscuitandbrew_</a></p>
    </div>
  </div>
  <div class="contact-photo">
    <img src="images/storefront.jpg" alt="The Biscuit &amp; Brew tea house storefront on Victoria Street, Nottingham" loading="lazy" />
  </div>
  <form class="contact-form" id="contactForm">
    <h3>Send us a message</h3>
    <div class="cf-two">
      <div class="cf-field"><input type="text" id="cfName" placeholder="Name" required /></div>
      <div class="cf-field"><input type="email" id="cfEmail" placeholder="Email" required /></div>
    </div>
    <div class="cf-field"><input type="tel" id="cfPhone" placeholder="Phone number (optional)" /></div>
    <div class="cf-field"><textarea id="cfMsg" rows="5" placeholder="Comment" required></textarea></div>
    <button type="submit" class="cf-btn">Send</button>
  </form>
</section>

<section id="returns">
  <div class="sec-head">
    <div class="sec-eyebrow">Good to know</div>
    <h2 class="sec-title">Returns Policy</h2>
    <p class="sec-sub">We want you to love every sip — here's how returns work.</p>
  </div>
  <div class="policy-wrap">
    <p>We want you to love every sip of your tea from Biscuit &amp; Brew! But we understand that sometimes things don't go as planned. Our returns policy is designed to make things as smooth and fair as possible for you.</p>
    <h3>Can I Return My Tea?</h3>
    <p>Due to the nature of loose-leaf tea, we cannot accept returns on any tea products that have been opened or partially used. This is to ensure freshness and quality for all our customers. However, if your tea is still sealed and unopened, we'll gladly process a return for you.</p>
    <h3>What If My Tea Arrives Damaged or Isn't Right?</h3>
    <p>If your order arrives damaged, or if we've made a mistake, please let us know within 7 days of receiving your order. We'll work with you to make it right, whether that means sending a replacement or issuing a refund. Just <a data-go="contact">reach out to us</a> with a photo and details of the issue.</p>
    <h3>How to Start a Return</h3>
    <p>If your item qualifies for a return (e.g. unopened tea or a non-perishable item), follow these simple steps:</p>
    <ol>
      <li><b>Contact us:</b> Email us at <a href="mailto:returns@biscuitandbrew.com">returns@biscuitandbrew.com</a> with your order number and a brief description of the reason for the return.</li>
      <li><b>Prepare the package:</b> Make sure the item is securely packaged to avoid damage on its way back to us.</li>
      <li><b>Ship it back:</b> Once we receive your return, we'll process it and issue your refund within a few days.</li>
    </ol>
    <h3>Return Shipping Costs</h3>
    <p>Customers are responsible for return shipping costs unless the item was damaged or there was an error on our part. We recommend using a trackable shipping method to ensure it reaches us safely.</p>
    <h3>Questions? We're Here to Help!</h3>
    <p>If you have any questions about our returns policy or need help with a specific return, don't hesitate to <a data-go="contact">reach out</a>.</p>
  </div>
</section>

<section id="brew">
  <div class="sec-head">
    <div class="sec-eyebrow">Brew Guide</div>
    <h2 class="sec-title">How to Brew Loose Leaf Tea</h2>
    <p class="sec-sub">A little care makes all the difference. Here's how to get the most out of every blend.</p>
  </div>
  <div class="policy-wrap">
    <h3 style="margin-top:0">What You'll Need</h3>
    <div class="brew-need">
      <div class="bn-card"><div class="bn-img" style="background-image:url('images/brew-brewer.jpg')"></div><div class="bn-name">Brewer</div><div class="bn-desc">First (and most importantly!) is a brewer, to hold your loose leaf tea. We use Japanese cast iron teapots at Biscuit and Brew, but for a single cup, a mug from home is fine.</div></div>
      <div class="bn-card"><div class="bn-img" style="background-image:url('images/brew-infuser.jpg')"></div><div class="bn-name">Infuser</div><div class="bn-desc">A key difference between teabags and loose leaf tea is that for the latter you'll need a tea strainer. Many teapots, including our cast iron ones, come with a strainer inside. However if you're looking to brew in a mug, you might want to acquire a single cup tea infuser/strainer. These can be single use or metal, and include mesh ball and basket infusers.</div></div>
      <div class="bn-card"><div class="bn-img" style="background-image:url('images/brew-water.jpg')"></div><div class="bn-name">Water</div><div class="bn-desc">Freshly drawn and boiled water is needed to a great loose leaf cup of tea, this can be boiled from the kettle or on the hob. The ideal temperature of the water also depends on your type of tea — but more on this later!</div></div>
      <div class="bn-card"><div class="bn-img" style="background-image:url('images/brew-tea.jpg')"></div><div class="bn-name">Loose Leaf Tea</div><div class="bn-desc">Ensure you have some loose leaf tea ready to brew. Most tea found in teabags will have a loose leaf version available. For tips on some good teas to start with, see the bottom of this page.</div></div>
    </div>
    <div class="brew-note"><b>Optional: Thermometer</b><p>All teas will taste great with water boiled straight from the kettle. However, if you're wanting to extract the best flavours from your loose leaf tea, a thermometer can help ensure you are brewing at the right temperature for the tea you are using.</p></div>
  </div>
  <div class="brew-steps">
    <div class="bstep">
      <div class="bs-num"><span class="sl">Step</span><span class="sn">1</span></div>
      <div class="bs-body"><h4>Fill Your Mug or Teapot</h4><p>First, fill your brewer with freshly boiled water. Our cast iron teapots can hold up to 500ml. Mugs are around 200ml.</p><a class="bs-cta" data-go="accessories">View Teapots &amp; Infusers</a></div>
    </div>
    <div class="bstep">
      <div class="bs-num"><span class="sl">Step</span><span class="sn">2</span></div>
      <div class="bs-body"><h4>Check Temperature</h4><p>The temperature of your water can be an important factor in extracting the best flavours from your leaves. If you are brewing black, herbal or fruit teas, 90–100°C is perfect. For green, white or oolong teas, around 80°C is ideal. If you are brewing the latter, feel free to wait a few minutes before steeping.</p></div>
    </div>
    <div class="bstep">
      <div class="bs-num"><span class="sl">Step</span><span class="sn">3</span></div>
      <div class="bs-body"><h4>Add Loose Leaf Tea</h4><p>When your water is at the perfect temperature, it's time to put your tea in your strainer and add it to your brewer! For every 200ml of water we recommend using 1tsp (2.5g) of loose leaf tea. Add two heaped teaspoons to your teapot, or one to your mug.</p><a class="bs-cta" data-go="products">Explore Loose Leaf Tea</a></div>
    </div>
    <div class="bstep">
      <div class="bs-num"><span class="sl">Step</span><span class="sn">4</span></div>
      <div class="bs-body"><h4>Steep the Leaves</h4><p>Allow your tea to steep to extract your loose leaf flavours. Again, this depends on the type of tea you choose. Most blends require 3–5 minutes, while white or green tea is more delicate and requires a slightly shorter 2–3 minutes. These are only recommendations, and don't be afraid to steep for longer or shorter depending on personal preference! If you are unsure, the recommended time is usually found on your loose leaf tea bag.</p></div>
    </div>
    <div class="bstep">
      <div class="bs-num"><span class="sl">Step</span><span class="sn">5</span></div>
      <div class="bs-body"><h4>Remove the Infuser</h4><p>Once you have steeped for the appropriate length of time, carefully remove your infuser from the tea or mug.</p></div>
    </div>
    <div class="bstep">
      <div class="bs-num"><span class="sl">Step</span><span class="sn">6</span></div>
      <div class="bs-body"><h4>Enjoy!</h4><p>Now you have a perfectly brewed cup of tea to enjoy.</p></div>
    </div>
  </div>
</section>

<section id="music">
  <div class="sec-head">
    <div class="sec-eyebrow">Journal</div>
    <h2 class="sec-title">Why Music and Tea Make The Perfect Pairing</h2>
    <p class="article-meta">Posted on 31 Jan. 2025</p>
  </div>
  <div class="policy-wrap">
    <p>One of the first things you'll notice when you browse our tea menu is how inspired we are by music. Over the years, we've blended teas to the sound of Harry Styles, The Beatles, and the classic Pogues song, Fairytale of New York.</p>
    <p>But what does it mean to blend tea to music? Can a drink really be inspired by a song? In this blog, we'll take a closer look at our musical tea flavours and discover how pairing tea with music makes for a more immersive experience.</p>

    <h3>The Origin of Our Music Blends</h3>
    <p>The history of Biscuit and Brew really begins with our music teas, which we introduced as a way for our owner, Darren, to promote his music (under the name Arthur Dove). As any musician will know, finding new ways to catch people's attention is difficult, and promoting music through PR and radio plugging can be expensive — plus, it doesn't always work!</p>
    <p>After developing a casual interest in tea blending, Darren envisioned people connecting with his songs more deeply if they could taste something while listening to them. After all, people typically immerse themselves in music by listening to melodies, reading lyrics, and looking at cover art, but they rarely get to engage their most evocative physical sense at the same time: taste. We'd also never seen anyone use sound as an inspiration before — most of the tea blends we'd encountered at that point were based on food, smells or other tangible experiences.</p>
    <p>What made the concept even more exciting was the opportunity to elevate drinking tea into an immersive experience that engages as many of your senses as possible. We're used to hearing about fine wine and food being savoured in unique ways — such as at Dans Le Noir, the London restaurant where you eat in total darkness to intensify the flavours — so why not tea too?</p>
    <p>So, we began crafting our first musical tea experiments in 2019 — Little Picture, Lull, Hound on the Hunt and Sobre — which were inspired by Darren's songs, then we branched out into covering some household names: Strawberry Fields Forever, Watermelon Sugar, and Fairytale of New York.</p>

    <h3>How We Create Our Music Blends</h3>
    <p>When crafting any of our tea blends, taste is our main consideration (of course), but we also think scent is super important. That sounds obvious, but we've found that a lot of teas don't particularly taste like they smell, which is always a bit disappointing. The other factor we consider is colour. This doesn't just mean creating blends that brew into bright, vibrant-looking drinks, but also making sure we capture colours that reflect the taste — and for our music blends, the sound — of the tea.</p>
    <p>Helpfully, Darren is synaesthetic, so he can often perceive the feeling of a particular colour when listening to music. Guided by this sense, we tweak the ingredients of our music blends so they steep into very distinct tea liquors (the fancy term for tea leaves brewed in water) and often go through a few test liquors before we settle on the right one.</p>
    <p>Our blueberry and cinnamon green tea Lull is a good example. We blended a few options, one of which was a floral tea with peppermint and ginger that steeped into a deep reddish brown. However, for Darren, the song feels particularly blue/purple, and you might sense a similar vibe when you listen to it: it's got a wintery, brooding atmosphere, and there's something icy and melancholy about the melody.</p>
    <p>In the end we opted for a sweeter, slightly spiced blend, and added blue pea flowers so it steeps into a rich purple. The goal is ultimately for the tea and the song to feel like they're coming from the same creative place, so this felt a lot more appropriate (we ended up using the original idea for another blend: Winter's Glow). Essentially, once the taste, smell and sound of a blend align into something cohesive, we know we're onto something good.</p>

    <h3>How To Enjoy Our Music Blends</h3>
    <p>Our goal has always been to encourage you to slow down, eliminate distractions, and truly savour what you're eating and drinking, be it in the comfort of our cafe or through the ritual of brewing loose leaf tea at home. Our music teas are one way you can really lean into this practice.</p>
    <p>To get the best experience from drinking our teas, try to focus on the activity as much as possible. Eating and drinking are often treated as passive tasks, done whilst watching TV, scrolling on our phones or daydreaming, with the goal of simply filling ourselves up or quenching our thirst. But, with deep and sustained focus, you can make the experience far more rewarding.</p>
    <p>So, find a comfy place to sit, and whilst your tea brews, take a minute to bring yourself into the present moment. Notice any stray thoughts or distractions that crowd out your mind, and gently bring yourself back to what you're doing: enjoying a nice cup of tea.</p>
    <p>This might be difficult at first — our minds have a tendency to move at a hundred miles per hour! — but it's easy once you get the hang of it. Then, queue up the song that inspired the tea you've chosen (you can find links to the relevant songs embedded below) and take a sip. Focus intentionally on the tastes and sounds and observe how they might be connected. How do the flavours and scents of the tea reflect the atmosphere and melody of the music? What about the colour of the tea? As you sip and listen, remember to hold your attention as best you can on what you're tasting and hearing.</p>
    <p>If you want to go one step further, you could experiment with restricting your other senses. A few years ago we set up a makeshift sensory deprivation room at the Corn Exchange in Leeds — blacked out windows, blindfolds, the lot — and invited people to try our music teas whilst listening to the songs they represent. We found that guiding people to focus more closely on taste and sound made the flavours even more intense and strengthened their connection with the music. We'd encourage you to try a similar experiment at home if you have the means.</p>
    <p>So, that's the story of our music blends! Whilst we've focussed specifically on a few flavours here, practicing engaged and mindful drinking can help you get the most out of any of our teas. Take a look at our <a data-go="products">menu</a> and see if you can build the habit.</p>
    <p>Happy drinking!</p>
  </div>
</section>

<section id="wholesale">
  <div class="sec-head">
    <div class="sec-eyebrow">Trade</div>
    <h2 class="sec-title">Wholesale</h2>
    <p class="sec-sub">We provide our loose leaf tea and biodegradable pyramid teabags to carefully selected retailers throughout the UK.</p>
  </div>
  <form class="contact-form" id="wholesaleForm">
    <h3>Trade Enquiry</h3>
    <div class="cf-two">
      <div class="cf-field"><input type="text" id="whName" placeholder="Name *" required /></div>
      <div class="cf-field"><input type="email" id="whEmail" placeholder="Email *" required /></div>
    </div>
    <div class="cf-field"><input type="tel" id="whPhone" placeholder="Phone number *" required /></div>
    <div class="cf-field"><textarea id="whMsg" rows="5" placeholder="Comment *" required></textarea></div>
    <button type="submit" class="cf-btn">Send</button>
    <p class="cf-required">Fields marked with a * are compulsory</p>
  </form>
</section>

<section id="privacy">
  <div class="sec-head">
    <div class="sec-eyebrow">Good to know</div>
    <h2 class="sec-title">Privacy Policy</h2>
    <p class="sec-sub">We respect your privacy just as much as we love a good cup of tea.</p>
  </div>
  <div class="policy-wrap">
    <p>Hello and welcome to Biscuit &amp; Brew! We're thrilled to have you here, sipping tea with us. At Biscuit &amp; Brew, we believe in transparency and respect your privacy just as much as we love a good cup of tea. Here's what you need to know about how we handle your information:</p>

    <h3>1. The Information We Collect</h3>
    <p>When you browse our site, sign up, or make a purchase, we may collect:</p>
    <ul>
      <li><b>Personal Information</b> like your name, email, and shipping address.</li>
      <li><b>Payment Information</b> to process orders, but don't worry — we don't store this directly. It's securely handled by trusted payment providers.</li>
      <li><b>Browsing Information</b> (like cookies) to enhance your shopping experience, making our website faster and easier for you to use.</li>
    </ul>

    <h3>2. Why We Collect Your Information</h3>
    <p>We use your information to:</p>
    <ul>
      <li>Process your orders and get that tea to you as soon as possible.</li>
      <li>Improve your experience on our website.</li>
      <li>Send you updates on new teas, offers, and Biscuit &amp; Brew happenings, but only if you've signed up to hear from us.</li>
    </ul>

    <h3>3. Sharing Your Information</h3>
    <p>We only share your information when it's essential. That means with:</p>
    <ul>
      <li>Trusted third-party partners (like delivery services) to get your tea to your doorstep.</li>
      <li>Payment processors to handle transactions securely.</li>
    </ul>
    <p>We'll never sell your information, and sharing is only for business and legal reasons.</p>

    <h3>4. Keeping Your Information Safe</h3>
    <p>Your information's security is our priority. We use industry-standard security measures to protect it from unauthorized access, and we review these measures regularly.</p>

    <h3>5. Your Choices</h3>
    <p>You're in control! You can:</p>
    <ul>
      <li>Update or delete your information at any time by logging into your account.</li>
      <li>Unsubscribe from marketing emails by clicking the link in any email.</li>
      <li>Limit cookies through your browser settings.</li>
    </ul>

    <h3>6. Questions?</h3>
    <p>If you have any questions, feel free to <a data-go="contact">contact us</a>.</p>
    <p>The Biscuit &amp; Brew Team</p>
  </div>
</section>

<section id="media">
  <div class="sec-head">
    <div class="sec-eyebrow">Press</div>
    <h2 class="sec-title">Media</h2>
    <p class="sec-sub">Telling the Biscuit &amp; Brew story.</p>
  </div>
  <div class="policy-wrap">
    <p>We love sharing the Biscuit &amp; Brew story. Whether you're a journalist, blogger, podcaster or fellow tea lover, we're always happy to help with features, interviews and collaborations.</p>
    <p>For all press and media enquiries, please <a data-go="contact">get in touch</a> and we'll get back to you as soon as we can.</p>

    <h3>What We Can Share</h3>
    <ul>
      <li>Our story and background — how Biscuit &amp; Brew began, and what makes our music-inspired loose leaf blends different.</li>
      <li>High-resolution logos and product photography.</li>
      <li>Interviews with our founder, Darren (also known as Arthur Dove).</li>
      <li>Tea samples for honest reviews, where available.</li>
    </ul>

    <p>Drop us a line through our <a data-go="contact">contact page</a> and tell us a little about your publication or project — we'd love to hear from you.</p>
  </div>
</section>

<section id="ourname">
  <div class="sec-head">
    <div class="sec-eyebrow">Our Story</div>
    <h2 class="sec-title">How Did We Get The Name Biscuit &amp; Brew?</h2>
  </div>
  <p class="name-lead">The answer goes back to the very beginning, before we were a tea house, or really a business at all.</p>
  <div class="name-wrap">
    <div class="name-row">
      <div class="name-img"><img src="images/name-1.jpg" alt="Friends gathered together drinking tea" loading="lazy" /></div>
      <div class="name-text">
        <p>At first, the goal was simply to blend some music-inspired teas to promote Darren's music (under the name Arthur Dove). So we began as Arthur Dove Tea Co., and experimented with some homemade blends to give to our friends and colleagues (like Lull and Little Picture).</p>
        <p>Over time, we started trying out flavours that would appeal to a wider audience — like Rhubarb and Custard and Jaffa Cake — and at that point, it made sense to expand things a little. We started inviting friends over, not just to try the teas, but to see how they were made. Those gatherings became a regular thing: just us and our friends, hanging out, drinking tea, eating biscuits. No fuss, no grand occasion. Just a biscuit and a brew.</p>
      </div>
    </div>
    <div class="name-row rev">
      <div class="name-img"><img src="images/name-2.jpg" alt="A tea gathering with friends around a table" loading="lazy" /></div>
      <div class="name-text">
        <p>The name chose itself really! The more teas we made and the more gatherings we hosted, the more we felt like we were onto something special. A cup of tea with friends is such a simple, joyful thing, right? We began to wonder: could we bottle up that experience and recreate it somewhere bigger?</p>
        <p>That's when we decided to open the tea house. At its heart, we want your visit to feel like those early gatherings: good tea, good company, and something sweet on the side, all in a relaxed and welcoming space. We like to think we're inviting you into our home, just like we did for our friends all those years ago.</p>
      </div>
    </div>
    <div class="name-row">
      <div class="name-img"><img src="images/name-3.jpg" alt="Homemade loose leaf tea blends and biscuits" loading="lazy" /></div>
      <div class="name-text">
        <p>Although we decided pretty quickly that we didn't want to serve the usual biscuits you'd eat at home, we still wanted our menu to reflect our roots. We made our signature blend, Biscuit Brew, to commemorate the choice to become a tea house. It's a biscuit in tea form, so it encapsulates our story pretty well! It's also now our most popular tea, which feels like a fitting tribute. We also serve tea-flavoured biscuits with our afternoon teas, so whichever way you spin it, the spirit of those early days is alive and well.</p>
      </div>
    </div>
  </div>
  <div class="name-close">
    <p>So, that's the story of our name! If a biscuit and brew sounds good to you, <a class="lnk" data-go="visit">pop in</a> and see for yourself, or check out our <a class="lnk" data-go="products">tea menu</a> to take the experience home.</p>
    <p class="happy">Happy drinking!</p>
    <a class="fav-shop" data-go="visit" style="display:inline-block;text-decoration:none;margin-top:20px">Visit Us</a>
  </div>
</section>

<section id="caffeine">
  <div class="sec-head">
    <div class="sec-eyebrow">Journal</div>
    <h2 class="sec-title">Caffeine Guide</h2>
    <p class="article-meta">Posted on 21 Feb. 2025</p>
  </div>
  <div class="article-hero"><img src="images/caffeine-hero.jpg" alt="A spread of different teas, from black to herbal" loading="lazy" /></div>
  <div class="policy-wrap">
    <p>From morning rituals to afternoon pick-me-ups, caffeine plays a huge role in 21st century life. Some depend on it to power through the day, while others prefer to stay clear of it altogether. In this blog, we'll take a closer look at caffeine — its history, its benefits, and its potential drawbacks — and discuss how you can find your perfect brew.</p>

    <h3>What is caffeine?</h3>
    <p>Caffeine is a natural stimulant found in many seeds, nuts and plants, including coffee beans, cacao beans, kola nuts and guarana (a Brazilian rainforest plant). It works by inhibiting the effects of adenosine, a neurotransmitter that normally relaxes the brain and makes you feel tired as the day goes on.</p>
    <p>By connecting to adenosine receptors in the brain without activating them, caffeine reduces tiredness, increases blood adrenaline levels and activates neurotransmitters linked to dopamine (associated with pleasure, satisfaction and motivation) and norepinephrine (associated with alertness, focus and attention).</p>
    <p>This is how caffeine can improve cognitive function, increase athletic endurance and help provide a boost in overall mood. However, some people are more sensitive to caffeine than others. Many find that caffeine inhibits restful sleep and leads to feelings of restlessness and anxiety. Too much caffeine may also give some people headaches, migraines, and high blood pressure, and pregnant women are advised to avoid it entirely.</p>

    <h3>A brief history of caffeine</h3>
    <p>While Chinese legend claims Emperor Shen Nung discovered caffeinated tea over 4000 years ago, people likely began to use caffeine regularly as a stimulant around 141 BC, in imperial China. According to African mythologies meanwhile, coffee's energising effects were discovered by Ethiopian goat herders in the 9th century, CE.</p>
    <p>By the 15th century, coffee cultivation had spread across the Arabian Peninsula, with social gatherings over coffee becoming commonplace. The 17th and 18th centuries saw coffee and tea arrive in Europe, where it rapidly became a staple of social life. Tea rooms, coffee houses and so-called "pleasure gardens" sprang up across Europe at this time, offering affordable spaces for people of all backgrounds to gather.</p>
    <p>The Industrial Revolution then ushered in mass consumption of caffeine, particularly among the working classes, who relied on it to endure long hours in factories and workhouses. With the invention of instant coffee and tea bags in the 20th century, these drinks became more convenient to make at home. When caffeinated soft drinks and energy drinks took off in the 1980s, caffeine became cemented as the world's most widely used psychoactive stimulant.</p>

    <div class="article-img"><img src="images/caffeine-cups.jpg" alt="Five cups of differently-coloured loose leaf brews on a wooden table" loading="lazy" /></div>

    <h3>How does caffeine content vary for different kinds of tea?</h3>
    <p>There are a few factors that affect how much caffeine a cup of tea contains. Broken tea leaves — such as those found in tea bags — will release more caffeine when brewed compared to whole leaves, and the more tea leaves in your cup or bag, the more caffeine you'll drink. Longer brew times and higher water temperatures will also increase the caffeine content, as the hot water will act faster to release the caffeine from the leaves.</p>
    <p>Some types of tea also naturally contain more caffeine than others. Black teas like English Breakfast, Assam and Darjeeling generally contain the most caffeine because they are fully oxidised (meaning the leaves have been exposed to air for the maximum amount of time).</p>
    <p>Green tea is less oxidised than black tea, which preserves its lighter colour and flavour, as well as a slightly lower caffeine content. It also contains L-theanine — an amino acid that promotes relaxation and focus — meaning it gives you a gentler energy lift, without the jitters or crash often associated with caffeine. Matcha (ground green tea whisked into hot water) generally contains more caffeine than regular green tea because you're consuming the entire leaf.</p>
    <p>White tea — the most delicate of the tea types — is made from young tea buds and leaves that are minimally processed. It's a great choice for those who are sensitive to caffeine but still want a little pick-me-up.</p>

    <h3>Which teas are caffeine free?</h3>
    <p>The most common types of caffeine free tea are herbal blends like peppermint, chamomile and lavender, and <a data-go="herbal">fruit infusions</a>, neither of which contain caffeinated tea leaves. Both are perfect for any time of the day, especially in the evening when you want a warm, comforting drink without worrying about sleep disruption.</p>
    <p><a data-go="rooibos">Rooibos</a> — also known as African red tea or redbush tea — is also caffeine free, because it's made from the leaves of the Aspalathus linearis plant. Its rich, nutty, and subtly sweet taste makes it a great choice for those who prefer milk in their tea, but don't want to drink caffeine.</p>

    <h3>What's the difference between decaffeinated and caffeine free tea?</h3>
    <p>Decaffeinated blends offer a great solution for anyone looking to avoid caffeine. This is where usually caffeinated tea leaves are chemically altered using carbon dioxide, green coffee beans, or the naturally occurring solvent ethyl acetate. This process removes most of the caffeine, although a small amount will remain.</p>
    <p>Black teas, green teas and some oolong teas are readily available in decaf versions, and while some people think these teas taste slightly weaker and more processed than caffeinated blends, for many the difference is negligible.</p>
    <p>Ultimately, the best way to find your perfect caffeine level is to experiment with <a data-go="products">different types of loose leaf tea</a>. Pay attention to how your body reacts and choose the teas that make you feel the best. If you're looking to avoid caffeine altogether, try a herbal or fruit infusion, or get acquainted with rooibos.</p>

    <h3>The Highlights</h3>
    <ul>
      <li>Caffeine is a natural stimulant found in coffee, tea, and cacao that blocks sleep-inducing adenosine.</li>
      <li>Drinking caffeinated drinks can boost focus, energy, and mood, but may also lead to side effects like headaches and poor sleep.</li>
      <li>Black tea has the most caffeine, and white tea has the least. Green tea has slightly less caffeine than black tea, but drinking it in powdered form (matcha) will give you a stronger boost.</li>
      <li>Herbal teas like peppermint, chamomile and rooibos, as well as fruit teas, are naturally caffeine free.</li>
      <li>While decaf teas are not completely caffeine free, they undergo a process to remove most caffeine, and the remaining amount shouldn't have any effect.</li>
      <li>Experimenting with different teas and brewing methods can help you find the perfect balance for your energy levels and lifestyle.</li>
    </ul>
    <p>Happy drinking!</p>
  </div>
</section>

<section id="newsletter">
  <h2>Join our exclusive tea club</h2>
  <p class="nsub">For 20% off your first order, secret menus, shop gossip and more. Fill in your details and we'll send your discount code as a thank you.</p>
  <form class="nl-club" id="nlForm">
    <div class="nlc-two">
      <input type="text" id="nlFirst" placeholder="First name" required />
      <input type="text" id="nlLast" placeholder="Last name" required />
    </div>
    <input type="email" id="nlEmail" placeholder="Email" required />
    <button type="submit" class="nl-club-btn">Subscribe &amp; get 20% off</button>
  </form>
</section>

<section id="footcols">
  <div class="fc-wrap">
    <div class="fc-brand">
      <div class="fc-logo">BISCUIT &amp; BREW</div>
      <p>Handcrafted loose leaf tea blends, inspired by cakes, biscuits, cocktails and music. Made in Nottingham since 2017.</p>
      <div class="fc-social">
        <a href="https://www.facebook.com/biscuitandbrewteahouse/" target="_blank" rel="noopener" aria-label="Facebook">f</a>
        <a href="https://www.instagram.com/biscuitandbrew_/" target="_blank" rel="noopener" aria-label="Instagram">&#9678;</a>
      </div>
    </div>
    <div class="fc-col">
      <h4>Highlights</h4>
      <a data-go="products">Our Loose Leaf Tea</a>
      <a data-go="book">Book A Table</a>
      <a data-go="cafemenu">Cafe &amp; Lounge Menu</a>
      <a data-go="book">Afternoon Tea</a>
    </div>
    <div class="fc-col">
      <h4>Useful Info</h4>
      <a data-go="wholesale">Wholesale</a>
      <a data-go="faq">FAQ</a>
      <a data-go="contact">Contact Us</a>
      <a data-go="visit">Visit Us</a>
      <a data-go="returns">Returns Policy</a>
      <a data-go="privacy">Privacy Policy</a>
    </div>
    <div class="fc-col">
      <h4>Reading</h4>
      <a data-go="media">Media</a>
      <a data-go="story">Our Story</a>
      <a data-go="caffeine">Caffeine Guide</a>
      <a data-go="brew">How to Brew Loose Leaf Tea</a>
      <a data-go="music">Music &amp; Tea</a>
      <a data-go="ourname">Our Name</a>
    </div>
  </div>
  <div class="fc-pay" aria-label="Accepted payment methods">
    <svg class="pl" viewBox="0 0 48 30" role="img" aria-label="American Express"><rect width="48" height="30" rx="4" fill="#1F72CD"/><text x="24" y="19" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-weight="bold" font-size="10" fill="#fff">AMEX</text></svg>
    <svg class="pl" viewBox="0 0 48 30" role="img" aria-label="Apple Pay"><rect width="48" height="30" rx="4" fill="#fff"/><path transform="translate(9,7) scale(0.85)" fill="#000" d="M8.9 3.2c.5-.6.8-1.4.7-2.2-.7 0-1.5.5-2 1.1-.4.5-.8 1.3-.7 2.1.8 0 1.5-.4 2-1zM9.6 4.3c-1.1-.1-2 .6-2.6.6-.6 0-1.4-.6-2.3-.6-1.2 0-2.3.7-2.9 1.8-1.2 2.1-.3 5.2.9 6.9.6.8 1.2 1.7 2.1 1.7.8 0 1.1-.5 2.1-.5s1.3.5 2.1.5c.9 0 1.5-.8 2-1.6.4-.6.6-1.2.8-1.8-.1 0-1.6-.6-1.6-2.4 0-1.5 1.2-2.2 1.3-2.3-.7-1-1.8-1.1-2.2-1.1z"/><text x="34" y="20" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-weight="600" font-size="11" fill="#000">Pay</text></svg>
    <svg class="pl" viewBox="0 0 48 30" role="img" aria-label="Diners Club"><rect width="48" height="30" rx="4" fill="#fff"/><circle cx="24" cy="15" r="9" fill="#0079BE"/><circle cx="24" cy="15" r="4.5" fill="#fff"/></svg>
    <svg class="pl" viewBox="0 0 48 30" role="img" aria-label="Discover"><rect width="48" height="30" rx="4" fill="#fff"/><text x="4" y="19" font-family="Arial,Helvetica,sans-serif" font-weight="bold" font-size="7.6" fill="#222">DISCOVER</text><circle cx="40" cy="20" r="5" fill="#F76E11"/></svg>
    <svg class="pl" viewBox="0 0 48 30" role="img" aria-label="Google Pay"><rect width="48" height="30" rx="4" fill="#fff"/><text x="15" y="20" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-weight="bold" font-size="13" fill="#4285F4">G</text><text x="31" y="20" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-size="11" fill="#5F6368">Pay</text></svg>
    <svg class="pl" viewBox="0 0 48 30" role="img" aria-label="Maestro"><rect width="48" height="30" rx="4" fill="#fff"/><circle cx="20" cy="15" r="8" fill="#0099DF"/><circle cx="28" cy="15" r="8" fill="#ED0006" fill-opacity=".85"/></svg>
    <svg class="pl" viewBox="0 0 48 30" role="img" aria-label="Mastercard"><rect width="48" height="30" rx="4" fill="#fff"/><circle cx="20" cy="15" r="8" fill="#EB001B"/><circle cx="28" cy="15" r="8" fill="#F79E1B" fill-opacity=".85"/></svg>
    <svg class="pl" viewBox="0 0 48 30" role="img" aria-label="Shop Pay"><rect width="48" height="30" rx="4" fill="#5A31F4"/><text x="20" y="20" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-weight="bold" font-size="11" fill="#fff">shop</text><text x="38" y="20" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-size="9" fill="#fff">Pay</text></svg>
    <svg class="pl" viewBox="0 0 48 30" role="img" aria-label="UnionPay"><rect width="48" height="30" rx="4" fill="#fff"/><rect x="7" y="6" width="11" height="18" rx="2" fill="#E21836"/><rect x="18" y="6" width="11" height="18" rx="2" fill="#00447C"/><rect x="29" y="6" width="11" height="18" rx="2" fill="#007B84"/></svg>
    <svg class="pl" viewBox="0 0 48 30" role="img" aria-label="Visa"><rect width="48" height="30" rx="4" fill="#fff"/><text x="24" y="20" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-style="italic" font-weight="bold" font-size="14" fill="#1A1F71">VISA</text></svg>
  </div>
</section>

<footer>
  <div class="f-left">BISCUIT &amp; BREW</div>
  <div class="f-center">&copy; 2026 BISCUIT &amp; BREW &middot; Rooted in the hills.</div>
  <div class="f-right"><a href="https://www.instagram.com/biscuitandbrew_/" target="_blank" rel="noopener">Instagram</a> &nbsp;&bull;&nbsp; <a href="https://www.facebook.com/biscuitandbrewteahouse/" target="_blank" rel="noopener">Facebook</a></div>
</footer>

<div id="modal">
  <div class="modal-card">
    <button class="modal-close" id="modalClose">&times;</button>
    <div class="mgal" id="mGal">
      <div class="mgal-track" id="mGalTrack"></div>
      <button class="mgal-nav prev" id="mGalPrev" aria-label="Previous photo">&#8249;</button>
      <button class="mgal-nav next" id="mGalNext" aria-label="Next photo">&#8250;</button>
      <div class="mgal-dots" id="mGalDots"></div>
    </div>
    <div class="modal-cat" id="mCat"></div>
    <div class="modal-name" id="mName"></div>
    <div class="modal-rating" id="mRating"><span class="ms" id="mStars">★★★★★</span><span class="mr" id="mReviews"></span></div>
    <div class="modal-desc" id="mDesc"></div>
    <div class="modal-vlabel" id="mVlabel">Select size</div>
    <div class="modal-variants" id="mVariants"></div>
    <div class="modal-trust">
      <div class="modal-stock"><b>✓ In stock</b> &middot; Pickup at Biscuit &amp; Brew, usually ready in 24 hours<br/><span class="save">Subscribe &amp; save 10%</span> on repeat orders</div>
      <div class="modal-badges"><span>Sustainable</span><span>Blended in the UK</span><span>Invented by us</span></div>
    </div>
    <div class="modal-extra" id="mExtra">
      <div class="me-row" id="mTasteRow"><span class="me-h">Taste</span><span class="me-v" id="mTaste"></span></div>
      <div class="me-row" id="mIngRow"><span class="me-h">Ingredients</span><span class="me-v" id="mIng"></span></div>
      <div class="me-row" id="mBrewRow"><span class="me-h">How to brew</span><span class="me-v" id="mBrew"></span></div>
      <div class="me-row" id="mPairRow"><span class="me-h">Biscuit pairing</span><span class="me-v" id="mPair"></span></div>
    </div>
    <div class="modal-foot">
      <div class="qty"><button id="qMinus">&minus;</button><span id="qVal">1</span><button id="qPlus">+</button></div>
      <button class="addbtn" id="addBtn">Add to cart</button>
    </div>
    <div class="modal-recs" id="mAlso">
      <div class="rec-title">You may also like</div>
      <div class="rec-row" id="mAlsoRow"></div>
    </div>
    <div class="modal-recs" id="mRecent">
      <div class="rec-title">Recently viewed</div>
      <div class="rec-row" id="mRecentRow"></div>
    </div>
  </div>
</div>
<div id="toast"></div>

<div id="promoModal" aria-hidden="true">
  <div class="pm-card">
    <button class="pm-close" id="pmClose" aria-label="Close">&times;</button>
    <div class="pm-eyebrow">Welcome to Biscuit &amp; Brew</div>
    <h2>Get <span class="pm-amber">20% off</span><br/>your first order! &#127873;</h2>
    <p>Sign up now for exclusive deals, new treats, and 20% off your first order.</p>
    <form id="pmForm">
      <div class="pm-field"><label for="pmName">Name</label><input type="text" id="pmName" placeholder="Your name" required /></div>
      <div class="pm-field"><label for="pmEmail">Email</label><input type="email" id="pmEmail" placeholder="your@email.com" required /></div>
      <button type="submit" class="pm-btn">Subscribe</button>
    </form>
  </div>
</div>

<div id="cartOverlay"></div>
<aside id="cart" aria-label="Shopping bag">
  <div class="cart-head"><span class="cart-title">Your bag</span><button class="cart-close" id="cartClose">&times;</button></div>
  <div id="cartItems"></div>
  <div class="cart-empty" id="cartEmpty">Your bag is empty.<br><span>Add a blend to begin your ritual.</span></div>
  <div class="cart-foot" id="cartFoot">
    <div class="cart-sub"><span>Subtotal</span><span id="cartTotal">&pound;0.00</span></div>
    <button class="checkout" id="checkoutBtn">Checkout</button>
    <p class="cart-note">Taxes &amp; shipping calculated at checkout.</p>
  </div>
</aside>

<script>
__JS__
</script>
</body>
</html>
"""

HTML = (HTML.replace("__CSS__", css)
            .replace("__HEROCSS__", HERO_CSS)
            .replace("__HERO__", hero_uri)
            .replace("__JS__", JS))

# inline static (non-catalog) image paths used in markup (Our Story <img>, Instagram posters)
for rel, uri in uri_map.items():
    HTML = HTML.replace('src="' + rel + '"', 'src="' + uri + '"')
    HTML = HTML.replace('poster="' + rel + '"', 'poster="' + uri + '"')
    HTML = HTML.replace("url('" + rel + "')", "url('" + uri + "')")

# Embed the transparent logo as a PNG (keep alpha — JPEG would fill the background)
def png_data_uri(path, max_w=300):
    img = Image.open(path).convert("RGBA")
    if img.width > max_w:
        h = round(img.height * max_w / img.width)
        img = img.resize((max_w, h), Image.LANCZOS)
    buf = io.BytesIO(); img.save(buf, format="PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
logo_uri = png_data_uri(os.path.join(PUB, "images/logo-mark.png"))
HTML = HTML.replace('src="images/logo-mark.png"', 'src="' + logo_uri + '"')

# Embed ONLY the (compressed) hero video so the scroll-scrubbed hero works offline.
# The heavy Instagram reel videos are NOT embedded (kept as poster tiles linking out),
# which keeps the single file small and avoids the iPad open issue.
video_files = { "videos/hero.mp4": "videos/hero.mp4" }
for rel, path in video_files.items():
    with open(os.path.join(PUB, path), "rb") as vf:
        vb = vf.read()
    vuri = "data:video/mp4;base64," + base64.b64encode(vb).decode()
    HTML = HTML.replace('src="' + rel + '"', 'src="' + vuri + '"')
    print(f"  video {rel}: {len(vb)//1024} KB")

out = os.path.join(PUB, "biscuit-and-brew-ipad.html")
with open(out, "w") as f:
    f.write(HTML)
print("WROTE", out, f"({len(HTML)//1024} KB)")
