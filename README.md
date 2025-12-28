# YugmaCare: AI-Powered Emergency Response System

A complete Streamlit-based web application for immediate medical emergency guidance, hospital localization, and resource mobilization.

# Features

### 🚨 Emergency Triage
* **Instant Analysis:** Uses an NLP intent engine to analyze user input (e.g., "chest pain", "severe burns") and determine urgency.
* **First Aid Protocols:** Displays step-by-step, visual first aid cards to stabilize patients before help arrives.
* **Helpline Integration:** One-tap access to national emergency numbers (108, 112, 102).

### 📍 Hospital Localization
* **Geolocation Services:** Integrates Google Maps Embed API to find hospitals based on user input.
* **Dynamic Filtering:** Allows users to filter between "Government" and "Private" hospitals.
* **Real-Time Routing:** Provides visual direction and location data relative to the user's city.

### 🤝 Support & Resources
* **Government Schemes:** Instantly lists relevant health schemes (e.g., PM-JAY, Ayushman Bharat) for financial aid.
* **NGO Directory:** Connects users with verified NGOs for additional support.
* **Multilingual Support:** Full interface support for English, Hindi, and Marathi to ensure accessibility.

### 🛠️ Technical Highlights
* **Zero-Login Access:** Designed for emergencies where time is critical; no sign-up required.
* **Lightweight Architecture:** Optimized for fast loading even on low-bandwidth networks.
* **Privacy Focused:** No personal data retention after the session ends.

# Installation

### 1. Clone or download the project
git clone [https://github.com/your-username/yugmacare.git](https://github.com/your-username/yugmacare.git)
cd yugmacare

### 2. Install Python dependencies
pip install -r requirements.txt

### 3.Run the application
streamlit run app.py

# Usage

### 1. Launch the App
* **Run the command above.**
* **The app will open in your default browser at http://localhost:8501.**

### 2. Select Language
* **Use the sidebar to choose between English, Hindi, or Marathi.**

### 3. Describe Emergency
* **Type the emergency situation in the text box (e.g., "Snake bite", "Road accident").**
* **Click "Get Help".**

### 4. Follow Guidance
* **Immediate: Follow the on-screen First Aid steps.**
*  **Call: Use the one-tap buttons to call ambulances.**
*  **Navigate: View the map to find the nearest hospital.**

### 5. Access Resources
* **Scroll down to view applicable Government Schemes and NGO contacts for financial/medical support.**

# Project Structure
## Project Structure

**` 
yugmacare/
├── app.py                  # Main Streamlit application
├── logic/
│   └── intent_engine.py    # NLP logic for analyzing user input
├── data/
│   ├── emergency_data.json # First aid protocols and steps
│   ├── support_resources.json # NGO and Govt scheme database
│   └── emergency_texts.json # Multilingual UI text strings
├── static/
│   └── style.css           # Custom CSS for UI styling
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
`**

### Machine Learning & AI Features
* **Rule-Based NLP: Uses keyword mapping and fuzzy matching to detect emergency types from unstructured text.**
* **Intent Recognition: Classifies inputs into categories (e.g., cardiac, trauma, toxicity) to serve relevant data.**
*  **Location Intelligence: Google Maps integration for spatial queries and hospital filtering.**

### Data Sources
* **First Aid Data: Standard protocols sourced from medical guidelines.**
* **Hospital Data: Dynamically fetched via Google Maps.**
* **Schemes & NGOs: Verified list of national schemes and support organizations.**

# Troubleshooting

### Map not loading:
* **Ensure you have an internet connection, as the embedded map fetches data live from Google.**

### ModuleNotFoundError:
* **Run pip install -r requirements.txt again to ensure all libraries (streamlit, etc.) are installed.**

### Port already in use:
* **If port 8501 is taken, run:**
  streamlit run app.py --server.port 8502

# license
This project is provided as-is for educational and development purposes. It is a prototype and should not be used as a replacement for professional medical advice.
