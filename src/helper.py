# To Extract data from PDF:
from langchain_community.document_loaders import PyPDFLoader,DirectoryLoader
def load_data(data_path):
    loader = DirectoryLoader(data_path, 
                            glob='*.pdf',
                            loader_cls=PyPDFLoader
                           )
    
    documents = loader.load()
    return documents

# To create chunks of text :
from langchain_text_splitters import RecursiveCharacterTextSplitter
def text_spliter(text):
text_split = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    add_start_index=True,
)
text_chunks = text_split.split_documents(text)
return text_chunks