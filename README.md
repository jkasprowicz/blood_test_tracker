# Blood Test Tracker

Overview
Blood Test Tracker is a comprehensive project designed to track, display, and provide feedback on blood test results. Leveraging the power of the OpenAI API, this application aims to enhance the user experience by offering insightful feedback and analysis of the test data.

Features
- **Track Blood Test Results:** Easily input and store blood test data.
- **Display Results:** View your test results in a clear and concise manner.
- **Feedback and Analysis:** Receive detailed feedback and insights on your blood test results, powered by the OpenAI API.
- **User-Friendly Interface:** An intuitive and easy-to-navigate interface built with Django, CSS, and JavaScript.

## Technology Stack
- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, JavaScript
- **API Integration:** OpenAI API
- **Database:** SQLite (default), with options for other databases
- **Styling:** Bootstrap, custom CSS
- **JavaScript Libraries:** jQuery, Chart.js (for data visualization)

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/blood_test_tracker.git
   cd blood_test_tracker
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the Database:**
   ```bash
   python manage.py migrate
   ```

5. **Run the Server:**
   ```bash
   python manage.py runserver
   ```

6. **Access the Application:**
   Open your browser and go to `http://127.0.0.1:8000`.

## Usage
1. **Log In / Sign Up:** Create an account or log in to your existing account.
2. **Enter Blood Test Results:** Navigate to the input form and enter your blood test data.
3. **View Results:** Check your blood test results on the dashboard.
4. **Get Feedback:** Click on the feedback button to receive detailed analysis and insights.

## Contribution
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
If you have any questions or suggestions, please feel free to contact me at [joao.kasprowicz@univali.br].

---

Thank you for checking out Blood Test Tracker! Your feedback and contributions are highly appreciated.
