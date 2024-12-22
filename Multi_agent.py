import os
from langchain.agents import Tool, initialize_agent
from langchain.tools import DuckDuckGoSearchRun
from langchain.prompts import PromptTemplate
import google.generativeai as genai



from dotenv import load_dotenv
load_dotenv() 
api_key = os.environ.get('GOOGLE_API')
genai.configure(api_key=api_key)
llm=genai.GenerativeModel("gemini-pro")

# 2. Define Tools
search_tool = Tool(
    name="DuckDuckGo Search",
    func=DuckDuckGoSearchRun().run,
    description="A tool for searching the web using DuckDuckGo."
)

# 3. Define Prompt Templates
data_collector_prompt = PromptTemplate(
    input_variables=["company_name"],
    template="""You are a Senior Researcher with expertise in industry analysis. Your task is to investigate the company "{company_name}" and its industry. Answer the following questions:
    1. What industry or industries does the company operate in? Provide context and details.
    2. What are the company’s main products or services?
    3. Identify the company's strategic focus areas (e.g., operations, supply chain, customer experience).
    4. Highlight 5 key trends or developments in this industry relevant to AI, ML, and GenAI. Provide references or credible sources for each trend.
    Present your findings in a clear, structured manner for further analysis."""
)

use_case_generator_prompt = PromptTemplate(
    input_variables=["trends"],
    template="""You are an AI Strategist tasked with creating actionable and innovative use cases for the company "{company_name}" based on the following trends:
    {trends}  
    Analyze these trends and propose AI, ML, and GenAI use cases to improve the company’s processes, customer satisfaction, and operational efficiency. Provide your analysis structured into four sections for each use case:
    1. **Pros**: The advantages and benefits of implementing this solution.
    2. **Cons**: Potential challenges and drawbacks of the solution.
    3. **Opportunities**: Strategic opportunities the solution unlocks.
    4. **Risks**: Associated risks and mitigation strategies.
    Your goal is to generate impactful and feasible use cases tailored to the company and its industry."""
)

resource_collector_prompt = PromptTemplate(
    input_variables=["use_cases"],
    template="""You are a Resource Specialist with expertise in AI and ML solutions. Your task is to identify and collect resources to support the following use cases:
     {use_cases} 
     For each use case, provide the following:
      1. Datasets: Relevant datasets available on platforms like Kaggle, HuggingFace, or GitHub (provide links and a brief description).
      2. APIs: Suitable APIs or tools that can be integrated to implement the use case (provide details and links).
      3. Research Papers: Key papers or articles supporting the solution (provide titles, summaries, and links).
      Structure your response as a comprehensive list with resources categorized by use case."""
)

# 4. Define Tasks (simulate task assignment manually)
def data_collector_task(company_name):
    prompt = data_collector_prompt.format(company_name=company_name)
    response = llm.generate_content(contents=prompt)  
    return response.text 

def use_case_generator_task(trends,company_name):
    prompt = use_case_generator_prompt.format(trends=trends,company_name=company_name)
    response = llm.generate_content(contents=prompt)  
    return response.text 

def resource_collector_task(use_cases):
    prompt = resource_collector_prompt.format(use_cases=use_cases)
    response = llm.generate_content(contents=prompt)  
    return response.text 

# 5. Execute Multi-Agent Workflow
def run_multi_agent_system(company_name):
    # Step 1: Data Collector Task
    print("===================================================================================================================================================================")
    print("Step 1: Running Data Collector Task...")
    print("===================================================================================================================================================================")
    trends = data_collector_task(company_name)
    print(f"Trends Identified:\n{trends}\n")
    
    # Step 2: Use Case Generator Task
    print("===================================================================================================================================================================")
    print("Step 2: Running Use Case Generator Task...")
    print("===================================================================================================================================================================")
    use_cases = use_case_generator_task(trends,company_name)
    print(f"Use Cases Generated:\n{use_cases}\n")
    
    # Step 3: Resource Collector Task
    print("===================================================================================================================================================================")
    print("Step 3: Running Resource Collector Task...")
    print("===================================================================================================================================================================")
    resources = resource_collector_task(use_cases)
    print(f"Resources Collected:\n{resources}\n")
    
    return {
        "trends": trends,
        "use_cases": use_cases,
        "resources": resources
    }

# Run the system for a sample company
#company_name =input("Enter a  Company Name:")
#result = run_multi_agent_system(company_name)





