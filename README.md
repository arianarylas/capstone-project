# capstone-project
Global Education Access Dashboard - A data driven web application anaylzing global education disparties, built with FastAPI, SQLite, and Streamlit.

Ariana Ryals, is the front developer she will focus on streamlit dashboard, data visualization, and CI/CD setup. Ethan White, is the backend developer he will focus on FastAPI endpoints, SQLite schema,  Google Cloud Storage and testing.

Phase 1 - (Current) Planning: Create proposal, diagrams 
Phase 2- Development: Backend API, database setup, frontend dashboard 
Phase 3- Finalization: Testing, deployment, documentation 

The dataset we have chose is the Global Education dataset from kaggle sources from UNESCO data.

# CI/CD & Deployment
This project implements a fully automated CI/CD pipeline using Github Actions and Google Cloud.
#Workflow:
- Every push to main triggers 'flake8' to ensure code quality in PEP8 compliance.
- Testing: Automated unit test are excuted via 'pytest'.
- A Dockerfile builds the application into a lightweight container
- The container is pushed to Artifact Registry and deployed to Google Cloud Run
#Setup Requirements:
- Secrets: The pipeline requires 'GCP_Credientals' stored in Github Secrets
- Enviornment: The backend is configured to run on port 8080 within the container.