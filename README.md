# 🛍️ AI-Powered Product Finder From Trendyol

AI-powered product analysis and recommendation system for Trendyol. It analyzes product features and user reviews using intelligent agents to help users find the most suitable products based on their preferences.

![](https://github.com/cakiryusuff/AI-Powered-Product-Finder-From-Trendyol/blob/main/readme_video/trendyolproject.gif)

## 📌 Features

- 🔎 Natural language product search (e.g. "Siyah kol çantası en fazla 2000 TL")
- 🤖 Intelligent product filtering and analysis
- 💬 Sentiment analysis on user reviews
- 🧠 Smart summary of each product
- 🔗 Direct product links to Trendyol

## 🧠 How It Works

1. **User Input**: The user enters a product description and optional preferences.
2. **Query Agent**: Extracts product features using a language model.
3. **Web Scraping**: Finds matching products from Trendyol.
4. **Product Detail Agent**: Retrieves name, price, brand, and other features.
5. **Analysis Agent**: Summarizes and ranks the products.
6. **Sentiment Agent**: Analyzes the sentiment of customer reviews.

---

## 🚀 Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/AI-Powered-Product-Finder-From-Trendyol.git
cd AI-Powered-Product-Finder-From-Trendyol
```

2. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install required packages:
   
```bash
pip install -r requirements.txt
```

## ⚙️ Usage (Terminal)

Simply run the main file:

```bash
python app.py
```

You'll be asked to enter a product query in natural language. The application will scrape Trendyol and show product summaries and sentiment insights in the terminal.
