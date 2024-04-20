# FAQ Search Application

It allows users to search for frequently asked questions (FAQs) using a multilingual sentence transformer model to find the most relevant FAQ question and its corresponding answer based on the user query.

_This project is done as a part of **Human Language Technologies** elective course._

## [Demo](https://youtu.be/4kJYUkWfp04?feature=shared)

## Problem Statement

Many companies often receive a large number of similar questions from their clients. Manually answering these questions can be time-consuming and inefficient. Similarly, it can be time-consuming for users to search through a long list of FAQs. Therefore, there is a need for an automated system that can quickly provide relevant answers to user queries.

## Solution

This project provides a solution by building a web application that utilizes a sentence transformer model to understand the semantic similarity between user queries and FAQ questions. By encoding both the user query and FAQ questions into high-dimensional embeddings, the model can efficiently compute similarity scores and retrieve the most relevant FAQ.

## How to Use

1. Clone the repository to your local machine:

```bash
git clone https://github.com/your-username/faq-search-web-app.git
cd faq-search-web-app
```

2. Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

3. Start the FastAPI backend server:

```bash
uvicorn main:app --reload
```

4. Open the frontend React app in a separate terminal:

```bash
cd frontend
npm install
npm start
```

5. Open your web browser and navigate to [http://localhost:3000](http://localhost:3000) to access the FAQ search web app.
