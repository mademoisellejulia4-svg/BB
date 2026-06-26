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
  /* ===== STANDALONE STATIC HERO (offline, no video) ===== */
  #hero{ height:100vh; }
  #sticky{ position:relative; }
  .hero-bg{ position:absolute; inset:0; background-size:cover; background-position:center;
    animation:heroZoom 18s ease-in-out infinite alternate; }
  @keyframes heroZoom{ from{ transform:scale(1.02);} to{ transform:scale(1.12);} }
  .hero-veil{ position:absolute; inset:0;
    background:radial-gradient(120% 90% at 50% 40%, rgba(3,3,3,0.35), rgba(3,3,3,0.85) 80%); }
  .hero-center{ position:absolute; inset:0; display:flex; flex-direction:column;
    align-items:center; justify-content:center; text-align:center; padding:0 24px; }
  .hero-title{ font-family:'Cormorant Garamond',serif; font-weight:500;
    font-size:clamp(40px,11vw,120px); letter-spacing:.22em; padding-left:.22em;
    color:rgba(var(--amber-rgb),0.92); text-shadow:0 2px 50px rgba(0,0,0,0.7); }
  .hero-tag{ margin-top:18px; font-family:'Cormorant Garamond',serif; font-style:italic;
    font-size:clamp(18px,3.4vw,30px); color:rgba(255,255,255,0.82);
    text-shadow:0 2px 24px rgba(0,0,0,0.7); }

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

  /* promo banner */
  document.body.classList.add('promo-on');
  $('#promoX').addEventListener('click',()=>{ document.body.classList.remove('promo-on'); $('#promo').style.display='none'; });

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

  buildCategories(); renderCart();
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
  <span><b>20% off</b> your first order when you subscribe to the mail list</span>
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
      <a data-go="cafemenu">Cafe &amp; Lounge Menu</a>
      <a data-go="kidsmenu">Kids Menu</a>
      <a data-go="visit">Experiences</a>
      <a data-go="visit">Events</a>
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
    <div class="hero-bg" style="background-image:url('__HERO__')"></div>
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
        <div class="v-row"><span>Mon</span><span>Closed</span></div>
        <div class="v-row"><span>Tue &ndash; Sat</span><span>9:00 &ndash; 17:00</span></div>
        <div class="v-row"><span>Sun</span><span>10:00 &ndash; 16:00</span></div>
      </div>
    </div>
    <div class="visit-col">
      <div class="v-eyebrow">Experiences</div>
      <h3>Afternoon Tea</h3>
      <p>Book the full afternoon tea experience &mdash; scones, finger sandwiches, cake and a pot of loose leaf tea &mdash; or join one of our guided tea-tasting events. Booking online, or gift it with a voucher.</p>
    </div>
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
  <h2>Join our Tea Club.</h2>
  <p class="nsub">Exclusives, news, gossip &amp; tea talk.</p>
  <form class="nl-form" id="nlForm">
    <input type="email" id="nlEmail" placeholder="Your email" required />
    <button type="submit" class="nl-begin">BEGIN &rarr;</button>
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
      <a data-go="visit">Book A Table</a>
      <a data-go="visit">Cafe &amp; Lounge Menu</a>
      <a data-go="visit">Afternoon Tea</a>
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
    <div class="modal-desc" id="mDesc"></div>
    <div class="modal-vlabel" id="mVlabel">Select size</div>
    <div class="modal-variants" id="mVariants"></div>
    <div class="modal-foot">
      <div class="qty"><button id="qMinus">&minus;</button><span id="qVal">1</span><button id="qPlus">+</button></div>
      <button class="addbtn" id="addBtn">Add to cart</button>
    </div>
  </div>
</div>
<div id="toast"></div>

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
video_files = { "videos/igA.mp4": "videos/igA.mp4", "videos/igB.mp4": "videos/igB.mp4" }
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
