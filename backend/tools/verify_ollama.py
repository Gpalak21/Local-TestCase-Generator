
import ollama
import sys

def verify_ollama_connection():
    print("🔄 Connecting to local Ollama instance...")
    try:
        # 1. List models to verify connection
        models = ollama.list()
        print(f"✅ Connection successful! Found {len(models['models'])} models.")
        
        # 2. Check for llama3.2
        target_model = "llama3.2:latest"
        found = any(m['model'] == target_model for m in models['models'])
        
        if not found:
            print(f"❌ '{target_model}' not found. Please run 'ollama pull llama3.2'")
            return False
            
        print(f"✅ Target model '{target_model}' is available.")
        
        # 3. Test Generation (Handshake)
        print(f"🔄 Testing generation with '{target_model}'...")
        response = ollama.chat(
            model=target_model,
            messages=[{'role': 'user', 'content': 'Say "Hello, World!" in JSON format: {"message": "..."}'}]
        )
        
        content = response['message']['content']
        print(f"✅ Received response:\n{content}")
        return True
        
    except Exception as e:
        print(f"❌ Error connecting to Ollama: {e}")
        return False

if __name__ == "__main__":
    success = verify_ollama_connection()
    sys.exit(0 if success else 1)
