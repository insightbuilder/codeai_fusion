To design a URL shortener system similar to TinyURL, the system needs to efficiently map long URLs to short, unique URLs and provide features such as URL customization, expiration, and analytics. We'll use Python, PostgreSQL, and relevant libraries to achieve this.

### **Functional Requirements**

1. **Generate Unique Short URL**:
   
   - Map long URLs to short URLs using base62 encoding or a hash function.

2. **Redirection**:
   
   - Redirect the user to the original long URL when the short URL is accessed.

3. **Custom Short URLs** (optional):
   
   - Allow users to define their custom short URL slug.

4. **Link Expiration**:
   
   - Support setting expiration dates for short URLs, after which they become inactive.

5. **Analytics** (optional):
   
   - Provide usage statistics such as the number of clicks, unique users, geographic location, etc.

---

### **System Architecture**

#### **Components**:

1. **API Backend**: Handles URL creation, redirection, and analytics.
2. **PostgreSQL Database**: Stores URLs, expiration dates, and analytics.
3. **Web Interface** (optional): Allows users to input long URLs and receive short URLs.

---

### **Database Schema Design**

```sql
-- Table to store original and shortened URLs
CREATE TABLE urls (
    id SERIAL PRIMARY KEY,
    long_url TEXT NOT NULL,
    short_url TEXT UNIQUE,       -- Generated short URL or user-defined
    custom_url TEXT,             -- Optional user-defined short URL
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,        -- Optional expiration timestamp
    clicks INTEGER DEFAULT 0     -- Stores number of times the link was clicked
);

-- Table for tracking analytics (optional)
CREATE TABLE url_analytics (
    id SERIAL PRIMARY KEY,
    short_url_id INTEGER REFERENCES urls(id),
    accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address TEXT,             -- IP address of the user accessing the link
    user_agent TEXT              -- User agent string of the browser/device
);
```

---

### **Algorithms and Code Implementation**

#### **1. Generate Unique Short URL**

For generating unique short URLs, we can use base62 encoding. Base62 uses alphanumeric characters (a-z, A-Z, 0-9) to create short URLs.

```python
import string
import random
import base64

# Base62 characters (62 possibilities)
BASE62 = string.ascii_letters + string.digits

# Encode an integer into Base62 for the short URL
def base62_encode(num):
    if num == 0:
        return BASE62[0]

    encoded = []
    while num:
        num, rem = divmod(num, 62)
        encoded.append(BASE62[rem])
    return ''.join(reversed(encoded))

# Generate a random short URL if no custom URL is provided
def generate_short_url():
    return ''.join(random.choices(BASE62, k=6))  # Random 6-character short URL
```

#### **2. URL Shortening Function**

The core function for shortening a URL, with optional customization and expiration.

```python
import psycopg2
from datetime import datetime, timedelta

# Initialize connection to PostgreSQL
def init_db():
    conn = psycopg2.connect(
        dbname='url_shortener',
        user='youruser',
        password='yourpassword',
        host='localhost',
        port='5432'
    )
    return conn

# Shorten URL function
def shorten_url(long_url, custom_url=None, expiration_days=None):
    conn = init_db()
    cursor = conn.cursor()

    # Check if custom URL is already taken
    if custom_url:
        cursor.execute("SELECT id FROM urls WHERE short_url = %s", (custom_url,))
        if cursor.fetchone():
            raise ValueError("Custom short URL is already in use.")
        short_url = custom_url
    else:
        # Generate a unique short URL
        while True:
            short_url = generate_short_url()
            cursor.execute("SELECT id FROM urls WHERE short_url = %s", (short_url,))
            if not cursor.fetchone():
                break

    # Calculate expiration date if specified
    expires_at = None
    if expiration_days:
        expires_at = datetime.now() + timedelta(days=expiration_days)

    # Insert the URL into the database
    cursor.execute(
        "INSERT INTO urls (long_url, short_url, custom_url, expires_at) VALUES (%s, %s, %s, %s) RETURNING id",
        (long_url, short_url, custom_url, expires_at)
    )
    conn.commit()
    conn.close()

    return f"Shortened URL: http://short.ly/{short_url}"

# Example usage
print(shorten_url("https://example.com/long-url"))
```

#### **3. URL Redirection**

The redirection function looks up the short URL in the database and redirects the user to the original long URL.

```python
from flask import Flask, redirect, abort
import psycopg2
from datetime import datetime

app = Flask(__name__)

# Function to get long URL from the short URL
def get_long_url(short_url):
    conn = init_db()
    cursor = conn.cursor()

    # Retrieve the long URL from the database
    cursor.execute("SELECT long_url, expires_at FROM urls WHERE short_url = %s", (short_url,))
    result = cursor.fetchone()
    conn.close()

    if result:
        long_url, expires_at = result
        # Check if the link has expired
        if expires_at and expires_at < datetime.now():
            return None
        return long_url
    return None

# Route to handle the redirection
@app.route('/<short_url>')
def redirect_url(short_url):
    long_url = get_long_url(short_url)
    if long_url:
        return redirect(long_url)
    else:
        abort(404)  # Return 404 if the short URL doesn't exist or has expired

if __name__ == '__main__':
    app.run(debug=True)
```

#### **4. Analytics and Click Tracking**

You can track clicks and user information like IP address and user agent.

```python
from flask import request

# Modify the redirect function to track analytics
@app.route('/<short_url>')
def redirect_url(short_url):
    long_url = get_long_url(short_url)
    if long_url:
        # Track click
        track_click(short_url)
        return redirect(long_url)
    else:
        abort(404)

def track_click(short_url):
    conn = init_db()
    cursor = conn.cursor()

    # Get the short URL ID
    cursor.execute("SELECT id FROM urls WHERE short_url = %s", (short_url,))
    short_url_id = cursor.fetchone()

    if short_url_id:
        # Log the click with IP address and user agent
        cursor.execute(
            "INSERT INTO url_analytics (short_url_id, ip_address, user_agent) VALUES (%s, %s, %s)",
            (short_url_id, request.remote_addr, request.headers.get('User-Agent'))
        )
        # Update click count
        cursor.execute("UPDATE urls SET clicks = clicks + 1 WHERE id = %s", (short_url_id,))
        conn.commit()

    conn.close()
```

---

### **Features Overview**

- **Unique Short URLs**: Use base62 encoding or random URL generation.
- **Redirection**: Redirect users to the original long URL when they access the short URL.
- **Custom Short URLs**: Allow users to define their own short URLs.
- **Link Expiration**: Support URL expiration after a specific time period.
- **Analytics**: Track the number of clicks, IP addresses, and user agents of visitors.

### **Scaling Considerations**

- Use caching (e.g., Redis) to speed up lookups of frequently accessed URLs.
- Use a load balancer to distribute requests across multiple application instances.
- Shard the database or move to a NoSQL solution for very high traffic systems.

This design will let you rapidly develop and deploy a fully functional URL shortener system using Python and PostgreSQL.
