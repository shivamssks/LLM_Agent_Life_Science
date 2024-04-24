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
        rephrase = PromptTemplate(
                input_variables=["question", "agent_ans"], template=REPHRASE_TEMPLATE
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
    query2 = "retrieve information on the top 5 genes using internet and their names exhibiting differential expression between the dexamethasone-treated and untreated groups. use the provided datasets: counts_data.csv and sample_info.csv."
    query3 = "top 1 genes that are differentially expressed between dexamethasone and untreated groups. give me more information about this gene and any diovery related to that gene. use this data .\\Data\\counts_data.csv and .\\Data\\sample_info.csv?" 
    query4 = "Qene is the important part of human bodey structure. can you gi@=vem the genes that most significant for dexamethasone treated patients. counts_data.csv and .\\Data\\sample_info.csv?"
    query5 = "Is it possible to conduct a differential expression analysis? If so, please proceed with the analysis using the appropriate tool and confirm the completion of the analysis with a response of 'yes' and the observations you made while performing the analysis. use this data counts_data.csv and sample_info.csv "
    query6 = "Inquiring through web search, I'm soliciting information on the top 5 genes, their nomenclature, and significant findings regarding their expression discrepancies between dexamethasone-treated and untreated cohorts. Additionally, I aim to undertake a differential expression analysis utilizing the provided datasets, '.\\Data\\counts_data.csv' and  '.\\Data\\sample_info.csv,' which reside in the specified directory, Data. This analysis involves scrutinizing gene expression patterns to discern variations in response to dexamethasone treatment compared to untreated conditions. Through differential expression analysis, statistical methods will be employed to identify genes showing significant alterations in expression levels between the two groups. This comprehensive investigation intends to unravel the molecular mechanisms underlying the effects of dexamethasone treatment, potentially shedding light on its therapeutic efficacy or uncovering novel gene targets for further research."
    query7 = "you are delving into details concerning the top five genes, encompassing their names and noteworthy discoveries regarding differences in their expression among groups treated with and without dexamethasone. Moreover, my objective is to carry out a comparative expression analysis utilizing the datasets provided in the Data Directory directory. This analysis involves scrutinizing gene expression patterns to identify disparities in response to dexamethasone treatment versus untreated conditions. Utilizing statistical methodologies, this investigation aims to pinpoint genes exhibiting significant alterations in expression levels between the two groups. This comprehensive inquiry seeks to unveil the molecular mechanisms underpinning the effects of dexamethasone treatment, potentially providing insights into its therapeutic effectiveness or uncovering novel gene targets for further investigation. Please use the files counts_data.csv and sample_info.csv for this purpose."
    query8 = "What are the observation can be made about the genes after performing normalization on the data and also find the different relevant techniques of normalization.\\Data\\counts_data.csv and .\\Data\\sample_info.csv"
    query9 = "What recent discoveries have been made in the field of life sciences through the utilization of generative AI?"
    query10 = "Who won IPL 2023 finals.give answer in one word?"
    query11 = "Differential expression is not used to find the most significant genes but I wnat you to find the most signifcnat genes use this data .\\Data\\counts_data.csv and .\\Data\\sample_info.csv"
    query12 = "The purpose of differential expression analysis isn't to identify the most significant genes, but I'm requesting that you identify the most significant genes using the provided data located at .\Data\counts_data.csv and .\Data\sample_info.csv and also identify if there any wrong information provided it is not correct."
    # query8 = "Which teams are in 2023  IPL finals. Use web search?"
    # query9 = "tell me about taiwan eathquake in 2024"
    # query10 = "What recent discoveries have been made in the field of life sciences through the utilization of generative AI?"
    # query13 = "After normalizing the data from '.\\Data\\counts_data.csv' and '.\\Data\\sample_info.csv', what observations arise regarding gene behavior? This process adjusts data to eliminate technical biases, enabling fair comparisons across samples. It allows for the identification of genes showing consistent expression patterns across samples and those significantly upregulated or downregulated under specific conditions. Moreover, normalization enhances the detection of subtle gene expression changes that might otherwise be obscured by technical noise. Comparative analysis enables researchers to discern gene expression alterations associated with different experimental conditions or disease states. Additionally, normalization aids in identifying housekeeping genes with stable expression levels across samples, crucial for accurate data interpretation. Overall, insights gained from normalization shed light on the dynamic behavior of genes, unveiling underlying biological processes and potential therapeutic targets, advancing our understanding of molecular biology and guiding the development of diagnostic tools and treatments."
    all_tools = [deseqAnalysis(),websearch(),top_results()]
    agent = LifescienceAgent(all_tools,"claude")
    agent.main()
    result = agent.run(query12)



        


