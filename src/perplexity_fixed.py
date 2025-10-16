import re
import sys
import json
import random
import asyncio
import mimetypes
import os
from uuid import uuid4
from curl_cffi import requests, CurlMime

class PerplexityError(Exception):
    pass


class AsyncMixin:
    def __init__(self, *args, **kwargs):
        self.__storedargs = args, kwargs
        self.async_initialized = False
        
    async def __ainit__(self, *args, **kwargs):
        pass
    
    async def __initobj(self):
        assert not self.async_initialized
        self.async_initialized = True
        
        # pass the parameters to __ainit__ that passed to __init__
        await self.__ainit__(*self.__storedargs[0], **self.__storedargs[1])
        return self
    
    def __await__(self):
        return self.__initobj().__await__()


class Client(AsyncMixin):
    '''
    A client for interacting with the Perplexity AI API.
    '''
    async def __ainit__(self, cookies=None):
        # If no cookies provided, cookies must be passed explicitly
        if cookies is None:
            cookies = {}
        self.session = requests.AsyncSession(headers={
            'accept': 'text/event-stream',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'en-US,en;q=0.5',
            'content-type': 'application/json',
            'origin': 'https://www.perplexity.ai',
            'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Brave";v="140"',
            'sec-ch-ua-arch': '"x86"',
            'sec-ch-ua-bitness': '"64"',
            'sec-ch-ua-full-version-list': '"Chromium";v="140.0.0.0", "Not=A?Brand";v="24.0.0.0", "Brave";v="140.0.0.0"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Linux"',
            'sec-ch-ua-platform-version': '"6.12.48"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
            'x-perplexity-request-reason': 'perplexity-query-state-provider'
        }, cookies=cookies, impersonate='chrome')
        self.own = bool(cookies)
        self.copilot = 0 if not cookies else float('inf')
        self.file_upload = 0 if not cookies else float('inf')
        self.signin_regex = re.compile(r'"(https://www\.perplexity\.ai/api/auth/callback/email\?callbackUrl=.*?)"')
        self.timestamp = format(random.getrandbits(32), '08x')
        self.visitor_id = str(uuid4())  # Generate visitor_id
        self.user_nextauth_id = None   # Will be populated from session if available

        # Initialize session and extract user info
        try:
            session_resp = await self.session.get('https://www.perplexity.ai/api/auth/session')
            if session_resp.status_code == 200:
                try:
                    session_data = session_resp.json()
                    # Extract user ID if available in session
                    if 'user' in session_data and session_data['user']:
                        self.user_nextauth_id = session_data['user'].get('id')
                except (json.JSONDecodeError, KeyError):
                    pass
        except Exception as e:
            print(f"Warning: Could not initialize session: {e}")
    
    async def _create_payload(self, query, mode, model, sources, files, follow_up, incognito, language='en-US', prompt_source='user', query_source='home', should_ask_for_mcp_tool_confirmation=True, search_focus='internet', timezone='Europe/Berlin'):
        """Helper to create the JSON payload for the API request."""
        
        # Validate sources - now supports all available sources including edgar
        valid_sources = ['web', 'scholar', 'social', 'edgar']
        if isinstance(sources, str):
            sources = [sources]  # Convert single string to list
        
        for source in sources:
            if source not in valid_sources:
                raise PerplexityError(f"Invalid source '{source}'. Valid sources: {valid_sources}")
        
        model_preference_map = {
            'auto': { None: 'turbo' },
            'pro': {
                None: 'pplx_pro', 'sonar': 'experimental', 'gpt-4.5': 'gpt45', 'gpt-4o': 'gpt4o',
                'claude 3.7 sonnet': 'claude2', 'gemini 2.0 flash': 'gemini2flash', 'grok-2': 'grok',
                'claude': 'claude2', 'gemini2flash': 'gemini2flash', 'grok4': 'grok4', 'pplx_pro': 'pplx_pro',
                'sonar': 'sonar', 'gpt41': 'gpt41', 'claude37sonnetthinking': 'claude37sonnetthinking', 'o3': 'o3',
                'claude45sonnet': 'claude45sonnet', 'claude45sonnetthinking': 'claude45sonnetthinking',
                'gpt5': 'gpt5', 'gpt5thinking': 'gpt5thinking'
            },
            'reasoning': {
                None: 'pplx_reasoning', 'r1': 'r1', 'o3-mini': 'o3mini', 'claude 3.7 sonnet': 'claude37sonnetthinking'
            },
            'deep research': { None: 'pplx_alpha', 'pplx_alpha': 'pplx_alpha' },
            'deep lab': { None: 'pplx_beta', 'pplx_beta': 'pplx_beta' }
        }

        assert mode in model_preference_map, f'Invalid search mode: {mode}'
        if mode in ['pro', 'reasoning', 'deep lab'] and model is None:
            raise PerplexityError(f"Model selection is required for '{mode}' mode.")
        assert model in model_preference_map[mode], f"Invalid model '{model}' for mode '{mode}'."

        # Handle file uploads using the proper Perplexity API flow (like ref.py)
        uploaded_files = []
        if files:
            for filename, file_content in files.items():
                try:
                    # Get file type
                    file_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
                    
                    # Ensure file_content is bytes
                    if isinstance(file_content, str):
                        file_data = file_content.encode('utf-8')
                    else:
                        file_data = file_content
                    
                    # Get upload URL from Perplexity
                    file_upload_info = (await self.session.post(
                        'https://www.perplexity.ai/rest/uploads/create_upload_url?version=2.18&source=default',
                        json={
                            'content_type': file_type,
                            'file_size': len(file_data),
                            'filename': filename,
                            'force_image': False,
                            'source': 'default',
                        }
                    )).json()

                    # Create multipart form data using CurlMime
                    mp = CurlMime()
                    for key, value in file_upload_info['fields'].items():
                        mp.addpart(name=key, data=value)
                    
                    # Add the file content
                    mp.addpart(name='file', content_type=file_type, filename=filename, data=file_data)

                    # Upload to S3
                    upload_resp = await self.session.post(file_upload_info['s3_bucket_url'], multipart=mp)
                    
                    if not upload_resp.ok:
                        raise PerplexityError(f'File upload error for {filename}: {upload_resp.status_code}')

                    # Get the final URL (same logic as ref.py)
                    if 'image/upload' in file_upload_info['s3_object_url']:
                        uploaded_url = re.sub(
                            r'/private/s--.*?--/v\d+/user_uploads/',
                            '/private/user_uploads/',
                            upload_resp.json()['secure_url']
                        )
                    else:
                        uploaded_url = file_upload_info['s3_object_url']

                    uploaded_files.append(uploaded_url)
                    
                except Exception as e:
                    raise PerplexityError(f"Failed to upload file {filename}: {str(e)}")

        final_query = query

        return {
            'query_str': final_query,
            'params': {
                'attachments': uploaded_files + (follow_up.get('attachments', []) if follow_up else []),
                'language': language,
                'timezone': timezone,
                'search_focus': search_focus,
                'search_recency_filter': None,
                'frontend_context_uuid': str(uuid4()),
                'frontend_uuid': str(uuid4()),
                'mode': 'concise' if mode == 'auto' else 'copilot',
                'model_preference': model_preference_map[mode][model],
                'is_related_query': False,
                'is_sponsored': False,
                'visitor_id': getattr(self, 'visitor_id', str(uuid4())),  # Store visitor_id if available
                'user_nextauth_id': getattr(self, 'user_nextauth_id', None),  # From session if available
                'prompt_source': prompt_source,
                'query_source': query_source,
                'is_incognito': incognito,
                'time_from_first_type': None,  # Can be tracked if needed
                'local_search_enabled': False,
                'use_schematized_api': True,
                'send_back_text_in_streaming_api': False,
                'supported_block_use_cases': [
                    'answer_modes', 'media_items', 'knowledge_cards', 'inline_entity_cards',
                    'place_widgets', 'finance_widgets', 'sports_widgets', 'shopping_widgets',
                    'jobs_widgets', 'search_result_widgets', 'clarification_responses',
                    'inline_images', 'inline_assets', 'inline_finance_widgets',
                    'placeholder_cards', 'diff_blocks', 'inline_knowledge_cards',
                    'entity_group_v2', 'refinement_filters', 'canvas_mode', 'maps_preview'
                ],
                'client_coordinates': None,
                'mentions': [],
                'dsl_query': final_query,
                'skip_search_enabled': True,
                'is_nav_suggestions_disabled': False,
                'always_search_override': False,
                'override_no_search': False,
                'comet_max_assistant_enabled': False,
                'should_ask_for_mcp_tool_confirmation': should_ask_for_mcp_tool_confirmation,
                # Legacy fields for backward compatibility
                'last_backend_uuid': follow_up.get('backend_uuid') if follow_up else None,
                'read_write_token': follow_up.get('read_write_token') if follow_up else None,
                'source': 'default',
                'sources': sources,
                'version': '2.18'
            }
        }

    async def search(self, query, mode='auto', model=None, sources=['web'], files={}, language='en-US', follow_up=None, incognito=False, prompt_source='user', query_source='home', should_ask_for_mcp_tool_confirmation=True, search_focus='internet', timezone='Europe/Berlin'):
        """Performs a non-streaming search and returns the final JSON result."""
        json_data = await self._create_payload(query, mode, model, sources, files, follow_up, incognito, language, prompt_source, query_source, should_ask_for_mcp_tool_confirmation, search_focus, timezone)

        try:
            resp = await self.session.post('https://www.perplexity.ai/rest/sse/perplexity_ask', json=json_data, stream=True)
            if resp.status_code != 200:
                raise PerplexityError(f"HTTP Error {resp.status_code}: {resp.text}")

            chunks = []
            async for chunk in resp.aiter_lines(delimiter=b'\r\n\r\n'):
                content = chunk.decode('utf-8')
                
                if content.startswith('event: message\r\n'):
                    try:
                        data_part = content[len('event: message\r\ndata: '):]
                        content_json = json.loads(data_part)
                        
                        # Parse text field if it exists
                        if 'text' in content_json and isinstance(content_json['text'], str):
                            try:
                                content_json['text'] = json.loads(content_json['text'])
                            except json.JSONDecodeError:
                                pass
                        
                        chunks.append(content_json)
                        
                    except Exception as e:
                        chunks.append({"error": "Parse error", "message": str(e)})
                
                elif content.startswith('event: end_of_stream\r\n'):
                    break
            
            if chunks:
                return chunks[-1]
            else:
                raise PerplexityError("No response received from the API")
                
        except Exception as e:
            raise PerplexityError(f"Search request failed: {str(e)}")

    async def search_stream(self, query, mode='auto', model=None, sources=['web'], files={}, language='en-US', follow_up=None, incognito=False, prompt_source='user', query_source='home', should_ask_for_mcp_tool_confirmation=True, search_focus='internet', timezone='Europe/Berlin'):
        """Performs a streaming search, yielding each JSON chunk."""
        json_data = await self._create_payload(query, mode, model, sources, files, follow_up, incognito, language, prompt_source, query_source, should_ask_for_mcp_tool_confirmation, search_focus, timezone)

        try:
            resp = await self.session.post('https://www.perplexity.ai/rest/sse/perplexity_ask', json=json_data, stream=True)
            if resp.status_code != 200:
                raise PerplexityError(f"HTTP Error {resp.status_code}: {resp.text}")

            async for chunk in resp.aiter_lines(delimiter=b'\r\n\r\n'):
                content = chunk.decode('utf-8')
                
                if content.startswith('event: message\r\n'):
                    try:
                        data_part = content[len('event: message\r\ndata: '):]
                        content_json = json.loads(data_part)
                        
                        # Parse text field if it exists
                        if 'text' in content_json and isinstance(content_json['text'], str):
                            try:
                                content_json['text'] = json.loads(content_json['text'])
                            except json.JSONDecodeError:
                                pass
                        
                        yield content_json
                        
                    except Exception as e:
                        yield {"error": "Parse error", "message": str(e)}
                
                elif content.startswith('event: end_of_stream\r\n'):
                    return
                    
        except Exception as e:
            yield {'error': 'Stream failed', 'message': str(e)}