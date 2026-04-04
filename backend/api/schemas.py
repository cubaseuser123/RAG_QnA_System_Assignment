from pydantic import BaseModel

class QuestionRequest(BaseModel):
    question : str

class SourceNode(BaseModel):
    file : str
    page : str
    excerpt : str

class AnswerResponse(BaseModel):
    answer : str
    sources : list[SourceNode]

class InjestRequest(BaseModel):
    path : str

class InjestResponse(BaseModel):
    message : str
    chunks_injested : int

class HealthResponse(BaseModel):
    status : str
    vector_store : str
    llm : str
    