# Importing necessary libraries
import os  # Used to access environment variables (like the API key)
import google.generativeai as genai  # The Google Gemini API library
from dotenv import load_dotenv  # Function to load the .env file

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

# The 'if __name__ == "__main__":' block is a standard Python convention.
# It means "run the code inside this block ONLY if this script is executed directly" (e.g., by running 'python main.py').
# It WONT run if this file is imported as a module by another script.
if __name__ == "__main__":
    
    # --- Step 1: Setup ---
    configure_api()
    model = get_gemini_model()
    
    # --- Step 2: Run Test ---
    print("\n--- Starting Gemini API Test ---")
    
    test_query = "Who is the Prime Minister of India"
    
    response_text = ask_gemini(model, test_query)
    
    # --- Step 3: Show Results ---
    print("\n--- Gemini's Response ---")
    print(response_text)
    print("--------------------------")
        
    print("\n--- Test complete ---")