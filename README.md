# Cold Email Generator

![image](https://github.com/user-attachments/assets/dfe0344d-5c6c-432b-9dcb-0aa3967a9a14)

## Project Overview

The **Cold Email Generator** project is a tool that automates the process of generating personalized cold emails based on job descriptions scraped from company career pages. The application leverages **LangChain** with the **ChatGroq** model for extracting job postings and generating emails. The user's portfolio is stored in a vector store, and relevant portfolio links are attached to the emails based on the job's required skills.


## Features

- **Web Scraping**: Scrapes job descriptions from career pages.
- **Job Posting Extraction**: Extracts job details such as company name, role, experience, skills, and description using LLMs.
- **Cold Email Generation**: Generates a personalized cold email for the job, including relevant portfolio links.
- **MongoDB Integration**: Job postings and cold emails are stored in a MongoDB database.
- **Portfolio Link Matching**: Matches job-required skills with portfolio projects and adds them to the email.

## Project Structure

### 1. **Main.py**
The main file that sets up the **Streamlit** web application interface.

- **Functions**:
  - Creates the Streamlit interface where users can input a URL and generate cold emails based on job postings.
  - Scrapes job descriptions from the provided URL.
  - Loads the user's portfolio for querying relevant projects.
  - Extracts job postings from the website.
  - Generates a cold email using the job description and matching portfolio links.

### 2. **Chains.py**
This file contains the logic for interacting with the **ChatGroq** LLM and handling MongoDB storage. Responsible for extracting job descriptions and generating cold emails.
  
- **Functions**:
  - Uses a language model to extract job descriptions from scraped text.
  - Uses job description data to generate a cold email with the most relevant portfolio links.

### 3. **Portfolio.py**
This file handles the user's portfolio, which is stored in a vector database using **ChromaDB**. Manages portfolio loading and querying of relevant links based on skills.
  
- **Functions**:
  - Loads the portfolio from a CSV file and stores it in a vector database.
  - Queries the vector database for relevant portfolio links based on required skills from the job description.

### 4. **Utils.py**
This file contains utility functions for cleaning text data.

- **Functions**:
  - Cleans the raw text by removing HTML tags, URLs, special characters, and extra spaces.

### 5. **Portfolio.csv**
A CSV file containing the user's portfolio with two columns: `Techstack` and `Links`.
## Installation

### Prerequisites

- **Python 3.9+**
- **MongoDB** (locally or cloud service like MongoDB Atlas)
- **Streamlit**
- **ChromaDB**
- **LangChain**

### Environment Variables

Create a `.env` file and ensure the following environment variables are set:

- `MONGODB_URI`: MongoDB connection URI
- `GROQ_API_KEY`: API key for ChatGroq LLM

### Setup

1. Clone the repository:
    ```bash
    git clone <repo-url>
    cd <repo-directory>
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up MongoDB and ensure the correct environment variables are set in `.env`.

4. Run the Streamlit application:
    ```bash
    streamlit run main.py
    ```

## MongoDB Collections

- **job_description**: Stores the extracted job descriptions.
- **cold_emails**: Stores the generated cold emails.


## How the Application Works

1. The user enters the URL of a company's career page.
2. The application scrapes the job postings from the page and processes them with a prompt to extract details.
3. The user's portfolio is queried to find matching projects based on the skills required for the job.
4. A personalized cold email is generated that highlights the user's relevant skills and portfolio projects.
5. The cold email is displayed on the screen and stored in MongoDB.

## Future Enhancements

- **Automated Email Sending**: Integrate an email-sending service like SendGrid to send the cold emails directly.
- **Additional Job Posting Sources**: Expand scraping functionality to other job portals.
- **AI Job Matching**: Implement job recommendations based on the user's skills and past experience.
- **Enhanced Portfolio Querying**: Improve the portfolio linking by incorporating more advanced semantic search.
