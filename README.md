# 🛡️ NovaCare Fall Detection System

<div align="center">

![NovaCare](https://img.shields.io/badge/NovaCare-Fall%20Detection-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square)
![Flask](https://img.shields.io/badge/Flask-2.3.0-green?style=flat-square)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.0-38B2AC?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

**An intelligent IoT-based fall detection system designed to enhance safety for elderly individuals and people with physical disabilities.**

[Features](#-key-features) • [Architecture](#-iot-architecture) • [Installation](#-installation) • [Usage](#-usage) • [Team](#-development-team)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [IoT Architecture](#-iot-architecture)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [Dashboards](#-dashboards)
- [Development Team](#-development-team)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

**NovaCare** is a comprehensive fall detection system that leverages **Edge AI** and **Computer Vision** to provide real-time monitoring and automated emergency response for vulnerable individuals. The system integrates seamlessly with assistive robotics to bridge the gap between accident detection and assistance arrival.

### Project Objectives

- ✅ **Real-Time Monitoring**: Continuously analyze user posture using computer vision
- ✅ **Accurate Detection**: Detect fall events with **≥95% accuracy** using pose estimation models
- ✅ **Automated Response**: Initiate emergency alerts without user intervention
- ✅ **Instant Notification**: Dispatch alerts to caregivers with identity, location, and event details
- ✅ **Response Time**: Achieve **<2 seconds** end-to-end latency

---

## ✨ Key Features

### 🏥 **Multi-Dashboard Interface**

#### 1️⃣ Primary User Dashboard
- 🎤 Multimodal communication (Voice, Sign Language, Touch)
- 💊 Medication management and reminders
- 🤖 Autonomous follow mode
- 👁️ Visual assistance (Object identification, Text reading)

#### 2️⃣ Caregiver Dashboard
- 📹 Live video monitoring
- 📍 Real-time GPS location tracking
- 🔔 Instant fall detection alerts
- 📊 Activity and wellbeing metrics
- 🔋 Battery status monitoring

#### 3️⃣ Health Professional Dashboard
- 📈 24-hour vitals trends (Heart Rate, BP, SpO2)
- 📉 Weekly activity pattern analysis
- 💊 Medication adherence tracking
- 📝 Fall incident history
- 🩺 Clinical notes and health summaries

#### 4️⃣ Emergency Service Dashboard
- 🚨 Critical incident management
- 📍 GPS coordinates and access notes
- 🏥 Patient summary and allergies
- 🌡️ Environmental sensor data
- 🚑 Nearest EMS units and hospitals
- ⏱️ Real-time incident timer

---

## 🏗️ IoT Architecture

NovaCare follows the **4-Layer + Communication Protocol IoT Model** with **2 Management Pillars**:

### **Layer 1: IoT Devices Layer (Sensing)**
- 📷 HD RGB Camera for continuous video capture
- 🎥 Visual sensors mounted on assistive rover

### **Layer 2: IoT Gateway / Aggregation Layer**
- 🖥️ **Raspberry Pi 5** as edge gateway device
- 📡 Wi-Fi connectivity for cloud transmission
- 🔗 USB/CSI camera interface

### **Layer 3: Processing Engine / Event Processing Layer**

#### Edge Processing (On-Device)
- 🧠 AI Inference Engine: MediaPipe Pose / YOLOv8-Pose
- 📊 Real-time skeletal landmark extraction
- ⚡ Fall detection algorithm analyzing keypoint velocity

#### Cloud Event Processing
- 📨 Receives "Fall Detected" JSON payloads
- 🔔 Triggers notification microservices (SMS/Email/Push)
- 💾 Event logging and analytics

### **Layer 4: Application Layer (API & Dashboard)**
- 🌐 **Guardian Dashboard**: Web portal for caregivers
- 📱 RESTful APIs for mobile/web applications
- 🔐 Secure authentication and authorization

### **Communications Layer**
- 📡 **MQTT Protocol**: Lightweight real-time message transmission
- 🔒 Encrypted data channels
- ⚡ Low-latency alert propagation

### **Management Pillars**

#### 🔧 Pillar 1: Devices Manager
- ❤️ Health monitoring for cameras and edge devices
- 📦 OTA (Over-the-Air) firmware updates
- 🔍 Performance metrics tracking

#### 🔐 Pillar 2: Identity & Access Manager (IAM)
- 🔑 Authentication for dashboard access
- 🛡️ Device security with API keys and certificates
- 🔒 End-to-end encryption for video feeds
- 👥 Role-based access control (RBAC)

---

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask 2.3.0 (Python)
- **Architecture**: SOLID Principles, Clean Architecture
- **Patterns**: Dependency Injection, Abstract Base Classes (ABC)

### Frontend
- **HTML5** with Jinja2 templating
- **Tailwind CSS** for modern, responsive UI
- **Vanilla JavaScript (ES6+)** - Modular architecture (API/UI separation)
- **Chart.js** for data visualization

### AI/ML
- **MediaPipe Pose** for pose estimation
- **YOLOv8-Pose** for fall detection
- **Edge AI** on Raspberry Pi 5

### Communication
- **MQTT** for real-time alerts
- **RESTful APIs** for data exchange

### Design
- 🌑 Dark theme with glassmorphism effects
- 🎨 Smooth animations and transitions
- ♿ Accessibility-first design

---

## 📁 Project Structure

```
IoT-Fall-Detection/
│
├── app/
│   ├── __init__.py                 # Flask application factory
│   │
│   ├── blueprints/                 # Flask Blueprints (Routes)
│   │   ├── __init__.py
│   │   ├── primary_user.py         # Primary user routes
│   │   ├── caregiver.py            # Caregiver routes
│   │   ├── health_professional.py  # Health pro routes
│   │   └── emergency.py            # Emergency service routes
│   │
│   ├── services/                   # Business Logic Layer
│   │   ├── __init__.py
│   │   ├── communication_service.py
│   │   ├── health_service.py
│   │   ├── navigation_service.py
│   │   ├── caregiver_service.py
│   │   ├── health_professional_service.py
│   │   └── emergency_service.py
│   │
│   ├── interfaces/                 # Abstract Base Classes (DIP)
│   │   ├── __init__.py
│   │   ├── input_handler.py
│   │   ├── notification_system.py
│   │   ├── medical_knowledge_base.py
│   │   ├── vision_service.py
│   │   └── settings_service.py
│   │
│   ├── models/                     # Data Models
│   │   ├── __init__.py
│   │   └── enums.py                # Enumerations (InputMode, etc.)
│   │
│   ├── templates/                  # Jinja2 HTML Templates
│   │   ├── base.html               # Base template with navigation
│   │   ├── index.html              # Homepage
│   │   ├── primary_user/
│   │   │   └── dashboard.html
│   │   ├── caregiver/
│   │   │   └── dashboard.html
│   │   ├── health_professional/
│   │   │   └── dashboard.html
│   │   └── emergency/
│   │       └── dashboard.html
│   │
│   └── static/                     # Static Assets
│       └── js/                     # JavaScript (Modular)
│           ├── primary_user/
│           │   ├── api.js          # API calls
│           │   └── ui.js           # UI interactions
│           ├── caregiver/
│           │   ├── api.js
│           │   └── ui.js
│           ├── health_professional/
│           │   ├── api.js
│           │   └── ui.js
│           └── emergency/
│               ├── api.js
│               └── ui.js
│
├── config.py                       # Flask configuration
├── run.py                          # Application entry point
├── requirements.txt                # Python dependencies
├── start.bat                       # Windows startup script
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

---

## 🚀 Installation

### Prerequisites

- **Python 3.8+**
- **pip** (Python package manager)
- **Git**

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/IoT-Fall-Detection.git
cd IoT-Fall-Detection
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
python run.py
```

Or use the Windows batch script:

```bash
start.bat
```

The application will be available at: **http://127.0.0.1:5000**

---

## 📖 Usage

### 1. **Access the Homepage**
Navigate to `http://127.0.0.1:5000` to see the NovaCare landing page with:
- Project overview
- IoT architecture details
- Key features
- Development team credits

### 2. **Select a Dashboard**
Choose from four specialized dashboards:
- **Primary User** - For elderly users and individuals with disabilities
- **Caregiver** - For family members and guardians
- **Health Professional** - For doctors and medical staff
- **Emergency** - For first responders and dispatch

### 3. **Explore Features**
Each dashboard provides real-time data, interactive charts, and role-specific functionality.

---

## 📊 Dashboards

### 🧑 Primary User Dashboard
![Primary User](https://img.shields.io/badge/User-Primary-blue?style=flat-square)

- Communication hub with multimodal input (Voice, Sign Language, Touch)
- Medication schedule and reminders
- Autonomous follow mode toggle
- Visual assistance tools
- RAG-based medical query system

**Route**: `/primary-user/dashboard`

---

### 👨‍👩‍👧 Caregiver Dashboard
![Caregiver](https://img.shields.io/badge/User-Caregiver-purple?style=flat-square)

- Real-time activity monitoring
- GPS location tracking
- Battery status
- Wellbeing score
- Live fall detection alerts

**Route**: `/caregiver/dashboard`

---

### 🏥 Health Professional Dashboard
![Health Pro](https://img.shields.io/badge/User-Health%20Pro-green?style=flat-square)

- Current vital signs (HR, BP, SpO2, Temp, RR)
- 24-hour vitals trends (Chart.js)
- Weekly activity patterns
- Blood pressure trends
- Medication adherence tracking
- Fall incident history
- 7-day health summary

**Route**: `/health-professional/dashboard`

---

### 🚨 Emergency Service Dashboard
![Emergency](https://img.shields.io/badge/User-Emergency-red?style=flat-square)

- Critical incident details
- GPS coordinates and address
- Patient summary (age, allergies, medications)
- Immediate concerns
- Environmental sensor data
- Nearest EMS units
- Nearby hospitals with availability
- Response status updates
- Healthcare proxy contact

**Route**: `/emergency/dashboard`

---

## 👥 Development Team

| Name | Student ID | Program | Role |
|------|-----------|---------|------|
| **Basant Awad** | 22101405 | Computer Science | Developer |
| **Nadira El-Sirafy** | 22101377 | Computer Science | Developer |
| **Noureen Yasser** | 22101109 | AI Science | AI Specialist |
| **Muhammad Mustafa** | 22101336 | AI Science | AI Specialist |
| **Ramez Asaad** | 22100506 | AI Science | AI Specialist |

### 🏫 University Project - 2025

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 🙏 Acknowledgments

- **MediaPipe** by Google for pose estimation
- **Flask** framework for web development
- **Tailwind CSS** for modern UI design
- **Chart.js** for interactive data visualization
- **Raspberry Pi Foundation** for edge computing platform

---

## ⚡ Powered by Stitch

<div align="center">

**NovaCare Fall Detection System** • © 2025 • All Rights Reserved

*Enhancing safety through intelligent monitoring*

</div>

