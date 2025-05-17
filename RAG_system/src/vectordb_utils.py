from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, UnstructuredHTMLLoader, JSONLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List
from langchain_mongodb import MongoDBAtlasVectorSearch
from pymongo import MongoClient
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import os
import uuid
class Vector_Utils:
    def __init__(self, controller):
        self.controller = controller
        self.vectorstore=None
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=720, chunk_overlap=100)
        self.retriever = None
        self.init_utils()
        
    def init_utils(self):
        self.init_vector_db()
        self.init_chain()
    def init_vector_db(self):
        if os.environ.get("VECTOR_DB_NAME")=="mongodb":
            try:
                mongo_connection = os.environ.get("MONGODB_URL","")
                if mongo_connection:
                    import certifi
                    certifi_path = certifi.where()
                    mongo_connection=mongo_connection+f"&tls=true&tlsCAFile={certifi_path}"
                    client = MongoClient(mongo_connection)
                    MONGODB_COLLECTION = client[os.environ.get("MONGODB_DB")][os.environ.get("MONGO_COLLECTION")]
                else:
                    print("MongoDB url is not found")
                    return 0
                if client.admin.command('ping')["ok"]:
                    self.vectorstore = MongoDBAtlasVectorSearch(
                        collection=MONGODB_COLLECTION,
                        embedding=self.controller.embed_model,
                        index_name="vector_index",
                    )
            except Exception as e:
                print(f"Error Mongodb: {e}") 
                
    def load_and_split_document(self,file_path: str) -> List[Document]:
        if file_path.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
        elif file_path.endswith('.docx'):
            loader = Docx2txtLoader(file_path)
        elif file_path.endswith('.html'):
            loader = UnstructuredHTMLLoader(file_path)
        elif file_path.endswith('.json'):
            loader = JSONLoader(file_path,jq_schema=".",text_content=False,)
        else:
            raise ValueError(f"Unsupported file type: {file_path}")
        documents = loader.load()
        return self.text_splitter.split_documents(documents)
    
    def index_document_to_vectordb(self,file_path: str) -> bool:
        try:
            splits = self.load_and_split_document(file_path)
            # Add metadata to each split
            for split in splits:
                split.metadata['uuid'] = str(uuid.uuid4())
            self.vectorstore.add_documents(splits)
            return True
        except Exception as e:
            print(f"Error indexing document: {e}")
            return False

    def delete_doc_from_vectordb(self,uuid: int):
        try:
            if os.environ.get("VECTOR_DB_NAME")=="mongodb":
                # Directly call delete_many on the raw collection
                result = self.vectorstore.collection.delete_many({"uuid": uuid})
                print(f"Deleted {result.deleted_count} documents with uuid {uuid}")
                return True
        except Exception as e:
            print(f"Error deleting document with uuid {uuid} from {self.db_type}: {str(e)}")
            return False
        
    
    def init_chain(self):
        # Instantiate Atlas Vector Search as a retriever
        self.retriever = self.vectorstore.as_retriever()
        
        # Define prompt template
        template = """
        Use the following pieces of context to answer the question at the end.
        {context}
        Question: {question}
        """
        custom_rag_prompt = PromptTemplate.from_template(template)
        
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        # Create chain
        self.controller.rag_chain = (
        {"context": self.retriever | format_docs, "question": RunnablePassthrough()}
        | custom_rag_prompt
        | self.controller.chat_model
        | StrOutputParser()
        )

        
        

    