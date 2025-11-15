from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import google.generativeai as genai
import time
import re
import os

app = Flask(__name__, static_folder='static')
CORS(app)

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyCWMCKlDTi7yqIqCYCiBuPBvOJ1r-dDu0w"
genai.configure(api_key=GEMINI_API_KEY)

# Model name - Using gemini-2.5-flash (newest model with good rate limits: 10 RPM, 250K TPM)
# Fallback to other available models if needed
MODEL_NAME = 'gemini-2.5-flash'

def get_model():
    """Get or initialize the Gemini model"""
    try:
        return genai.GenerativeModel(MODEL_NAME)
    except Exception:
        # Try alternative model names (prioritize newer models with higher limits)
        alternative_models = [
            'gemini-2.0-flash',      # 15 RPM, 1M TPM
            'gemini-2.5-pro',        # 2 RPM, 125K TPM (more powerful)
            'gemini-2.0-flash-exp',  # Experimental
            'gemini-2.5-flash-lite', # Lite version
            'gemini-2.0-flash-lite', # Lite version
            'gemini-1.5-flash',      # Fallback to older model
            'gemini-1.5-pro'         # Fallback to older model
        ]
        for alt_model in alternative_models:
            try:
                return genai.GenerativeModel(alt_model)
            except Exception:
                continue
        # If all fail, raise error with available models
        raise Exception("Could not initialize model. Please check your API key and model availability.")

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/models', methods=['GET'])
def list_models():
    """Debug endpoint to list available models"""
    try:
        models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                models.append({
                    'name': m.name,
                    'display_name': m.display_name,
                    'description': m.description
                })
        return jsonify({'models': models, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

def generate_with_retry(model, prompt, max_retries=3):
    """Generate content with retry logic for rate limits"""
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            error_str = str(e)
            
            # Check if it's a rate limit/quota error
            if '429' in error_str or 'quota' in error_str.lower() or 'rate' in error_str.lower():
                # Extract retry delay if available
                retry_delay = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                
                # Try to extract delay from error message
                if 'retry in' in error_str.lower():
                    try:
                        # Look for delay in seconds
                        delay_match = re.search(r'retry in ([\d.]+)s', error_str.lower())
                        if delay_match:
                            retry_delay = float(delay_match.group(1)) + 0.5
                    except:
                        pass
                
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                else:
                    raise Exception(f"Rate limit exceeded. Please wait a moment and try again. Error: {error_str}")
            else:
                # For other errors, raise immediately
                raise e
    
    raise Exception("Failed to generate content after retries")

@app.route('/simplify', methods=['POST'])
def simplify():
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Create a prompt for text simplification
        prompt = f"""Simplify the following text by replacing complex words and sentences with simpler, easier-to-understand alternatives. 
        Maintain the exact same meaning and context. Make it accessible to a general audience while preserving all important information.

        Original text:
        {text}

        Simplified text:"""
        
        # Generate simplified text with retry logic
        model = get_model()
        simplified_text = generate_with_retry(model, prompt)
        
        return jsonify({
            'original': text,
            'simplified': simplified_text,
            'success': True
        })
    
    except Exception as e:
        error_message = str(e)
        # Provide user-friendly error messages
        if '429' in error_message or 'quota' in error_message.lower():
            error_message = "Rate limit exceeded. Please wait a moment before trying again. Check your API quota limits."
        elif 'rate' in error_message.lower():
            error_message = "Too many requests. Please wait a moment and try again."
        
        return jsonify({
            'error': error_message,
            'success': False
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

