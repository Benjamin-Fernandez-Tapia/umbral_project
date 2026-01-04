# Umbral (Alpha Prototype)
### Real-time Behavioral Risk Detection for Subway Safety via Edge AI

> **Status:** Proof of Concept (PoC)
> **Context:** Developed during [Hackathon 2025,Universidad Alberto Hurtado] (10h Sprint)

## 📋 Project Overview
Umbral is a specialized AI system designed to detect **pre-suicidal behaviors** and **high-risk anomalies** in subway stations. Unlike traditional surveillance that waits for an incident, Umbral uses computer vision and behavioral inference to alert security personnel *before* the yellow line is crossed.

## 🛠️ Tech Stack & Architecture
This prototype was built to run on limited hardware (Edge context) to simulate real-world constraints:

* **Core Logic:** Python
* **Vision/Inference:** [Menciona librería: ej. OpenCV / PyTorch] + Fine-tuned Llama 3.2 (Edge version)
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