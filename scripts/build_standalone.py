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
  const NAV_CAT={ vouchers:1, matcha:1 };
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
      <a data-go="vouchers">Gifts &amp; Bundles</a>
      <a data-go="matcha">Accessories</a>
    </div>
    <div class="nav-group">
      <div class="nav-h">Cafe &amp; Lounge</div>
      <a data-go="visit">Cafe &amp; Lounge</a>
      <a data-go="visit">Experiences</a>
      <a data-go="visit">Events</a>
    </div>
    <div class="nav-group">
      <div class="nav-h">About Us</div>
      <a data-go="visit">Our Story</a>
      <a data-go="footcols">Visit Us</a>
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
      <a href="#" onclick="return false">Our Story</a>
      <a href="#" onclick="return false">Caffeine Guide</a>
      <a href="#" onclick="return false">How to Brew Loose Leaf Tea</a>
      <a href="#" onclick="return false">Music &amp; Tea</a>
      <a href="#" onclick="return false">Our Name</a>
    </div>
  </div>
</section>

<footer>
  <div class="f-left">BISCUIT &amp; BREW</div>
  <div class="f-center">&copy; 2026 BISCUIT &amp; BREW &middot; Rooted in the hills.</div>
  <div class="f-right"><a href="#" onclick="return false">Instagram</a> &nbsp;&bull;&nbsp; <a href="#" onclick="return false">Facebook</a></div>
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

out = os.path.join(PUB, "biscuit-and-brew-ipad.html")
with open(out, "w") as f:
    f.write(HTML)
print("WROTE", out, f"({len(HTML)//1024} KB)")
