from playwright.sync_api import sync_playwright
import logging
import json
import time

logger = logging.getLogger(__name__)

def smooth_auto_scroll(page, max_scrolls=100, step_size=300, scroll_delay=0.5):
    for i in range(max_scrolls):
        page.evaluate(f"""() => {{
            window.scrollBy(0, {step_size});
        }}""")
        time.sleep(scroll_delay)

        reached_bottom = page.evaluate("""() => {
            return (window.innerHeight + window.scrollY) >= document.body.scrollHeight;
        }""")
        if reached_bottom:
            break

def convert_to_review_url(product_url: str) -> str:
    if '/yorumlar' in product_url:
        return product_url.split('?')[0]
    
    base_url = product_url.split('?')[0]
    
    return f"{base_url}/yorumlar"

def safe_text(parent, selector):
    try:
        el = parent.query_selector(selector)
        return el.inner_text().strip() if el else None
    except:
        return None

def get_basic_info(page, link):
    product_info = {"product_link": link}
    product_info["price"] = safe_text(page, "div.product-price-container span.prc-dsc")
    product_info["brand"] = safe_text(page, "a.product-brand-name-with-link")
    product_info["name"] = safe_text(page, "h1.pr-new-br span")

    attributes = {}
    li_elements = page.query_selector_all("li.detail-attr-item")
    for li in li_elements:
        key = safe_text(li, "span.attr-name.attr-key-name-w")
        value = safe_text(li, "div.attr-name.attr-value-name-w")
        if key and value:
            attributes[key] = value
    product_info["attributes"] = attributes
    return product_info

def get_qna(page):
    qna = []
    page.wait_for_timeout(2000)
    try:
        page.click('button.navigate-all-questions-btn', timeout=7000)
        page.wait_for_timeout(2000)
        div_qa_elements = page.query_selector_all("div.qna-item")
        for div in div_qa_elements:
            question = safe_text(div, "div.item-content h4")
            answer = safe_text(div, "div.answer h5")
            qna.append({"question": question, "answer": answer})
        return qna
    except Exception:
        logging.warning("❗ Soru-cevap verisi alınamadı.")
        return []
    
def get_comments(page, product_url):
    comments_url = convert_to_review_url(product_url)
    page.goto(comments_url, wait_until="load")
    page.wait_for_timeout(3000)

    button = page.query_selector('button.reviews-onboarding-complete-button')
    if button:
        button.click(timeout=7000)
    
    comments = []
    for star in [5, 4, 3, 2, 1]:
        try:
            page.click("div.dropdown-label:has-text('Puan')")
            page.wait_for_timeout(1000)

            clear_button = page.query_selector("button.btn.btn-clear:has-text('Temizle')")
            if clear_button:
                clear_button.click()
                page.wait_for_timeout(1000)
        except Exception as e:
            logging.info("🔹 Temizleme aşaması atlandı: Temizle butonu yok veya zaten temiz.")

        star_selector = f"span.ps-stars-rate:has-text('{star}.0')"
        if not page.query_selector(star_selector):
            logging.info(f"⚠️ {star} yıldız filtresi mevcut değil, atlanıyor.")
            page.click("div.dropdown-label:has-text('Puan')")
            continue

        try:
            page.click(star_selector)
            page.wait_for_timeout(1000)
            page.click("button.btn.btn-apply:has-text('Uygula')")
            page.wait_for_timeout(1000)

            logging.info(f"🌟 {star} yıldızlı yorumlar çekiliyor...")
            smooth_auto_scroll(page, max_scrolls=10, step_size=400, scroll_delay=0.5)
            div_comment_elements = page.query_selector_all("div.comment")

            for div in div_comment_elements[:50]:  # En fazla 50 yorum
                comment_text = safe_text(div, "div.comment-text p")
                star_divs = div.query_selector_all("div.star-w div.full")
                stars = 0
                for star in star_divs:
                    if "width: 100%; max-width: 100%;" in star.get_attribute("style"):
                        stars += 1 
                comments.append({"comment": comment_text, "stars": stars})
        except Exception as e:
            logging.warning(f"❌ {star} yıldızlı yorumlar çekilirken hata oluştu: {e}")
    return comments

def save_to_json(data, filename="product_data.json"):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        logging.info(f"💾 Veriler '{filename}' dosyasına kaydedildi.")
    except Exception as e:
        logging.error(f"❌ JSON dosyasına yazma hatası: {e}")

def get_card_details(product_links: list):
    logging.info("🟡 Ürün detaylarını alma işlemi başlatıldı.")
    all_products = []
    all_comments = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        for link in product_links:
            try:
                logging.info(f"🔗 Açılan URL: {link}")
                page.goto(link, wait_until="load")

                product_info = get_basic_info(page, link)
                logging.info(f"📦 Ürün: {product_info['brand']} {product_info['name']} - {product_info['price']}")

                # TODO: Get product descriptions from site given by seller 
            
                product_info["qna"] = get_qna(page)
                logging.info(f"🔉 {len(product_info['qna'])} Soru ve Cevap toplandı.")

                comments = get_comments(page, link)
                all_comments.append(comments)
                logging.info(f"💬 {len(comments)} yorum toplandı.")

                all_products.append(product_info)
                logging.info("✅ Ürün başarıyla işlendi.")

            except Exception as e:
                logging.error(f"❌ Ürün detayları alınırken hata oluştu: {e}")

    save_to_json(all_products)
    return all_products, all_comments