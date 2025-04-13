from query_agent import ProductFeatures
from get_product_links import scrape_trendyol
from get_product_details import get_card_details
from product_analysis_agents import product_analysis_func, review_sentiment_fun

def main():
    text = input("🔍 Ürün ve özellikleri girin: ")

    print("\n🔎 Ürünler aranıyor...")
    product_list = ProductFeatures(text)
    product_links = scrape_trendyol(product_list)
    product_details, product_comments = get_card_details(product_links)

    if not product_details:
        print("❌ Ürün bulunamadı.")
        return

    print("🧠 Ürünler analiz ediliyor...")
    product_analysis = product_analysis_func(product_details)
    product_comment_analysis = review_sentiment_fun(product_comments)


    for i, (p, c, d, l) in enumerate(zip(product_analysis, product_comment_analysis, product_details, product_links), start=1):
        print("\n" + "-"*50)
        print(f"{i}. Ürün: {d['name']}")
        print(f"💰 Fiyat: {d['price']}")
        print(f"📌 Marka: {d['brand']}")
        print(f"🔗 Ürün Linki: {l}")
        
        print("\n🧠 Yapay Zekaya göre ürünün iyi yanları: ", p.pros)
        print("\n🧠 Yapay Zekaya göre ürünün kötü yanları: ", p.cons)
        print("\n🧠 Yapay Zekaya göre ürünün önemli özellikleri: ", p.important_features)
        print("\n🧠 Yapay Zekaya göre ürünün Soru-Cevap kısmından önemli kısımlar: ", p.key_points_from_QA)
        print("\n🧠 Yapay Zekaya göre ürünün kritik detayları: ", p.crit_details)
        print("\n🧠 Yapay Zekaya göre ürün için tavsiyeler: ", p.recommendations)
        
        print("\n")
        print("💬 Yorumlara Göre Ürünün İyi Yönleri", c.praises,"\n")
        print("💬 Yorumlara Göre Ürünün Kötü Yönleri: ", c.complaints,"\n")
        print("💬 Yorumların Özeti: ", c.summary_of_comments,"\n")

if __name__ == "__main__":
    main()
