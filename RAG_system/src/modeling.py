from pydantic import BaseModel, Field
class QueryInput(BaseModel):
    question: str
    
class QueryResponse(BaseModel):
    answer: str