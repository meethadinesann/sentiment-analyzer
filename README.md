# Product Sentiment Analyzer and Review Dashboard

A full-stack web application that scrapes product reviews from Flipkart, performs sentiment analysis using NLP, and displays interactive insights on a dashboard.

## Live Demo
- **Frontend:** https://sentiment-analyzer-frontend-xi.vercel.app
- **Backend:** https://sentiment-analyzer-asdz.onrender.com

## Features
- Real-time product review scraping from Flipkart using Selenium
- Sentiment classification (Positive/Negative/Neutral) using VADER NLP
- Interactive pie chart and bar chart visualization using Recharts
- Search history and pagination
- Auto-scraping when a new product is searched
- Data stored in MongoDB Atlas cloud database

## Tech Stack
| Layer | Technology |
|---|---|
| Frontend | React, Vite, Recharts, Axios |
| Backend | Flask, Python, Flask-CORS |
| Scraping | Selenium, WebDriver Manager |
| NLP | VADER (NLTK) |
| Database | MongoDB Atlas |
| Deployment | Vercel (frontend), Render + Docker (backend) |

## Project Structure
sentiment_analyzer/
├── scraper/          # Selenium scraper + data cleaning + sentiment analysis
├── backend/          # Flask REST API
├── frontend/         # React application
└── Dockerfile        # Docker configuration for Render deployment

## API Endpoints
| Endpoint | Method | Description |
|---|---|---|
| `/api/health` | GET | Check if API is running |
| `/api/products` | GET | List all scraped products |
| `/api/reviews` | GET | Get reviews for a product |
| `/api/sentiment` | GET | Get sentiment summary |
| `/api/scrape` | POST | Scrape a new product |

## Setup Instructions

### Scraper
```bash
cd scraper
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 scrape_reviews.py
```

### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 app.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Environment Variables
Create a `.env` file in the `backend/` folder:
MONGO_URI=your_mongodb_connection_string
FLASK_PORT=5000