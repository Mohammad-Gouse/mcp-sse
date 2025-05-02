# """

# *** MCP Server ***

# """

# from mcp.server.fastmcp import FastMCP


# mcp = FastMCP(name="MCP Server")


# @mcp.tool()
# def greeting(hint: str) -> str:
#     """
#     This tool just displays a message.

#     Args:
#         hint: The hint is always "MCP Server"
#     """
#     return "Hey, Lads! This is Felix Kewa and this is my own remote MCP Server!"


# @mcp.tool()
# def add(a: int, b: int) -> int:
#     """
#     This tool is used to add two numbers.

#     Args:
#         a: The first number
#     """
#     return a + b


# if __name__ == "__main__":

#     # mcp.settings.host = "0.0.0.0"
#     mcp.settings.port = 3005
#     mcp.run(transport="sse")


# File: server.py
 
# Install: pip install langchain langchain-community langchain-aws faiss-cpu boto3
 
from mcp.server.fastmcp import FastMCP
import pandas as pd
import requests
 
# from langchain.vectorstores import FAISS
# from langchain_aws import BedrockEmbeddings
# from langchain.docstore.document import Document
 
# from botocore.config import Config
# import json
# import os
 
# mcp = FastMCP(name="MCP Server")
mcp = FastMCP(
    name="Configured MCP Server",
    # port=8080,  # Sets the default SSE port
    # host="127.0.0.1",  # Sets the default SSE host
    # log_level="DEBUG",  # Sets the logging level
    # on_duplicate_tools="warn",  # Warn if tools with the same name are registered (options: 'error', 'warn', 'ignore')
)
from langchain_community.vectorstores import FAISS
 
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain.document_loaders import PyPDFLoader, TextLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
 
# Simulated refund history to track transactions (in a real scenario, this would be a database)
refund_history = {
    "123": [{"amount": 5, "date": "2025-04-15"}, {"amount": 3, "date": "2025-04-15"}],
    "678": [{"amount": 2, "date": "2025-04-15"}],
}
 
base_url = "https://664f25d4fafad45dfae28919.mockapi.io/api/test"
 
# Simulated aggregate daily refund total (in a real scenario, this would be fetched via APIGEE/CRM)
daily_refund_total = {
    "2025-04-15": 90  # Total refunds processed today (across all customers)
}
 
# # Configure Bedrock for embeddings
# bedrock_config = Config(region_name="us-east-1")
# embeddings = BedrockEmbeddings(
#     model_id="amazon.titan-embed-text-v1",
#     credentials_profile_name="default",
#     region_name="us-east-1",
# )
 
# Use a unique index name for customer data to avoid conflicts
# CUSTOMER_FAISS_INDEX = "faiss_index"
 
 
# def initialize_customer_vector_store():
#     embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
#     # Sample customer data
#     try:
#         if not (os.path.exists("plans.pdf") and os.path.exists("faq.txt")):
#             raise FileNotFoundError("plans.pdf or faq.txt not found.")
#         pdf_loader = PyPDFLoader("plans.pdf")
#         text_loader = TextLoader("faq.txt")
#         documents = pdf_loader.load() + text_loader.load()
#     except FileNotFoundError as e:
#         raise Exception(f"Error: {str(e)}. Please create these files.")
 
#     # Split documents
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#     chunks = text_splitter.split_documents(documents)
 
#     # Create or load FAISS vector store
#     if not os.path.exists("faiss_index"):
#         vector_store = FAISS.from_documents(chunks, embeddings)
#         vector_store.save_local("faiss_index")
#         print("FAISS vector store created.")
#     else:
#         vector_store = FAISS.load_local(
#             "faiss_index", embeddings, allow_dangerous_deserialization=True
#         )
#         print("FAISS vector store loaded.")
 
#     return vector_store
 
 
# Initialize the vector store
# customer_vector_store = initialize_customer_vector_store()
 
 
@mcp.tool()
def greeting(hint: str) -> str:
    """
    This tool just displays a message.
 
    Args:
        hint: The hint is always "MCP Server"
    """
    return "Hey, Lads! This is Felix Kewa and this is my own remote MCP Server!"
 
 
@mcp.tool()
def add(a: int, b: int) -> int:
    """
    This tool is used to add two numbers.
 
    Args:
        a: The first number
        b: The second number
    """
    return a + b
 
 
# @mcp.tool()
# def get_customer(customer_id: str) -> dict:
#     """
#     Fetches customer details by ID using FAISS vector store.
 
#     Args:
#         customer_id: The ID of the customer
#     """
#     # Search for the customer in the FAISS vector store
#     query = f"customer_id: {customer_id}"
#     results = customer_vector_store.similarity_search(query, k=5)  # Get more candidates
 
#     if not results:
#         return {"error": f"Customer {customer_id} not found"}
 
#     # Filter results by exact customer_id match in metadata
#     matching_result = None
#     for result in results:
#         if result.metadata.get("customer_id") == customer_id:
#             matching_result = result
#             break
 
#     if not matching_result:
#         return {"error": f"Customer {customer_id} not found"}
 
