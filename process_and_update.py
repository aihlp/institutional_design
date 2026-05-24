#!/usr/bin/env python3
"""
Knowledge Extraction and Wiki Update Script

This script:
1. Reads input text from workflow dispatch or inbox files
2. Calls OpenRouter API to extract structured entities (definitions, facts, research)
3. Updates the repository wiki with the extracted entities
"""

import os
import sys
import json
import time
import subprocess
import re
from datetime import datetime
from pathlib import Path

import requests
import json5


# Configuration
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "openrouter/free"  # Free model router
DEFAULT_PROMPT_TEMPLATE = """You are a precise data extraction tool. Your entire response must be a single valid JSON object and nothing else. Do not include any markdown formatting, explanations, or code fences.

Your task is to analyze text and extract knowledge organized into two fundamental dimensions:

BASIC (STATIC) PARTS - The constituent elements:
1. DEFINITIONS: Explanations of terms, concepts, or specialized vocabulary; foundational conceptual primitives
2. FACTS: Verifiable statements, data points, empirical observations, or established information
3. CONCEPTS: Abstract ideas, theoretical constructs, or mental models that organize thinking
4. ENTITIES: Concrete objects, actors, organizations, or identifiable things in the domain

DYNAMIC (RELATIONAL) PARTS - The connections and flows between elements:
5. RELATIONSHIPS: Connections, associations, or links between entities/concepts (e.g., "causes", "influences", "part-of")
6. PROCESSES: Sequences of actions, transformations, or temporal flows that describe how things change
7. MECHANISMS: Causal pathways, explanatory logics, or functional operations that produce outcomes
8. CONTEXTS: Situational conditions, environmental factors, or boundary conditions that shape meaning

Return your analysis as a JSON object with exactly eight arrays: "definitions", "facts", "concepts", "entities", "relationships", "processes", "mechanisms", and "contexts".
Each item should have a "text" field (the extracted content), optionally a "context" field (additional relevant information), and for dynamic parts, optionally "source" and "target" fields to specify relinks.

Example format:
{
  "definitions": [
    {"text": "Term explanation", "context": "Related concept"}
  ],
  "facts": [
    {"text": "Verifiable statement"}
  ],
  "concepts": [
    {"text": "Abstract idea or theoretical construct", "context": "Domain area"}
  ],
  "entities": [
    {"text": "Concrete object or actor", "context": "Type or category"}
  ],
  "relationships": [
    {"text": "Connection description", "source": "Entity A", "target": "Entity B"}
  ],
  "processes": [
    {"text": "Process description", "source": "Starting state", "target": "Ending state"}
  ],
  "mechanisms": [
    {"text": "Causal mechanism", "source": "Cause", "target": "Effect"}
  ],
  "contexts": [
    {"text": "Contextual condition", "context": "Applicable domain"}
  ]
}

CRITICAL INSTRUCTIONS:
- Output ONLY the raw JSON object. No markdown, no code blocks, no explanations.
- Do not wrap your response in ```json or ``` markers.
- Do not add any text before or after the JSON object.
- The JSON must start with { and end with }.
- If you cannot extract any entities from a category, use an empty array [].
- For DYNAMIC parts (relationships, processes, mechanisms), try to identify source and target when possible to enable relinking.

Begin your response with { and end with }."""
MAX_RETRIES = 2  # Maximum 2 attempts: one with json_schema, one with json_object fallback
RETRY_DELAY_BASE = 2  # seconds
RATE_LIMIT_DELAY = 30  # seconds to wait on 429 errors


def build_extraction_json_schema() -> dict:
    """
    Build a JSON schema for structured output dynamically.
    
    The schema defines the expected output format but the parser will accept
    ANY valid JSON and normalize it, so this is just a hint to the model.
    
    Returns:
        JSON schema object for the response_format parameter
    """
    return {
        "name": "knowledge_extraction",
        "strict": False,
        "schema": {
            "type": "object",
            "properties": {
                "definitions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"},
                            "context": {"type": "string"}
                        },
                        "required": ["text"]
                    }
                },
                "facts": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"},
                            "context": {"type": "string"}
                        },
                        "required": ["text"]
                    }
                },
                "concepts": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"},
                            "context": {"type": "string"}
                        },
                        "required": ["text"]
                    }
                },
                "entities": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"},
                            "context": {"type": "string"}
                        },
                        "required": ["text"]
                    }
                },
                "relationships": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"},
                            "source": {"type": "string"},
                            "target": {"type": "string"}
                        },
                        "required": ["text"]
                    }
                },
                "processes": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"},
                            "source": {"type": "string"},
                            "target": {"type": "string"}
                        },
                        "required": ["text"]
                    }
                },
                "mechanisms": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"},
                            "source": {"type": "string"},
                            "target": {"type": "string"}
                        },
                        "required": ["text"]
                    }
                },
                "contexts": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"},
                            "context": {"type": "string"}
                        },
                        "required": ["text"]
                    }
                }
            },
            "required": ["definitions", "facts", "concepts", "entities", "relationships", "processes", "mechanisms", "contexts"]
        }
    }


def log(message: str):
    """Print a log message."""
    print(f"[INFO] {message}")


