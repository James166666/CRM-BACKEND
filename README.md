# Personal CRM - MyCircle

Welcome to MyCircle, a user-friendly Personal CRM built with Django and React.js. With MyCircle, you can manage your contacts, track interactions, and never miss a follow-up.

## Features

- **Contact Management**: Seamlessly add, edit, and delete contacts.
- **Interaction Tracking**: Keep a log of all your interactions - meetings, calls, emails, and more.
- **Calendar Integration**: Set remindar for follow-ups or important dates on your own calendar。
- **Task Management**: Use the Trello-like board to manage notes and prioritize tasks.
- **Responsive UI**: Enjoy a modern and responsive interface built with React.js.

## Prerequisites

Ensure you have the following installed on your local machine:

- Python (3.8 or newer)
- Node.js (14.0 or newer)
- npm

## Setup & Installation

### Frontend (Javascript)

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/ITProject-Thu-12pm/CRM-Web.git
   ```

2. Navigate to the frontend directory:
   ```bash
   cd CRM-Web
   ```

3. Install the required packages:
   ```bash
   npm install
   ```

4. Start the React development server:
   ```bash
   npm start
   ```
   Open http://localhost:3000 to view it in your browser.

### Backend (Django) - Need Python version less than 3.9

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/ITProject-Thu-12pm/CRM-BACKEND.git
   ```

2. Navigate to the backend directory:
   ```bash
   cd CRM-BACKEND
   ```

3. Create a virtual environment:
   ```bash
   python -m venv env
   ```
   Note: Use `python3` instead of `python` if your default Python version is Python 2.x.

4. Activate the virtual environment:
   - On Windows: `env\Scripts\activate`
   - On macOS and Linux: `source env/bin/activate`

5. Install the required packages:
   - On macOS and Linux:
   ```bash
   pip install -r requirements.txt
   ```
   - On Windows:
   ```
   python -m pip install -r requirements.txt
   ```
   Note: Use `pip3` instead of `pip` if you are using Python 3 and have both Python 2 and Python 3 installed.

6. Navigate to the directory where manage.py is located:
   ```bash
   cd crm
   ```

7. Run migrations:
   ```bash
   python manage.py migrate
   ```
   Note: Use `python3` instead of `python` if your default Python version is Python 2.x.

8. Start the Django server:
   ```bash
   python manage.py runserver
   ```
   Note: Use `python3` instead of `python` if your default Python version is Python 2.x.

## Usage

1. Open and running two terminal at the same time, one for back-end server and one for front-end.
2. For back-end terminal `python manage.py runserver`, for front-end terminal `npm start`.
3. Open your browser and navigate to `http://localhost:3000` to access the frontend.
4. The backend API can be accessed at `http://localhost:8000`.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