#     # Debug: Log the retrieved page_content
#     print(f"Retrieved page_content for customer {customer_id}: {matching_result.page_content}")
 
#     try:
#         customer_data = json.loads(matching_result.page_content)
#     except json.JSONDecodeError as e:
#         return {"error": f"Failed to parse customer data: {str(e)}. Raw content: {matching_result.page_content}"}
 
#     return {
#         "customer_id": customer_data["customer_id"],
#         "plan": customer_data["plan"],
#         "data_limit": customer_data["data_limit"]
#     }
 
# @mcp.tool()
# def get_billing_history(customer_id: str) -> list:
#     """
#     Fetches billing history for a customer using FAISS vector store.
 
#     Args:
#         customer_id: The ID of the customer
#     """
#     # Search for the customer in the FAISS vector store
#     query = f"customer_id: {customer_id}"
#     results = customer_vector_store.similarity_search(query, k=5)  # Get more candidates
 
#     if not results:
#         return [{"error": f"Customer {customer_id} not found"}]
 
#     # Filter results by exact customer_id match in metadata
#     matching_result = None
#     for result in results:
#         if result.metadata.get("customer_id") == customer_id:
#             matching_result = result
#             break
 
#     if not matching_result:
#         return [{"error": f"Customer {customer_id} not found"}]
 
#     # Debug: Log the retrieved page_content
#     print(f"Retrieved page_content for customer {customer_id}: {matching_result.page_content}")
 
#     try:
#         customer_data = json.loads(matching_result.page_content)
#     except json.JSONDecodeError as e:
#         return [{"error": f"Failed to parse customer data: {str(e)}. Raw content: {matching_result.page_content}"}]
 
#     return customer_data["billing_history"]
 
 
# @mcp.tool()
# def check_velocity_rules(customer_id: str, amount: float) -> dict:
#     """
#     Use the check_velocity_rules tool to validate a refund request for customer {customer_id} with amount {amount}.
 
#     Rules:
#     - $5/customer per refund limit
#     - $100/day aggregate limit (across all customers)
#     - Escalation for >$100 refunds
 
#     Args:
#         customer_id: The ID of the customer
#         amount: The refund amount to validate
 
#     Returns:
#         dict: {"status": "approved"} or {"status": "escalate"} or {"status": "denied", "reason": "..."}
#     """
#     # Rule 1: Check per-refund limit ($5/customer per refund)
#     if amount > 5:
#         return {
#             "status": "denied",
#             "reason": f"Refund amount ${amount} exceeds $5/customer per refund limit",
#         }
 
#     # Rule 2: Check daily aggregate limit ($100/day across all customers)
#     today = "2025-04-15"  # Hardcoded for testing (use datetime.today().strftime("%Y-%m-%d") in production)
#     current_daily_total = daily_refund_total.get(today, 0)
#     if current_daily_total + amount > 100:
#         return {
#             "status": "denied",
#             "reason": f"Daily aggregate limit of $100 exceeded. Current total: ${current_daily_total}, requested: ${amount}",
#         }
 
#     # Rule 3: Escalate if refund amount > $100
#     if amount > 100:
#         return {"status": "escalate"}
 
#     return {"status": "approved"}
 
 
# @mcp.tool()
# def process_refund(customer_id: str, amount: float) -> dict:
#     """
#     Based on the validation result {validation_result}, decide whether to process the refund or escalate. If the status is "approved", use the process_refund tool for customer {customer_id} with amount {amount}. If the status is "escalate", indicate that escalation is required.
 
#     Args:
#         customer_id: The ID of the customer
#         amount: The refund amount to process
 
#     Returns:
#         dict: Result of the refund process (e.g., success, denied, or escalated)
#     """
#     # Step 1: Validate velocity rules
#     velocity_result = check_velocity_rules(customer_id, amount)
 
#     if velocity_result["status"] == "denied":
#         return {"status": "failed", "reason": velocity_result["reason"]}
#     elif velocity_result["status"] == "escalate":
#         return {
#             "status": "escalated",
#             "message": "Refund amount exceeds $100, escalation required",
#         }
 
#     # Step 2: Process the refund (simulate success for now)
#     today = "2025-04-15"  # Hardcoded for testing
#     if customer_id not in refund_history:
#         refund_history[customer_id] = []
#     refund_history[customer_id].append({"amount": amount, "date": today})
 
#     # Update daily aggregate total
#     daily_refund_total[today] = daily_refund_total.get(today, 0) + amount
 
#     return {
#         "status": "success",
#         "message": f"Refund of ${amount} processed for customer {customer_id}",
#     }
 
 
# @mcp.tool()
# async def get_customer_data(customer_id: str) -> str:
#     """
#     "Do not guess" "Return only what the tool says"
#     Fetches customer Data by customer ID using get_customer_data tool If NO data found then just say No data found for this customer.
 
#     Args:
#         customer_id: The ID of the customer
#     """
#     # Example API call or DB query here
#     response = requests.get(
#         f"https://664f25d4fafad45dfae28919.mockapi.io/api/test/Customer/{customer_id}"
#     )
 
