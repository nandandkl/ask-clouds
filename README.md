#🌤️ Ask Clouds
Ask Clouds is a sleek and interactive weather web app built with Django. It fetches real-time weather data and displays temperature, humidity, and forecast trends with modern visual elements. Users can search for any city and get beautifully presented climate insights, powered by OpenWeatherMap.

##🌐 Live Demo:
🔗 You can experience the ask-clouds web app by opening link (https://ask-clouds.onrender.com/) in your browser.

##✨ Features
1. Location Search: Users can enter any city to retrieve weather data.
2. Real-time Weather Info: Current temperature, humidity, wind speed, and more.
3. Dynamic Backgrounds: Weather-based UI updates for a more immersive experience.
4. 5-Hour Forecast Visualization: Smooth SVG temperature and humidity charts.
5. Error Handling: Friendly UI feedback for invalid or not-found cities.
6. Responsive Design: Works seamlessly across desktops, tablets, and mobile devices.

##🛠️ Technologies Used
Frontend: HTML, CSS (Glassmorphism & Animations), Bootstrap Icons, JavaScript (modular)
Backend: Python, Django
Weather API: OpenWeatherMap API
Machine Learning: Numpy, Pandas, Scikit-Learn
Others: SVG, CSS Animations, Django Templating

##📦 Installation
Follow these steps to set up the project locally:

1. Clone the Repository

bash
Copy
Edit
git clone https://github.com/yourusername/ask-clouds.git
cd ask-clouds

2. Create & Activate Virtual Environment

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install Dependencies

bash
Copy
Edit
pip install -r requirements.txt

4. Run Migrations

bash
Copy
Edit
python manage.py migrate

5. Start the Server

bash
Copy
Edit
python manage.py runserver
Visit in Browser
Open http://localhost:8000 to see the app.

##🤝 Contributing
Contributions are welcome! To contribute:

- Fork the repository.
- Create a feature branch.
- Commit your changes and push to your fork.
- Submit a pull request.

##💬 Feedback
 Found a bug? Have a feature request?
 Open an issue
 Or reach out via GitHub
