# Medical-ChatBot-using-langchain

## steps to run the project

1. install the requirements
 ```bash
   pip install -r requirements.txt
   ```

2. Clone the repository:
```bash
   git clone https://github.com/Gurnoor0001/Medical-ChatBot-using-langchain.git
   ``` 

3. Create a .env file in the root directory of the project and add the following variables:
```bash
   PINECONE_API_KEY=your_pinecone_api_key
   LLM_api_key=your_llm_api_key
   ```

4. # run the following command to store the index
python store_index.py

5. # run the following command to start the server 
python app.py

6. # open up localhost:5000 in your browser
   

## Techstack Used:
- Python
- LangChain
- Flask
- Google LLM
- Pinecone