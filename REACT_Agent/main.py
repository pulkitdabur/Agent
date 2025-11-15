from tools import get_summary,addition 
from google import genai
from dotenv import load_dotenv
import os
import re
load_dotenv()

class Chat:
    """Wrapper class for Google's Gemini API"""
    
    def __init__(self, system=""):
        API_key=os.getenv("API_KEY")
        print(API_key)
        self.system = system
        self.messages = []
        self.genai_client = genai.Client(api_key=API_key)
        self.chat = self.genai_client.chats.create(model="gemini-2.0-flash")
        
        if self.system:
            self.messages.append({"role": "system", "content": system})
            self.chat.send_message(self.system)

    def __call__(self, message):
        if message:
            self.messages.append({"role": "user", "content": message})

        response = self.chat.send_message(message)
        result = response.text

        self.messages.append({"role": "assistant", "content": result})
        return result

class ReActAgent:
    """
    A ReAct (Reasoning and Acting) agent that can use tools to answer questions.
    
    The agent follows the ReAct pattern:
    1. Reason about the task
    2. Act by calling appropriate tools
    3. Observe the results
    4. Repeat until the task is complete
    """
    
    def __init__(self):
        self.memory = []
        self.system_prompt = (
            "You are a helpful assistant. You can use the following tools:\n"
            "- get_summary(query: str): to search Wikipedia\n"
            "- addition(a: int, b:int): to evaluate a math expression\n"
            "When you need to use a tool, respond with: Action: <tool_name>[<input>]\n"
            "Otherwise, respond normally as the assistant.\n"
        )
        

        self.chat = Chat( system=self.system_prompt)

    def __call__(self, message):
        """Process a user message and return a response, using tools if necessary."""
        full_input = "\n".join(self.memory + [f"User: {message}"])
        
        response = self.chat(full_input)
        
        self.memory.append(f"User: {message}")
        self.memory.append(f"Assistant: {response}")

        # Check if the response contains a tool invocation
        if response.startswith("Action:"):
            tool_call = re.match(r'Action:\s*(\w+)\[(.*?)\]', response)
            if not tool_call:
                return "Invalid tool format."

            tool_name, tool_arg = tool_call.groups()
            result = self.invoke_tool(tool_name, tool_arg.strip())
            # print(result)
            self.memory.append(f"Observation: {result}")
            
            # Recursive call to process the tool result
            return self(f"Observation: {result}")
        else:
            # print("RESPONSE-->>",response)
            return response

    def invoke_tool(self, name, arg):
        """Execute a tool with the given argument."""
        try:
            if name == "get_summary":
                return get_summary(arg)
            elif name == "addition":
                print("insdie",arg)
                return addition(arg)
            else:
                return f"Unknown tool: {name}"
        except Exception as e:
            return f"Error executing {name}: {str(e)}"


def main():
    print("Hello from react-agent!")
    test_chat = ReActAgent()

    print(test_chat("add 5 and 4"))

if __name__ == "__main__":
    main()
