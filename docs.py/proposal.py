'''
Capstone Proposal: Global Education Access Dashboard

Project Overview
The Global Education Access Dashboard is a full-stack web application designed to analyze and visualize education disparities. The UNESCO education statistics sources from Kaggle, sets the foundation of the project as it provides meaningful insights on literacy rates, school enrollment, gender parity, and government spending. Our chosen datasets help users understand where educational inequality is prevalent and why. The target users for our development include policy makers, non-profit organizations, researchers and educators who are interested in development.

Social Impact
Access to quality education is necessary to reduce poverty and inequalities. Though global progress is shown, there are still millions of children who are not in school, and gender gaps still exist across many regions in education. THis dashboard aims to make complex education data accessible and interpretable. To make the data more easy to understand, enforces the decision makers to enforce policy with clear, visual evidence to advocate for change.

Dataset Selection
The dataset weve chosen is the Global Education dataset published on Kaggle by imtkaggleteam, and is originally sourced from the UNESCO Institute for Statistics (UIS). It contains country-level data including primary and secondary enrollment rates, literacy rates by gender, out-of-school children, and education expenditure. This dataset was chosen because of its depth, credibility, and relevance to social impact. Its global representation enables meaningful comparisons through countries and regions.

Technical Architecture
Our application is built using Backend - FastAPI, Database - SQLite for structured data storage, Cloud Storage- Google Cloud Storage for raw data and backups, Frontend - Streamlit for interactive data visualization and user interaction, CI/CD - Github Actions

Dashboard Design
The dashboard will feature interactive visualizations that can range from a choropleth world map that displays literacy rates or enrollment rations by country. A bar chart comparing gender parity across regions. A time series line chart tracking enrollment trends over time for selected countries. We intend for users to be able to filter fields like country, region, and year enabling personal exploration of the data.

Data Management Plan
Raw CSV files will be held in Google CLoud Storage, cleaned and readable using Python, and stored in SQLite. The FastAPI backend will give the processed data to the Streamlit frontend. Data will be refreshed manually at project milestones.

Ethical Considerations
All data being used is available publicly and redacted at the country level. We will clearly acknowledge and label data limitations such as missing values, avoid misleading scales, and ensure that all data and insights are framed constructively rather than tarnishing specific regions or nations.

Team Roles
Ethan White leads backend development: FastAPI, SQLite, Google Cloud Storage, and testing.
Ariana Ryals leads frontend development: Streamlit dashboard, visualizations, and CI/CD.
Both members collaborate on architecture design, endpoint planning, and documentation.

Project Objectives
Develop a Streamlit dashboard with at least three interactive charts visualizing global education indicators.
Build a FastAPI backend with a minimum of three functional REST API endpoints connected to an SQLite database.
Store and retrieve raw datasets using Google Cloud Storage with a documented ingestion pipeline.
Deploy an automated CI/CD pipeline using GitHub Actions.
Deliver actionable insights on education access disparities across at least five world regions.
'''
