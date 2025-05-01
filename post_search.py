import os
import jwt
import requests
from datetime import datetime
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def get_ghost_token():
    """
    Generate JWT token for Ghost Admin API authentication.
    
    Returns:
        str: JWT token for API authentication
        
    Raises:
        ValueError: If GHOST_ADMIN_API_KEY is not found in environment variables
        Exception: If token generation fails
    """
    try:
        # Get API key from environment
        key = os.getenv('GHOST_ADMIN_API_KEY')
        if not key:
            raise ValueError("GHOST_ADMIN_API_KEY not found in environment variables")

        # Split the key into ID and SECRET
        id, secret = key.split(':')

        # Prepare header and payload
        iat = int(datetime.now().timestamp())
        header = {'alg': 'HS256', 'typ': 'JWT', 'kid': id}
        payload = {
            'iat': iat,
            'exp': iat + 5 * 60,  # Token expires in 5 minutes
            'aud': '/admin/'
        }

        # Create the token
        token = jwt.encode(
            payload,
            bytes.fromhex(secret),
            algorithm='HS256',
            headers=header
        )

        return token
    except Exception as e:
        logger.error(f"Failed to generate Ghost token: {str(e)}")
        raise

def get_ghost_api_url():
    """
    Get the Ghost Admin API URL from environment variables.
    
    Returns:
        str: Complete Ghost Admin API URL
        
    Raises:
        ValueError: If GHOST_URL is not found in environment variables
    """
    base_url = os.getenv('GHOST_URL')
    if not base_url:
        raise ValueError("GHOST_URL not found in environment variables")
    
    # Remove trailing slash if present
    base_url = base_url.rstrip('/')
    return f"{base_url}/ghost/api/admin"

def get_edit_url(post_id):
    """
    Generate the Ghost admin editor URL for a specific post.
    
    Args:
        post_id (str): The ID of the post to generate the edit URL for
        
    Returns:
        str: Complete URL to edit the post in Ghost admin
        
    Raises:
        ValueError: If GHOST_URL is not found in environment variables
    """
    base_url = os.getenv('GHOST_URL')
    if not base_url:
        raise ValueError("GHOST_URL not found in environment variables")
    return f"{base_url}/ghost/#/editor/post/{post_id}/" 

def search_posts(search_term):
    """
    Search for posts in Ghost that match the given search term in their title.
    
    This function:
    1. Searches for posts with titles containing the search term
    2. Displays detailed information about each matching post
    3. Provides both public URL and admin edit URL for each post
    
    Args:
        search_term (str): The term to search for in post titles
        
    Returns:
        list: List of matching post objects from the Ghost API
        
    Raises:
        Exception: If any error occurs during the search process
    """
    try:
        # Get authentication token and API URL
        token = get_ghost_token()
        api_url = get_ghost_api_url()

        # Set up headers
        headers = {
            'Authorization': f'Ghost {token}',
            'Content-Type': 'application/json',
            'Accept-Version': 'v5.0'
        }

        # Search for posts
        posts_url = f"{api_url}/posts/"
        response = requests.get(
            posts_url,
            headers=headers,
            params={
                'limit': 'all',
                'filter': f"title:~'{search_term}'"
            }
        )
        response.raise_for_status()
        posts = response.json()['posts']

        logger.info(f"Found {len(posts)} posts matching search term: '{search_term}'")

        # Display matching posts
        if posts:
            print("\nMatching Posts:")
            print("-" * 50)
            for post in posts:
                edit_url = get_edit_url(post['id'])
                print(f"Title: {post['title']}")
                print(f"Published: {post['published_at']}")
                print(f"Status: {post['status']}")
                print(f"Visibility: {post['visibility']}")
                print(f"URL: {post['url']}")
                print(f"Edit URL: {edit_url}")
                print("-" * 50)
        else:
            print(f"\nNo posts found matching: '{search_term}'")

        return posts

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    # Check for required environment variables
    required_vars = ['GHOST_URL', 'GHOST_ADMIN_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        logger.info("Please create a .env file with the following variables:")
        logger.info("GHOST_URL=your_ghost_url")
        logger.info("GHOST_ADMIN_API_KEY=your_admin_api_key")
        exit(1)
    
    # Get search term from user
    search_term = input("Enter search term: ").strip()
    if not search_term:
        print("Search term cannot be empty")
        exit(1)
    
    search_posts(search_term) 