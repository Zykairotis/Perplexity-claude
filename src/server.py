#!/usr/bin/env python3
"""
Perplexity AI Web Server
A FastAPI web server for the Perplexity AI client with REST API and web interface
"""

import asyncio
import json
import os
import sys
import time
from typing import Dict, List, Optional, Union
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, File, UploadFile, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Add the current directory to Python path for local imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from perplexity_api import PerplexityAPI, SearchMode, ProModel, ReasoningModel, SearchSource, PerplexityAPIError
from perplexity_profiles import SearchProfile, validate_profile, list_available_profiles

def load_cookies_from_file() -> Dict[str, str]:
    """Load cookies from JSON file using path from .example.env"""
    # Try multiple possible paths for cookies.json
    possible_paths = [
        "cookies.json",  # Current directory
        "/app/cookies.json",  # Docker container path
        "../cookies.json",  # Parent directory
        "/home/mewtwo/Zykairotis/Perplexity-claude/cookies.json",  # Original path
    ]

    for cookie_path in possible_paths:
        try:
            with open(cookie_path, 'r') as f:
                cookie_data = json.load(f)
                cookies = cookie_data.get('cookies', {})
                if cookies:
                    print(f"✅ Loaded {len(cookies)} cookies from {cookie_path}")
                    return cookies
                else:
                    print(f"⚠️ No cookies found in {cookie_path}")
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            continue

    print(f"⚠️ Could not load cookies from any of the attempted paths: {possible_paths}")
    return {}

