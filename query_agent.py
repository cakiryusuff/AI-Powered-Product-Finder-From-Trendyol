from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic import BaseModel, Field
from typing import Optional
import logging
import os

load_dotenv()

logger = logging.getLogger(__name__)

class ProductAnalysis(BaseModel):
    product_name: str
    category: str = Field(description="Category of wanted product")
    min_price: Optional[int] = Field(default=0, description="Set the min price to 0 if not mentioned.")
    max_price: Optional[int] = None
    query: str = Field(description="Clean query for search of product")
    color: Optional[str] = Field(default=None, description="Optional color filter for product")
    material: Optional[str] = Field(default=None, description="Optional material filter for product")

def ProductFeatures(prompt: str = 'I want a black stainless steel thermos bottle for hiking, under 300 TL.') -> ProductAnalysis:
    logger.info("-"*50)
    logger.info(f"Kullanıcıdan gelen doğal dil sorgusu: {prompt}")

    query_agent = Agent(
        'gpt-4o-mini',
        result_type=ProductAnalysis,
        system_prompt=(
            "You are an intelligent Query Parsing Agent. "
            "Your task is to analyze the user's search query written in natural language and extract the structured information needed to find the most relevant product on an e-commerce platform like Trendyol. "
            "Focus on identifying key elements such as: "
            "- Product name or category "
            "- Desired features (e.g., color, size, brand, capacity, material) "
            "- Price range (if mentioned) "
            "- User intent (e.g., cheapest, best rated, most popular) "
            "- Any other relevant filters "
            "Do it in Turkish Language"
        )
    )

    try:
        result = query_agent.run_sync(prompt)
        logger.info("Query Agent başarılı şekilde çalıştı.")
        logger.debug(f"Agent çıktısı: {result}")
        return result.data
    except Exception as e:
        logger.error("Query Agent çalışırken bir hata oluştu.", exc_info=True)
        raise e
