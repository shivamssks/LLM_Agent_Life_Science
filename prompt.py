# flake8: noqa
PREFIX = """
You are an expert chemist and your task is to respond to the question or
solve the problem to the best of your ability using the provided tools.
"""

FORMAT_INSTRUCTIONS = """
You can only respond with a single complete
"Thought, Action, Action Input" format
OR a single "Final Answer" format.

Complete format:

Thought: (reflect on your progress and decide what to do next)
Action: (the action name, should be one of [{tool_names}])
Action Input: (the input string to the action)

AND

Final Answer: (Rephrased: "You must provide the final answer to the original input question, along with details on the number and names of tools utilized, as well as the iterations employed, all presented in a JSON format.)
"""

QUESTION_PROMPT = """
Answer the question below using the following tools:

{tool_strings}

Use the tools provided, using the most specific tool available for each action.
Your final answer should contain all information necessary to answer the question and subquestions.

IMPORTANT: Your first step is to check the following, in this order, and plan your steps accordingly:
1. Were you asked to do any of the following: perform the differential expression analysis,find top 5 significant genes,and information about them?
If so, your first step is to check if the valid is provided to perform the analysis then perform the analysis, if not, include a warning in your final answer.
2. Were you asked to perform websearch on the given query if yes then check are you able to connect to the internet or not if not then include a warning in your final answer.
Do not skip these steps.


Question: {input}
"""

SUFFIX = """
Thought: {agent_scratchpad}
"""
FINAL_ANSWER_ACTION = "Final Answer:"


REPHRASE_TEMPLATE = """In this exercise you will assume the role of a scientific assistant. Your task is to answer the provided question as best as you can, based on the provided solution draft.
The solution draft follows the format "Thought, Action, Action Input, Observation", where the 'Thought' statements describe a reasoning sequence. The rest of the text is information obtained to complement the reasoning sequence, and it is 100% accurate.
Your task is to write an answer to the question based on the solution draft, and the following guidelines:
The text should have an educative and assistant-like tone, be accurate, follow the same reasoning sequence than the solution draft and explain how any conclusion is reached.
Question: {question}

Solution draft: {agent_ans}

Answer:
"""