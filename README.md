# 🌸 HerHealth AI — Women's Health Companion

HerHealth AI is a React-based women's health education and wellness companion designed to provide accessible, easy-to-understand health information through a safety-first, Retrieval-Augmented Generation (RAG) approach.

> HerHealth AI is an educational wellness application. It does not diagnose diseases, prescribe medication, or replace qualified healthcare professionals.

---

## ✨ Features

### 🧠 RAG-Based Health Assistant

HerHealth AI uses a local women's health knowledge base and a relevance-based retrieval system to find information related to a user's question.

### 💬 Health Chat

Users can ask general women's health questions and receive educational responses based on the application's knowledge base.

### 🛡️ Safety-First Design

The application checks for potentially concerning symptoms before providing a normal educational response.

Examples include:

- Severe pain
- Heavy bleeding
- Fainting
- Chest pain
- Difficulty breathing

When concerning symptoms are detected, the application encourages the user to seek appropriate medical care.

### 📅 Menstrual Cycle Tracker

Users can enter:

- Last period date
- Cycle length

The application provides an estimated next period date.

### 📝 Daily Health Check-In

Users can record symptoms during their current session.

### 📊 Health Insights

The application can summarize session-based information such as:

- Number of check-ins
- Frequently reported symptoms
- Cycle tracking status

### 📖 Women's Health Education

The application provides educational topics covering areas such as:

- Menstrual cycle
- Period pain
- PMS
- Menstrual hygiene
- Healthy habits
- When to seek medical care
- Endometriosis awareness
- PCOS awareness

---

## 🧠 RAG Architecture

The project follows a simple local RAG pipeline:

```text
                 User Question
                       │
                       ▼
                 Safety Check
                       │
                       ▼
                RAG Retriever
                       │
                       ▼
          Women's Health Knowledge Base
                       │
                       ▼
              Relevant Documents
                       │
                       ▼
             Local Response Engine
                       │
                       ▼
                 Answer + Sources
```
---

## 📚 Knowledge Base

The health knowledge base is stored locally in:
```
data/healthKnowledge.js
```
Current educational topics include:

- Menstrual Cycle Basics
- Period Pain
- Premenstrual Syndrome
- Menstrual Hygiene
- Heavy Menstrual Bleeding
- Irregular or Infrequent Periods
- Healthy Habits and Wellbeing
- When to Seek Medical Care
- Endometriosis Awareness
- PCOS Awareness
- HerHealth AI Safety and Limitations

The project uses information from trusted health sources such as the World Health Organization for its educational knowledge base.

---

## 🔍 RAG Retriever

The retrieval system is located at:
```
src/rag/retriever.js
```
It performs relevance-based matching between:
```
User Question
      ↓
Keywords
      ↓
Knowledge Base Documents
      ↓
Relevance Score
      ↓
Top Relevant Documents
```

The retriever currently considers:

- Title matches
- Category matches
- Keyword matches
- Content matches
- Keyword phrase matches

---

## 🛡️ Responsible AI

Healthcare applications require careful handling of safety.

HerHealth AI follows these principles:

- Do not diagnose diseases.
- Do not claim certainty about a user's condition.
- Do not prescribe medication.
- Do not replace healthcare professionals.
- Do not manage emergencies.
- Prefer retrieved health information over unsupported claims.
- Direct users toward appropriate medical care when symptoms may require prompt attention.

The application is intended for general health education and wellness support.

---

## 🛠️ Tech Stack

- React
- Vite
- JavaScript
- HTML
- CSS
- Retrieval-Augmented Generation (RAG)
- GitHub

---

## 📁 Project Structure

```text
women-health-ai/
│
├── data/
│   └── healthKnowledge.js
│
├── public/
│
├── src/
│   ├── ai/
│   │   └── localAssistant.js
│   │
│   ├── rag/
│   │   └── retriever.js
│   │
│   ├── assets/
│   │
│   ├── App.jsx
│   ├── App.css
│   ├── index.css
│   └── main.jsx
│
├── .gitignore
├── index.html
├── package.json
├── package-lock.json
└── README.md
```
---

## 🚀 Getting Started

1. Clone the repository
```
git clone YOUR_GITHUB_REPOSITORY_URL
```
2. Open the project
```
cd women-health-ai
```
3. Install dependencies
```
npm install
```
4. Start the development server
```
npm run dev
```
5. Open the application

Open:
```
http://localhost:5173
```

---

## 🧪 Testing

Try questions such as:

- Why do I have period cramps?
- What is PMS?
- What is a normal menstrual cycle?
- How can I maintain menstrual hygiene?
- What is PCOS?

Safety testing can include:

- I have very heavy bleeding.
- I have severe pain and fainting.
- I have chest pain and difficulty breathing.

---

## 🔮 Future Improvements

Planned improvements include:

 - Improved semantic RAG retrieval
 - Better source citations
 - More comprehensive women's health knowledge
 - Multilingual support
 - Improved conversational responses
 - Browser-based open-source LLM
 - Voice interaction
 - Better accessibility
 - Improved mobile experience
 - Free static deployment
 - Automated testing

---

## 🔐 Privacy

- The current prototype uses session-based React state.
- Health information is not intentionally stored in a remote database.
- Users should avoid entering personally identifying or highly sensitive information into the prototype.

---

## ⚠️ Medical Disclaimer

HerHealth AI provides general educational information and wellness support.

It is not a medical device, doctor, diagnostic system, or emergency service.

The application cannot:

- Diagnose medical conditions
- Confirm diseases
- Prescribe medication
- Replace professional medical advice
- Manage emergencies

If someone experiences severe, sudden, rapidly worsening, or concerning symptoms, they should seek appropriate medical care.

---

## 🌱 Learning Goals

This project was created to explore practical applications of:

- Artificial Intelligence
- Retrieval-Augmented Generation
- Responsible AI
- Healthcare UX
- React development
- Frontend architecture
- Knowledge retrieval
- Safety-first AI design

---

## 👩‍💻 Author

Nikita Chougule

Built as a learning and portfolio project focused on AI, women's health technology, and responsible application development.

---

## ⭐ Support

If you find this project useful or interesting, consider giving the repository a ⭐ on GitHub.
Feedback and suggestions are welcome.