def log_error(message: str):
    """Print an error message."""
    print(f"[ERROR] {message}", file=sys.stderr)


def get_input_text() -> tuple[str, str]:
    """
    Get input text and source label from environment variables.
    
    Returns:
        Tuple of (text, source_label)
    """
    # Check for manual dispatch input
    manual_text = os.environ.get("INPUT_TEXT", "").strip()
    manual_source = os.environ.get("INPUT_SOURCE", "").strip()
    
    if manual_text:
        source = manual_source if manual_source else "manual"
        return manual_text, source
    
    # Check for file-based input
    inbox_path = os.environ.get("INBOX_PATH", "inbox").strip()
    file_pattern = os.environ.get("FILE_PATTERN", "").strip()
    
    if not inbox_path:
        inbox_path = "inbox"
    
    if file_pattern:
        # Specific file triggered the workflow
        matching_files = list(Path(inbox_path).glob(file_pattern))
        if matching_files:
            txt_file = matching_files[0]
            content = txt_file.read_text(encoding="utf-8").strip()
            source = txt_file.stem  # filename without extension
            if content:
                return content, source
    
    # Look for any .txt files in inbox
    inbox_dir = Path(inbox_path)
    if inbox_dir.exists():
        txt_files = sorted(inbox_dir.glob("*.txt"))
        if txt_files:
            # Process the most recently modified file
            txt_file = max(txt_files, key=lambda f: f.stat().st_mtime)
            content = txt_file.read_text(encoding="utf-8").strip()
            source = txt_file.stem
            if content:
                return content, source
    
    return "", ""


