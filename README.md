Here are the exact steps to run the application, including both the **Backend** and **Frontend** processes:

---

##  Running the Application

### 1. Backend Setup

* **Create Virtual Environment**: Run `py -m venv venv` to create a dedicated environment for dependencies.
* **Activate Environment**: Run `venv\Scripts\activate` to start the virtual environment.
* **Seed Database**: Run `python -m app.scripts.seed` to populate your database with initial data.
* **Start Server**: Run `uvicorn app.main:app --port 8001` to launch the backend on port **8001**.

### 2. Frontend Setup

* **Install Dependencies**: Run `npm install` to download all necessary libraries like `lucide-react`.
* **Start Application**: Run `npm run dev` to launch the development server.
* **View App**: Open `http://localhost:5174` (or the port shown in your terminal) in your browser.

