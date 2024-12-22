from Multi_agent import run_multi_agent_system
import streamlit as st
import re
from dotenv import load_dotenv
load_dotenv() 

st.title("Market Research & Use Case Generation Multi Ai Agent System")
st.markdown("""
This application allows you to input a company name and get insights from a multi-agent system:
1. **Data Collector Agent**: Gathers industry trends and company details.
2. **Use Case Generator Agent**: Creates AI/ML use cases.
3. **Resource Collector Agent**: Suggests datasets, APIs, and research papers.
""")

# User Input
company_name = st.text_input("Enter the Company Name:", placeholder="e.g., Tesla, Amazon")

# Execute Button
if st.button("Run Multi-Agent System"):
    if not company_name.strip():
        st.error("Please enter a valid company name!")
    else:
        st.info("Processing... Please wait.")
        # Execute the system
        result = run_multi_agent_system(company_name)
        
        # Display Results
        st.success("Processing complete! Explore the results below.")
        
        # Step 1: Trends
        with st.expander("Step 1: Data Collector Agent - Trends Identified"):
            st.text_area("Trends Output", value=result["trends"], height=300)

        # Step 2: Use Cases
        with st.expander("Step 2: Use Case Generator Agent - Use Cases Generated"):
            st.text_area("Use Cases Output", value=result["use_cases"], height=300)

        # Step 3: Resources
        with st.expander("Step 3: Resource Collector Agent - Resources Collected"):
            st.text_area("Resources Output", value=result["resources"], height=300)

        
result = run_multi_agent_system(company_name)
# Prepare the Markdown content for download
def prepare_markdown(result):
    markdown_content = "# Multi-Agent System Summary\n\n"

    # Step 1: Trends
    markdown_content += "## Step 1: Data Collector Agent - Trends Identified\n"
    markdown_content += f"{result['trends']}\n\n"
    
    # Step 2: Use Cases
    markdown_content += "## Step 2: Use Case Generator Agent - Use Cases Generated\n"
    markdown_content += f"{result['use_cases']}\n\n"
    
    # Step 3: Resources
    markdown_content += "## Step 3: Resource Collector Agent - Resources Collected\n"
    markdown_content += f"{result['resources']}\n\n"

    return markdown_content

# Generate Markdown content
markdown_content = prepare_markdown(result)

# Display result in Streamlit
#st.title("Market Research & Use Case Generation Multi-AI Agent System")
#st.markdown("This application allows you to input a company name and get insights from a multi-agent system.")

# Display the results with clickable links
with st.expander("Download Summary"):
    # Regex pattern to find URLs in the output
    url_pattern = r'(https?://[^\s]+)'
    
    # Replace URLs in the output with Markdown formatted links
    clickable_output = re.sub(url_pattern, r'[\1](\1)', result["resources"])
    
    # Display the result with clickable links using markdown
    st.markdown(clickable_output, unsafe_allow_html=True)

# Provide download button for the entire summary as a markdown file
st.download_button(
    label="Download Summary as Markdown File",
    data=markdown_content,
    file_name="multi_agent_system_summary.md",
    mime="text/markdown"
)