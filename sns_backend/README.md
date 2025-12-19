# SNS Backend API

A Django-based SNS (Social Network Service) backend with PostgreSQL support. Posts are identified by unique SHA-256 hash values generated from the account ID and post timestamp.

## Features

- User authentication (signup/login/logout)
- Post creation, editing, and deletion
- Timeline viewing
- Like functionality
- Reply system
- SHA-256 based post IDs

## Setup

1. Install dependencies:
```bash
pip3 install -r requirements.txt
```

2. Configure database (PostgreSQL recommended for production):
```bash
# Edit .env file with your database credentials
DB_NAME=sns_db
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
```

3. Run migrations:
```bash
python3 manage.py migrate
```

4. Start the development server:
```bash
python3 manage.py runserver
```

## API Endpoints

### Authentication Endpoints

#### Sign Up
Create a new user account.

**Endpoint:** `POST /signup/`

**curl example:**
```bash
curl -X POST http://localhost:8000/signup/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

**JavaScript example:**
```javascript
const signup = async (username, password) => {
  const response = await fetch('http://localhost:8000/signup/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      username: username,
      password: password
    })
  });
  return await response.json();
};

// Usage
signup('testuser', 'testpass123').then(console.log);
```

#### Login
Authenticate and start a session.

**Endpoint:** `POST /login/`

**curl example:**
```bash
curl -X POST http://localhost:8000/login/ \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

**JavaScript example:**
```javascript
const login = async (username, password) => {
  const response = await fetch('http://localhost:8000/login/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include', // Important for session cookies
    body: JSON.stringify({
      username: username,
      password: password
    })
  });
  return await response.json();
};

// Usage
login('testuser', 'testpass123').then(console.log);
```

#### Logout
End the current session.

**Endpoint:** `POST /logout/`

**curl example:**
```bash
curl -X POST http://localhost:8000/logout/ \
  -b cookies.txt
```

**JavaScript example:**
```javascript
const logout = async () => {
  const response = await fetch('http://localhost:8000/logout/', {
    method: 'POST',
    credentials: 'include'
  });
  return await response.json();
};

// Usage
logout().then(console.log);
```

### Public Endpoints

#### View Post
Get a single post by its ID.

**Endpoint:** `GET /view/<post_id>/`

**curl example:**
```bash
curl http://localhost:8000/view/abc123.../
```

**JavaScript example:**
```javascript
const viewPost = async (postId) => {
  const response = await fetch(`http://localhost:8000/view/${postId}/`);
  return await response.json();
};

// Usage
viewPost('your_post_id_here').then(console.log);
```

**Response format:**
```json
{
  "ID": "sha256_hash_here",
  "ACCOUNT": "username",
  "TIME": 1671234567,
  "CONTENT": "Post content here",
  "LIKED": 5,
  "RELATED": "parent_post_id_or_null"
}
```

#### Timeline
Get recent posts.

**Endpoint:** `GET /timeline/<number>/`

**curl example:**
```bash
curl http://localhost:8000/timeline/10/
```

**JavaScript example:**
```javascript
const getTimeline = async (count) => {
  const response = await fetch(`http://localhost:8000/timeline/${count}/`);
  return await response.json();
};

// Usage - get 10 most recent posts
getTimeline(10).then(console.log);
```

**Response format:**
```json
[
  {
    "ID": "sha256_hash_here",
    "ACCOUNT": "username",
    "TIME": 1671234567,
    "CONTENT": "Post content here",
    "LIKED": 5,
    "RELATED": null
  },
  // ... more posts
]
```

#### Like Post
Add a like to a post (anonymous, increment counter).

**Endpoint:** `GET /like/<post_id>/`

**curl example:**
```bash
curl http://localhost:8000/like/abc123.../
```

**JavaScript example:**
```javascript
const likePost = async (postId) => {
  const response = await fetch(`http://localhost:8000/like/${postId}/`);
  return await response.json();
};

// Usage
likePost('your_post_id_here').then(console.log);
```

**Response format:**
```json
{
  "liked": 6
}
```

### Authenticated Endpoints

#### Create Post
Create a new post (requires login).

**Endpoint:** `POST /post/`

**curl example:**
```bash
curl -X POST http://localhost:8000/post/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "content": "Hello, world! This is my first post.",
    "related": null
  }'
```

**JavaScript example:**
```javascript
const createPost = async (content, relatedPostId = null) => {
  const response = await fetch('http://localhost:8000/post/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
    body: JSON.stringify({
      content: content,
      related: relatedPostId
    })
  });
  return await response.json();
};

// Usage - create a new post
createPost('Hello, world! This is my first post.').then(console.log);

// Usage - create a reply to another post
createPost('This is a reply!', 'parent_post_id_here').then(console.log);
```

**Response format:**
```json
{
  "id": "generated_sha256_hash"
}
```

#### Edit Post
Edit your own post (requires login and ownership).

**Endpoint:** `POST /edit/<post_id>/`

**curl example:**
```bash
curl -X POST http://localhost:8000/edit/abc123.../ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "content": "Updated post content",
    "related": null
  }'
```

**JavaScript example:**
```javascript
const editPost = async (postId, content, relatedPostId = null) => {
  const response = await fetch(`http://localhost:8000/edit/${postId}/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
    body: JSON.stringify({
      content: content,
      related: relatedPostId
    })
  });
  return await response.json();
};

// Usage
editPost('your_post_id_here', 'Updated content').then(console.log);
```

#### Delete Post
Delete your own post (requires login and ownership).

**Endpoint:** `POST /delete/<post_id>/`

**curl example:**
```bash
curl -X POST http://localhost:8000/delete/abc123.../ \
  -b cookies.txt
```

**JavaScript example:**
```javascript
const deletePost = async (postId) => {
  const response = await fetch(`http://localhost:8000/delete/${postId}/`, {
    method: 'POST',
    credentials: 'include'
  });
  return await response.json();
};

// Usage
deletePost('your_post_id_here').then(console.log);
```

## Data Model

### Post Table Structure
- **ID**: SHA-256 hash (primary key)
- **ACCOUNT**: Username of the poster
- **TIME**: Unix epoch timestamp
- **CONTENT**: Post text content (max 1000 characters)
- **LIKED**: Number of likes (integer)
- **RELATED**: ID of parent post (null for top-level posts)

### Post ID Generation
Post IDs are generated using SHA-256 hash of:
```
hash_input = account_id + unix_timestamp
post_id = sha256(hash_input)
```

## Error Responses

All endpoints return JSON error responses with appropriate HTTP status codes:

```json
{
  "error": "Error message description"
}
```

Common status codes:
- `400`: Bad Request (invalid input)
- `401`: Unauthorized (login required)
- `403`: Forbidden (permission denied)
- `404`: Not Found (resource doesn't exist)
- `500`: Internal Server Error

## Development Notes

- The current setup uses SQLite for development. Uncomment PostgreSQL configuration in `settings.py` for production use.
- CSRF protection is disabled for API endpoints using `@csrf_exempt`.
- Session-based authentication is used (cookies required for authenticated endpoints).
- All timestamps are in Unix epoch format.
- Maximum post content length is 1000 characters.