#     if response.status_code == 200:
#         data = response.json()
#         return f"{data}"
#     else:
#         return "Failed to fetch customer data."
 
 
# @mcp.tool()
# async def get_usage_data(customer_id: str) -> str:
#     """
#     "Do not guess" "Return only what the tool says"
#     Fetches customer usage data by customer ID using get_usage_data tool If NO data found then just say No data found for this customer.
 
#     Args:
#         customer_id: The ID of the customer
#     """
#     # Example API call or DB query here
#     response = requests.get(f"{base_url}/usage_data?customer_id={customer_id}")
#     print({"responseData": response})
 
#     if response.status_code == 200:
#         data = response.json()
#         return f"{data}"
#     else:
#         return "Failed to fetch usage data."
 
 
# @mcp.tool()
# def get_complaint_history(customer_id: str) -> str:
#     """
#     "Do not guess" "Return only what the tool says"
#     Retrieves the complaint history for the given customer.
#     Useful to avoid repeat escalations.
 
#     Args:
#         customer_id: The ID of the customer
#     """
 
#     # Example API call or DB query here
#     response = requests.get(
#         f"https://6800a021b72e9cfaf7280fde.mockapi.io/api/v1/complaints?customer_id={customer_id}"
#     )
 
#     if response.status_code == 200:
#         history = response.json()
#         if not history:
#             return "No past complaints."
#         return "\n".join(
#             [f"Status - {c['status']} , Message -{c['message']}" for c in history]
#         )
#     else:
#         return "No Complaints found for this customer."
 
 
# @mcp.tool()
# def get_escalation_history(customer_id: str) -> str:
#     """
#     "Do not guess" "Return only what the tool says"
#     Retrieves the escalation reason for the given customer.
#     Useful to avoid repeat escalations.
 
#     Args:
#         customer_id: The ID of the customer
#     """
 
#     # Example API call or DB query here
#     response = requests.get(
#         f"https://68009c7ab72e9cfaf7280225.mockapi.io/api/v1/Escalations?complaint_id={customer_id}"
#     )
 
#     if response.status_code == 200:
#         history = response.json()
#         if not history:
#             return "No past complaints."
#         return "\n".join(
#             [
#                 f"notified via - {c['notified_via']} , escalation_reason -{c['escalation_reason']}"
#                 for c in history
#             ]
#         )
#     else:
#         return "No Complaints found for this customer."
 
 
# @mcp.tool()
# def plan_recommendation(customer_id: str) -> str:
#     """
#     "Do not guess" "Return only what the tool says"
#     use get_usage_data tool to fetch usage data by customer ID and then recommend plan from data
#     fetched from plan_recommendation tool
 
#     Args:
#         customer_id: The ID of the customer
#     """
 
#     response = requests.get(f"{base_url}/usage_data/{customer_id}")
 
#     if response.status_code == 200:
#         usage_data = response.json()
#     else:
#         return "No data found for this customer."
 
#     query = f"Plan for {usage_data.data_used_gb}GB monthly usage"
#     top_matches = customer_vector_store.similarity_search(query, k=1)
 
#     if not top_matches:
#         return "No suitable plan found."
 
#     # Step 3: Return top plan (plain)
#     return (
#         f"Plan for {usage_data} monthly usage\n"
#         f"Recommended plan: {top_matches[0].page_content.strip()}"
#     )
 
 
@mcp.tool()
def search_excel_records(
    search_keyword: str, file_path: str = "Nav.xlsx", column_name: str = "Scheme Code"
):
    """
    Search all sheets in an Excel file for records with an exact match of the keyword in the specified column (default: 'Scheme Code').
 
    Args:
        file_path (str, optional): Path to the Excel file (local, URL, Google Drive URL, or S3 URI)
        search_keyword (str): Keyword to match exactly in the specified column
        column_name (str, optional): Column to search in (defaults to 'Scheme Code')
 
    Returns:
        List of dictionaries containing records with exact matches from all sheets
    """
    try:
        # Load the Excel file with all sheets
        xls = pd.ExcelFile(file_path)
        results = []
 
        # Iterate through all sheets
        for sheet_name in xls.sheet_names:
            # Load the current sheet
            df = pd.read_excel(file_path, sheet_name=sheet_name)
 
            # Check if column exists in the sheet
            if column_name not in df.columns:
                continue  # Skip sheet if column doesn't exist
 
            # Perform exact match for the keyword in the specified column
            mask = df[column_name].astype(str) == str(search_keyword)
            matching_rows = df[mask]
 
            # Convert matching rows to list of dictionaries
            if not matching_rows.empty:
                sheet_results = matching_rows.to_dict("records")
                # Add sheet name to each record
                for record in sheet_results:
                    record["Sheet_Name"] = sheet_name
                results.extend(sheet_results)
 
        # Return results or indicate no matches found
        if not results:
            return [
                {
                    "message": f"No exact matches found for '{search_keyword}' in column '{column_name}'"
                }
            ]
        return results
 
    except Exception as e:
        return [{"error": str(e)}]
 
 
if __name__ == "__main__":
    # mcp.settings.host = "0.0.0.0"
    mcp.settings.port = 3005
    mcp.run(transport="sse")
 
 