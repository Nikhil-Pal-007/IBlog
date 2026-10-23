# iBlog — Blogging Platform

iBlog is a full-stack blogging website built using **Python and Django**. It allows users to create, publish, and share blog posts while interacting with other users through likes, comments, replies, follows, notifications, and messaging.

The project also includes AI-related tools for text summarization, English–Hindi translation, text-to-speech, grammar and spelling suggestions, and basic mood detection.

I built this project to strengthen my practical knowledge of Django, database relationships, authentication, frontend development, JavaScript, and integrating Python libraries into a real-world web application.

## Features

### 1. User Authentication and Profiles

- User registration and login
- User logout
- User profile pages
- Profile pictures and biographies
- Follow and unfollow users
- View other users' profiles
- Search for creators
- Notifications and unread notification counts

### 2. Blog Management

- Create and publish blog posts
- Edit and delete your own blog posts
- Upload images with blog posts
- Organize posts by category
- View individual blog details
- Track blog views
- Like and unlike posts
- Comment on blog posts
- Reply to comments
- Delete your own comments
- Save and unsave blog posts
- View saved blogs
- Share blog posts

### 3. Blog Categories

Users can organize their posts into the following categories:

- Technology
- Travel
- Food
- Entertainment
- Fitness
- Photography
- Nature
- Personal Stories
- Sports
- Self Improvement

### 4. Search

The navbar includes a search feature that helps users discover creators and blog posts.

Creator search results can display profile pictures, usernames, and short biographies.

### 5. Trending Blogs and Top Creators

**Trending Blogs:** Blog views are tracked and can be used to identify popular posts.

**Top Creators:** Creator rankings can be based on the number of blog posts published by each user.

### 6. Messaging and Notifications

- Inbox for user messages
- Messaging between users
- Unread message indicators
- Notifications for relevant user activity, such as follows and comments
- Notification badge in the navbar

### 7. AI Tools

iBlog includes several tools designed to make writing and reading content more convenient.

#### Text Summarization

Users can enter longer text and generate a shorter summary.

**Library:** `sumy`

#### English–Hindi Translation

Users can translate text between English and Hindi in both directions:

- English to Hindi
- Hindi to English

**Library:** `argostranslate`

Argos Translate is used for offline machine translation after the required language models have been installed. Translation does not rely on Google Translator or the `deep-translator` package.

**Important:** The required English and Hindi translation models must be installed on the system for offline translation to work. Supported translation directions depend on the installed language packages.

#### Text-to-Speech

Users can convert text into spoken audio.

**Library:** `gTTS`

This feature uses Google Text-to-Speech and therefore requires an internet connection.

#### Grammar and Spelling Suggestions

The writing interface provides grammar and spelling suggestions to help users improve their blog content.

Suggestions are displayed for the user to review rather than automatically replacing the original text.

**Library:** `language-tool-python`

#### Mood Detection

The application includes a basic keyword-based mood detection feature that identifies possible moods from text, such as:

- Motivated
- Curious
- Relaxed

This is a simple rule-based implementation, not a trained machine learning model.

## Technologies Used

### Backend
- Python
- Django

### Frontend
- HTML5
- CSS3
- JavaScript
- Bootstrap
- Font Awesome

### Database
- SQLite

### Python Libraries
- Django
- `sumy` — text summarization
- `argostranslate` — offline English–Hindi translation
- `gTTS` — text-to-speech
- `language-tool-python` — grammar and spelling suggestions

## Project Structure

The main project structure is organized as follows. The exact files and folders may vary depending on the current project version.

```text
IBlog/
│
├── accounts/
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── ai_tools/
│   ├── views.py
│   └── urls.py
│
├── iblog/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── media/
├── static/
├── templates/
│
├── db.sqlite3
├── manage.py
├── requirements.txt
└── README.md
```

## Database

iBlog uses **SQLite** as its database.

The local database file is:

```text
db.sqlite3
```

SQLite integrates easily with Django and is convenient for local development and portfolio projects without requiring a separate database server.

## Installation and Setup

### Prerequisites

Install the following before running the project:

- Python
- pip
- Git (if cloning the repository)

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Open the project directory

```bash
cd IBlog
```

### 3. Create and activate a virtual environment

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 4. Install the dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Make sure `requirements.txt` includes the packages required by your actual implementation.

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Create an administrator account

```bash
python manage.py createsuperuser
```

Follow the terminal instructions to create the account.

### 7. Configure offline translation

Install Argos Translate if it is listed in your requirements:

```bash
pip install argostranslate
```

Install the English and Hindi language packages using the Argos Translate package manager or Python API. The translation models need to be downloaded and installed before the first offline translation.

If your application already includes the language-model installation process, follow the existing implementation instead of installing the packages again.

### 8. Start the development server

```bash
python manage.py runserver
```

Open the local development server in your browser:

```text
http://127.0.0.1:8000/
```

## Authentication and Permissions

iBlog uses Django's built-in authentication system for user authentication.

Access to certain actions is restricted according to the logged-in user. For example, users can edit or delete their own blog posts but cannot edit or delete posts belonging to other users.

The application also uses CSRF protection for relevant POST requests and associates user-specific content, such as saved blogs and messages, with the appropriate users.

## What I Learned

Developing iBlog helped me practice:

- Django project and app architecture
- Models, migrations, and the Django ORM
- ForeignKey, OneToOneField, and ManyToManyField relationships
- User authentication and permissions
- URL routing, views, templates, and template tags
- Forms and CSRF protection
- Static files and media uploads
- SQLite database integration
- JavaScript DOM manipulation and event handling
- Fetch requests and asynchronous frontend interactions
- Building likes, comments, replies, follows, and bookmarks
- Implementing messaging and notification features
- Integrating third-party Python libraries
- Implementing offline machine translation
- Connecting frontend components to Django backend logic
- Debugging template, URL, database, and JavaScript errors
- Making the user interface responsive across screen sizes

## Challenges Faced

During development, I worked through issues involving URL routing, template rendering, database relationships, model changes, JavaScript behavior, and frontend responsiveness.

I also explored the limitations of online translation and text-to-speech services and used Argos Translate for offline English–Hindi translation.

These challenges helped me understand how separate Django components work together in a complete web application.

## Future Improvements

Potential improvements include:

- More advanced blog recommendations
- Improved search and filtering
- Pagination for blog lists
- Enhanced real-time messaging
- More advanced notification handling
- Further improvements to the blog editor
- Production deployment with a suitable database
- Additional performance and security improvements

## Project Status

**Status: Completed learning and portfolio project.**

The core blogging features and additional tools have been implemented. The project can be further improved as I continue learning Python and Django.

## Author

**Nitin**

Built as part of my learning journey in Python and Django web development.

## License

This project was created primarily for learning and portfolio purposes. No specific open-source license is granted unless a license file is added to the repository.
