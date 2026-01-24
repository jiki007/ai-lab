import os
import pypdf
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ Error: API Key not found in .env file")
    exit()
client = genai.Client(api_key=api_key)

#Function
def extract_text_from_pdf(pdf_path: str) -> str:
    """Opens a PDF and pulls out all the text."""
    print(f"Loading {pdf_path}...")
    try:
        reader = pypdf.PdfReader(pdf_path)
        full_text = ""
        # Loop through every page and grab text
        for page in reader.pages:
            full_text += page.extract_text() + "\n"
        return full_text
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        return ""
    
#Loading the data
filename = "data.pdf"
pdf_content = extract_text_from_pdf(filename)

if not pdf_content:
    print("⚠️ No text found. Creating a dummy context for testing...")
    pdf_content = "This is a dummy PDF content because the file was not found."

print(f"✅ Extracted {len(pdf_content)} characters from PDF.")

system_prompt = f"""
You are an expert analyst. 
Use the following document to answer the user's questions:
----------------
{pdf_content}
----------------
"""


chat = client.chats.create(
    model='gemini-2.5-flash',
    config=genai.types.GenerateContentConfig(
        system_instruction=system_prompt
    )
)

print("--- 🟡 LEVEL 2: Simple RAG System ---")
print("Ask me about the pdf file.")


while True:
    try:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            break
            
        response = chat.send_message(user_input)
        print(f"AI: {response.text}")
        
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"Error: {e}")