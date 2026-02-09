#!/usr/bin/env python3
"""
Script Generator Module
Generates video scripts using either Ollama (local) or Groq (cloud API)
"""

import os
import json
from typing import Dict, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Try importing LLM libraries
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    print("⚠️  Ollama not installed. Install with: pip install ollama")

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    print("⚠️  Groq not installed. Install with: pip install groq")


class ScriptGenerator:
    """Generate video scripts using LLMs"""
    
    def __init__(self):
        self.use_ollama = os.getenv('USE_OLLAMA', 'true').lower() == 'true'
        self.ollama_model = os.getenv('OLLAMA_MODEL', 'llama3.1:8b')
        self.groq_model = os.getenv('GROQ_MODEL', 'llama-3.1-8b-instant')
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        
    def generate_script(self, topic: str, duration: int = 60) -> Dict[str, str]:
        """
        Generate a video script for the given topic
        
        Args:
            topic: The topic/subject for the video
            duration: Target duration in seconds (default: 60)
            
        Returns:
            Dictionary containing title, script, and metadata
        """
        
        prompt = self._create_prompt(topic, duration)
        
        # Use Ollama if available and configured
        if self.use_ollama and OLLAMA_AVAILABLE:
            return self._generate_with_ollama(prompt, topic)
        
        # Otherwise use Groq
        elif GROQ_AVAILABLE and self.groq_api_key:
            return self._generate_with_groq(prompt, topic)
        
        else:
            raise RuntimeError(
                "No LLM backend available. Please install and configure either "
                "Ollama or Groq. See README.md for setup instructions."
            )
    
    def _create_prompt(self, topic: str, duration: int) -> str:
        """Create the prompt for script generation"""
        
        words_estimate = duration * 2.5  # Average speaking rate: 150 words/minute
        
        prompt = f"""Create a compelling {duration}-second YouTube video script about: {topic}

Requirements:
- Target length: approximately {int(words_estimate)} words
- Structure:
  1. HOOK (first 5 seconds): Grab attention immediately with a question or bold statement
  2. MAIN CONTENT (next {duration-15} seconds): Deliver the core message with 3-5 key points
  3. CALL-TO-ACTION (last 10 seconds): Encourage engagement (like, subscribe, comment)

Style Guidelines:
- Conversational and engaging tone
- Short, punchy sentences
- Use "you" to address the viewer directly
- Include rhetorical questions to maintain engagement
- Avoid jargon unless explaining it
- End with an open question to drive comments

Format your response EXACTLY like this:

TITLE: [Catchy video title here]

SCRIPT:
[Your script here - write it as one continuous piece that flows naturally when spoken]

TAGS: [5-8 relevant tags, comma-separated]

Do not include timestamps, scene descriptions, or narrator notes. Just write the exact words to be spoken."""

        return prompt
    
    def _generate_with_ollama(self, prompt: str, topic: str) -> Dict[str, str]:
        """Generate script using local Ollama"""
        
        print(f"🤖 Generating script with Ollama ({self.ollama_model})...")
        
        try:
            response = ollama.chat(
                model=self.ollama_model,
                messages=[
                    {
                        'role': 'system',
                        'content': 'You are an expert YouTube scriptwriter who creates engaging, conversational video scripts that keep viewers hooked.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ]
            )
            
            content = response['message']['content']
            return self._parse_script_response(content, topic)
            
        except Exception as e:
            raise RuntimeError(f"Ollama generation failed: {str(e)}")
    
    def _generate_with_groq(self, prompt: str, topic: str) -> Dict[str, str]:
        """Generate script using Groq API"""
        
        print(f"🤖 Generating script with Groq ({self.groq_model})...")
        
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY not set in environment variables")
        
        try:
            client = Groq(api_key=self.groq_api_key)
            
            response = client.chat.completions.create(
                model=self.groq_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert YouTube scriptwriter who creates engaging, conversational video scripts that keep viewers hooked."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1024
            )
            
            content = response.choices[0].message.content
            return self._parse_script_response(content, topic)
            
        except Exception as e:
            raise RuntimeError(f"Groq generation failed: {str(e)}")
    
    def _parse_script_response(self, content: str, topic: str) -> Dict[str, str]:
        """Parse the LLM response into structured components"""
        
        # Extract title
        title = topic  # Default fallback
        if "TITLE:" in content:
            title_line = content.split("TITLE:")[1].split("\n")[0].strip()
            if title_line:
                title = title_line
        
        # Extract script
        script = ""
        if "SCRIPT:" in content and "TAGS:" in content:
            script = content.split("SCRIPT:")[1].split("TAGS:")[0].strip()
        elif "SCRIPT:" in content:
            script = content.split("SCRIPT:")[1].strip()
        else:
            # If no clear markers, use the whole content
            script = content.strip()
        
        # Extract tags
        tags = []
        if "TAGS:" in content:
            tags_line = content.split("TAGS:")[1].strip()
            tags = [tag.strip() for tag in tags_line.split(",")]
        
        # If no tags, generate from topic
        if not tags:
            tags = topic.lower().split() + ["youtube", "educational"]
        
        return {
            "title": title,
            "script": script,
            "tags": tags[:8],  # Max 8 tags
            "topic": topic,
            "word_count": len(script.split())
        }


def main():
    """Test the script generator"""
    
    # Load a topic from config
    try:
        with open('config/topics.json', 'r') as f:
            topics_data = json.load(f)
            topic_obj = topics_data['topics'][0]
            topic = topic_obj['title']
    except:
        topic = os.getenv('DEFAULT_TOPIC', 'The Future of AI Technology')
    
    # Generate script
    generator = ScriptGenerator()
    result = generator.generate_script(topic)
    
    # Display results
    print("\n" + "="*60)
    print(f"📝 TITLE: {result['title']}")
    print("="*60)
    print(f"\n{result['script']}\n")
    print("="*60)
    print(f"🏷️  TAGS: {', '.join(result['tags'])}")
    print(f"📊 Word Count: {result['word_count']}")
    print("="*60)
    
    # Save to file
    output_dir = os.getenv('OUTPUT_DIR', 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    with open(f'{output_dir}/script.json', 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"\n✅ Script saved to {output_dir}/script.json")


if __name__ == "__main__":
    main()
