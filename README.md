# Tech Enforcement System (Smart Ticketing)

An automated smart‑city enforcement solution developed for the System Analysis & Design Course Competition at Chung Yuan Christian University. This project streamlines violation record entry, ticket issuance, and real‑time dashboard synchronization.

## 🔍 Overview

- **Course Project**: System Analysis & Design Competition, Jan 2025  
- **Team**: 4 members (Roles: Technical Contributor & Developer)  
- **Tech Stack**:  
  - Backend: Python (Flask/Django)  
  - OCR: YOLO-based license‑plate recognition  
  - Database: PostgreSQL  
  - Containerization: Docker  
  - Geocoding: Google Maps API  
  - Dashboard Integration: REST API calls to the Taipei City Dashboard  

## 🚀 Features

1. **Violation Record Entry**  
   - Web form for manual entry by traffic authorities  
   - Auto-fill location via reverse geocoding  

2. **License‑Plate OCR & Automated Ticketing**  
   - YOLO‑based model trained to 95% recognition accuracy  
   - Text extraction & validation  
   - Automated PDF ticket generation  

3. **PDF Reporting**  
   - Styled ticket template (violation details, location map, timestamp)  
   - Downloadable and printable PDF output  

4. **Role‑Based Access Control**  
   - User roles: Administrator, Traffic Officer, Viewer  
   - Permissions managed via PostgreSQL  

5. **Real‑Time Dashboard Synchronization**  
   - Push new violation data to the [Taipei‑City‑Dashboard Public](https://github.com/raytan0715/Taipei-City-Dashboard) (forked from `taipei-doit/Taipei-City-Dashboard`)  
   - Data modules updated via Dockerized services  

## Demo & Walkthrough
**https://youtu.be/JF0WH6qmQgo**
