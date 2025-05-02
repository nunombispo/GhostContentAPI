# Ghost Content API Tools

A collection of Python scripts for managing Ghost blog content through the Ghost Admin API.

If these scripts were useful to you, consider donating to support the Developer Service Blog: https://buy.stripe.com/bIYdTrggi5lZamkdQW

## Scripts

### 1. Update Posts to Paid Status (`update_posts_to_paid.py`)

Updates the visibility of posts in a Ghost blog to "paid" status for all posts published before the current year that are not already marked as paid.

Features:

- Automatically identifies posts from previous years that are not marked as paid
- Updates post visibility to "paid" status
- Handles API authentication securely
- Provides detailed logging of the update process
- Implements proper error handling and collision detection

### 2. Update Posts to Members Status (`update_posts_member.py`)

Updates the visibility of posts in a Ghost blog to "members" status for all public posts published in the current year.

Features:

- Automatically identifies public posts from the current year
- Updates post visibility to "members" status
- Handles API authentication securely
- Provides detailed logging of the update process
- Implements proper error handling and collision detection

### 3. Post Search (`post_search.py`)

Searches for posts in your Ghost blog by title and displays detailed information about matching posts.

Features:

- Search posts by title using partial matches
- Display comprehensive post information including:
  - Title
  - Publication date
  - Status
  - Visibility
  - Public URL
  - Admin edit URL
- Handles API authentication securely
- Provides detailed logging of the search process

## Prerequisites

- Python 3.6 or higher
- Required Python packages:
  - `requests`
  - `python-jwt`
  - `python-dotenv`

## Installation

1. Clone this repository or download the scripts
2. Install the required packages:

```bash
pip install requests python-jwt python-dotenv
```

## Configuration

Create a `.env` file in the same directory as the scripts with the following variables:

```
GHOST_URL=your_ghost_url
GHOST_ADMIN_API_KEY=your_admin_api_key
```

- `GHOST_URL`: Your Ghost blog URL (e.g., `https://your-blog.com`)
- `GHOST_ADMIN_API_KEY`: Your Ghost Admin API key (format: `id:secret`)

## Usage

### Update Posts to Paid Status

```bash
python update_posts_to_paid.py
```

This script will:

1. Connect to your Ghost blog using the Admin API
2. Find all posts from previous years that are not marked as paid
3. Update their visibility to "paid" status
4. Log the progress and results

### Update Posts to Members Status

```bash
python update_posts_member.py
```

This script will:

1. Connect to your Ghost blog using the Admin API
2. Find all public posts from the current year
3. Update their visibility to "members" status
4. Log the progress and results

### Search Posts

```bash
python post_search.py
```

This script will:

1. Prompt you to enter a search term
2. Search for posts with matching titles
3. Display detailed information about each matching post
4. Provide both public and admin edit URLs for each post

## Output

All scripts provide detailed logging of their operations:

- Number of posts found that need updating (for update scripts)
- Success/failure status for each post update
- Total number of successfully updated posts
- Detailed post information (for search script)

## Error Handling

The scripts include comprehensive error handling:

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
