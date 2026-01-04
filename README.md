# Umbral (Alpha Prototype)
### Real-time Behavioral Risk Detection for Subway Safety via Edge AI

> **Status:** Proof of Concept (PoC)
> **Context:** Developed during [Hackathon 2025,Universidad Alberto Hurtado] (10h Sprint)

## 📋 Project Overview
Umbral is a specialized AI system designed to detect **pre-suicidal behaviors** and **high-risk anomalies** in subway stations. Unlike traditional surveillance that waits for an incident, Umbral uses computer vision and behavioral inference to alert security personnel *before* the yellow line is crossed.

## 🛠️ Tech Stack & Architecture
This prototype was built to run on limited hardware (Edge context) to simulate real-world constraints:

* **Core Logic:** Python
* **Vision/Inference:** [cv2,mediapipe,pyttsx3,Tensorflow.js,time,sys] + Fine-tuned Llama 3.2 (Edge version)
* **Dataset:** Custom dataset of erratic body language (pacing, tunnel gazing, isolation).
* **Alert System:** Text-to-Speech (TTS) generation for immediate radio alerts to security guards.

## ⚙️ How it Works
1.  **Input:** Ingests video feed simulating CCTV.
2.  **Processing:** Extracts pose estimation and analyzes temporal movement patterns.
3.  **Inference:** The LLM evaluates the scene context against risk markers.
4.  **Action:** Generates a descriptive audio alert (e.g., *"Warning: Platform 2, subject showing erratic pacing for 2 minutes"*).

## 🚀 Future Roadmap (Why OpenAI Grove?)
The current PoC proves the concept but faces latency challenges in complex crowds. The next iteration aims to integrate **GPT-4o Vision** capabilities to improve reasoning accuracy and reduce false positives in high-density environments.

---

*Disclaimer: This code was created during a hackathon sprint. It serves as a demonstration of technical viability, not a production-ready product.*

graph TD
    %% Definitions of styles
    classDef input fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef edge Process fill:#fff3e0,stroke:#e65100,stroke-width:2px,stroke-dasharray: 5 5;
    classDef aiModel fill:#d1c4e9,stroke:#512da8,stroke-width:2px;
    classDef decision fill:#ffe0b2,stroke:#f57c00,stroke-width:2px,shape:rhombus;
    classDef action fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px;

    %% Main Flow
    subgraph Station Environment [Subway Station Environment]
        A[CCTV Camera Source]:::input
    end

    subgraph Edge Compute Unit [Edge AI Compute Unit / Local Server]
        B[Video Ingestion & Preprocessing<br/>Frame Sampling/Resizing] --> C[Computer Vision Analysis<br/>Pose Estimation/Object Tracking]
        C --> D[Behavioral Inference Engine<br/>Fine-tuned Llama 3.2 Model]:::aiModel
        D --> E{Risk Threshold Check<br/>Is score > critical?}:::decision
    end

    subgraph Response System [Security Response System]
        F[Generate Dynamic Alert Script<br/>Natural Language Text] --> G[Text-to-Speech conversion<br/>TTS Audio generation]
        G --> H[Transmit to Security Radio/Dispatch<br/>Audio Alert Output]:::action
    end

    %% Connections
    A --> B
    E -- Yes / High Risk --> F
    E -- No / Normal Behavior --> B

    %% Styling loops for continuous monitoring
    style B stroke-dasharray: 0
    style C stroke-dasharray: 0
