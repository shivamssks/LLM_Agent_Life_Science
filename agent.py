from langchain import PromptTemplate, chains
# from rmrkl import ChatZeroShotAgent,RetryAgentExecutor, STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION
from langchain import agents
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
from tools import *
from tools.gene_analysis import *
from tools.search  import websearch
from langchain import OpenAI
from tools import *
from langchain.agents import initialize_agent, AgentType
from prompt import *
import os
from langchain import PromptTemplate, chains

from langchain_anthropic import ChatAnthropic
# 
os.environ["OPENAI_API_KEY"] = ""
os.environ["ANTHROPIC_API_KEY"]=""

class LifescienceAgent():
    def __init__(self,tools,model_name,max_iterations=None):
        """
        Initializes the class instance with the given parameters.

        Args:
            llm (object): The language model object.
            tools (list): A list of tool objects.
            agent (object): The agent object.
            model_name (str): The name of the model.

        Returns:
            None
        """
        self.tools = tools
        self.model_name = model_name
        self.max_iter = max_iterations
    def main(self):
        if self.model_name == "claude":
            self.llm = ChatAnthropic(model='claude-3-opus-20240229')
        else:
            self.llm  = OpenAI()

        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, # Or any other agent type
            agent_kwargs={"suffix":SUFFIX,
            "format_instructions":FORMAT_INSTRUCTIONS,
            "question_prompt":QUESTION_PROMPT},
            verbose=True,
            max_iterations=self.max_iter
            )
      

    def run(self,query):
        """
        Run function to execute the given query using the agent.
        Parameters:
            query (unknown): The query to be executed.
        Returns:
            unknown: The result of running the query using the agent.
        """
        
        return self.agent.run(query)
    
if __name__=="__main__":
    query1 = "Give me the top 5 genes and their names and information about them using web search that are differentially expressed between dexamethasone and untreated groups. perform differential expression analysis on .\\Data\\counts_data.csv and .\\Data\\sample_info.csv"
    all_tools = [deseqAnalysis(),websearch(),top_results()]
    agent = LifescienceAgent(all_tools,"claude")
    agent.main()
    result = agent.run(query12)



        


