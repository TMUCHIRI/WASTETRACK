# WasteTrack ♻️

WasteTrack is a professional, high-performance waste management and reporting platform. It bridges the gap between citizens, waste collectors, and city administrators through real-time tracking, AI-optimized routing, and a gamified rewards system.

## 🌟 Key Features

### 🤵 For Citizens
- **Smart Reporting:** Report waste with GPS location and photo evidence.
- **Urgency Levels:** Flag reports based on fullness or environmental risk.
- **Rewards System:** Earn points for accurate reporting and clean-up participation.
- **Tracking:** View the status of your reported bins in real-time.

### 🚛 For Collectors
- **Live Scheduling:** View assigned collection tasks and details.
- **Route Optimization:** Get AI-powered optimized paths to reduce fuel and time.
- **In-field Verification:** Submit proof of collection with photos and feedback.
- **Live Tracking:** Share location with dispatch while on duty.

### 🏛 For Administrators
- **Dashboard Analytics:** Comprehensive overview of total waste, weights, and types.
- **AI Clustering:** Automatically group reports into optimized collection batches.
- **Collector Management:** Assign tasks to specific teams or individual collectors.
- **Point Verification:** Review collector feedback and award/penalize citizen points based on reporting accuracy.
- **Regional Thresholds:** Dynamically adjust fullness thresholds for collection by region.

---

## 🏗 Tech Stack

- **Backend:** [Django](https://www.djangoproject.com/) / [Django REST Framework](https://www.django-rest-framework.org/)
- **Frontend:** [Angular 17+](https://angular.io/) / [Angular Material](https://material.angular.io/)
- **Database:** [PostgreSQL](https://www.postgresql.org/)
- **Auth:** JWT (JSON Web Tokens)
- **Maps Real-time:** [Google Maps API](https://developers.google.com/maps)
- **Messaging:** [AfricasTalking SMS API](https://africastalking.com/)

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+ & npm
- PostgreSQL

### 🔧 Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd BACKEND/waste_backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\\Scripts\\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure your `.env` file (Database, Secret Key, API Keys).
5. Run migrations:
   ```bash
   python manage.py migrate
   ```
6. Start the server:
   ```bash
   python manage.py runserver
   ```

### 🎨 Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd FRONTEND/waste-track-frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   ng serve
   ```
4. Open [http://localhost:4200](http://localhost:4200) in your browser.

---

## 📸 Screenshots
*(Screenshots coming soon...)*

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

---
Developed with ❤️ by the WasteTrack Team.
