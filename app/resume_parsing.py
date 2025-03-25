# resume_parsing.py

from docx import Document
from langchain.docstore.document import Document as LCDocument
from langchain.text_splitter import RecursiveCharacterTextSplitter, SentenceTransformersTokenTextSplitter
import chromadb
from chromadb.utils import embedding_functions 

import os

class ResumeParser:
    def __init__(self, collection_name="resume-context"):
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction()

        # Create Chroma client (in-memory)
        self.chroma_client = chromadb.Client()

        # Create or get the collection
        self.collection_name = collection_name
        self.collection = self.chroma_client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=self.embedding_function
        )

    def parse_resume(self, file_obj):
        """Extracts text from .docx file."""
        doc = Document(file_obj)
        return "\n".join([p.text for p in doc.paragraphs])

    def chunk_resume(self, resume_text):
        # Step 1: Character-based split
        char_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        char_chunks = char_splitter.split_text(resume_text)

        # Step 2: Token-based split
        token_splitter = SentenceTransformersTokenTextSplitter(chunk_overlap=5, tokens_per_chunk=20)
        token_chunks = []
        for chunk in char_chunks:
            token_chunks += token_splitter.split_text(chunk)

        # Step 3: Wrap into LangChain Documents
        return token_chunks


    def embed_resume(self, documents):
        """Stores resume chunks in ChromaDB."""
        ids=[str(i) for i in range(len(documents))]
        self.collection.add( ids= ids, documents= documents)

    def candidate_name_extract(self):

        candidate_name_retrived= self.collection.query(query_texts="what is the name of the person in the resume?", n_results=2)
        candidated_name="".join(candidate_name_retrived["documents"][0])
        return candidated_name

    def candidate_skills_extract(self, job_description):

        candidate_skills_retrived= self.collection.query(query_texts=job_description['skills'], n_results=5)
        candidate_skills= "".join(candidate_skills_retrived["documents"][0])
        return candidate_skills
