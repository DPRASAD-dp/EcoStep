import os
import json
from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)
def get_llm_response(prompt: str):
    """Get response from the LLM"""
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Error calling API: {str(e)}"

def get_decision_from_llm(question: str):
    """Ask the LLM to decide if the query requires SQL or direct answer"""
    prompt = f"""
You are an AI assistant. Decide if the user's question can be answered by querying the SQLite table receipts(id, item_name, carbon_footprint, quantity, category, current_date).
- If YES, respond with JSON: {{"mode":"SQL","query":"<SQL_QUERY>"}}
- If NO, respond with JSON: {{"mode":"DIRECT","answer":"<your direct answer>"}}

Question: {question}
    """
    return get_llm_response(prompt)

def format_sql_results(question: str, sql_results: str):
    """Pass the SQL results back to the LLM for formatting"""
    prompt = f"""
The user asked: "{question}"

I queried a database and got these raw results:
{sql_results}

Please format this information into a natural, helpful response that answers the user's question.
Do not mention SQL or database queries in your response.
"""
    return get_llm_response(prompt)

def parse_llm_decision(response: str):
    """Parse the LLM response into mode and payload"""
    try:
        # Try to parse the JSON response
        obj = json.loads(response)
        mode = obj.get("mode", "DIRECT")
        payload = obj.get("query") if mode == "SQL" else obj.get("answer", response)
        return mode, payload
    except json.JSONDecodeError:
        # If not valid JSON, return as direct answer
        return "DIRECT", f"I'm having trouble understanding that. Could you rephrase your question?"

def run_sql(query: str, cursor):
    """Execute SQL query and return results as formatted string"""
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        if not rows:
            return "No results found."
        
        # Format with header
        header = [desc[0] for desc in cursor.description]
        result_data = []
        for row in rows:
            row_dict = {header[i]: row[i] for i in range(len(header))}
            result_data.append(row_dict)
        
        return json.dumps(result_data, indent=2)
    except sqlite3.Error as e:
        return f"SQLite error: {e}"
