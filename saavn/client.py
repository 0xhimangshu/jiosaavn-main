import json
import logging
from typing import Dict, Optional

import httpx

from .routes import Route

logging.getLogger("httpx").setLevel(logging.WARNING)


class HttpClient:
    """A high-performance HTTP client with standardized error handling."""

    def __init__(self, headers: Optional[Dict[str, str]] = None) -> None:
        """Initialize the HTTP client with optional headers.
        
        Args:
            headers: Optional dictionary of HTTP headers to include with requests.
        """
        self.headers = headers
        self.client = httpx.Client(
            headers=headers,
            timeout=30.0,  # Set reasonable timeout
            verify=True,   # Enable SSL verification
            http2=True     # Enable HTTP/2 for better performance
        )

    def __enter__(self) -> 'HttpClient':
        """Context manager entry point."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit point that ensures proper client cleanup."""
        self.client.close()

    def _handle_response(self, response: httpx.Response) -> Dict:
        """Handle HTTP response and return parsed JSON data.
        
        Args:
            response: The HTTP response to process.
            
        Returns:
            Parsed JSON response as dictionary.
            
        Raises:
            httpx.RequestError: If response status is not 200.
            ValueError: If JSON parsing fails.
        """
        if response.status_code != 200:
            raise httpx.RequestError(f"Request failed with status {response.status_code}: {response.text}")
        try:
            return response.json()
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to decode JSON response: {str(e)}")

    def get(self, route: Route) -> Dict:
        """Make an optimized GET request to the specified route.
        
        Args:
            route: The Route object containing the URL to request.
            
        Returns:
            The JSON response as a dictionary.
            
        Raises:
            httpx.RequestError: If the request fails.
            ValueError: If the response cannot be parsed as JSON.
        """
        response = self.client.get(route.url)
        return self._handle_response(response)

    def post(self, route: Route) -> Dict:
        """Make an optimized POST request to the specified route.
        
        Args:
            route: The Route object containing the URL to request.
            
        Returns:
            The JSON response as a dictionary.
            
        Raises:
            httpx.RequestError: If the request fails.
            ValueError: If the response cannot be parsed as JSON.
        """
        response = self.client.post(route.url)
        return self._handle_response(response)

    def get_buffer(self, url: str) -> bytes:
        """Make an optimized GET request and return raw response content.
        
        Args:
            url: The URL to request.
            
        Returns:
            The raw response content as bytes.
            
        Raises:
            httpx.RequestError: If the request fails.
        """
        response = self.client.get(url)
        if response.status_code != 200:
            raise httpx.RequestError(f"Request failed with status {response.status_code}: {response.text}")
        return response.content
