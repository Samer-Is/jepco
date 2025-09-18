"""
Test script to verify OpenAI API key functionality
"""

import os
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

def test_openai_api():
    """Test OpenAI API connection and functionality"""
    
    print("🧪 Testing OpenAI API Key...")
    
    # Get API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ No API key found in environment variables")
        return False
    
    print(f"✅ API key found: {api_key[:20]}...{api_key[-10:]}")
    
    try:
        # Initialize client
        client = openai.OpenAI(api_key=api_key)
        print("✅ OpenAI client initialized successfully")
        
        # Test with a simple completion
        print("🔄 Testing API call...")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'Hello, JEPCO!' in both English and Arabic."}
            ],
            max_tokens=100,
            temperature=0.7
        )
        
        # Extract and display response
        ai_response = response.choices[0].message.content.strip()
        print("✅ API call successful!")
        print(f"🤖 Response: {ai_response}")
        
        return True
        
    except openai.AuthenticationError:
        print("❌ Authentication failed - Invalid API key")
        return False
    
    except openai.RateLimitError:
        print("❌ Rate limit exceeded")
        return False
    
    except openai.APIError as e:
        print(f"❌ API Error: {str(e)}")
        return False
    
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_openai_api()
    if success:
        print("\n🎉 OpenAI API key is working correctly!")
        print("✅ Ready to run the JEPCO chatbot")
    else:
        print("\n💥 API key test failed!")
        print("❌ Please check your API key configuration")
