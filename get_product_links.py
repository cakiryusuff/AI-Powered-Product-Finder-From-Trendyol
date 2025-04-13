from playwright.sync_api import sync_playwright
from query_agent import ProductAnalysis, ProductFeatures

import logging
import json
import time

logging.basicConfig(
    level=logging.INFO,  # DEBUG ile daha fazla detay alabilirsin
    format='[%(asctime)s] [%(levelname)s] - %(message)s',
    handlers=[
        logging.FileHandler("app.log", mode='a', encoding='utf-8'),
        logging.StreamHandler()  # Konsola da yazdırır
    ]
)

logger = logging.getLogger(__name__)

def scrape_trendyol(product_features: ProductAnalysis) -> list:
    logger.info(f"Scrape işlemi başlatıldı: {product_features}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        search_url = f"https://www.trendyol.com/sr?q={product_features.query}"
        logger.info(f"Açılan URL: {search_url}")
        page.goto(search_url, wait_until="load")

        page.wait_for_timeout(3000)

        try:
            page.click('#onetrust-accept-btn-handler', timeout=7000)
            page.wait_for_timeout(1000)
            logger.info("Çerez onayı başarıyla verildi.")
        except Exception as e:
            logger.warning("Çerez onaylanırken hata oluştu.", exc_info=True)

        if product_features.color:
            try:
                logger.info(f"Renk filtresi uygulanıyor: {product_features.color}")
                page.click('div.fltrs-wrppr.hide-fltrs div.fltr-cntnr-ttl:has-text("Renk")', timeout=7000)
                page.wait_for_timeout(2000)
                page.click(f'a[title="{product_features.color.title()}"]', timeout=7000)
                page.wait_for_timeout(2000)
                page.click('div.fltr-item-text', timeout=7000)
                page.wait_for_timeout(2000)
                logger.info(f"Renk filtresi başarıyla uygulandı: {product_features.color}")
            except Exception as e:
                logger.warning(f"Renk filtresi uygulanırken hata oluştu: {product_features.color}", exc_info=True)

        if product_features.material:
            try:
                logger.info(f"Materyal filtresi uygulanıyor: {product_features.material}")
                page.click('div.fltrs-wrppr.hide-fltrs div.fltr-cntnr-ttl:has-text("Materyal")', timeout=7000)
                page.wait_for_timeout(1000)
                page.click(f'div[role="gridcell"] a.fltr-item-wrppr:has-text("{product_features.material.title()}")', timeout=7000)
                logger.info(f"Materyal filtresi başarıyla uygulandı: {product_features.material}")
            except Exception as e:
                logger.warning(f"Materyal filtresi uygulanırken hata oluştu: {product_features.material}", exc_info=True)

        if product_features.min_price is not None and product_features.max_price is not None:
            try:
                logger.info(f"Fiyat filtresi uygulanıyor: min={product_features.min_price}, max={product_features.max_price}")
                page.wait_for_timeout(1000)
                page.click('div.fltrs-wrppr.hide-fltrs div.fltr-cntnr-ttl:has-text("Fiyat")', timeout=7000)
                page.wait_for_timeout(1000)
                page.fill('input.fltr-srch-prc-rng-input.min', str(product_features.min_price), timeout=7000)
                page.wait_for_timeout(1000)
                page.fill('input.fltr-srch-prc-rng-input.max', str(product_features.max_price), timeout=7000)
                page.wait_for_timeout(1000)
                page.click('button.fltr-srch-prc-rng-srch', timeout=7000)
                page.wait_for_timeout(2000)
                logger.info("Fiyat filtresi başarıyla uygulandı.")
            except Exception as e:
                logger.warning("Fiyat filtresi uygulanırken hata oluştu.", exc_info=True)

        page.click('div.selected-order:has-text("Önerilen")', timeout=7000)
        page.wait_for_timeout(2000)
        page.click('span.search-dropdown-text:has-text("En çok değerlendirilen")', timeout=7000)
        page.wait_for_timeout(4000)

        cards = page.query_selector_all("div.p-card-wrppr.with-campaign-view")
        logger.info(f"Toplam {len(cards)} ürün kartı bulundu.")

        # TODO: GET ALL PRODUCTS PRICE FOR COMPARE
        
        product_links = []
        for i, card in enumerate(cards[:1]):
            try:
                link_element = card.query_selector("a")
                if link_element:
                    href = link_element.get_attribute("href")
                    full_link = f"https://www.trendyol.com{href}"
                    product_links.append(full_link)
                    logger.info(f"{i+1}. Ürün linki: {full_link}")
                    print(f"{i+1}. Ürün linki: {full_link}")
                else:
                    logger.warning(f"{i+1}. kartta <a> etiketi bulunamadı.")
            except Exception as e:
                logger.error(f"{i+1}. kart işlenirken hata oluştu.", exc_info=True)
                
        browser.close()
        logger.info("Tarayıcı kapatıldı. Scraping işlemi tamamlandı.")
        
        return product_links