def call_openrouter(text: str, use_schema: bool = True) -> tuple[dict | None, bool]:
    """
    Call OpenRouter API to extract entities from text.
    
    Args:
        text: The input text to process
        use_schema: If True, use json_schema response format; if False, use json_object
        
    Returns:
        Tuple of (parsed JSON dict or None, schema_supported boolean)
        schema_supported indicates whether the API supports json_schema format
    """
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        log_error("OPENROUTER_API_KEY environment variable not set")
        return None, True
    
    model = os.environ.get("OPENROUTER_MODEL", DEFAULT_MODEL)
    prompt_template = os.environ.get("OPENROUTER_PROMPT_TEMPLATE", DEFAULT_PROMPT_TEMPLATE)
    
    # Get repo URL for HTTP-Referer header
    github_server = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
    github_repo = os.environ.get("GITHUB_REPOSITORY", "unknown/repo")
    repo_url = f"{github_server}/{github_repo}"
    
    # Build user message with clear instruction
    user_prompt = f"""{prompt_template}

Text to analyze:
{text}"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": repo_url,
        "X-Title": "Knowledge Extractor"
    }
    
    # Build payload with appropriate response format
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 24000,  # Maximum output tokens to avoid truncation
    }
    
    # Use json_schema if requested, otherwise json_object
    if use_schema:
        payload["response_format"] = {
            "type": "json_schema",
            "json_schema": build_extraction_json_schema()
        }
    else:
        payload["response_format"] = {"type": "json_object"}
    
    # Note: removed "provider": {"require_parameters": true} - overly restrictive on free tier
    # Note: removed "plugins" - not needed for basic extraction
    
    # Add provider routing hints for openrouter/free to ensure JSON-capable model selection
    if model == "openrouter/free":
        payload["provider"] = {
            "order": ["Anthropic", "Google", "Meta"],
            "allow_fallbacks": True,
            "require_parameters": False
        }
        # Also add a specific model hint for reliable JSON output
        # Try claude-3-haiku first as it's free and supports json_schema well
        payload["models"] = [
            "anthropic/claude-3-haiku",
            "google/gemini-flash-1.5",
            "meta-llama/llama-3-8b-instruct"
        ]
    
    try:
        log(f"Calling OpenRouter API with {'json_schema' if use_schema else 'json_object'} format...")
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload, timeout=60)
        
        # Check for OpenRouter errors returned inside HTTP 200
        if response.status_code == 200:
            result = response.json()
            # Check for error field in response body
            if "error" in result:
                error_info = result.get("error", {})
                error_code = error_info.get("code", "")
                error_msg = error_info.get("message", "Unknown error")
                
                # Handle 429 rate limit specifically
                if error_code == 429 or "rate limit" in error_msg.lower():
                    log_error("Rate limit (429) received from OpenRouter")
                    log(f"Waiting {RATE_LIMIT_DELAY} seconds before continuing...")
                    time.sleep(RATE_LIMIT_DELAY)
                    return None, True  # Signal to retry with backoff
                
                log_error(f"OpenRouter API error: {error_msg}")
                return None, True
        
        # Log raw response for debugging empty responses (after error check)
        if response.status_code == 200 and (not response.text or len(response.text.strip()) == 0):
            log_error("Empty response body from API (HTTP 200 but no content)")
            return None, True
        
        # Check HTTP status code - handle different error codes appropriately
        if response.status_code == 403:
            log_error("HTTP 403 Forbidden received from OpenRouter API")
            log_error("Please check the following:")
            log_error("  1. OPENROUTER_API_KEY secret is valid and has credits")
            log_error("  2. OPENROUTER_MODEL variable specifies an accessible free model")
            log_error(f"     Current model: {model}")
            log_error("     Note: 'openrouter/free' is a special router that auto-selects a free model")
            log_error("  3. Required headers (Authorization, Content-Type, HTTP-Referer, X-Title) are set correctly")
            log_error(f"     HTTP-Referer: {repo_url}")
            log_error("  4. Model is available at https://openrouter.ai/models?q=free")
            return None, True
        
        # Handle rate limiting (429) - wait and signal for retry
        if response.status_code == 429:
            log_error("HTTP 429 received - rate limit exceeded")
            log(f"Waiting {RATE_LIMIT_DELAY} seconds before continuing...")
            time.sleep(RATE_LIMIT_DELAY)
            return None, True
        
        # Handle service unavailable (503)
        if response.status_code == 503:
            log_error("HTTP 503 received - service unavailable")
            return None, True
        
        # For other non-200 status codes
        if response.status_code != 200:
            log_error(f"Unexpected HTTP status code: {response.status_code}")
            log_error(f"Response body: {response.text[:500]}")
            return None, True
        
        result = response.json()
        
        # Debug: log the full response structure for debugging
        log(f"API response structure: choices={len(result.get('choices', []))}, model={result.get('model', 'unknown')}")
        
        if not result.get("choices"):
            log_error(f"Full API response: {json.dumps(result, indent=2)[:1500]}")
        
        choices = result.get("choices", [])
        if not choices:
            log_error("No choices in API response")
            return None, True
        
        choice = choices[0]
        finish_reason = choice.get("finish_reason", "")
        content = choice.get("message", {}).get("content", "")
        
        # Debug: log if content is empty but choices exist
        if not content and choices:
            log_error(f"Choice has no content. Choice structure: {json.dumps(choice, indent=2)[:800]}")
            log_error(f"Finish reason: {finish_reason}")
            log_error(f"Model used: {result.get('model', 'unknown')}")
            # This often happens when the model doesn't support the response_format parameter
            # Try falling back to json_object format
            return None, False
        
        # Validate finish_reason is "stop" (not "length")
        if finish_reason == "length":
            log_error("Response truncated due to max_tokens limit (finish_reason: length)")
            return None, True
        
        if not content:
            log_error("Empty response from API (no content in choices)")
            return None, True
        
        # Try to parse JSON
        parsed = parse_json_response(content)
        if parsed:
            return parsed, True
        
        # If parsing failed, the schema might not be supported
        log_error(f"Failed to parse JSON from response: {content[:200]}...")
        return None, False  # Signal that json_schema may not be supported
        
    except requests.exceptions.Timeout as e:
        log_error(f"API request timed out: {e}")
        return None, True
    except requests.exceptions.RequestException as e:
        log_error(f"API request failed: {e}")
        return None, True
    except json.JSONDecodeError as e:
        log_error(f"Failed to parse API response as JSON: {e}")
        return None, True


def normalize_json_to_structure(data: dict) -> dict:
    """
    Normalize any JSON object to the required eight-category structure.
    
    Uses heuristic key mapping:
    - definitions, definition, defines, glossary → definitions
    - facts, fact, findings, observations → facts
    - concepts, concept, ideas, constructs → concepts
    - entities, entity, actors, organizations → entities
    - relationships, relationship, connections, links → relationships
    - processes, process, sequences, flows → processes
    - mechanisms, mechanism, causal pathways → mechanisms
    - contexts, context, conditions, boundaries → contexts
    
    Args:
        data: Any valid JSON dict
        
    Returns:
        Normalized dict with definitions, facts, concepts, entities, relationships, processes, mechanisms, contexts arrays
    """
    result = {
        "definitions": [], 
        "facts": [], 
        "concepts": [], 
        "entities": [], 
        "relationships": [], 
        "processes": [], 
        "mechanisms": [], 
        "contexts": []
    }
    
    # Key category mappings
    definition_keys = {"definitions", "definition", "defines", "glossary", "terms", "terminology"}
    fact_keys = {"facts", "fact", "findings", "observations", "data_points", "statements", "information"}
    concept_keys = {"concepts", "concept", "ideas", "constructs", "theoretical_constructs", "mental_models"}
    entity_keys = {"entities", "entity", "actors", "organizations", "objects", "things"}
    relationship_keys = {"relationships", "relationship", "connections", "links", "associations", "relations"}
    process_keys = {"processes", "process", "sequences", "flows", "transformations", "actions"}
    mechanism_keys = {"mechanisms", "mechanism", "causal_pathways", "explanatory_logics", "functional_operations"}
    context_keys = {"contexts", "context", "conditions", "boundaries", "situational_factors", "environmental_factors"}
    
    def extract_text_from_item(item) -> dict | None:
        """Extract text and context from various item formats."""
        if isinstance(item, str):
            return {"text": item.strip()} if item.strip() else None
        elif isinstance(item, dict):
            # Look for text-like fields
            text_fields = ["text", "content", "value", "statement", "point", "description", "title", "name"]
            context_fields = ["context", "source", "reference", "note", "details", "explanation"]
            
            text_value = None
            context_value = None
            
            for field in text_fields:
                if field in item and isinstance(item[field], str) and item[field].strip():
                    text_value = item[field].strip()
                    break
            
            for field in context_fields:
                if field in item and isinstance(item[field], str) and item[field].strip():
                    context_value = item[field].strip()
                    break
            
            # If no text field found, try to concatenate all string values
            if not text_value:
                all_strings = [v for v in item.values() if isinstance(v, str) and v.strip()]
                if all_strings:
                    text_value = all_strings[0].strip()
            
            if text_value:
                result_item = {"text": text_value}
                if context_value:
                    result_item["context"] = context_value
                return result_item
            return None
        return None
    
    def process_array(arr: list, category: str):
        """Process an array and add items to the appropriate category."""
        for item in arr:
            extracted = extract_text_from_item(item)
            if extracted:
                result[category].append(extracted)
    
    def categorize_key(key: str) -> str:
        """Determine which category a key belongs to."""
        key_lower = key.lower()
        if key_lower in definition_keys:
            return "definitions"
        elif key_lower in fact_keys:
            return "facts"
        elif key_lower in concept_keys:
            return "concepts"
        elif key_lower in entity_keys:
            return "entities"
        elif key_lower in relationship_keys:
            return "relationships"
        elif key_lower in process_keys:
            return "processes"
        elif key_lower in mechanism_keys:
            return "mechanisms"
        elif key_lower in context_keys:
            return "contexts"
        else:
            return "facts"  # Safe default
    
    def process_value(key: str, value, depth: int = 0):
        """Recursively process a value and categorize it."""
        # Prevent infinite recursion
        if depth > 5:
            return
        
        if isinstance(value, list):
            category = categorize_key(key)
            process_array(value, category)
        elif isinstance(value, dict):
            # Check if this dict looks like a data item (has text-like content)
            extracted = extract_text_from_item(value)
            if extracted:
                category = categorize_key(key)
                result[category].append(extracted)
            else:
                # Recurse into nested dicts
                for nested_key, nested_value in value.items():
                    process_value(nested_key, nested_value, depth + 1)
        elif isinstance(value, str) and value.strip():
            # Plain string value - add to facts by default
            result["facts"].append({"text": value.strip()})
    
    # Process all top-level keys
    for key, value in data.items():
        process_value(key, value)
    
    return result


def parse_json_response(content: str) -> dict | None:
    """
    Parse JSON from API response, handling potential markdown formatting and any structure.
    
    This function:
    1. Handles code fences (```json ... ```) with a regex that correctly captures nested braces
    2. Strips any preamble text before the first {
    3. Parses the JSON using multiple stages (json → json5 → sanitized fallback)
    4. Normalizes it to the required {definitions, facts, research} structure
    
    Args:
        content: Raw response content
        
    Returns:
        Normalized dict with definitions, facts, research arrays, or None if no JSON found
    """
    # Remove markdown code blocks if present - use greedy pattern for nested braces
    content = content.strip()
    
    # Try to extract JSON from markdown code blocks (greedy pattern handles nested braces)
    json_match = re.search(r'```(?:json)?\s*(\{.*\})\s*```', content, re.DOTALL)
    if json_match:
        content = json_match.group(1)
    
    # If still wrapped in backticks or has prefix text, find the first JSON object
    if not content.startswith('{'):
        # Find the first { and last } to extract the complete JSON object
        brace_match = re.search(r'\{.*\}', content, re.DOTALL)
        if brace_match:
            content = brace_match.group(0)
    
    # Check if we have any JSON-like content
    if not content.startswith('{'):
        log_error(f"No JSON object found in response. Content starts with: {content[:200]}")
        return None
    
    # Stage 1: Try strict json.loads() (fast path for well-formed JSON)
    try:
        data = json.loads(content)
        
        # Validate it's a dict
        if not isinstance(data, dict):
            log_error(f"Parsed JSON is not an object: {type(data)}")
            return None
        
        # Normalize to required structure using heuristic key mapping
        normalized = normalize_json_to_structure(data)
        
        # Return the normalized structure (always has definitions, facts, research keys)
        return normalized
        
    except json.JSONDecodeError as e:
        # Log the problematic content for debugging (first 200 chars)
        log_error(f"Stage 1 (json.loads) failed: {e}")
    
    # Stage 2: Try json5.loads() (handles trailing commas, unquoted keys, single quotes)
    try:
        data = json5.loads(content)
        
        # Validate it's a dict
        if not isinstance(data, dict):
            log_error(f"Parsed JSON5 is not an object: {type(data)}")
            return None
        
        # Normalize to required structure
        normalized = normalize_json_to_structure(data)
        log("Stage 2 (json5) succeeded in parsing malformed JSON")
        return normalized
        
    except Exception as e:
        log_error(f"Stage 2 (json5.loads) failed: {e}")
    
    # Stage 3: Attempt to sanitize and fix common JSON errors
    # Try to fix the character at the reported error position
    try:
        sanitized = _sanitize_json_content(content)
        if sanitized != content:
            data = json.loads(sanitized)
            
            # Validate it's a dict
            if not isinstance(data, dict):
                log_error(f"Sanitized JSON is not an object: {type(data)}")
                return None
            
            # Normalize to required structure
            normalized = normalize_json_to_structure(data)
            log("Stage 3 (sanitization) succeeded in fixing JSON")
            return normalized
    except Exception as e:
        log_error(f"Stage 3 (sanitization) failed: {e}")
    
    # Stage 4: All attempts failed
    log_error("All JSON parsing stages failed")
    return None


def _sanitize_json_content(content: str) -> str:
    """
    Attempt to sanitize and fix common JSON syntax errors.
    
    This function tries to fix:
    - Unescaped quotes inside string values
    - Unescaped backslashes
    - Control characters like newlines inside strings
    
    Args:
        content: Raw JSON content with potential syntax errors
        
    Returns:
        Sanitized JSON content
    """
    # First, try to identify the error position by attempting to parse
    # and catching the JSONDecodeError to get the position
    try:
        json.loads(content)
        return content  # Already valid
    except json.JSONDecodeError as e:
        error_pos = e.pos
        error_msg = str(e)
    
    # Common fixes based on error message patterns
    # Fix unescaped quotes inside strings by finding string boundaries
    result = []
    i = 0
    in_string = False
    escape_next = False
    
    while i < len(content):
        char = content[i]
        
        if escape_next:
            result.append(char)
            escape_next = False
            i += 1
            continue
        
        if char == '\\':
            result.append(char)
            escape_next = True
            i += 1
            continue
        
        if char == '"' and not escape_next:
            in_string = not in_string
            result.append(char)
            i += 1
            continue
        
        if in_string and char in '\n\r\t':
            # Escape control characters inside strings
            if char == '\n':
                result.append('\\n')
            elif char == '\r':
                result.append('\\r')
            elif char == '\t':
                result.append('\\t')
            i += 1
            continue
        
        result.append(char)
        i += 1
    
    sanitized = ''.join(result)
    
    # Try to fix trailing commas before } or ]
    sanitized = re.sub(r',(\s*[}\]])', r'\1', sanitized)
    
    # Try to fix unquoted keys (simple case: word followed by colon)
    # Only do this if it looks like JSON5-style unquoted keys
    # sanitized = re.sub(r'([{,]\s*)([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'\1"\2":', sanitized)
    
    return sanitized


def clone_wiki(repo_url: str, wiki_dir: Path) -> bool:
    """
    Clone the repository wiki.
    
    Args:
        repo_url: Base repository URL
        wiki_dir: Directory to clone into
        
    Returns:
        True on success, False on failure
    """
    token = os.environ.get("WIKI_PUSH_TOKEN", "")
    if not token:
        log_error("WIKI_PUSH_TOKEN environment variable not set")
        return False
    
    wiki_url = f"{repo_url}.wiki.git"
    
    # Insert token for authentication
    auth_url = wiki_url.replace("https://", f"https://{token}@")
    
    try:
        log(f"Cloning wiki from {wiki_url}...")
        subprocess.run(
            ["git", "clone", "--depth", "1", auth_url, str(wiki_dir)],
            check=True,
            capture_output=True,
            text=True
        )
        return True
    except subprocess.CalledProcessError as e:
        log_error(f"Failed to clone wiki: {e.stderr}")
        return False


def read_wiki_page(wiki_dir: Path, page_name: str) -> str:
    """
    Read content of a wiki page.
    
    Args:
        wiki_dir: Wiki directory
        page_name: Page name (without .md extension)
        
    Returns:
        Page content or empty string if doesn't exist
    """
    page_path = wiki_dir / f"{page_name}.md"
    if page_path.exists():
        return page_path.read_text(encoding="utf-8")
    return ""


def write_wiki_page(wiki_dir: Path, page_name: str, content: str):
    """
    Write content to a wiki page.
    
    Args:
        wiki_dir: Wiki directory
        page_name: Page name (without .md extension)
        content: Page content
    """
    page_path = wiki_dir / f"{page_name}.md"
    page_path.write_text(content, encoding="utf-8")


def append_entities_to_page(existing_content: str, entities: list[dict], date_str: str, source: str) -> str:
    """
    Append entities to wiki page content, avoiding duplicates.
    
    Args:
        existing_content: Current page content
        entities: List of entity dicts with 'text' and optional 'context'
        date_str: Date string for heading
        source: Source label
        
    Returns:
        Updated page content
    """
    if not entities:
        return existing_content
    
    heading = f"## {date_str} – {source}"
    
    # Build new entries
    new_entries = []
    for entity in entities:
        text = entity.get("text", "").strip()
        context = entity.get("context", "").strip()
        
        if not text:
            continue
        
        # Format entry
        if context:
            entry = f"- **{text}** *(context: {context})*"
        else:
            entry = f"- **{text}**"
        
        # Check for duplicate in existing content under same date/source
        if heading in existing_content and entry in existing_content:
            log(f"Skipping duplicate entry: {text[:50]}...")
            continue
        
        new_entries.append(entry)
    
    if not new_entries:
        return existing_content
    
    # Build updated content
    if not existing_content.strip():
        # New page - add title
        category = "Knowledge Base"
        if "Definitions" in str(entities):
            category = "Definitions"
        content = f"# {category}\n\n"
    else:
        content = existing_content.rstrip() + "\n\n"
    
    content += f"{heading}\n"
    for entry in new_entries:
        content += f"{entry}\n"
    
    return content


def format_dynamic_entry(entry: dict, category: str) -> str:
    """
    Format a dynamic entry (relationships, processes, mechanisms) with relinking information.
    
    Args:
        entry: Entry dict with text, source, target fields
        category: Category name for formatting
        
    Returns:
        Formatted markdown string
    """
    text = entry.get("text", "")
    source = entry.get("source", "")
    target = entry.get("target", "")
    context = entry.get("context", "")
    
    # Build the base entry
    parts = [f"- **{text}**"]
    
    # Add relink information if present
    if source and target:
        parts.append(f"*(links: [[{source}]] → [[{target}]])*)")
    elif source:
        parts.append(f"*(from: [[{source}]])*)")
    elif target:
        parts.append(f"*(to: [[{target}]])*)")
    
    # Add context if present
    if context:
        parts.append(f"*(context: {context})*")
    
    return " ".join(parts)


def generate_home_page(extracted_data: dict) -> str:
    """
    Generate Home page content with index and cross-references to all knowledge categories.
    
    Args:
        extracted_data: Dict with all eight entity arrays
        
    Returns:
        Markdown content for Home page
    """
    content = "# Knowledge Base Index\n\n"
    content += "This wiki organizes knowledge into **two fundamental dimensions**: Basic (static) parts and Dynamic (relational) parts.\n\n"
    
    # Basic (Static) Parts Section
    content += "## Basic (Static) Parts\n\n"
    content += "The constituent elements that make up the knowledge base:\n\n"
    
    basic_categories = [
        ("Definitions", "definitions", "Explanations of terms, concepts, or specialized vocabulary"),
        ("Facts", "facts", "Verifiable statements, data points, empirical observations"),
        ("Concepts", "concepts", "Abstract ideas, theoretical constructs, mental models"),
        ("Entities", "entities", "Concrete objects, actors, organizations, identifiable things"),
        ("Contexts", "contexts", "Situational conditions, environmental factors, boundary conditions")
    ]
    
    for display_name, key, description in basic_categories:
        entities = extracted_data.get(key, [])
        count = len(entities) if entities else 0
        content += f"### [[{display_name}]]\n"
        content += f"{description}\n\n"
        if count > 0:
            content += f"*Recent entries: {count}*\n\n"
    
    # Dynamic (Relational) Parts Section
    content += "## Dynamic (Relational) Parts\n\n"
    content += "The connections and flows between elements that enable relinking:\n\n"
    
    dynamic_categories = [
        ("Relationships", "relationships", "Connections, associations, or links between entities/concepts"),
        ("Processes", "processes", "Sequences of actions, transformations, temporal flows"),
        ("Mechanisms", "mechanisms", "Causal pathways, explanatory logics, functional operations")
    ]
    
    for display_name, key, description in dynamic_categories:
        entities = extracted_data.get(key, [])
        count = len(entities) if entities else 0
        content += f"### [[{display_name}]]\n"
        content += f"{description}\n\n"
        if count > 0:
            content += f"*Recent entries: {count} (with source/target relinks)*\n\n"
    
    # Cross-reference summary
    content += "## Navigation Guide\n\n"
    content += "- **Start here**: Browse [[Definitions]] and [[Concepts]] to understand key terms\n"
    content += "- **Explore connections**: Check [[Relationships]], [[Processes]], and [[Mechanisms]] for causal links\n"
    content += "- **Find concrete examples**: Look at [[Entities]] and [[Facts]] for specific instances\n"
    content += "- **Understand context**: Review [[Contexts]] for situational factors\n\n"
    
    content += "---\n"
    content += f"*Last updated: {datetime.now().strftime('%Y-%m-%d')}*\n"
    
    return content


def update_wiki(wiki_dir: Path, extracted_data: dict, date_str: str, source: str) -> bool:
    """
    Update wiki pages with extracted entities.
    
    Args:
        wiki_dir: Wiki directory
        extracted_data: Dict with definitions, facts, concepts, entities, relationships, processes, mechanisms, contexts arrays
        date_str: Date string for headings
        source: Source label
        
    Returns:
        True on success, False on failure
    """
    # Basic (static) parts - simple list entries
    basic_pages = {
        "Definitions": extracted_data.get("definitions", []),
        "Facts": extracted_data.get("facts", []),
        "Concepts": extracted_data.get("concepts", []),
        "Entities": extracted_data.get("entities", []),
        "Contexts": extracted_data.get("contexts", [])
    }
    
    # Dynamic (relational) parts - entries with source/target relinks
    dynamic_pages = {
        "Relationships": extracted_data.get("relationships", []),
        "Processes": extracted_data.get("processes", []),
        "Mechanisms": extracted_data.get("mechanisms", [])
    }
    
    updates_needed = False
    
    # Process basic pages
    for page_name, entities in basic_pages.items():
        if not entities:
            continue
        
        existing = read_wiki_page(wiki_dir, page_name)
        updated = append_entities_to_page(existing, entities, date_str, source)
        
        if updated != existing:
            write_wiki_page(wiki_dir, page_name, updated)
            updates_needed = True
            log(f"Updated {page_name}.md")
    
    # Process dynamic pages with relinking
    for page_name, entities in dynamic_pages.items():
        if not entities:
            continue
        
        # Format dynamic entries with relinks
        formatted_entries = []
        for entry in entities:
            formatted = format_dynamic_entry(entry, page_name)
            formatted_entries.append({"text": formatted})
        
        existing = read_wiki_page(wiki_dir, page_name)
        updated = append_entities_to_page(existing, formatted_entries, date_str, source)
        
        if updated != existing:
            write_wiki_page(wiki_dir, page_name, updated)
            updates_needed = True
            log(f"Updated {page_name}.md")
    
    # Create/update Home page with index and cross-references
    home_content = generate_home_page(extracted_data)
    existing_home = read_wiki_page(wiki_dir, "Home")
    if home_content != existing_home:
        write_wiki_page(wiki_dir, "Home", home_content)
        updates_needed = True
        log("Updated Home.md with index and cross-references")
    
    return updates_needed


def push_wiki_changes(wiki_dir: Path, source: str) -> bool:
    """
    Commit and push wiki changes.
    
    Args:
        wiki_dir: Wiki directory
        source: Source label for commit message
        
    Returns:
        True on success, False on failure
    """
    token = os.environ.get("WIKI_PUSH_TOKEN", "")
    if not token:
        log_error("WIKI_PUSH_TOKEN not set")
        log_error("Please ensure the WIKI_PUSH_TOKEN secret is configured with a GitHub classic token.")
        log_error("The token must have 'repo' and 'wiki' scopes.")
        log_error("Create token at: https://github.com/settings/tokens/new (select 'Classic' token)")
        return False
    
    # Verify token has wiki access by attempting a lightweight git fetch
    # Note: GitHub's /repos/{owner}/{repo}/wiki API endpoint is unreliable (often returns 404 even for existing wikis)
    # Instead, we verify access by checking if we can fetch from the wiki remote
    github_repo = os.environ.get("GITHUB_REPOSITORY", "")
    if github_repo:
        log("Verifying WIKI_PUSH_TOKEN has wiki access via git fetch...")
        try:
            fetch_result = subprocess.run(
                ["git", "fetch", "origin"],
                cwd=wiki_dir,
                capture_output=True,
                text=True,
                timeout=15
            )
            if fetch_result.returncode != 0:
                stderr_output = fetch_result.stderr.lower()
                if "authentication" in stderr_output or "403" in stderr_output or "permission" in stderr_output:
                    log_error("Git fetch failed: WIKI_PUSH_TOKEN lacks wiki scope or authentication failed")
                    log_error(f"Fetch error: {fetch_result.stderr.strip()}")
                    log_error("Ensure the token has 'repo' (or 'public_repo') AND 'wiki' scopes.")
                    log_error("Create a new classic token at: https://github.com/settings/tokens/new")
                    return False
                elif "404" in stderr_output or "not found" in stderr_output:
                    log_error("Git fetch failed: Wiki may not be enabled or repository not found")
                    log_error(f"Fetch error: {fetch_result.stderr.strip()}")
                    return False
                else:
                    log(f"Git fetch returned non-zero exit code, proceeding anyway: {fetch_result.stderr.strip()}")
            else:
                log("Wiki access verified successfully via git fetch")
        except subprocess.TimeoutExpired:
            log_error("Git fetch timed out - network issue or slow response")
            # Continue anyway - verification is optional
        except Exception as e:
            log_error(f"Failed to verify wiki access via git fetch: {e}")
            # Continue anyway - verification is optional
    
    try:
        # Configure git user
        subprocess.run(
            ["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"],
            cwd=wiki_dir,
            check=True,
            capture_output=True
        )
        subprocess.run(
            ["git", "config", "user.name", "github-actions[bot]"],
            cwd=wiki_dir,
            check=True,
            capture_output=True
        )
        
        # Stage all changes
        subprocess.run(
            ["git", "add", "-A"],
            cwd=wiki_dir,
            check=True,
            capture_output=True
        )
        
        # Check if there are changes to commit
        status_result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=wiki_dir,
            check=True,
            capture_output=True,
            text=True
        )
        
        if not status_result.stdout.strip():
            log("No wiki changes to commit")
            return True
        
        # Commit
        commit_msg = f"Update wiki from: {source}"
        subprocess.run(
            ["git", "commit", "-m", commit_msg],
            cwd=wiki_dir,
            check=True,
            capture_output=True
        )
        
        # Prepare remote URL with token - always set it to ensure authentication
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=wiki_dir,
            check=True,
            capture_output=True,
            text=True
        )
        remote_url = result.stdout.strip()
        
        # Always insert token for authentication (in case it was cloned without token)
        if "@" not in remote_url:
            auth_url = remote_url.replace("https://", f"https://{token}@")
            subprocess.run(
                ["git", "remote", "set-url", "origin", auth_url],
                cwd=wiki_dir,
                check=True,
                capture_output=True
            )
            log("Set authenticated remote URL")
        
        # Unset the URL-specific extraheader that overrides token in URL
        # This is critical: actions/checkout sets http.https://github.com/.extraheader
        # which takes precedence over the token embedded in the remote URL
        subprocess.run(
            ["git", "config", "--local", "--unset-all", "http.https://github.com/.extraheader"],
            cwd=wiki_dir,
            check=False,  # Don't fail if key doesn't exist
            capture_output=True
        )
        log("Unset GITHUB_TOKEN extraheader to allow WIKI_PUSH_TOKEN authentication")
        
        # Push with conflict handling - token in URL will now be used
        for attempt in range(2):
            try:
                subprocess.run(
                    ["git", "push", "origin", "master"],
                    cwd=wiki_dir,
                    check=True,
                    capture_output=True,
                    text=True
                )
                log("Wiki changes pushed successfully")
                return True
            except subprocess.CalledProcessError as e:
                error_output = e.stderr or ""
                # Check for 403 permission denied specifically
                if "403" in error_output or "permission denied" in error_output.lower():
                    log_error("HTTP 403 Permission Denied when pushing to wiki")
                    log_error("The WIKI_PUSH_TOKEN does not have proper permissions.")
                    log_error("Required fixes:")
                    log_error("  1. Create a NEW classic token at: https://github.com/settings/tokens/new")
                    log_error("  2. Select scopes: 'repo' (or 'public_repo') AND 'wiki'")
                    log_error("  3. Ensure the token owner has write access to the repository")
                    log_error("  4. Update the WIKI_PUSH_TOKEN secret in repository Settings > Secrets > Actions")
                    return False
                
                if "rejected" in error_output.lower() and attempt == 0:
                    log("Push rejected, attempting rebase...")
                    subprocess.run(
                        ["git", "pull", "--rebase", "origin", "master"],
                        cwd=wiki_dir,
                        check=True,
                        capture_output=True
                    )
                    subprocess.run(
                        ["git", "push", "origin", "master"],
                        cwd=wiki_dir,
                        check=True,
                        capture_output=True
                    )
                    log("Wiki changes pushed after rebase")
                    return True
                else:
                    log_error(f"Failed to push wiki changes: {error_output}")
                    return False
                    
    except subprocess.CalledProcessError as e:
        log_error(f"Git operation failed: {e.stderr if hasattr(e, 'stderr') else e}")
        return False
    except Exception as e:
        log_error(f"Unexpected error pushing wiki: {e}")
        return False


def main():
    """Main entry point."""
    log("Starting knowledge extraction workflow...")
    
    # Get input
    text, source = get_input_text()
    
    if not text:
        log("No input text provided. Exiting gracefully.")
        sys.exit(0)
    
    log(f"Processing input from source: {source}")
    log(f"Text length: {len(text)} characters")
    
    # Attempt 1: Use json_schema for structured output
    extracted, schema_supported = call_openrouter(text, use_schema=True)
    
    # If first attempt failed and schema may not be supported, try with json_object fallback
    if not extracted and not schema_supported:
        log("json_schema may not be supported, retrying with json_object format...")
        extracted, _ = call_openrouter(text, use_schema=False)
    
    # Handle rate limit scenario - if we got a 429, the function already waited
    # and returned None, so we should abort rather than retry immediately
    if not extracted:
        log_error("Failed to extract entities from text after maximum 2 attempts")
        sys.exit(1)
    
    # Validate extracted data
    total_entities = (
        len(extracted.get("definitions", [])) +
        len(extracted.get("facts", [])) +
        len(extracted.get("concepts", [])) +
        len(extracted.get("entities", [])) +
        len(extracted.get("relationships", [])) +
        len(extracted.get("processes", [])) +
        len(extracted.get("mechanisms", [])) +
        len(extracted.get("contexts", []))
    )
    log(f"Extracted {total_entities} entities:")
    log(f"  - Definitions: {len(extracted.get('definitions', []))}")
    log(f"  - Facts: {len(extracted.get('facts', []))}")
    log(f"  - Concepts: {len(extracted.get('concepts', []))}")
    log(f"  - Entities: {len(extracted.get('entities', []))}")
    log(f"  - Relationships: {len(extracted.get('relationships', []))}")
    log(f"  - Processes: {len(extracted.get('processes', []))}")
    log(f"  - Mechanisms: {len(extracted.get('mechanisms', []))}")
    log(f"  - Contexts: {len(extracted.get('contexts', []))}")
    
    if total_entities == 0:
        log("No entities extracted. Nothing to add to wiki.")
        sys.exit(0)
    
    # Get repository URL from environment
    repo_url = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
    repo_name = os.environ.get("GITHUB_REPOSITORY", "")
    if repo_name:
        wiki_url = f"{repo_url}/{repo_name}"
    else:
        log_error("GITHUB_REPOSITORY not set")
        sys.exit(1)
    
    # Clone wiki
    wiki_dir = Path("/tmp/wiki_checkout")
    if wiki_dir.exists():
        subprocess.run(["rm", "-rf", str(wiki_dir)], check=True)
    
    if not clone_wiki(wiki_url, wiki_dir):
        sys.exit(1)
    
    # Update wiki pages
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    
    if not update_wiki(wiki_dir, extracted, date_str, source):
        log("No wiki updates needed (all entries may be duplicates)")
        sys.exit(0)
    
    # Push changes
    if not push_wiki_changes(wiki_dir, source):
        sys.exit(1)
    
    log("Knowledge extraction complete!")


if __name__ == "__main__":
    main()
