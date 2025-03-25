import os
from dotenv import load_dotenv
from pathlib import Path
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser


# Load .env from project root
load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / '.env')
gorq_key= os.getenv("API_KEY")


class Chain:

    def __init__(self):
        self.llm= ChatGroq( model="llama-3.1-8b-instant",
        temperature=0,
        groq_api_key=gorq_key)

    def extract_job(self, job_posting_extracted):
        prompt_extract = PromptTemplate.from_template(
                    """  
                        ### SCRAPED TEXT FROM WEBSITE:
                        {page_data}
                        ### INSTRUCTION:
                        The scraped text is from the career's page of a website.
                        Your job is to extract the deatils about the job and return them in JSON format containing the 
                        following keys: `role`, `experience`, `skills` and `description' and if you have required and good_to_have the dont mention them seperately as key instead make it as a list.
                        I dont want you to mention keys other than the above mentioned keys and I dont want the nested json
                        Only return the valid JSON.
                        ### VALID JSON (NO PREAMBLE):    
                """
                )

        chain_extract = prompt_extract | self.llm
        job_description_scraped = chain_extract.invoke(input={'page_data': job_posting_extracted})

        try:               
            json_parser = JsonOutputParser()
            job_description= json_parser.parse(job_description_scraped.content)
            return job_description
        except Exception as err:
            print("Encountred the error while parsing the job", err)

        
    def write_mail(self, job_description, candidated_name, candidate_skills):
                prompt_email = PromptTemplate.from_template(
                """  
                ### JOB DESCRIPTION:
                {job_description}

                ### CANDIDATE skills:
                {candidate_skills}

                ### Candidate Name:
                {candidate_name}

                ### INSTRUCTION:
                Write a professional and short concise email to the hiring manager expressing interest in the above job. 
                start with the name and introduction of the candidate’s and highlight relevant skills and experience from the resume that align with the job description.
                The tone should be enthusiastic, confident, and tailored to the job.

                ### EMAIL (NO PREAMBLE):
                """
            )


                chain_email = prompt_email | self.llm
                email_for_hiring_manager = chain_email.invoke({"job_description": str(job_description), "candidate_skills" : candidate_skills, "candidate_name" : candidated_name})
                return email_for_hiring_manager.content


if __name__=="__main__":
    print(gorq_key)
