from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from pydantic import BaseModel, Field
from typing import Optional, List
import logging
import os

class ProductAnalysResults(BaseModel):
    pros: list[str]
    cons: list[str]
    important_features: list[str]
    key_points_from_QA: list[str]
    crit_details: list[str]
    recommendations: list[str]
    

def product_analysis_func(product_analysis: list) -> list[ProductAnalysResults]:
    product_analysis_agent = Agent(
        'gpt-4o-mini',
        deps_type=list,
        result_type=ProductAnalysResults,
        system_prompt=(
            "You are a Experienced Product Analyst. You will analyze user reviews, Q&A, and product features provided for a given product and offer the user a summary with valuable information about the product."
            "Your goal is to provide the user with the following:"
            "Identify the pros and cons of the product."
            "Highlight the important features of the product."
            "Emphasize key points from the Q&A section about the product."
            "Provide the user with critical details and recommendations."
            "Pay attention to the key terms mentioned in the reviews and Q&A. Effectively analyze both positive and negative feedback. Also, mention product features that are frequently mentioned in the questions."
            "Be objective and concise in your review."
            "Do it in Turkish Language"
        )
    )

    @product_analysis_agent.system_prompt
    async def add_product(ctx: RunContext[list]) -> str:
        return f"The given product and its features {ctx.deps}"
    
    analysies = []
    for i in product_analysis:
        result = product_analysis_agent.run_sync("Give me detailed information about product", deps=i)
        analysies.append(result.data)
    
    return analysies
    
class ReviewSentimentResults(BaseModel):
    praises: List[str] = Field(
        description="List of frequently mentioned positive feedback or compliments about the product."
    )
    complaints: List[str] = Field(
        description="List of frequently mentioned problems, criticisms, or complaints about the product."
    )
    summary_of_comments: str = Field(
        description="A short natural language summary describing the overall impression of the product based on customer reviews."
    )
    
    
def review_sentiment_fun(product_reviews: List = None) -> List[ReviewSentimentResults]:
    review_sentiment_agent = Agent(
        'gpt-4o-mini',
        deps_type=List,
        result_type=ReviewSentimentResults,
        system_prompt="You are a Senior Review Sentiment Analyzer."
        "Your task is to analyze customer reviews about a product and determine the overall sentiment, most common positive aspects, and most common negative aspects."
        "Analyze the reviews carefully. Focus on common patterns or repeating opinions. Be objective and concise in your summary."
        "Do it in Turkish Language"
    )
    
    @review_sentiment_agent.system_prompt
    async def reviews(ctx: RunContext[List]) -> str:
        return f"The given reviews is {ctx.deps}"
    
    results = []
    for product_review in product_reviews:
        result = review_sentiment_agent.run_sync("Give me detailed information about reviews", deps=product_review)
        results.append(result.data)
    return results