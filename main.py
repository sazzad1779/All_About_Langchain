from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv(override=True)
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, HTTPException
import os
import shutil
from RAG_system.src.modeling import QueryInput,QueryResponse
import uvicorn
from RAG_system.src.controller import controller
from RAG_system.src.langchain_utils import LangchainUtils
from RAG_system.src.vectordb_utils import Vector_Utils

ctrl  = controller()
langUtils = LangchainUtils(ctrl)
vectorUtils = Vector_Utils(ctrl)
app = FastAPI()
# CORS settings
origins = [
    "*"
    # Add production domain here if needed
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat", response_model=QueryResponse)
def chat(query_input: QueryInput):
    answer = langUtils.call_llm(query_input.question)
    return QueryResponse(answer=answer)

@app.post("/upload-doc")
def upload_and_index_document(file: UploadFile = File(...)):
    allowed_extensions = ['.pdf', '.docx', '.html','.json']
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail=f"Unsupported file type. Allowed types are: {', '.join(allowed_extensions)}")
    temp_file_path = f"temp_{file.filename}"
    try:
        # Save the uploaded file to a temporary file
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        success = vectorUtils.index_document_to_vectordb(temp_file_path)
        if success:
            return {"message": f"File {file.filename} has been successfully uploaded and indexed."}
        else:
            # db_utils.delete_document_record(file_id)
            raise HTTPException(status_code=500, detail=f"Failed to index {file.filename}.")
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

# 👇 This lets you run it like: python main.py
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

