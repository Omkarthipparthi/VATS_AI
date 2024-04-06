import os
from typing import Dict, List
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_core.pydantic_v1 import BaseModel
from langchain_experimental.tabular_synthetic_data.openai import (
    OPENAI_TEMPLATE,
    create_openai_data_generator,
)
from langchain_experimental.tabular_synthetic_data.prompts import (
    SYNTHETIC_FEW_SHOT_PREFIX,
    SYNTHETIC_FEW_SHOT_SUFFIX,
)
from langchain_openai import ChatOpenAI

load_dotenv() 
MY_ENV_VAR = os.getenv('OPENAI_API_KEY')
class MCQ(BaseModel):
    id: int
    wholeQuestion: str
    allOptions: list
    correctOption: str
    
    
examples = [
    {
        "example": 
        """
        id: 1, 
        wholeQuestion: What is the measure of variability that represents the average distance between each data point and the mean of the data set?, 
        allOptions: Standard Deviation, Mean, Variance, Range, 
        correctOption:  Standard Deviation, 
        userSelected: Mean
        isCorrect: No
        """
    },
    {
        "example": 
        """
        id: 2, 
        wholeQuestion: Which of the following is a measure of central tendency?, 
        allOptions Code: Variance, Standard Deviation, Median, Range, 
        correctOption Code:  Median, 
        userSelected: Variance
        isCorrect: No
        """
    },
    {
        "example": 
        """
        id: 3, 
        wholeQuestion: What does the p-value in hypothesis testing represent?, 
        allOptions Code: Level of significance, Probability of observing the data given that the null hypothesis is true, Type I error rate, Type II error rate, 
        correctOption Code:  Level of significance, 
        userSelected: Level of significance
        isCorrect: Yes
        """
    },
        {
        "example": 
        """
        id: 4, 
        wholeQuestion: Which statistical test is used to determine the relationship between two categorical variables?, 
        allOptions Code: ANOVA, T-test, Chi-square test, Regression analysis,
        correctOption Code:  Chi-square test, 
        userSelected: T-test
        isCorrect: No
        """
    },
        
]

# class exam_prep_aid_evaluation:
#     def evaluation(selections: Dict[int, str], mcqs: List[MCQ]):
#         results = []
#         correct_ids = []
#         for mcq_id, user_selection in selections.items():
#             mcq = next((q for q in mcqs if q.id == mcq_id), None)
#             if mcq is None:
#                 continue

#             is_correct = mcq.correctOption == user_selection
#             if is_correct:
#                 correct_ids.append(mcq_id)

#             result = {
#                 "id": mcq_id,
#                 "wholeQuestion": mcq.wholeQuestion,
#                 "allOptions": mcq.allOptions,
#                 "correctOption": mcq.correctOption,
#                 "userSelected": user_selection,
#                 "isCorrect": is_correct
#             }
#             results.append(result)
        
#         # Return both results and the correct ids
#         return {"results": results, "correct_ids": correct_ids}

#     def regenerate(selections: Dict[int, str], mcqs: List[MCQ]):
#         results = []
#         for mcq_id, user_selection in selections.items():
#             # Find the MCQ that matches the ID from the selections
#             mcq = next((q for q in mcqs if q.id == mcq_id), None)
#             if mcq is None:
#                 continue
            
#             # Check if the user's selection is correct
#             is_correct = mcq.correctOption == user_selection
#             result_str = (
#                 f"id: {mcq_id}, "
#                 f"wholeQuestion: {mcq.wholeQuestion}, "
#                 f"allOptions: {', '.join(mcq.allOptions)}, "
#                 f"correctOption: {mcq.correctOption}, "
#                 f"userSelected: {user_selection}, "
#                 f"isCorrect: {'Yes' if is_correct else 'No'}"
#             )
#             results.append({"example": result_str})
#         print(results)

#         OPENAI_TEMPLATE = PromptTemplate(input_variables=["example"], template="{example}")

#         prompt_template = FewShotPromptTemplate(
#             prefix=SYNTHETIC_FEW_SHOT_PREFIX,
#             examples=examples,
#             suffix=SYNTHETIC_FEW_SHOT_SUFFIX,
#             input_variables=["subject", "extra"],
#             example_prompt=OPENAI_TEMPLATE,
#         )


#         synthetic_data_generator = create_openai_data_generator(
#             output_schema=MCQ,
#             llm=ChatOpenAI(temperature=1, openai_api_key = MY_ENV_VAR, model_name = 'gpt-4'), 
#             prompt=prompt_template,
#         )


#         synthetic_results = synthetic_data_generator.generate(
#             subject="Statistics",
#             extra="Generate similar multiple-choice question (MCQ) on Statistics, \
#                 Ensure it reflects our examples, and every question you generate must be unique, \
#                 Ensure the question is clear, with one correct answer and three plausible distractors., \
#                 Focus on core concepts and common pitfalls. I want you to analyse the questions present, and once you finished analysing, \
#                 keep progressively increasing the difficulty of questions the user got right, and change the questions variation the user got wrong, this entire purpose is that,\
#                 we want to provide a personalized support experience to the user.",
#             runs=2, 
#         )


#         print(synthetic_results)
#         return synthetic_results




class exam_prep_aid_evaluation:
    def evaluation(selections: Dict[int, str], mcqs: List[MCQ]):
        results = []
        for mcq_id, user_selection in selections.items():
            # Find the MCQ that matches the ID from the selections
            mcq = next((q for q in mcqs if q.id == mcq_id), None)
            if mcq is None:
                continue

            # Check if the user's selection is correct
            is_correct = mcq.correctOption == user_selection
            result_str = (
                f"id: {mcq_id}, "
                f"wholeQuestion: {mcq.wholeQuestion}, "
                f"allOptions: {', '.join(mcq.allOptions)}, "
                f"correctOption: {mcq.correctOption}, "
                f"userSelected: {user_selection}, "
                f"isCorrect: {'Yes' if is_correct else 'No'}"
            )
            results.append({"example": result_str})
        print(results)

        OPENAI_TEMPLATE = PromptTemplate(input_variables=["example"], template="{example}")

        prompt_template = FewShotPromptTemplate(
            prefix=SYNTHETIC_FEW_SHOT_PREFIX,
            examples=examples,
            suffix=SYNTHETIC_FEW_SHOT_SUFFIX,
            input_variables=["subject", "extra"],
            example_prompt=OPENAI_TEMPLATE,
        )


        synthetic_data_generator = create_openai_data_generator(
            output_schema=MCQ,
            llm=ChatOpenAI(temperature=1, openai_api_key = MY_ENV_VAR, model_name = 'gpt-4'), 
            prompt=prompt_template,
        )


        synthetic_results = synthetic_data_generator.generate(
            subject="Statistics",
            extra="Generate similar multiple-choice question (MCQ) on Statistics, \
                Ensure it reflects our examples, and every question you generate must be unique, \
                Ensure the question is clear, with one correct answer and three plausible distractors., \
                Focus on core concepts and common pitfalls. I want you to analyse the questions present, and once you finished analysing, \
                keep progressively increasing the difficulty of questions the user got right, and change the questions variation the user got wrong, this entire purpose is that,\
                we want to provide a personalized support experience to the user.",
            runs=2, 
        )


        print(synthetic_results)
        return synthetic_results





