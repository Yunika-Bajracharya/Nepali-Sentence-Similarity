from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware  # Import CORSMiddleware
from typing import List
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine
from collections import defaultdict

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update this with your frontend URL
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)
    
# Load the pre-trained multilingual sentence transformer model
model = SentenceTransformer("Yunika/muril-base-sentence-transformer")

# Sample FAQ data (Nepali language)
faq_data = [
    {"question": "What services do you provide?", "answer": "We offer AI and software development services."},
    {"question": "तपाईंको सेवा कति समयदेखि उपलब्ध छ?", "answer": "हामी सेवा २४/७ उपलब्ध छौं।"},
    {"question": "How did your company earn credibility?", "answer": "Our company has earned credibility from customers for our expertise, capabilities, and responsive services."},
    {"question": "तपाईंको कम्पनीले डाटा विज्ञान र मेशिन लर्निङमा कसरी सहयोग गर्दछ?", "answer": "हामी अनुभवी विशेषज्ञहरूसंग सहयोग गर्दछौं र स्थानिय र विशेषज्ञ अनुसन्धान गर्दछौं।"},
    {"question": "How do you ensure the security and privacy of our data?", "answer": "YWe prioritize data security and privacy by implementing robust encryption protocols and stringent access controls."},
    {"question": "तपाईंको कम्पनीको मूल्यांकन प्रक्रिया कसरी छ?", "answer": "हामी ग्राहकहरूको प्रतिपूर्ति, अभिज्ञता र साथिहरूको सहयोगमा भर गरिएको छ।"},
    {"question": "Do you offer custom AI solutions tailored to our specific business needs?", "answer": "solutely! We specialize in developing custom AI solutions tailored to meet the unique requirements and challenges of each client's business environment."},
    {"question": "तपाईंको कम्पनीमा गर्ने क्षमता परीक्षण सेवा कुन-कुन हुन्छ?", "answer": "हामी सांदर्भिक परिस्थितिमा क्षमता परीक्षण, परिणाम विश्लेषण, और उपायको विश्लेषण प्रदान गर्दछौं।"},
    {"question": "How do you handle updates and maintenance of AI systems post-deployment?", "answer": "We provide ongoing support, updates, and maintenance services to ensure the optimal performance and reliability of your AI systems even after deployment."},
    {"question": "तपाईंले पूरा गरेका सफल AI परियोजनाहरूको उदाहरण प्रदान गर्न सक्छन्?", "answer": "निश्चितै! हामी सफलतापूर्वक AI समाधानहरू विभिन्न उद्योगमा लागू गरेका छौं, जसमा स्वास्थ्य सेवा, वित्त, र ई-कमर्स समेत छ। उदाहरणहरूमा व्यक्तिगत सिफारिस प्रणालीहरू, धनपरीक्षण एल्गोरिदमहरू, र चिकित्सा छवि विश्लेषण उपकरणहरू समावेश छ।"},
    {"question": "What is your approach to project management and communication?", "answer": "We follow agile methodologies for project management and maintain regular communication with our clients through scheduled meetings, progress reports, and collaborative tools"}
]    


# Encode all the FAQ questions using the pre-trained model
faq_embeddings = model.encode([faq["question"] for faq in faq_data])

# Create a dictionary to map embeddings to FAQ data
embedding_to_faq = defaultdict(list)
for i, embedding in enumerate(faq_embeddings):
    embedding_to_faq[tuple(embedding)].append(faq_data[i])

@app.get("/faq-data/")
async def get_faq():
    return faq_data

@app.get("/faq-search/")
async def search_faq(query: str = Query(..., description="Search query")):
    # Encode the user query
    query_embedding = model.encode([query])[0]

    # Perform similarity search
    similarities = [1 - cosine(query_embedding, faq_embedding) for faq_embedding in faq_embeddings]

    # Get the most similar FAQ question and its corresponding answer
    most_similar_idx = similarities.index(max(similarities))
    most_similar_faq = embedding_to_faq[tuple(faq_embeddings[most_similar_idx])][0]

    return {"question": most_similar_faq["question"], "answer": most_similar_faq["answer"], "score": max(similarities)}
