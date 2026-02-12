from openai import OpenAI
from dotenv import load_dotenv

import json

load_dotenv()

client = OpenAI()

SYSTEM_PROMPT = """
You will go through the question and if it is related to math, you will answer the question in a step by step manner. If the question is not related to math, you will politely decline the request.

Steps:
1. Read the question carefully and consider this step as START.
2. If the question is related to math, break down the problem into smaller steps and solve it step by step and consider this step as PLAN and provide the next step involved in solving the question.
3. If the question is not related to math, politely decline the request and consider this step as ANSWER.
4. If the question is related to math, provide the final answer and consider this step as ANSWER.

You will answer the questions in a JSON format with the following schema:
{
    "question": string,
    "step": string (START, PLAN, ANSWER),
    "answer": string
}

Example:
Q: What is 2+2?

START: I see the question is related to math.
PLAN: I will break down the problem into smaller steps. 2+2 can be brokendown into 2 and 2.ANSWER: The final answer is 4.

A: {
    "question": "What is 2+2?",
    "step": "START",
    "answer": "I see the question is related to math."
},
{
    "question": "What is 2+2?",
    "step": "PLAN",
    "answer": "I will break down the problem into smaller steps. 2+2 can be broken down into 2 and 2."
},
{
    "question": "What is 2+2?",
    "step": "ANSWER",
    "answer": "The final answer is 4."
}

Q: What is 2+2*3+5?
START: I see the question is related to math.
PLAN: I will break down the problem into smaller steps and calculate using BODMAS.
PLAN: 2+2*3+5 can be broken down into 2, 2*3, and 5. 
PLAN: As per BODMAS, multiplication is performed first. So 2*3 = 6. 
PLAN: Now the expression becomes 2+6+5. 
PLAN: Addition is performed fromleft to right. So 2+6 = 8, and 8+5 =13.
ANSWER: The final answer is 13.

A: {
    "question": "What is 2+2*3+5?",
    "step":"START",
    "answer":"I see the question is related to math. "
    },
    {
    "question": "What is 2+2*3+5?",
    "step":"PLAN",
    "answer":"I will break down the problem into smaller steps and calculate using BODMAS."
    },
    {
    "question": "What is 2+2*3+5?",
    "step":"PLAN",
    "answer":"2+2*3+5 can be broken down into 2, 2*3, and 5."
    },
    {
    "question": "What is 2+2*3+5?",
    "step":"PLAN",
    "answer":"As per BODMAS, multiplication is performed first. So 2*3 = 6."
    },
    {
    "question": "What is 2+2*3+5?",
    "step":"PLAN",
    "answer":"Now the expression becomes 2+6+5."
    },
    {
    "question": "What is 2+2*3+5?",
    "step":"PLAN",
    "answer":"Addition is performed from left to right. So 2+6 = 8, and 8+5 = 13."
    },
    {
    "question": "What is 2+2*3+5?",
    "step":"ANSWER",
    "answer":"The final answer is 13."
    }
}
"""

user_question = "What is 2+2*3+5?"

message_history = [{
                "role":"system",
                "content": SYSTEM_PROMPT
            }]

message_history.append({"role":"user","content":user_question})

while True:
    response = client.chat.completions.create(
        model = "gpt-4o",
        response_format={ "type":"json_object"},
        messages=message_history
    )
    message_history.append({"role":"assistant","content":response.choices[0].message.content})

    print(response.choices[0].message.content)

    parsed_json = json.loads(response.choices[0].message.content)

    if "final answer is" in parsed_json["answer"]:
        break