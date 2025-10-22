# Importing necessary libraries
import os  # Used to access environment variables (like the API key)
import google.generativeai as genai  # The Google Gemini API library
from dotenv import load_dotenv  # Function to load the .env file
import subprocess #to run shell or cmd commands

def configure_api():
    """
    Loads the API key from the .env file and configures the Gemini API.
    """
    print("Loading API key from .env file...")
    # This line loads the .env file and makes its variables accessible
    load_dotenv() 
    try:
        # Securely get the API key from the environment
        api_key = os.getenv("GEMINI_API_KEY")
        # Check if the key was actually found
        if not api_key:
            # If the key is missing, raise an error to stop the script
            raise ValueError("GEMINI_API_KEY not found in .env file.")
        # Configure the genai library with our key
        genai.configure(api_key=api_key)
        print("Gemini API configured successfully.")
    except ValueError as e:
        # Catch the error we raised and print a helpful message
        print(f"Error: {e}")
        print("Please make sure you have a .env file in the same directory,")
        print("and that it contains a line like: GEMINI_API_KEY=your_key_here")
        exit(1) # exit(1) indicates that the script terminated with an error
    except Exception as e:
        # Catch any other unexpected errors
        print(f"An unexpected error occurred during configuration: {e}")
        exit(1)

def get_gemini_model():
    """
    Initializes and returns the generative model.
    """
    # Using 'gemini-1.5-flash' - it's fast and effective for chat/Q&A
    # primary reason to use this model is that it is fast 
    print("Initializing Gemini model (gemini-2.5-flash)...")
    return genai.GenerativeModel('gemini-2.5-flash')

def ask_gemini(model, query):
    """
    Sends a query to the configured Gemini model and returns the text response.
    
    Args:
        model: The initialized GenerativeModel.
        query (str): The user's question.
        
    Returns:
        str: The text response from Gemini, or an error message.
    """
    if not query:
        return "Error: No query provided."
        
    print(f"\nSending query to Gemini: '{query}'")
    try:
        # The main API call
        response = model.generate_content(query)
        # Return the plain text part of the response
        return response.text
    except Exception as e:
        # Handle potential API errors (network, quota, etc.)
        print(f"An error occurred while contacting the Gemini API: {e}")
        return "Sorry, I couldn't get a response from the API."
    
def execute_command(command):
    """
    Executes a shell command and returns its output or an error message.

    Args:
        command (str): The shell command to execute (e.g., "ls -l", "dir").

    Returns:
        str: The standard output of the command, or an error message.
    """
    print(f"\nExecuting local command: '{command}'")
    try:
        # Run the command
        # check=True: Raises an error if the command fails
        # capture_output=True: Catches the output
        # text=True: Formats output as a string
        # shell=True: Allows us to pass the command as a simple string
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True
        )

        # Return the command's standard output
        if result.stdout:
            return result.stdout
        else:
            return "Command executed successfully (no output)."

    except subprocess.CalledProcessError as e:
        # This 'except' block runs if check=True fails (command returns an error)
        print(f"Error executing command: {e}")
        # Return the error message so the user knows what went wrong
        return e.stderr
    except FileNotFoundError as e:
        # This 'except' block runs if the command itself isn't found
        print(f"Error: Command not found: {e}")
        return f"Error: The command '{command}' was not found on your system."

# The 'if __name__ == "__main__":' block is a standard Python convention.
# It means "run the code inside this block ONLY if this script is executed directly" (e.g., by running 'python main.py').
# It WONT run if this file is imported as a module by another script.
if __name__ == "__main__":
    
    # --- Step 1: Setup ---
    configure_api()
    model = get_gemini_model()
    
    # --- Test 1: The "Brain" (Gemini API) ---
    print("\n--- Starting Test 1: Gemini API Query ---")
    
    test_query = "Who won the FIFA World Cup in 2022?"
    response_text = ask_gemini(model, test_query)
    
    print("\n--- Gemini's Response ---")
    print(response_text)
    print("--------------------------")

    # --- Test 2: The "Hands" (Local Command) ---
    print("\n--- Starting Test 2: Local Command Executor ---")
    
    # Let's test a simple command.
    # Since you're using Git Bash, "ls -l" should work great.
    test_command = "ls -l" 
    # test_command = "dir" # <-- Use this line if you were on Windows CMD
    
    command_output = execute_command(test_command)
    
    print("\n--- Local Command's Output ---")
    print(command_output)
    print("-------------------------------")

    print("\n--- All tests complete ---")