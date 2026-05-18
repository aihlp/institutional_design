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


# Configuration
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "openrouter/free"  # Free model router
DEFAULT_PROMPT_TEMPLATE = """You are a precise data extraction tool. Your entire response must be a single valid JSON object and nothing else. Do not include any markdown formatting, explanations, or code fences.

Your task is to analyze text and extract three types of entities:

1. DEFINITIONS: Explanations of terms, concepts, or specialized vocabulary
2. FACTS: Verifiable statements, data points, or established information  
3. RESEARCH: Insights, hypotheses, study results, or emerging findings

Return your analysis as a JSON object with exactly three arrays: "definitions", "facts", and "research".
Each item should have a "text" field (the extracted content) and optionally a "context" field (additional relevant information).

Example format:
{
  "definitions": [
    {"text": "Term explanation", "context": "Related concept"}
  ],
  "facts": [
    {"text": "Verifiable statement"}
  ],
  "research": [
    {"text": "Research insight", "context": "Study reference"}
  ]
}

CRITICAL: Output ONLY the raw JSON object. No markdown, no code blocks, no explanations."""
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
                "research": {
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
            "required": ["definitions", "facts", "research"]
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
        
        # Validate response body is not empty before parsing
        if not response.text or len(response.text.strip()) == 0:
            log_error("Empty response body from API (HTTP 200 but no content)")
            return None, True
        
        result = response.json()
        choices = result.get("choices", [])
        if not choices:
            log_error("No choices in API response")
            return None, True
        
        choice = choices[0]
        finish_reason = choice.get("finish_reason", "")
        content = choice.get("message", {}).get("content", "")
        
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
    Normalize any JSON object to the required {definitions, facts, research} structure.
    
    Uses heuristic key mapping:
    - definitions, definition, defines, glossary → definitions
    - facts, fact, findings, observations → facts
    - research, analysis, insights, key_arguments, key_themes → research
    - Everything else → facts (safe default)
    
    Args:
        data: Any valid JSON dict
        
    Returns:
        Normalized dict with definitions, facts, research arrays
    """
    result = {"definitions": [], "facts": [], "research": []}
    
    # Key category mappings
    definition_keys = {"definitions", "definition", "defines", "glossary", "terms", "terminology"}
    fact_keys = {"facts", "fact", "findings", "observations", "data_points", "statements", "information"}
    research_keys = {"research", "analysis", "insights", "key_arguments", "key_themes", "hypotheses", 
                     "studies", "arguments", "themes", "conclusions"}
    
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
        elif key_lower in research_keys:
            return "research"
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
    3. Parses the JSON
    4. Normalizes it to the required {definitions, facts, research} structure
    
    Args:
        content: Raw response content
        
    Returns:
        Normalized dict with definitions, facts, research arrays, or None if no JSON found
    """
    # Remove markdown code blocks if present - handle both ```json and ``` variants
    content = content.strip()
    
    # Try to extract JSON from markdown code blocks (more robust pattern for nested braces)
    json_match = re.search(r'```(?:json)?\s*({.*?})\s*```', content, re.DOTALL)
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
        log_error(f"JSON decode error: {e}. Content starts with: {content[:200]}")
        return None


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


def update_wiki(wiki_dir: Path, extracted_data: dict, date_str: str, source: str) -> bool:
    """
    Update wiki pages with extracted entities.
    
    Args:
        wiki_dir: Wiki directory
        extracted_data: Dict with definitions, facts, research arrays
        date_str: Date string for headings
        source: Source label
        
    Returns:
        True on success, False on failure
    """
    pages = {
        "Definitions": extracted_data.get("definitions", []),
        "Facts": extracted_data.get("facts", []),
        "Research": extracted_data.get("research", [])
    }
    
    updates_needed = False
    for page_name, entities in pages.items():
        if not entities:
            continue
        
        existing = read_wiki_page(wiki_dir, page_name)
        updated = append_entities_to_page(existing, entities, date_str, source)
        
        if updated != existing:
            write_wiki_page(wiki_dir, page_name, updated)
            updates_needed = True
            log(f"Updated {page_name}.md")
    
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
        
        # Push with conflict handling
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
        len(extracted.get("research", []))
    )
    log(f"Extracted {total_entities} entities:")
    log(f"  - Definitions: {len(extracted.get('definitions', []))}")
    log(f"  - Facts: {len(extracted.get('facts', []))}")
    log(f"  - Research: {len(extracted.get('research', []))}")
    
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