# Initialize FastAPI app
app = FastAPI(
    title="Perplexity AI API Server",
    description="Web server for Perplexity AI with REST API and streaming support",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Default cookies (PLACEHOLDER - Load from cookies.json file)
# These are fallback values only and won't work without real authentication cookies
DEFAULT_COOKIES = {
    'pplx.visitor-id': 'your-visitor-id',
    'pplx.source-selection-v3-space-': '[]',
    '__stripe_mid': 'your-stripe-mid',
    'gov-badge': '3',
    'sidebar-upgrade-badge': '10',
    'pplx.personal-search-badge-seen': '{%22sidebar%22:true%2C%22settingsSidebar%22:false%2C%22personalize%22:false}',
    'pplx.tasks-settings-seen': 'true',
    'sidebarHiddenHubs': '[]',
    'finance-alert-page-visit': '1',
    'pplx.session-id': 'your-session-id',
    'next-auth.csrf-token': 'your-csrf-token',
    'pplx.source-selection-v3-space-id': '[%22web%22]',
    'next-auth.callback-url': 'https%3A%2F%2Fwww.perplexity.ai%2Fapi%2Fauth%2Fsignin-callback%3Fredirect%3Dhttps%253A%252F%252Fwww.perplexity.ai',
    'pplx.search-models-v4': '{%22research%22:%22pplx_alpha%22%2C%22search%22:%22experimental%22%2C%22studio%22:%22pplx_beta%22}',
    '__cflb': 'your-cflb-token',
    'cf_clearance': 'your-cloudflare-clearance-token',
    '__cf_bm': 'your-cloudflare-bm-token',
    '__stripe_sid': 'your-stripe-sid',
    '__Secure-next-auth.session-token': 'your-session-token-here',
    'AWSALB': 'your-aws-alb-cookie',
    'AWSALBCORS': 'your-aws-alb-cors-cookie',
    '_dd_s': 'your-datadog-session',
    'pplx.metadata': '{%22qc%22:0}',
}

# Pydantic models for request/response
class FollowUpData(BaseModel):
    last_backend_uuid: str
    read_write_token: str
    attachments: List[str] = []

class SearchRequest(BaseModel):
    query: str
    mode: str = "auto"
    model_preference: Optional[str] = None
    sources: List[str] = ["web"]
    language: str = "en-US"
    incognito: bool = False
    raw_response: bool = False
    follow_up: Optional[FollowUpData] = None
    profile: Optional[str] = None
    prompt_source: Optional[str] = None
    query_source: Optional[str] = None
    should_ask_for_mcp_tool_confirmation: Optional[bool] = None
    search_focus: Optional[str] = None
    timezone: Optional[str] = None
    space: Optional[str] = None

class SearchWithFilesRequest(BaseModel):
    query: str
    mode: str = "auto"
    model_preference: Optional[str] = None
    sources: List[str] = ["web"]
    language: str = "en-US"
    incognito: bool = False
    raw_response: bool = False
    stream: bool = False
    follow_up: Optional[FollowUpData] = None
    profile: Optional[str] = None
    prompt_source: Optional[str] = None
    query_source: Optional[str] = None
    should_ask_for_mcp_tool_confirmation: Optional[bool] = None
    search_focus: Optional[str] = None
    timezone: Optional[str] = None
    space: Optional[str] = None

class SearchResponse(BaseModel):
    query: str
    answer: str
    sources: List[Dict]
    mode: str
    model: Optional[str]
    language: str
    timestamp: float
    backend_uuid: Optional[str] = None
    context_uuid: Optional[str] = None
    related_queries: List[str] = []

class StreamMessage(BaseModel):
    type: str  # "status", "chunk", "final", "error"
    data: Dict

class CreateSpaceRequest(BaseModel):
    title: str
    description: str = ""
    emoji: str = ""
    instructions: str = ""
    access: int = 1
    auto_save: bool = False

# Global API instance and conversation storage
api_instance = None
conversation_storage = {}  # Simple in-memory storage for conversation tokens

async def get_api():
    """Get or create API instance"""
    global api_instance
    if api_instance is None:
        # Load cookies from JSON file first, then fallback to DEFAULT_COOKIES
        cookies = load_cookies_from_file()
        if not cookies:
            print("🔄 Using fallback DEFAULT_COOKIES")
            cookies = DEFAULT_COOKIES
        api_instance = PerplexityAPI(cookies)
    return api_instance

# Routes
@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve the main web interface"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Perplexity AI Client</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; text-align: center; margin-bottom: 30px; }
            .search-form { margin-bottom: 30px; }
            input[type="text"] { width: 100%; padding: 15px; border: 2px solid #ddd; border-radius: 8px; font-size: 16px; margin-bottom: 15px; }
            select { padding: 10px; border: 2px solid #ddd; border-radius: 8px; margin-right: 10px; margin-bottom: 10px; }
            button { background: #007bff; color: white; border: none; padding: 15px 30px; border-radius: 8px; font-size: 16px; cursor: pointer; }
            button:hover { background: #0056b3; }
            .result { margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #007bff; }
            .sources { margin-top: 20px; }
            .source { margin: 10px 0; padding: 10px; background: white; border-radius: 5px; }
            .loading { text-align: center; color: #666; }
            .error { color: #dc3545; background: #f8d7da; padding: 15px; border-radius: 8px; }
            .streaming { background: #e7f3ff; border-left: 4px solid #007bff; padding: 15px; margin: 10px 0; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔍 Perplexity AI Client</h1>
            
            <div class="search-form">
                <input type="text" id="query" placeholder="Enter your question..." />
                
                <div>
                    <select id="mode">
                        <option value="auto">Auto</option>
                        <option value="pro">Pro</option>
                        <option value="reasoning">Reasoning</option>
                        <option value="deep research">Deep Research</option>
                        <option value="deep lab">Deep Lab</option>
                    </select>
                    
                    <select id="model">
                        <option value="">Default Model</option>
                        
                        <!-- Pro Mode Models -->
                        <option value="experimental">Experimental (Sonar)</option>
                        <option value="gpt-4.5">GPT-4.5 (Pro)</option>
                        <option value="gpt-4o">GPT-4o (Pro)</option>
                        <option value="claude 3.7 sonnet">Claude 3.7 Sonnet (Pro)</option>
                        <option value="gemini 2.0 flash">Gemini 2.0 Flash (Pro)</option>
                        <option value="grok-2">Grok-2 (Pro)</option>
                        <option value="claude">Claude (Pro)</option>
                        <option value="gemini2flash">Gemini 2 Flash (Pro)</option>
                        <option value="grok4">Grok-4 (Pro)</option>
                        <option value="pplx_pro">PPLX Pro (Pro)</option>
                        <option value="gpt41">GPT-4.1 (Pro)</option>
                        <option value="claude37sonnetthinking">Claude 3.7 Sonnet Thinking (Pro)</option>
                        <option value="o3">O3 (Pro)</option>
                        <option value="claude45sonnet">Claude 4.5 Sonnet (Pro)</option>
                        <option value="claude45sonnetthinking">Claude 4.5 Sonnet Thinking (Pro)</option>
                        <option value="gpt5">GPT-5 (Pro)</option>
                        <option value="gpt5thinking">GPT-5 Thinking (Pro)</option>

                        <!-- Reasoning Mode Models -->
                        <option value="r1">R1 (Reasoning)</option>
                        <option value="o3-mini">O3-Mini (Reasoning)</option>
                        <option value="claude 3.7 sonnet">Claude 3.7 Sonnet (Reasoning)</option>

                        <!-- Deep Lab Model -->
                        <option value="pplx_beta">PPLX Beta (Deep Lab)</option>
                        
                        <!-- Deep Research Model -->
                        <option value="pplx_alpha">PPLX Alpha (Deep Research)</option>
                    </select>
                    
                    <select id="sources" multiple>
                        <option value="web" selected>Web</option>
                        <option value="scholar">Scholar</option>
                        <option value="social">Social</option>
                        <option value="edgar">Edgar (SEC Filings)</option>
                    </select>

                    <select id="profile">
                        <option value="">No Profile</option>
                        <option value="simple">⚡ Simple (No Enhancement)</option>
                        <option value="research">🔬 Research</option>
                        <option value="code_analysis">💻 Code Analysis</option>
                        <option value="troubleshooting">🔧 Troubleshooting</option>
                        <option value="documentation">📚 Documentation</option>
                        <option value="architecture">🏗️ Architecture</option>
                        <option value="security">🔒 Security</option>
                        <option value="performance">⚡ Performance</option>
                        <option value="tutorial">📖 Tutorial</option>
                        <option value="comparison">⚖️ Comparison</option>
                        <option value="trending">📈 Trending</option>
                        <option value="best_practices">✨ Best Practices</option>
                        <option value="integration">🔗 Integration</option>
                        <option value="debugging">🐛 Debugging</option>
                        <option value="optimization">🎯 Optimization</option>
                    </select>

                    <select id="space">
                        <option value="">No Space (Default)</option>
                        <option value="trading">📊 Trading Space</option>
                        <!-- Add more space options from your spaces.json here -->
                    </select>
                </div>
                
                <input type="file" id="files" multiple>
                
                <div style="margin: 10px 0;">
                    <label>
                        <input type="checkbox" id="rawResponse"> Raw Response (Debug Mode)
                    </label>
                    <br>
                    <label>
                        <input type="checkbox" id="continueChat"> Continue Previous Chat
                    </label>
                </div>

                <div style="margin: 15px 0; padding: 15px; background: #f8f9fa; border-radius: 8px;">
                    <h4>Advanced Options</h4>

                    <div style="margin-bottom: 10px;">
                        <label for="promptSource" style="display: block; margin-bottom: 5px;">Prompt Source:</label>
                        <input type="text" id="promptSource" placeholder="e.g., user, system, api" style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
                    </div>

                    <div style="margin-bottom: 10px;">
                        <label for="querySource" style="display: block; margin-bottom: 5px;">Query Source:</label>
                        <input type="text" id="querySource" placeholder="e.g., web_search, knowledge_base, custom" style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
                    </div>

                    <div style="margin-bottom: 10px;">
                        <label for="searchFocus" style="display: block; margin-bottom: 5px;">Search Focus:</label>
                        <select id="searchFocus" style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
                            <option value="">Default</option>
                            <option value="research">Research</option>
                            <option value="news">News</option>
                            <option value="academic">Academic</option>
                            <option value="technical">Technical</option>
                            <option value="business">Business</option>
                            <option value="creative">Creative</option>
                        </select>
                    </div>

                    <div style="margin-bottom: 10px;">
                        <label for="timezone" style="display: block; margin-bottom: 5px;">Timezone:</label>
                        <input type="text" id="timezone" placeholder="e.g., UTC, America/New_York" style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
                    </div>

                    <div style="margin-bottom: 10px;">
                        <label>
                            <input type="checkbox" id="askForMcpConfirmation"> Ask for MCP Tool Confirmation
                        </label>
                    </div>
                </div>
                
                <button onclick="search()">Search (Upload)</button>
                <button onclick="streamSearch()">Search (Stream)</button>
                <button onclick="streamSearchWithFiles()">Stream with Files</button>
                <button onclick="showCreateSpaceModal()" style="background: #28a745; margin-left: 10px;">➕ Create New Space</button>
            </div>
            
            <!-- Create Space Modal -->
            <div id="createSpaceModal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 1000;">
                <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background: white; padding: 30px; border-radius: 10px; max-width: 600px; width: 90%;">
                    <h2 style="margin-top: 0;">Create New Perplexity Space</h2>
                    
                    <div style="margin: 15px 0;">
                        <label style="display: block; margin-bottom: 5px; font-weight: bold;">Space Name *</label>
                        <input type="text" id="spaceName" placeholder="e.g., Trading Analysis" style="width: 100%; padding: 10px; border: 2px solid #ddd; border-radius: 5px;">
                    </div>
                    
                    <div style="margin: 15px 0;">
                        <label style="display: block; margin-bottom: 5px; font-weight: bold;">Description</label>
                        <textarea id="spaceDescription" placeholder="Detailed description of this space's purpose..." style="width: 100%; padding: 10px; border: 2px solid #ddd; border-radius: 5px; min-height: 80px;"></textarea>
                    </div>
                    
                    <div style="margin: 15px 0;">
                        <label style="display: block; margin-bottom: 5px; font-weight: bold;">Emoji</label>
                        <input type="text" id="spaceEmoji" placeholder="e.g., 📊" style="width: 100%; padding: 10px; border: 2px solid #ddd; border-radius: 5px;">
                    </div>
                    
                    <div style="margin: 15px 0;">
                        <label style="display: block; margin-bottom: 5px; font-weight: bold;">Instructions (System Prompt)</label>
                        <textarea id="spaceInstructions" placeholder="System prompt for the AI agent in this space..." style="width: 100%; padding: 10px; border: 2px solid #ddd; border-radius: 5px; min-height: 100px;"></textarea>
                    </div>
                    
                    <div style="margin: 15px 0;">
                        <label>
                            <input type="checkbox" id="autoSave" checked> Auto-save to spaces.json
                        </label>
                    </div>
                    
                    <div style="margin-top: 20px; display: flex; gap: 10px;">
                        <button onclick="createSpace()" style="flex: 1; padding: 12px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer;">Create Space</button>
                        <button onclick="closeCreateSpaceModal()" style="flex: 1; padding: 12px; background: #6c757d; color: white; border: none; border-radius: 5px; cursor: pointer;">Cancel</button>
                    </div>
                    
                    <div id="spaceCreationResult" style="margin-top: 15px;"></div>
                </div>
            </div>
            
            <div id="result"></div>
        </div>

        <script>
            const modeSelect = document.getElementById('mode');
            const modelSelect = document.getElementById('model');

            modeSelect.addEventListener('change', function() {
                if (this.value === 'auto' || this.value === 'deep research' || this.value === 'deep lab') {
                    modelSelect.disabled = true;
                    modelSelect.value = ''; // Reset to default
                } else {
                    modelSelect.disabled = false;
                }
            });

            // Initial check in case the default mode is 'auto'
            if (modeSelect.value === 'auto' || modeSelect.value === 'deep research' || modeSelect.value === 'deep lab') {
                modelSelect.disabled = true;
            }

            function search() {
                const query = document.getElementById('query').value;
                const mode = document.getElementById('mode').value;
                const model = document.getElementById('model').value;
                const sources = Array.from(document.getElementById('sources').selectedOptions).map(option => option.value);
                const profile = document.getElementById('profile').value;
                const space = document.getElementById('space').value;
                const files = document.getElementById('files').files;

                // Advanced options
                const promptSource = document.getElementById('promptSource').value;
                const querySource = document.getElementById('querySource').value;
                const searchFocus = document.getElementById('searchFocus').value;
                const timezone = document.getElementById('timezone').value;
                const askForMcpConfirmation = document.getElementById('askForMcpConfirmation').checked;

                if (!query.trim()) {
                    alert('Please enter a question');
                    return;
                }

                const formData = new FormData();
                formData.append('query', query);
                formData.append('mode', mode);
                if (model) {
                    formData.append('model_preference', model);
                }
                formData.append('sources', sources.join(','));
                formData.append('stream', 'false');

                // Add space parameter
                if (space) {
                    formData.append('space', space);
                }

                // Add advanced options
                if (promptSource) {
                    formData.append('prompt_source', promptSource);
                }
                if (querySource) {
                    formData.append('query_source', querySource);
                }
                if (searchFocus) {
                    formData.append('search_focus', searchFocus);
                }
                if (timezone) {
                    formData.append('timezone', timezone);
                }
                if (askForMcpConfirmation) {
                    formData.append('should_ask_for_mcp_tool_confirmation', 'true');
                }

                // Add files if any
                for (let i = 0; i < files.length; i++) {
                    formData.append('files', files[i]);
                }

                document.getElementById('result').innerHTML = '<div class="loading">🔍 Processing...</div>';

                if (files.length > 0) {
                    // Use file upload endpoint
                    fetch('/api/search/files', {
                        method: 'POST',
                        body: formData
                    })
                    .then(response => response.json())
                    .then(data => {
                        if(data.error || data.detail) {
                            document.getElementById('result').innerHTML = `<div class="error">Error: ${data.error || data.detail}</div>`;
                        } else {
                            displayResults(data);
                        }
                    })
                    .catch(error => {
                        document.getElementById('result').innerHTML = `<div class="error">Error: ${error.message}</div>`;
                    });
                } else {
                    // Use regular search endpoint
                    fetch('/api/search', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            query,
                            mode,
                            model_preference: model || null,
                            sources,
                            profile: profile || null,
                            space: space || null,
                            prompt_source: promptSource || null,
                            query_source: querySource || null,
                            search_focus: searchFocus || null,
                            timezone: timezone || null,
                            should_ask_for_mcp_tool_confirmation: askForMcpConfirmation || null
                        })
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.error || data.detail) {
                            document.getElementById('result').innerHTML = `<div class="error">Error: ${data.error || data.detail}</div>`;
                        } else {
                            displayResults(data);
                        }
                    })
                    .catch(error => {
                        document.getElementById('result').innerHTML = `<div class="error">Error: ${error.message}</div>`;
                    });
                }
            }

            function streamSearch() {
                const query = document.getElementById('query').value;
                const mode = document.getElementById('mode').value;
                const model = document.getElementById('model').value;
                const sources = Array.from(document.getElementById('sources').selectedOptions).map(option => option.value);
                const profile = document.getElementById('profile').value;
                const space = document.getElementById('space').value;

                // Advanced options
                const promptSource = document.getElementById('promptSource').value;
                const querySource = document.getElementById('querySource').value;
                const searchFocus = document.getElementById('searchFocus').value;
                const timezone = document.getElementById('timezone').value;
                const askForMcpConfirmation = document.getElementById('askForMcpConfirmation').checked;

                if (!query.trim()) {
                    alert('Please enter a question');
                    return;
                }

                if (document.getElementById('files').files.length > 0) {
                    alert('File uploads are not supported with WebSocket streaming. Please use "Stream with Files" button.');
                    return;
                }

                const requestData = {
                    query: query,
                    mode: mode,
                    model_preference: model,
                    sources: sources,
                    profile: profile,
                    space: space || null,
                    prompt_source: promptSource || null,
                    query_source: querySource || null,
                    search_focus: searchFocus || null,
                    timezone: timezone || null,
                    should_ask_for_mcp_tool_confirmation: askForMcpConfirmation || null
                };

                document.getElementById('result').innerHTML = '<div class="streaming">🔄 Connecting to stream...</div>';

                const ws = new WebSocket(`ws://${window.location.host}/ws/search`);
                
                ws.onopen = function() {
                    ws.send(JSON.stringify(requestData));
                };
                
                ws.onmessage = function(event) {
                    const message = JSON.parse(event.data);
                    handleStreamMessage(message);
                };
                
                ws.onerror = function(error) {
                    document.getElementById('result').innerHTML += `<div class="error">WebSocket error: ${error}</div>`;
                };
                
                ws.onclose = function() {
                    console.log('WebSocket connection closed');
                };
            }

            function streamSearchWithFiles() {
                const query = document.getElementById('query').value;
                const mode = document.getElementById('mode').value;
                const model = document.getElementById('model').value;
                const sources = Array.from(document.getElementById('sources').selectedOptions).map(option => option.value);
                const profile = document.getElementById('profile').value;
                const space = document.getElementById('space').value;
                const files = document.getElementById('files').files;
                const rawResponse = document.getElementById('rawResponse').checked;

                // Advanced options
                const promptSource = document.getElementById('promptSource').value;
                const querySource = document.getElementById('querySource').value;
                const searchFocus = document.getElementById('searchFocus').value;
                const timezone = document.getElementById('timezone').value;
                const askForMcpConfirmation = document.getElementById('askForMcpConfirmation').checked;

                if (!query.trim()) {
                    alert('Please enter a question');
                    return;
                }

                // Files are now optional - no need to require them

                const formData = new FormData();
                formData.append('query', query);
                formData.append('mode', mode);
                if (model) {
                    formData.append('model_preference', model);
                }
                formData.append('sources', sources.join(','));
                formData.append('raw_response', rawResponse);
                formData.append('continue_chat', document.getElementById('continueChat').checked);
                if (profile) {
                    formData.append('profile', profile);
                }
                if (space) {
                    formData.append('space', space);
                }

                // Add advanced options
                if (promptSource) {
                    formData.append('prompt_source', promptSource);
                }
                if (querySource) {
                    formData.append('query_source', querySource);
                }
                if (searchFocus) {
                    formData.append('search_focus', searchFocus);
                }
                if (timezone) {
                    formData.append('timezone', timezone);
                }
                if (askForMcpConfirmation) {
                    formData.append('should_ask_for_mcp_tool_confirmation', 'true');
                }

                // Add files
                for (let i = 0; i < files.length; i++) {
                    formData.append('files', files[i]);
                }

                document.getElementById('result').innerHTML = '<div class="streaming">📁 Uploading files and starting stream...</div>';

                // Use Server-Sent Events for streaming with files
                fetch('/api/search/files/stream', {
                    method: 'POST',
                    body: formData
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                    }
                    
                    const reader = response.body.getReader();
                    const decoder = new TextDecoder();
                    
                    function readStream() {
                        return reader.read().then(({ done, value }) => {
                            if (done) {
                                document.getElementById('result').innerHTML += '<div class="streaming">✅ Stream completed</div>';
                                return;
                            }
                            
                            const chunk = decoder.decode(value);
                            const lines = chunk.split('\\n');
                            
                            for (const line of lines) {
                                if (line.startsWith('data: ')) {
                                    const data = line.slice(6);
                                    if (data === '[DONE]') {
                                        return;
                                    }
                                    
                                    try {
                                        const message = JSON.parse(data);
                                        handleStreamMessage(message);
                                    } catch (e) {
                                        console.log('Failed to parse SSE data:', data);
                                    }
                                }
                            }
                            
                            return readStream();
                        });
                    }
                    
                    return readStream();
                })
                .catch(error => {
                    document.getElementById('result').innerHTML += `<div class="error">Stream error: ${error.message}</div>`;
                });
            }


            
            function handleStreamMessage(message) {
                const resultDiv = document.getElementById('result');
                
                if (message.type === 'status') {
                    resultDiv.innerHTML += `<div class="streaming">🔍 ${message.data.status}</div>`;
                } else if (message.type === 'raw_chunk') {
                    // Display raw chunk data for debugging
                    resultDiv.innerHTML += `<div class="streaming" style="background: #fff3cd; border-left: 4px solid #ffc107;">
                        <strong>🔧 Raw Chunk:</strong><br>
                        <pre style="font-size: 12px; overflow-x: auto; white-space: pre-wrap;">${JSON.stringify(message.data, null, 2)}</pre>
                    </div>`;
                } else if (message.type === 'chunk') {
                    if (message.data.step_type === 'SEARCH_WEB') {
                        resultDiv.innerHTML += `<div class="streaming">🌐 Web Search: ${message.data.content.queries?.[0]?.query || 'Unknown'}</div>`;
                    } else if (message.data.step_type === 'SEARCH_RESULTS') {
                        const count = message.data.content.web_results?.length || 0;
                        resultDiv.innerHTML += `<div class="streaming">📄 Found ${count} sources</div>`;
                    } else if (message.data.step_type === 'FINAL') {
                        resultDiv.innerHTML += `<div class="streaming">✅ Search completed</div>`;
                    }
                } else if (message.type === 'final') {
                    displayResult(message.data);
                } else if (message.type === 'error') {
                    resultDiv.innerHTML += `<div class="error">Error: ${message.data.error}</div>`;
                }
            }
            
            function displayResults(data) {
                const answer = data.answer || 'No answer found.';
                const sources = data.sources || [];
                const html = `
                    <div class="result">
                        <h3>💡 Answer</h3>
                        <p>${answer}</p>
                        
                        <div class="sources">
                            <h4>📚 Sources (${sources.length})</h4>
                            ${sources.slice(0, 5).map((source, i) => `
                                <div class="source">
                                    <strong>[${i + 1}] ${source.name || 'Unknown'}</strong><br>
                                    <a href="${source.url}" target="_blank">${source.url}</a>
                                </div>
                            `).join('')}
                        </div>
                        
                        ${data.related_queries && data.related_queries.length > 0 ? `
                            <div style="margin-top: 20px;">
                                <h4>🔗 Related Queries</h4>
                                ${data.related_queries.slice(0, 3).map(q => `
                                    <button onclick="document.getElementById('query').value='${q}'; search();" style="margin: 5px; padding: 8px 12px; background: #f8f9fa; border: 1px solid #ddd; border-radius: 5px; cursor: pointer;">
                                        ${q}
                                    </button>
                                `).join('')}
                            </div>
                        ` : ''}
                        
                        <div style="margin-top: 20px; font-size: 12px; color: #666;">
                            Mode: ${data.mode} | Model: ${data.model || 'Default'} | Time: ${new Date(data.timestamp * 1000).toLocaleTimeString()}
                        </div>
                    </div>
                `;
                
                document.getElementById('result').innerHTML = html;
            }
            
            // Allow Enter key to search
            document.getElementById('query').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    search();
                }
            });

            // Space creation functions
            function showCreateSpaceModal() {
                document.getElementById('createSpaceModal').style.display = 'block';
            }

            function closeCreateSpaceModal() {
                document.getElementById('createSpaceModal').style.display = 'none';
                // Clear form
                document.getElementById('spaceName').value = '';
                document.getElementById('spaceDescription').value = '';
                document.getElementById('spaceEmoji').value = '';
                document.getElementById('spaceInstructions').value = '';
                document.getElementById('spaceCreationResult').innerHTML = '';
            }

            async function createSpace() {
                const spaceName = document.getElementById('spaceName').value.trim();
                const spaceDescription = document.getElementById('spaceDescription').value.trim();
                const spaceEmoji = document.getElementById('spaceEmoji').value.trim();
                const spaceInstructions = document.getElementById('spaceInstructions').value.trim();
                const autoSave = document.getElementById('autoSave').checked;

                if (!spaceName) {
                    alert('Space name is required');
                    return;
                }

                document.getElementById('spaceCreationResult').innerHTML = '<div class="loading">Creating space...</div>';

                try {
                    const response = await fetch('/api/spaces/create', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            title: spaceName,
                            description: spaceDescription,
                            emoji: spaceEmoji,
                            instructions: spaceInstructions,
                            access: 1,
                            auto_save: autoSave
                        })
                    });

                    const data = await response.json();

                    if (response.ok && data.success) {
                        document.getElementById('spaceCreationResult').innerHTML = `
                            <div class="result">
                                <h3>✅ Space Created Successfully!</h3>
                                <p><strong>UUID:</strong> ${data.uuid}</p>
                                <p><strong>Title:</strong> ${data.title}</p>
                                <p><strong>Slug:</strong> ${data.slug}</p>
                                ${autoSave ? '<p style="color: #28a745;">✓ Saved to spaces.json</p>' : ''}
                                <button onclick="location.reload()" style="margin-top: 10px; padding: 8px 16px;">Reload Page</button>
                            </div>
                        `;
                    } else {
                        document.getElementById('spaceCreationResult').innerHTML = `
                            <div class="error">
                                Failed to create space: ${data.detail || data.error || 'Unknown error'}
                            </div>
                        `;
                    }
                } catch (error) {
                    document.getElementById('spaceCreationResult').innerHTML = `
                        <div class="error">Error: ${error.message}</div>
                    `;
                }
            }

            // Close modal on outside click
            document.getElementById('createSpaceModal').addEventListener('click', function(e) {
                if (e.target === this) {
                    closeCreateSpaceModal();
                }
            });
        </script>
    </body>
    </html>
    """



@app.post("/api/search", response_model=Union[SearchResponse, Dict])
async def api_search(request: SearchRequest):
    """REST API endpoint for search"""
    try:
        api = await get_api()
        
        # Convert follow_up to dict format expected by ref.py
        follow_up_dict = None
        if request.follow_up:
            follow_up_dict = {
                'backend_uuid': request.follow_up.backend_uuid,
                'attachments': request.follow_up.attachments
            }

        # Validate profile if provided
        search_profile = None
        if request.profile:
            search_profile = validate_profile(request.profile)
            if search_profile is None:
                available_profiles = list(list_available_profiles().keys())
                raise HTTPException(status_code=400, detail=f"Invalid profile '{request.profile}'. Available profiles: {available_profiles}")

        result = await api.search(
            query=request.query,
            mode=request.mode,
            model=request.model_preference,
            sources=request.sources,
            language=request.language,
            incognito=request.incognito,
            raw_response=request.raw_response,
            follow_up=follow_up_dict,
            profile=search_profile,
            prompt_source=request.prompt_source,
            query_source=request.query_source,
            should_ask_for_mcp_tool_confirmation=request.should_ask_for_mcp_tool_confirmation,
            search_focus=request.search_focus,
            timezone=request.timezone,
            space=request.space
        )
        
        if request.raw_response:
            return result
        
        return SearchResponse(
            query=result.query,
            answer=result.answer,
            sources=result.sources,
            mode=result.mode,
            model=result.model,
            language=result.language,
            timestamp=result.timestamp,
            backend_uuid=result.backend_uuid,
            context_uuid=result.context_uuid,
            related_queries=result.related_queries or []
        )
        
    except PerplexityAPIError as e:
        raise HTTPException(status_code=400, detail=f"API Error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")

@app.post("/api/search/files")
async def api_search_with_files(
    query: str = Form(...),
    mode: str = Form("auto"),
    model_preference: Optional[str] = Form(None),
    sources: str = Form("web"),
    files: List[UploadFile] = File(...),
    language: str = Form("en-US"),
    incognito: bool = Form(False),
    stream: bool = Form(False),
    follow_up_backend_uuid: Optional[str] = Form(None),
    follow_up_attachments: Optional[str] = Form(None),
    profile: Optional[str] = Form(None),
    prompt_source: Optional[str] = Form(None),
    query_source: Optional[str] = Form(None),
    should_ask_for_mcp_tool_confirmation: Optional[bool] = Form(None),
    search_focus: Optional[str] = Form(None),
    timezone: Optional[str] = Form(None),
    space: Optional[str] = Form(None)
):
    """API endpoint for search with file uploads"""
    try:
        api = await get_api()

        # Validate profile if provided
        search_profile = None
        if profile:
            search_profile = validate_profile(profile)
            if search_profile is None:
                available_profiles = list(list_available_profiles().keys())
                raise HTTPException(status_code=400, detail=f"Invalid profile '{profile}'. Available profiles: {available_profiles}")

        # Handle file content properly - keep as bytes for perplexity_fixed.py
        uploaded_files = {}
        for file in files:
            content = await file.read()
            uploaded_files[file.filename] = content  # Keep as bytes

        if stream:
            # Return streaming response
            async def generate_stream():
                async for chunk in api.search_stream(
                    query=query,
                    mode=mode,
                    model=model_preference,
                    sources=sources.split(','),
                    files=uploaded_files,
                    language=language,
                    incognito=incognito,
                    profile=search_profile,
                    prompt_source=prompt_source,
                    query_source=query_source,
                    should_ask_for_mcp_tool_confirmation=should_ask_for_mcp_tool_confirmation,
                    search_focus=search_focus,
                    timezone=timezone,
                    space=space
                ):
                    yield f"data: {json.dumps(chunk.to_dict())}\n\n"
                yield "data: [DONE]\n\n"
            
            return StreamingResponse(
                generate_stream(),
                media_type="text/plain",
                headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
            )
        else:
            # Regular search
            result = await api.search(
                query=query,
                mode=mode,
                model=model_preference,
                sources=sources.split(','),
                files=uploaded_files,
                language=language,
                incognito=incognito,
                profile=search_profile,
                prompt_source=prompt_source,
                query_source=query_source,
                should_ask_for_mcp_tool_confirmation=should_ask_for_mcp_tool_confirmation,
                search_focus=search_focus,
                timezone=timezone,
                space=space
            )
            return result
            
    except PerplexityAPIError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@app.post("/api/search/files/stream")
async def api_search_with_files_stream(
    query: str = Form(...),
    mode: str = Form("auto"),
    model_preference: Optional[str] = Form(None),
    sources: str = Form("web"),
    files: List[UploadFile] = File(default=[]),
    language: str = Form("en-US"),
    incognito: bool = Form(False),
    raw_response: bool = Form(False),
    continue_chat: bool = Form(False),
    profile: Optional[str] = Form(None),
    prompt_source: Optional[str] = Form(None),
    query_source: Optional[str] = Form(None),
    should_ask_for_mcp_tool_confirmation: Optional[bool] = Form(None),
    search_focus: Optional[str] = Form(None),
    timezone: Optional[str] = Form(None),
    space: Optional[str] = Form(None)
):
    """API endpoint for streaming search with file uploads"""
    try:
        api = await get_api()

        # Validate profile if provided
        search_profile = None
        if profile:
            search_profile = validate_profile(profile)
            if search_profile is None:
                available_profiles = list(list_available_profiles().keys())
                raise HTTPException(status_code=400, detail=f"Invalid profile '{profile}'. Available profiles: {available_profiles}")

        # Handle file content properly
        uploaded_files = {}
        for file in files:
            content = await file.read()
            uploaded_files[file.filename] = content
        
        # Handle follow_up data using continue_chat
        follow_up_dict = None
        
        if continue_chat:
            # Auto-use stored conversation tokens
            global conversation_storage
            if 'backend_uuid' in conversation_storage and 'read_write_token' in conversation_storage:
                follow_up_dict = {
                    'backend_uuid': conversation_storage['backend_uuid'],
                    'read_write_token': conversation_storage['read_write_token'],
                    'attachments': []
                }
        
        # Return Server-Sent Events stream
        async def generate_stream():
            try:
                status_msg = f"Processing {len(uploaded_files)} files..."
                if follow_up_dict:
                    status_msg += f" (Follow-up conversation)"
                yield f"data: {json.dumps({'type': 'status', 'data': {'status': status_msg}})}\\n\\n"
                
                async for chunk in api.search_stream(
                    query=query,
                    mode=mode,
                    model=model_preference,
                    sources=sources.split(','),
                    files=uploaded_files,
                    language=language,
                    incognito=incognito,
                    follow_up=follow_up_dict,
                    profile=search_profile,
                    prompt_source=prompt_source,
                    query_source=query_source,
                    should_ask_for_mcp_tool_confirmation=should_ask_for_mcp_tool_confirmation,
                    search_focus=search_focus,
                    timezone=timezone,
                    space=space
                ):
                    # Extract and store conversation tokens automatically
                    raw_data = chunk.to_dict() if hasattr(chunk, 'to_dict') else chunk.__dict__
                    
                    # Look for tokens in the raw_data field (which contains the original response)
                    if 'raw_data' in raw_data and raw_data['raw_data']:
                        original_response = raw_data['raw_data']
                        
                        # Store tokens for future continue_chat usage
                        if 'backend_uuid' in original_response and original_response['backend_uuid']:
                            conversation_storage['backend_uuid'] = original_response['backend_uuid']
                            print(f"🔑 Stored backend_uuid: {original_response['backend_uuid']}")
                        
                        if 'read_write_token' in original_response and original_response['read_write_token']:
                            conversation_storage['read_write_token'] = original_response['read_write_token']
                            print(f"🔑 Stored read_write_token: {original_response['read_write_token']}")
                    
                    # Also check top level (fallback)
                    if 'backend_uuid' in raw_data and raw_data['backend_uuid']:
                        conversation_storage['backend_uuid'] = raw_data['backend_uuid']
                    if 'read_write_token' in raw_data and raw_data['read_write_token']:
                        conversation_storage['read_write_token'] = raw_data['read_write_token']
                    
                    if raw_response:
                        # Return formatted raw chunk data for better readability
                        chunk_data = {
                            'type': 'raw_chunk',
                            'timestamp': raw_data.get('timestamp', time.time()),
                            'step_type': raw_data.get('step_type', 'unknown'),
                            'data': {
                                'raw_structure': raw_data,
                                'formatted_content': {
                                    'step': raw_data.get('step_type', 'unknown'),
                                    'content_keys': list(raw_data.get('content', {}).keys()) if isinstance(raw_data.get('content'), dict) else 'non-dict',
                                    'content_preview': str(raw_data.get('content', ''))[:200] + '...' if len(str(raw_data.get('content', ''))) > 200 else str(raw_data.get('content', '')),
                                    'backend_uuid': raw_data.get('backend_uuid'),
                                    'context_uuid': raw_data.get('context_uuid'),
                                    'read_write_token': raw_data.get('read_write_token'),
                                    'full_size_bytes': len(json.dumps(raw_data))
                                }
                            }
                        }
                    else:
                        # Return formatted chunk data
                        chunk_data = {
                            'type': 'chunk',
                            'data': {
                                'step_type': chunk.step_type,
                                'content': chunk.content,
                                'timestamp': chunk.timestamp
                            }
                        }
                    # Format ALL JSON responses with proper indentation for readability
                    formatted_json = json.dumps(chunk_data, indent=2, ensure_ascii=False)
                    yield f"data: {formatted_json}\\n\\n"
                
                # Format completion status with indentation
                completion_data = {'type': 'status', 'data': {'status': 'Stream completed'}}
                formatted_completion = json.dumps(completion_data, indent=2, ensure_ascii=False)
                yield f"data: {formatted_completion}\\n\\n"
                yield "data: [DONE]\\n\\n"
                
            except Exception as e:
                error_data = {'type': 'error', 'data': {'error': str(e)}}
                formatted_error = json.dumps(error_data, indent=2, ensure_ascii=False)
                yield f"data: {formatted_error}\\n\\n"
        
        return StreamingResponse(
            generate_stream(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stream setup failed: {str(e)}")

@app.websocket("/ws/search")
async def websocket_search(websocket: WebSocket):
    await websocket.accept()
    api = await get_api()
    try:
        data = await websocket.receive_json()
        query = data.get("query")
        mode = data.get("mode", "auto")
        model = data.get("model_preference")
        sources = data.get("sources", ["web"])
        profile = data.get("profile")
        prompt_source = data.get("prompt_source")
        query_source = data.get("query_source")
        should_ask_for_mcp_tool_confirmation = data.get("should_ask_for_mcp_tool_confirmation")
        search_focus = data.get("search_focus")
        timezone = data.get("timezone")
        space = data.get("space")

        # Validate profile if provided
        search_profile = None
        if profile:
            search_profile = validate_profile(profile)
            if search_profile is None:
                available_profiles = list(list_available_profiles().keys())
                await websocket.send_json({"type": "error", "data": {"error": f"Invalid profile '{profile}'. Available profiles: {available_profiles}"}})
                return

        try:
            await websocket.send_json({"type": "status", "data": {"status": f"Starting search: {query}"}})

            # Use the search_stream method
            async for chunk in api.search_stream(
                query=query,
                mode=mode,
                model=model,
                sources=sources,
                profile=search_profile,
                prompt_source=prompt_source,
                query_source=query_source,
                should_ask_for_mcp_tool_confirmation=should_ask_for_mcp_tool_confirmation,
                search_focus=search_focus,
                timezone=timezone,
                space=space
            ):
                # Send the chunk data
                await websocket.send_json({
                    "type": "chunk",
                    "data": {
                        "step_type": chunk.step_type,
                        "content": chunk.content,
                        "timestamp": chunk.timestamp
                    }
                })
            
            await websocket.send_json({"type": "status", "data": {"status": "Stream completed"}})

        except PerplexityAPIError as e:
            await websocket.send_json({"type": "error", "data": {"error": str(e)}})
        except Exception as e:
            await websocket.send_json({"type": "error", "data": {"error": f"Stream failed: {str(e)}"}})

    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        # Attempt to send an error message before closing
        try:
            await websocket.send_json({"type": "error", "data": {"error": f"An unexpected error occurred: {str(e)}"}})
        except Exception:
            pass # Ignore if sending fails because the socket is already closed

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": time.time()}

@app.get("/api/session")
async def session_info():
    """Get session information"""
    try:
        api = await get_api()
        session_info = await api.get_session_info()
        return session_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/modes")
async def get_modes():
    """Get available search modes and models"""
    return {
        "modes": ["auto", "pro", "reasoning", "deep research", "deep lab"],
        "pro_models": [
            "experimental", "gpt-4.5", "gpt-4o", "claude 3.7 sonnet", "gemini 2.0 flash", "grok-2",
            "gemini2flash", "grok4", "pplx_pro", "gpt41", "claude37sonnetthinking", "o3",
            "claude45sonnet", "claude45sonnetthinking", "gpt5", "gpt5thinking"
        ],
        "deep_research_models": ["pplx_alpha"],
        "deep_lab_models": ["pplx_beta"],
        "sources": ["web", "scholar", "social", "edgar"]
    }

@app.get("/api/profiles")
async def get_profiles():
    """Get available search profiles for enhanced queries"""
    profiles = list_available_profiles()
    return {
        "profiles": profiles,
        "usage": "Add profile parameter to search requests to enhance query effectiveness",
        "examples": {
            "research": "Detailed research with multiple sources",
            "code_analysis": "Code analysis with explanations and improvements",
            "troubleshooting": "Step-by-step troubleshooting with solutions"
        }
    }

@app.post("/api/spaces/create")
async def create_space(request: CreateSpaceRequest):
    """
    Create a new Perplexity space/collection
    
    Request body:
    - title: Name of the space (required)
    - description: Detailed description of the space's purpose
    - emoji: Emoji for the space (optional)
    - instructions: System prompt/instructions for the agent in this space
    - access: Access level (1 = private, default)
    - auto_save: If True, automatically save to spaces.json
    """
    try:
        api = await get_api()
        
        result = await api.create_space(
            title=request.title,
            description=request.description,
            emoji=request.emoji,
            instructions=request.instructions,
            access=request.access,
            auto_save=request.auto_save
        )
        
        return {
            "success": True,
            "uuid": result.get('uuid'),
            "title": result.get('title'),
            "slug": result.get('slug'),
            "full_response": result
        }
        
    except PerplexityAPIError as e:
        raise HTTPException(status_code=400, detail=f"API Error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")

@app.get("/api/spaces")
async def list_spaces():
    """Get list of configured spaces from spaces.json"""
    try:
        from perplexity_api import load_spaces_mapping
        spaces = load_spaces_mapping()
        return {
            "spaces": spaces,
            "count": len(spaces)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading spaces: {str(e)}")

def find_free_port():
    """Find an available port"""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

if __name__ == "__main__":
    port = 9522
    
    print("🚀 Starting Perplexity AI Server...")
    print(f"📱 Web Interface: http://localhost:{port}")
    print(f"📚 API Docs: http://localhost:{port}/docs")
    print(f"🔧 Health Check: http://localhost:{port}/api/health")
    print(f"🌐 Server running on port {port}")
    
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )