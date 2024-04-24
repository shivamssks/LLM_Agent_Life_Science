import pandas as pd
# from my_deseq_module import DeseqDataSet, DeseqStats, id_map
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats
from pydeseq2.default_inference import DefaultInference
from sanbomics.tools import id_map
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
from scipy.stats import gmean
import numpy as np

from langchain_anthropic import ChatAnthropic
from langchain import OpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
import os

import pandas as pd

os.environ["OPENAI_API_KEY"] = ""
# llm  = OpenAI()
significant_genes = None
class DeseqAnalysis:
    def __init__(self, counts_file, sample_info_file):
        """
        Initialize the class with the given counts file and sample info file.

        Parameters:
            counts_file (str): The file path to the counts file.
            sample_info_file (str): The file path to the sample info file.
        """
        self.counts = pd.read_csv(counts_file)
        self.sample_df = pd.read_csv(sample_info_file)
        self.inference = DefaultInference(n_cpus=8)


    def normalize_counts(self):
        """
    #     Normalize the count data using the median of ratios method.

    #     This method normalizes the count data by the median of ratios of counts to the geometric mean across samples.

    #     Returns:
    #         pd.DataFrame: The normalized count data.
    #     """
        filter_data = self.counts[self.counts.sum(axis=1) >= 10]
        sum_results = filter_data .sum(axis = 1)
        effective_library_size = np.exp(np.log(sum_results).mean())
        normalization_factors = sum_results / effective_library_size
        self.counts_data= filter_data.div(normalization_factors, axis=0)
        self.counts_data = self.counts_data.astype(int)
        # return counts_data

    def perform_deseq_analysis(self):
        """
        Perform differential expression analysis using DESeq2.

        This function performs differential expression analysis using the DESeq2 package. It takes the counts data and the sample metadata as input and performs the analysis to identify differentially expressed genes between the "dexamethasone" and "untreated" groups. The counts data is filtered to remove genes with less than 10 counts in any sample.

        Returns:
            stat_res (DeseqStats): The statistical results of the differential expression analysis.

        """
        columns = list(self.counts.columns)
        rows = list(self.sample_df.index)
        matches = list(set(columns).intersection(set(rows)))
        # counts_data = self.counts[self.counts.sum(axis=1) >= 10]
        dds = DeseqDataSet(counts=self.counts_data.T,
                           metadata=self.sample_df,
                           design_factors="dexamethasone",
                           inference=self.inference,
                           ref_level=["dexamethasone", "untreated"])
        dds.deseq2()
        stat_res = DeseqStats(dds, inference=self.inference)
        stat_res.summary()
        return stat_res

    def find_significant_genes(self, stat_res):
        """
        Finds significant genes based on statistical results.

        Args:
            stat_res (StatResults): The statistical results object containing the results dataframe.

        Returns:
            pandas.DataFrame: The dataframe with significant genes, including the symbol.

        Raises:
            None
        """
        res = stat_res.results_df[stat_res.results_df.baseMean >= 10]
        sigs = res[(res.padj < 0.05) & (abs(res.log2FoldChange) > 0.5)]
        mapper = id_map(species='human')
        sigs['Symbol'] = sigs.index.map(mapper.mapper)
        self.sigs = sigs.dropna(subset=['Symbol'])
        return sigs
    
class deseqAnalysis(BaseTool):
    name = "deseq_analysis"
    description = "Perform differential expression analysis using DESeq2."
    
    def _run(self,counts_file,sample_info_file):
        """
        This function runs the DeseqAnalysis on the given query.
        """
        print(counts_file, sample_info_file)
        # values1 = list(counts_file.values())
        # values2 =  list(sample_info_file.values())
        # file1 = values1[-1] 
        # file2 = values2[-1]
        # print(file1,file2)
        analysis = DeseqAnalysis(counts_file,sample_info_file)

        # analysis = DeseqAnalysis(file1, file2)
        analysis.normalize_counts()
        statistical_results = analysis.perform_deseq_analysis()
        global significant_genes
        significant_genes = analysis.find_significant_genes(statistical_results)

        return significant_genes
    

class top_results(BaseTool):
    name = "top_results"
    description = "This tool is used to give top most significant genes based on adjusted p values."
    
    def _run(self):
        top_genes = significant_genes.sort_values(by='padj').head(5)
        return top_genes


# Example 111usage:
if __name__=="__main__":
    os.environ["ANTHROPIC_API_KEY"]=""
    llm = ChatAnthropic(model='claude-3-opus-20240229')
    prompt = """
    your are an agent that can perform differential expression analysis on the data  provided pass the data in dictionary format "
    """
    tools = [deseqAnalysis(),top_results()]
    agent = initialize_agent(agent = AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,tools =tools,agent_kwargs={"prompt":prompt},
                                    llm =llm,verbose = True)
    agent.run("give me the top 1 genes that are differentially expressed between dexamethasone and untreated groups. perform differential expression analysis on .\\Data\\counts_data.csv and .\\Data\\sample_info.csv")

    # analysis = DeseqAnalysis(".\\Data\\counts_data.csv", ".\\Data\\sample_info.csv")
    # normalized_counts = analysis.normalize_counts()
    # statistical_results = analysis.perform_deseq_analysis()
    # significant_genes = analysis.find_significant_genes(statistical_results)
    # top_genes = significant_genes.sort_values(by='padj')
    # print(top_genes)      