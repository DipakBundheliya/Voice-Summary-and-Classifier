import numpy as np
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq


class my_summarizer:

    def __init__(self):
        self.audio_file = "audio_file"
        self.groq_api_key = "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"
    def summarize(self , text):
        chat = ChatGroq(temperature=0 , model_name="llama3-70b-8192" , api_key="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")

        system2 = "You are text summarizer , summarize this content"
        human="{text}"
        prompt = ChatPromptTemplate.from_messages([("system", system2), ("human", human)])

        chain = prompt | chat
        return chain.invoke({"text" : text}).content
    

