# 🎬 Movie Listing API with FastAPI

## Project Overview

The goal of this capstone project is to develop a **Movie Listing API** using **FastAPI**. This API will enable users to list movies, view listed movies, rate them, and add comments. The application is secured using **JWT (JSON Web Tokens)**, ensuring that only the user who listed a movie can edit it. The project will be deployed on a cloud platform.

## Features

### 🔑 User Authentication
- **User Registration**
- **User Login**
- **JWT Token Generation**

### 🎥 Movie Listing
- **View a Movie** (public access)
- **Add a Movie** (authenticated access)
- **View All Movies** (public access)
- **Edit a Movie** (only by the user who listed it)
- **Delete a Movie** (only by the user who listed it)

### ⭐ Movie Rating
- **Rate a Movie** (authenticated access)
- **Get Ratings for a Movie** (public access)

### 💬 Comments
- **Add a Comment to a Movie** (authenticated access)
- **View Comments for a Movie** (public access)
- **Add a Nested Comment to Another Comment** (authenticated access)

## Technical Requirements

### Language & Framework
- **Python** with **FastAPI**

### Authentication
- **JWT** (JSON Web Tokens) for securing endpoints

### Database
- Any **SQL** or **NoSQL** database

### Testing
- Include **unit tests** for the API endpoints

### Documentation
- **API documentation** using **OpenAPI/Swagger**

### Logging
- Log important details of the application

### Deployment
- Deploy the application on a **cloud server** of your choice

## Setup & Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/iamukn/movie-listing-api.git
   cd movie-listing-api
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   Add the SECRET_KEY environment variable 

5. **Run the database migrations (if you use any production level database):**
    - This project used Sqlite3, so migration isn't needed


6. **Start the FastAPI server:**

   ```bash
   python3 app.py
   ```

7. **Access the API documentation:**

   - Swagger UI: `http://127.0.0.1:8000/docs`

## Deployment

Deploy the application to a cloud platform such as **Heroku**, **AWS**, **Azure**, or **Google Cloud**. Ensure that the environment variables are properly configured on the server.

## Testing

Run the unit tests using **pytest**:

```bash
pytest
```

## Contributing

Feel free to fork this project, create a new branch, and submit a pull request with your improvements. All contributions are welcome!
