# 📦 Warehouse Management System (WMS) MVP

## 🚀 Project Overview

This project is a **Minimum Viable Product (MVP)** for a Warehouse Management System. It processes sales data, maps SKUs to Master SKUs (MSKUs), stores data in a relational database, and provides a user-friendly web app with AI-powered querying and visualizations.

---

## 📚 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup Instructions](#setup-instructions)
- [Project Structure](#project-structure)
- [How to Use](#how-to-use)
- [AI Tools Used](#ai-tools-used)
- [Submission Info](#submission-info)

---

## ✅ Features

### Part 1: Data Cleaning & SKU Mapping
- Map various SKUs to unified MSKUs.
- Auto-detection of SKU formats and combo products.
- Flexible input formats for different marketplaces.
- Error handling and logging.

### Part 2: Relational Database & Dashboard
- Backend-compatible CSV relational database using **Baserow** or **Teable.io**.
- Organized storage of orders, products, and sales.
- Dashboard to view metrics.

### Part 3: Web App Integration
- **Streamlit** GUI for drag-and-drop sales data uploads.
- Cleans and visualizes sales data.
- Interactive charts and filtered views.

### Part 4: AI Over Data Layer
- Users can ask natural-language queries like:
  - "Show sales for April"
  - "Add profit column"
  - "Plot sales by SKU"
- Adds calculated fields dynamically.
- Generates charts using Altair.

---

## 🧰 Tech Stack

| Layer        | Tool/Lib                                |
|--------------|-----------------------------------------|
| Language     | Python                                  |
| GUI          | Streamlit                               |
| AI Layer     | Custom NLP parser for query processing  |
| Charts       | Altair                                  |
| DB (No-code) | [Baserow](https://baserow.io/) / Teable |
| Others       | Pandas, datetime, etc.                  |

---

## 🛠️ Setup Instructions

1. **Clone the Repository**
```bash
git clone https://github.com/nourhammami/ywms.git

