# My Python Backend Project

This project is a backend application built with Python that utilizes the Gemini API, YouTube API, and OpenAI API. It serves as a foundation for a web application that fetches and displays data from these APIs on the frontend.

## Project Structure

```
my-python-backend
├── src
│   ├── app.py                     # Entry point of the application
│   ├── controllers
│   │   ├── gemini_controller.py   # Handles requests related to the Gemini API
│   │   ├── youtube_controller.py   # Handles requests related to the YouTube API
│   │   └── openai_controller.py    # Handles requests related to the OpenAI API
│   ├── services
│   │   ├── gemini_service.py       # Logic for interacting with the Gemini API
│   │   ├── youtube_service.py       # Logic for interacting with the YouTube API
│   │   └── openai_service.py        # Logic for interacting with the OpenAI API
│   ├── templates
│   │   └── index.html              # Main HTML template for the frontend
│   └── static
│       ├── css
│       │   └── styles.css          # CSS styles for the frontend
│       └── js
│           └── scripts.js          # JavaScript code for the frontend
├── requirements.txt                # Lists project dependencies
└── README.md                       # Documentation for the project
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd my-python-backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python src/app.py
   ```

## Usage

- Access the application in your web browser at `http://localhost:5000`.
- Use the frontend interface to interact with the APIs and view results.

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes. 

## License

This project is licensed under the MIT License.