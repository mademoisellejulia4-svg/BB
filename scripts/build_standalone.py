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
  .rv-grid{ max-width:1180px; margin:46px auto 0; display:grid; gap:22px; grid-template-columns:repeat(auto-fit, minmax(280px,1fr)); text-align:left; }
  .rv-card{ border:1px solid rgba(255,255,255,0.08); border-radius:16px; background:linear-gradient(160deg, rgba(255,255,255,0.045), rgba(255,255,255,0.015)); padding:26px 24px; display:flex; flex-direction:column; gap:12px; }
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
  const FAVS=[['black','caramel-apple-betty'],['green','pear-pistachio'],['herbal','cherry-kiss'],['black','biscuit-brew']];
  function buildFavourites(){
    const grid=$('#favGrid'); if(!grid) return; grid.innerHTML='';
    FAVS.forEach(([cid,pid])=>{
      const c=CAT[cid]; if(!c) return; const p=(c.products||[]).find(x=>x.id===pid); if(!p) return;
      const card=document.createElement('div'); card.className='fav-card';
      card.innerHTML='<div class="fav-medal"'+(c.image?' style="background-image:url(\\''+c.image+'\\')"':'')+'><span class="fav-badge">'+c.name+'</span></div>'+
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
  function openCategory(id){
    const c=CAT[id]; if(!c) return;
    $('#detailTitle').textContent=c.name; prodGrid.innerHTML='';
    c.products.forEach(p=>{
      const card=document.createElement('div'); card.className='prod-card';
      const chips=p.variants.map(v=>'<span class="pc-chip">'+v.size+' <b>'+fmt(v.price)+'</b></span>').join('');
      const pimg=p.image?'<div class="pc-img" style="background-image:url(\\''+p.image+'\\')"></div>':'';
      card.innerHTML=pimg+
        '<div class="pc-cat">'+c.name+'</div>'+
        '<div class="pc-name">'+p.name+'</div>'+
        (p.rating?'<div class="pc-stars">'+('★★★★★'.slice(0,p.rating))+' <span>'+(p.reviews||'')+(p.reviews?' reviews':'')+'</span></div>':'')+
        '<div class="pc-desc">'+(p.description||'')+'</div>'+
        '<div class="pc-variants">'+chips+'</div>'+
        '<div class="pc-from"><span><span class="lbl">From&nbsp;</span><span class="val">'+fmt(fromPrice(p))+'</span></span><span class="pc-view">View \\u2192</span></div>';
      card.addEventListener('click',()=>openModal(c,p));
      prodGrid.appendChild(card);
    });
    catView.classList.remove('active'); detailView.classList.add('active');
    window.scrollTo({top:$('#products').offsetTop-10,behavior:'smooth'});
  }
  function backToCats(){ detailView.classList.remove('active'); catView.classList.add('active'); }
  $('#backBtn').addEventListener('click',backToCats);

  /* ---- modal ---- */
  const modal=$('#modal'); let mProduct=null,mCat=null,mVarIdx=0,mQty=1;
  function openModal(c,p){
    mProduct=p; mCat=c; mVarIdx=0; mQty=1;
    const mImg=$('#mImg');
    if(p.image){ mImg.style.backgroundImage="url('"+p.image+"')"; mImg.classList.add('show'); }
    else { mImg.classList.remove('show'); mImg.style.backgroundImage=''; }
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
    modal.classList.add('open'); requestAnimationFrame(()=>modal.style.opacity='1');
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

  /* nav drawer */
  const nav=$('#nav'), navOv=$('#navOverlay');
  function openNav(){ nav.classList.add('open'); navOv.classList.add('open'); }
  function closeNav(){ nav.classList.remove('open'); navOv.classList.remove('open'); }
  $('#menuBtn').addEventListener('click',openNav);
  $('#navClose').addEventListener('click',closeNav);
  navOv.addEventListener('click',closeNav);
  const NAV_CAT={ vouchers:1, matcha:1, accessories:1, 'starter-kits':1 };
  document.querySelectorAll('[data-go]').forEach(a=>{
    a.addEventListener('click',()=>{
      const go=a.getAttribute('data-go'); closeNav();
      if(go==='products'){ backToCats(); $('#products').scrollIntoView({behavior:'smooth'}); }
      else if(NAV_CAT[go]){ $('#products').scrollIntoView({behavior:'smooth'}); setTimeout(()=>openCategory(go),420); }
      else { const el=document.getElementById(go); if(el) el.scrollIntoView({behavior:'smooth'}); }
    });
  });
  document.addEventListener('keydown',e=>{ if(e.key==='Escape') closeNav(); });

  /* hero: scroll-scrub the whole clip across ~3 viewport scrolls */
  (function(){
    const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
    const ramp=(p,a,b)=>clamp((p-a)/(b-a),0,1);
    const hero=$('#hero'), v=$('#heroVideo'), center=$('#sticky .hero-center');
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
    function onScroll(){ const p=prog(); const d=dur||v.duration||0; targetT=p*Math.max(0,d-0.05); if(center) center.style.opacity=(1-ramp(p,0.04,0.32)).toFixed(3); }
    function loop(){ curT+=(targetT-curT)*0.16; if(Math.abs(targetT-curT)<0.008) curT=targetT; if((dur||v.duration)&&Math.abs(v.currentTime-curT)>0.02){ try{v.currentTime=curT;}catch(e){} } requestAnimationFrame(loop); }
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
    <div class="brand">BISCUIT &amp; BREW</div>
  </div>
  <div class="hnav">
    <button class="shop" id="shopLink">SHOP</button>
    <button class="shop bag" id="bagBtn">BAG <span id="bagCount" class="bag-count">0</span></button>
  </div>
</header>

<div id="navOverlay"></div>
<nav id="nav" aria-label="Main menu">
  <div class="nav-head">
    <span class="brand">BISCUIT &amp; BREW</span>
    <button class="nav-close" id="navClose">&times;</button>
  </div>
  <div class="nav-body">
    <div class="nav-group">
      <div class="nav-h">Shop</div>
      <a data-go="products">Loose Leaf Tea</a>
      <a data-go="starter-kits">Starter Kits</a>
      <a data-go="vouchers">Gifts &amp; Bundles</a>
      <a data-go="accessories">Accessories</a>
    </div>
    <div class="nav-group">
      <div class="nav-h">Cafe &amp; Lounge</div>
      <a data-go="book">Book A Table</a>
      <a data-go="cafemenu">Cafe &amp; Lounge Menu</a>
      <a data-go="kidsmenu">Kids Menu</a>
      <a data-go="visit">Experiences</a>
    </div>
    <div class="nav-group">
      <div class="nav-h">About Us</div>
      <a data-go="story">Our Story</a>
      <a data-go="visit">Visit Us</a>
    </div>
  </div>
</nav>

<section id="hero">
  <div id="sticky">
    <video id="heroVideo" src="videos/hero.mp4" muted playsinline preload="auto" poster="images/black-tea.png"></video>
    <div class="hero-veil"></div>
    <div class="hero-center">
      <div class="hero-title">BISCUIT &amp; BREW</div>
      <div class="hero-tag">Rooted in the hills</div>
    </div>
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

<section id="favourites">
  <div class="sec-head" style="margin-bottom:0">
    <div class="sec-eyebrow">Personal Favourites</div>
    <h2 class="sec-title">Our Personal Favourites</h2>
    <p class="sec-sub">Not sure where to start with our range? Here are a few of the team's favourite blends.</p>
  </div>
  <div class="fav-grid" id="favGrid"></div>
  <button class="fav-shop" id="favShop">Shop our favourites &rarr;</button>
</section>

<section id="cafemenu">
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
</section>

<section id="kidsmenu" style="background:#0a0a14">
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

<section id="reviews">
  <div class="sec-head" style="margin-bottom:8px">
    <div class="sec-eyebrow">Reviews</div>
    <h2 class="sec-title">Hear What Our Customers Say</h2>
  </div>
  <div class="rv-ratings">
    <span class="rv-score"><span class="rv-num">4.98</span><span class="rv-stars">★★★★★</span><span class="rv-count">(42)</span></span>
    <span class="rv-verified">Verified reviews</span>
    <span class="rv-count">·&nbsp; Google 4.8 ★ · 155 reviews</span>
  </div>
  <div class="rv-grid">
    <div class="rv-card">
      <img class="rv-photo" src="images/review-teapot.jpg" alt="Customer's cast iron teapot" />
      <div class="rv-s">★★★★★</div>
      <p class="rv-q">"I'm so happy with my new teapot. The loose teas are so nice, and the customer service was excellent."</p>
      <div class="rv-prod">Loose Leaf Tea Starter Kit</div>
      <div class="rv-by"><b>Caroline Sutliffe</b> &middot; Verified</div>
    </div>
    <div class="rv-card">
      <img class="rv-photo" src="images/review-food.jpg" alt="Brunch at Biscuit &amp; Brew" />
      <div class="rv-s">★★★★★</div>
      <p class="rv-q">"Delicious food, reasonably priced, with such wonderful friendly staff &mdash; it makes you wonder why more people don't go there!"</p>
      <div class="rv-by"><b>Daniel McDonald-Smith</b> &middot; Google</div>
    </div>
    <div class="rv-card">
      <div class="rv-s">★★★★★</div>
      <p class="rv-q">"Quirky little tea shop which we loved! An amazing array of loose leaf tea, and the staff explained every flavour."</p>
      <div class="rv-by"><b>Verified guest</b> &middot; Tripadvisor</div>
    </div>
    <div class="rv-card">
      <div class="rv-s">★★★★★</div>
      <p class="rv-q">"Booked afternoon tea for a retirement &mdash; beautifully presented, a large warm scone with generous jam and clotted cream, and bottomless tea topped up as needed."</p>
      <div class="rv-by"><b>Verified guest</b> &middot; Tripadvisor</div>
    </div>
    <div class="rv-card">
      <div class="rv-s">★★★★★</div>
      <p class="rv-q">"Everything homemade and totally delicious &mdash; an amazing feast. Little teapots with the brewing time explained for each tea."</p>
      <div class="rv-by"><b>Verified guest</b> &middot; Tripadvisor</div>
    </div>
    <div class="rv-card">
      <div class="rv-s">★★★★★</div>
      <p class="rv-q">"A gem of a place &mdash; a cute little cafe with a lovely atmosphere and such friendly, attentive staff."</p>
      <div class="rv-by"><b>Google reviewer</b> &middot; Google</div>
    </div>
  </div>
  <a class="rv-cta" href="https://www.google.com/maps/search/?api=1&query=Biscuit%20%26%20Brew%20Nottingham" target="_blank" rel="noopener">Read &amp; leave a review →</a>
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

<section id="instagram">
  <div class="sec-head" style="margin-bottom:0">
    <div class="sec-eyebrow">Follow along</div>
    <h2 class="sec-title">Find Us On Instagram</h2>
    <div class="ig-handle"><a href="https://www.instagram.com/biscuitandbrew_/" target="_blank" rel="noopener">@biscuitandbrew_</a></div>
  </div>
  <div class="ig-grid">
    <a class="ig-tile" href="https://www.instagram.com/reel/DZrpOSkNASV/" target="_blank" rel="noopener">
      <video src="videos/igA.mp4" poster="images/instagram-1.jpg" autoplay muted loop playsinline preload="metadata"></video>
      <span class="ig-veil"></span>
      <span class="ig-ico">▶ Reel</span>
    </a>
    <a class="ig-tile" href="https://www.instagram.com/reel/DY2JboxNfP-/" target="_blank" rel="noopener">
      <video src="videos/igB.mp4" poster="images/instagram-2.jpg" autoplay muted loop playsinline preload="metadata"></video>
      <span class="ig-veil"></span>
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
      <a href="#" onclick="return false">Wholesale</a>
      <a href="#" onclick="return false">FAQ</a>
      <a href="#" onclick="return false">Contact Us</a>
      <a data-go="visit">Visit Us</a>
      <a href="#" onclick="return false">Returns Policy</a>
      <a href="#" onclick="return false">Privacy Policy</a>
    </div>
    <div class="fc-col">
      <h4>Reading</h4>
      <a href="#" onclick="return false">Media</a>
      <a data-go="story">Our Story</a>
      <a href="#" onclick="return false">Caffeine Guide</a>
      <a href="#" onclick="return false">How to Brew Loose Leaf Tea</a>
      <a href="#" onclick="return false">Music &amp; Tea</a>
      <a href="#" onclick="return false">Our Name</a>
    </div>
  </div>
  <div class="fc-pay">
    <span class="pay">AMEX</span><span class="pay">Apple Pay</span><span class="pay">Diners Club</span>
    <span class="pay">Discover</span><span class="pay">Google Pay</span><span class="pay">Maestro</span>
    <span class="pay">Mastercard</span><span class="pay">Shop Pay</span><span class="pay">Union Pay</span><span class="pay">Visa</span>
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
    <div class="modal-img" id="mImg"></div>
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
    <div class="modal-foot">
      <div class="qty"><button id="qMinus">&minus;</button><span id="qVal">1</span><button id="qPlus">+</button></div>
      <button class="addbtn" id="addBtn">Add to cart</button>
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

# inline the Instagram reel videos as data URIs so they autoplay offline
video_files = { "videos/hero.mp4": "videos/hero.mp4", "videos/igA.mp4": "videos/igA.mp4", "videos/igB.mp4": "videos/igB.mp4" }
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
