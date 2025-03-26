# Sentiment API

**ORCA Disruption Monitoring** is a web-based application designed to monitor and analyze global disruption events such as cyber-attacks, supply chain disruptions, natural disasters, and other business-critical incidents. It allows users to visualize trends, perform keyword analysis, and filter events by various criteria like time range, disruption type, and severity.

---

## 🚀 APIs

refer to `http://localhost:8000\docs`
---

## 🛠️ Technologies Used

### Backend
- **Python**
- **MongoDB** (Database)
- **Vader**: For calculating sentiment scores
- **GLiner**: For obtaining NER values based on labels = ["person", "nationality", "religious group", "political group", "facility", "organisation", "country", "city", "state"]

### Frontend
- **FastAPI**

---

## ⚙️ Installation and Setup

Follow these steps to set up the project on your local machine:

### Prerequisites
- **Docker** installed
- **MongoDB** instance running locally or in the cloud
---

### 1. Pull and run Docker Image

```bash
docker pull belindashh/api-disruption-sentiment:latest
docker run -p 8000:8000 belindashh/api-disruption-sentiment:latest
```

It should appear in your `http://localhost:8000`, the documentation can be found on `http://localhost:8000\docs`

---

### 2. Alternative

1. Clone git and go to Sentiment API directory:
   ```bash
   git clone https://github.com/artc-dsc/ORCA_Disruption-Monitoring.git
   cd "Sentiment API"
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a virtual env, recommend python 3.12

4. Run program:
   ```bash
   python main.py
   ```
   The program will run at `http://localhost:8000`.

---

### 3. Call APIs

<!-- 1. Navigate to the `frontend` folder:
   ```bash
   cd ../frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the frontend development server:
   ```bash
   npm start
   ```
   The frontend will run at `http://localhost:3000`. -->


## 🐞 Debugging and Logging

For debugging, add `console.log` statements in the following places:
- **Backend**: Inside MongoDB queries and API response blocks
- **Frontend**: Check responses using `console.log(response.data)` after API calls.

---

## 👨‍💻 Author

Developed by **[Belinda](https://github.com/belindashh)**.
