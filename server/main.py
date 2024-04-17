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
# model = SentenceTransformer("Yunika/muril-base-sentence-transformer")
model = SentenceTransformer('sbastola/muril-base-cased-sentence-transformer-snli-nepali-2')

# Sample FAQ data (Nepali language)
faq_data = [
    {"question": "What services do you provide?", "answer": "We offer AI and software development services."},
    # {"question": "तपाईंको सेवा कति समयदेखि उपलब्ध छ?", "answer": "हामी सेवा २४/७ उपलब्ध छौं।"},
    {"question": "What is your focus on research and keeping up with latest technologies?", "answer": "We have a dedicated research and development team that continuously monitors the latest advancements and best practices in AI technology, ensuring that our solutions are always at the forefront of innovation."},
    {"question": "How do you ensure the security and privacy of our data?", "answer": "We prioritize data security and privacy by implementing robust encryption protocols and stringent access controls."},
    {"question": "हाम्रो टोलीलाई तपाइँ प्रशिक्षण प्रदान गर्नुहुन्छ?", "answer": "हामी एआई समाधानहरूलाई प्रभावकारी रूपमा प्रयोग गर्न तपाईंको टोली आवश्यक सीप र ज्ञानले सुसज्जित छ भनी सुनिश्चित गर्न व्यापक प्रशिक्षण सत्रहरू र निरन्तर समर्थन प्रस्ताव गर्दछौं।"},
    {"question": "Do you offer custom AI solutions tailored to our specific business needs?", "answer": "Absolutely! We specialize in developing custom AI solutions tailored to meet the unique requirements and challenges of each client's business environment."},
    {"question": "तपाईं AI एल्गोरिदम र निर्णय प्रक्रियाहरूमा पारदर्शिताको कुन स्तर प्रदान गर्नुहुन्छ?", "answer": "हामी पारदर्शितामा विश्वास गर्छौं र विश्वास र समझलाई बढाउँदै हाम्रा ग्राहकहरूलाई हाम्रो एआई एल्गोरिदम र निर्णय प्रक्रियाको विस्तृत व्याख्या प्रदान गर्छौं।"},
    {"question": "How do you handle updates and maintenance of AI systems post-deployment?", "answer": "We provide ongoing support, updates, and maintenance services to ensure the optimal performance and reliability of your AI systems even after deployment."},
    {"question": "के तपाईं सफल AI परियोजनाहरू पूरा गर्नुभएको उदाहरणहरू प्रदान गर्न सक्नुहुन्छ?", "answer": "पक्कै पनि! हामीले स्वास्थ्य सेवा, वित्त, र ई-वाणिज्य लगायत विभिन्न उद्योगहरूमा AI समाधानहरू सफलतापूर्वक लागू गरेका छौं। उदाहरणहरूमा व्यक्तिगत सिफारिस प्रणालीहरू, धोखाधडी पत्ता लगाउने एल्गोरिदमहरू, र चिकित्सा छवि विश्लेषण उपकरणहरू समावेश छन्।"},
    {"question": "What is your approach to project management and communication?", "answer": "We follow agile methodologies for project management and maintain regular communication with our clients through scheduled meetings, progress reports, and collaborative tools."}
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
