# Ghost Content API - Post Visibility Updater

This script updates the visibility of posts in a Ghost blog to "paid" status for all posts published before the current year that are not already marked as paid.

## Features

- Automatically identifies posts from previous years that are not marked as paid
- Updates post visibility to "paid" status
- Handles API authentication securely
- Provides detailed logging of the update process
- Implements proper error handling and collision detection

## Prerequisites

- Python 3.6 or higher
- Required Python packages:
  - `requests`
  - `python-jwt`
  - `python-dotenv`

## Installation

1. Clone this repository or download the script
2. Install the required packages:

```bash
pip install requests python-jwt python-dotenv
```

## Configuration

Create a `.env` file in the same directory as the script with the following variables:

```
GHOST_URL=your_ghost_url
GHOST_ADMIN_API_KEY=your_admin_api_key
```

- `GHOST_URL`: Your Ghost blog URL (e.g., `https://your-blog.com`)
- `GHOST_ADMIN_API_KEY`: Your Ghost Admin API key (format: `id:secret`)

## Usage

Run the script using Python:

```bash
python update_posts_to_paid.py
```

The script will:

1. Connect to your Ghost blog using the Admin API
2. Find all posts from previous years that are not marked as paid
3. Update their visibility to "paid" status
4. Log the progress and results

## Output

The script provides detailed logging of its operations:

- Number of posts found that need updating
- Success/failure status for each post update
- Total number of successfully updated posts

## Error Handling

The script includes comprehensive error handling:

- Validates environment variables
- Handles API authentication errors
- Manages individual post update failures
- Provides detailed error messages in the logs

## Security

- API credentials are stored in environment variables
- JWT tokens are generated with a 5-minute expiration
- No sensitive data is logged

## License

This project is open source and available under the MIT License.
