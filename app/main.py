# app.py

import streamlit as st
from resume_parsing import ResumeParser
from langchain_community.document_loaders import WebBaseLoader
from cleaned_text import clean_text
from chains import Chain
import uuid


def email_gererator_app(llm, resume_parser):
    st.title("Cold Email generator for Hiring Manager")

    uploaded_file = st.file_uploader("Upload your resume (.docx)", type=["docx"])
    url_input=st.text_input("Enter a URL")
    submit_button= st.button("Submit")

    if url_input and uploaded_file and submit_button:
        try:
            st.code("🔁 Step 1: Starting job scraping...")

            loader = WebBaseLoader(url_input)
            st.code("✅ Step 2: Loaded job description from URL")

            job_posting_extracted = clean_text(loader.load().pop().page_content)
            st.code("✅ Step 3: Cleaned job description text")

            


            job_description = llm.extract_job(job_posting_extracted)
            st.code("✅ Step 4: Extracted job info using LLM")

            # Debugging output for job description
            st.code(f"📄 Job Description:\n{job_description}")

            # Extracting the text from the uploaded resume
            extracted_resume_text = resume_parser.parse_resume(uploaded_file)
            st.code("✅ Step 5: Extracted resume text from DOCX")

            # Chunking the resume
            resume_tokenized_chunks = resume_parser.chunk_resume(extracted_resume_text)
            st.code("✅ Step 6: Tokenized resume into chunks")

            # Embed resume into ChromaDB
            resume_parser.embed_resume(resume_tokenized_chunks)
            st.code("✅ Step 7: Embedded resume into vector store")

            # Extract candidate info
            candidate_name = resume_parser.candidate_name_extract()
            st.code(f"✅ Step 8: Extracted candidate name: {candidate_name}")

            candidate_skills = resume_parser.candidate_skills_extract(job_description)
            st.code(f"✅ Step 9: Extracted candidate skills: {candidate_skills}")

            # Generate email
            st.code(f"job description read", str(job_description))
            email_content = llm.write_mail(job_description, candidate_name, candidate_skills)
            st.code("✅ Step 10: Email generated successfully 📨", language="markdown")

            # Show email content
            st.markdown("### ✉️ Final Email:")
            st.code(email_content, language="markdown")
        except Exception as err:
            st.error(f"An Error Occurred: {err}")

            



if __name__=="__main__":
    chain_obj= Chain()
    resume_parser_obj= ResumeParser()
        # Ask user to enter name or email
    user_identifier = st.text_input("Enter your name or email (for session tracking):")

    # Generate a session ID based on input or UUID fallback
    if user_identifier:
        user_session_id = user_identifier.strip().replace(" ", "_").lower()
    else:
        user_session_id = str(uuid.uuid4())[:8]  # fallback

    st.set_page_config(layout="wide", page_title="Cold email generator")
    email_gererator_app(chain_obj, resume_parser_obj)
