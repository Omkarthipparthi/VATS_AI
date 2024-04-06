import json
import shutil
from fastapi import FastAPI, HTTPException, File, Form, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
# Assuming chat_gen is in job_matching.py and is the correct import for your setup
from app.job_matching import chat_gen  
from app.chat_gen import chat_gen as CG
from app.exam_prep_aid_generation import exam_prep_aid_generation
from pydantic import BaseModel
from typing import Dict, List, Optional

from app.exam_prep_aid_evaluation import exam_prep_aid_evaluation

class MCQ(BaseModel):
    id: int
    wholeQuestion: str
    allOptions: List[str]
    correctOption: str
class MCQListResponse(BaseModel):
    mcqs: List[MCQ]

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Define request and response models
class QuestionRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str

# Create an instance of chat_gen
JB_chat_instance = chat_gen()
CG_chat_instance = CG()

@app.post("/ask-pdf", response_model=ChatResponse)
async def ask_pdf_endpoint(question: str = Form(...), file: UploadFile = File(None)):
    try:
        # Process the question using the chat_gen instance
        answer = CG_chat_instance.ask_pdf(question)
        return ChatResponse(answer=answer)
    except Exception as e:
        # If there's an error, return a 500 error
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload-pdf/")
async def create_upload_file(file: UploadFile = File(...)):
    # Save the uploaded file to a specified location
    file_location = f"./data/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Update the chat_gen instance with the new file path
    try:
        jobs = JB_chat_instance.update_pdf_file_path(file_location)
        
        # try:
        #     jobs_dict = json.loads(jobs)
        # except json.JSONDecodeError as e:
        #     print(f"Error decoding JSON: {e}")
        #     # Handle the error or exit the code if necessary
        # else:
        #     op = ""
        #     for i in jobs_dict:
        #         print(f"Key (i): {i}, Type: {type(i)}")  # Debug print for the key
        #         if isinstance(jobs_dict[i], dict):
        #             for j in jobs_dict[i]:
        #                 value = jobs_dict[i][j]
        #                 print(f"Subkey (j): {j}, Type: {type(j)}")  # Debug print for the subkey
        #                 print(f"Value: {value}, Type: {type(value)}")  # Debug print for the value
        #                 op += "\n"+str(j) + ": " + str(value) + "\n"
        #         else:
        #             print(f"Error: The value for key '{i}' is not a dictionary. Actual value: {jobs_dict[i]}, Type: {type(jobs_dict[i])}")


        
        return JSONResponse(status_code=200, content={"filename": file.filename, "data": jobs })
    except Exception as e:
            # If there's an error updating the path, return a 500 error
        raise HTTPException(status_code=500, detail=str(e))
    


@app.post("/exam-prep-aid-generation/", response_model=MCQListResponse)
async def exam_prep_api(request: QuestionRequest):
    question = request.question
    print("OMKAR NOW 0",question )
    try:
        print("OMKAR NOW",question )
        raw_mcqs = exam_prep_aid_generation.generation()
        print("OMKAR NOW 2", raw_mcqs)
        mcqs = [MCQ(id=mcq.id, wholeQuestion=mcq.wholeQuestion, allOptions=mcq.allOptions, correctOption=mcq.correctOption) for mcq in raw_mcqs]
        print("OMKAR NOW 3", mcqs)
        return MCQListResponse(mcqs=mcqs)
    except Exception as e:
        # If there's an error, return a 500 error
        raise HTTPException(status_code=500, detail=str(e))
    
class EvaluationRequest(BaseModel):
    selections: Dict[int, str]
    mcqs: List[MCQ]

# @app.post("/exam-prep-aid-evaluation/")
# async def evaluate_mcq_selections(request: EvaluationRequest):
#     try:
#         evaluation_results = exam_prep_aid_evaluation.evaluation(request.selections, request.mcqs)
#         # Append the next step options to the evaluation results
#         evaluation_results["next_steps"] = ["More Questions", "Exit"]
#         return evaluation_results
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@app.post("/exam-prep-aid-evaluation/")
async def evaluate_mcq_selections(request: EvaluationRequest):
    try:
        # Initialize the evaluation class
        evaluator = exam_prep_aid_evaluation
        print("PPT", request)
        # Call the evaluation method
        evaluation_results = evaluator.evaluation(request.selections, request.mcqs)

        # Return the evaluation results
        return evaluation_results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
