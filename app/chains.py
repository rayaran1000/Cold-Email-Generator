import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv
from pymongo import MongoClient
import json

load_dotenv()

# MongoDB Connection 
MONGODB_URI = os.getenv("MONGODB_URI")
if not MONGODB_URI:
    raise ValueError("MONGODB_URI not set in environment variables")

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.1-70b-versatile")
        self.jd_collection = MongoClient(MONGODB_URI).cold_email_generator.job_description
        self.cold_email = MongoClient(MONGODB_URI).cold_email_generator.cold_emails

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `company name`, `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})

        try:
            json_parser = JsonOutputParser()
            doc = json_parser.parse(res.content)

            # Insert the data into MongoDB
            result = self.jd_collection.insert_many(doc)
            print(f"Inserted document IDs: {result.inserted_ids}")

            # Parse the result with the JSON parser
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except json.JSONDecodeError as e:
            print(f"JSON decoding failed: {e}")
            raise OutputParserException("Unable to decode JSON.")
        except OutputParserException as e:
            print(f"Output parsing failed: {e}")
            raise OutputParserException("Context too big. Unable to parse jobs.")
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You are Aranya Ray, a software engineer at Cognizant Technology Solutions.
            Over your experience, you have build multiple Data Science and Generative AI projects from scratch. 
            Your job is to write a cold email to the client regarding the job mentioned above describing the capability of yourself as a generative AI developer 
            in fulfilling their needs.
            Also add the most relevant ones from the following links to showcase your portfolio: {link_list}
            Remember you are Aranya, Software Engineer at Cognizant Technology Solutions. 
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):

            """
        )
        print(links)
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job), "link_list": links})
        self.cold_email.insert_one({"cold email": res.content})

        return res.content
