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

# Generate a JWT token for Ghost Admin API authentication
def get_ghost_token():
    """Generate JWT token for Ghost Admin API authentication."""
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

# Get the Ghost Admin API URL
def get_ghost_api_url():
    """Get the Ghost Admin API URL."""
    base_url = os.getenv('GHOST_URL')
    if not base_url:
        raise ValueError("GHOST_URL not found in environment variables")
    
    # Remove trailing slash if present
    base_url = base_url.rstrip('/')
    return f"{base_url}/ghost/api/admin"

# Update posts from previous years to paid status
def update_posts_to_paid():
    """Update posts from previous years to paid status."""
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

        # Calculate the start of the current year
        current_year = datetime.now().year
        start_of_current_year = f"{current_year}-01-01T00:00:00Z"

        # Get posts from previous years, that are not paid
        posts_url = f"{api_url}/posts/"
        response = requests.get(
            posts_url,
            headers=headers,
            params={
                'limit': 'all',
                'filter': f'visibility:-paid+published_at:<{start_of_current_year}'
            }
        )
        response.raise_for_status()
        posts = response.json()['posts']

        logger.info(f"Found {len(posts)} posts from previous years that are not paid")


        # Update each post to paid status
        updated_count = 0
        for post in posts:
            try:
                # Get the latest version of the post to ensure we have the current updated_at
                post_url = f"{api_url}/posts/{post['id']}/"
                post_response = requests.get(post_url, headers=headers)
                post_response.raise_for_status()
                current_post = post_response.json()['posts'][0]

                # Create the update data
                update_url = f"{api_url}/posts/{post['id']}/"
                update_data = {
                    'posts': [{
                        'id': post['id'],
                        'visibility': 'paid',
                        'updated_at': current_post['updated_at']
                    }]
                }

                # Update the post to paid status
                update_response = requests.put(
                    update_url,
                    headers=headers,
                    json=update_data
                )
                update_response.raise_for_status()
                updated_count += 1
                logger.info(f"Updated post: {post['title']}")
            except Exception as e:
                logger.error(f"Failed to update post {post['title']}: {str(e)}")
                continue

        logger.info(f"Successfully updated {updated_count} posts to paid status")
        return updated_count

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
    
    update_posts_to_paid() 