from flask import Flask, render_template, jsonify, request
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import PromptTemplate
from src.prompt import prompt_template
import os
from dotenv import load_dotenv

# Initialize Flask and load environment variables
app = Flask(__name__)
load_dotenv()

# Configuration
MY_API_KEY = os.getenv("my_key")
PINECONE_API_KEY = os.getenv("Pinecone_API_KEY")
PINECONE_INDEX_NAME = "embedding"

# 1. Setup Embeddings and Vector Store
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004", 
    api_key=MY_API_KEY
)

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)
vector_store = PineconeVectorStore(embedding=embeddings, index=index)

# 2. Setup LLM and Prompt
# Using "input" instead of "question" for compatibility with create_retrieval_chain
prompt = PromptTemplate(template=prompt_template, input_variables=["context", "input"])

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=MY_API_KEY,
    temperature=0.3 # Lower temperature for medical accuracy
)

# 3. Build Retrieval Chain
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)

docs_chain = create_stuff_documents_chain(llm, prompt)
retriever_chain = create_retrieval_chain(retriever, docs_chain)

# --- Routes ---

@app.route("/")
def index_route():
    return render_template("index.html")

@app.route('/ask', methods=['POST'])
def ask():
    try:
        # Securely parse incoming JSON
        data = request.get_json(force=True)
        user_message = data.get('message', '').strip()

        if not user_message:
            return jsonify({
                'success': False,
                'response': '',
                'error': 'Please enter a message.'
            }), 400

        # Run the chain
        # create_retrieval_chain returns a dict with 'answer' and 'context' keys
        result = retriever_chain.invoke({"input": user_message})
        bot_response = result.get("answer")

        if not bot_response:
            raise ValueError("The AI model returned an empty response.")

        return jsonify({
            'success': True,
            'response': bot_response,
            'error': ''
        })

    except Exception as e:
        app.logger.error(f"Error in /ask: {str(e)}")
        return jsonify({
            'success': False,
            'response': '',
            'error': 'I apologize, but I am having trouble processing that right now.'
        }), 500

# Error Handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Endpoint not found'}), 404

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    # Production safety: never run debug=True in an exposed environment
    app.run(host='0.0.0.0', port=port, debug=False)