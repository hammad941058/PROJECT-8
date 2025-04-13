import os
from dotenv import load_dotenv
from langchain import OpenAI, LLMChain, PromptTemplate
from newsapi import NewsApiClient
from langchain.chat_models import ChatOpenAI

#load env variables

load_dotenv()

#access api keys

open_api_key = "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"
if not open_api_key:
    raise ValueError("OpenAI API Key not found! Check your .env file.")

newsapi_key = os.getenv("NEWS_API_KEY")

#initilize the openAI API

openai = ChatOpenAI(openai_api_key=open_api_key)
#define the langchain template

template = """"
you are an AI assistant helping for finding the sentiment on news articles given that the following news
article, analyze it's sentiment(positive, negative and neutral)
"""
"""Article:{article}"""

prompt = PromptTemplate(
    template="""You are an AI assistant analyzing news sentiment. 
    Given the following news article, analyze its sentiment (positive, negative, neutral).

    Article: {article}""",
    input_variables=['article']
)

llm_chain = LLMChain(prompt=prompt, llm=openai)

#initilize Newsapi

newsapi = NewsApiClient(api_key=newsapi_key)

def get_news_article(query):
    articles = newsapi.get_everything(q=query, language='en', sort_by='relevancy')
    return articles.get('articles', [])


def extract_article_content(articles):
    content = []
    for i in articles:
        content.append(i['content'])  # Remove return inside the loop
    return content  # Return the entire list after loop

def analyze_sentiment(query):
    articles = get_news_article(query)
    content = extract_article_content(articles)

    if content:
        article_text = content[0]
        result = llm_chain.run({'article':article_text})

        return result
    else:
        return "No article found for the given query!!! try some another query"

