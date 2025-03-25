import os
from dotenv import load_dotenv

#load enivronment variables from .env file
load_dotenv()
gorq_key= os.getenv("API_KEY")



from langchain_groq import ChatGroq

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    groq_api_key=gorq_key

)
# response=llm.invoke("what is the capital city of Texas")
# print(response)


#web scraping the job details
from langchain_community.document_loaders import WebBaseLoader
loader = WebBaseLoader("https://careers.ace.aaa.com/us/en/job/JR202526566/Sr-Data-Scientist")
page_data= loader.load().pop().page_content
print(page_data)