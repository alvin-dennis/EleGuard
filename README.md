# 🛡️ Eleguard

Eleguard is an intelligent elephant detection and deterrent system powered by **computer vision** and **IoT**.  
It uses a Raspberry Pi with a camera module to detect elephants, trigger alerts, and activate deterrent mechanisms to protect farmlands and communities.

---

## 🛠️ Tech Stack

Languages: Python, Bash
Libraries: OpenCV, Picamera2, NumPy, Roboflow, Inference SDK, Twilio, PySerial, PyGame
Hardware: Raspberry Pi, Camera Module, GSM Module, GPS

## 🚀 Features

- Real-time elephant detection using computer vision (OpenCV + Roboflow inference).
- Emergency alerts via GSM (Twilio SMS support).
- Automatic deterrent activation (low-frequency sound emitter).
- GPS logging and image capture for event records.
- Lightweight deployment on Raspberry Pi.

---

## 📦 Installation

You can set up the project in **two ways**:  

1. Classic Python environment (`requirements.txt`)  

2. Modern [uv](https://github.com/astral-sh/uv) package manager (recommended)

### 1️⃣ Classic Environment (pip/venv)

1. Clone the repository:

    ```bash
    git clone https://github.com/alvin-dennis/DevMate.git
    ```

2. Create and activate a virtual environment:

    ```shell
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Rename `.env.example` file to `.env`
5. Fill the `.env` with your credentials

    ```json
    TWILIO_ACCOUNT_SID=your_account_sid
    TWILIO_AUTH_TOKEN=your_auth_token
    TWILIO_PHONE_NUMBER=+1234567890
    TARGET_PHONE_NUMBER=+1987654321

    ALERT_SOUND_FILE=

    ROBOFLOW_API_KEY=your_api_key
    ```

6. Run EleGuard :

    ```bash
    python3 app.py
    ```

## 2️⃣ UV Environment (faster installs)

1. Clone the repository:

    ```bash
    git clone https://github.com/alvin-dennis/DevMate.git
    ```

2. Install Dependencies:

    ```shell
    uv sync
    ```

3. Rename `.env.example` file to `.env`
4. Fill the `.env` with your credentials

    ```json
    TWILIO_ACCOUNT_SID=your_account_sid
    TWILIO_AUTH_TOKEN=your_auth_token
    TWILIO_PHONE_NUMBER=+1234567890
    TARGET_PHONE_NUMBER=+1987654321

    ALERT_SOUND_FILE=

    ROBOFLOW_API_KEY=your_api_key
    ```

5. Run EleGuard :

    ```bash
    uv run main.py
    ```

## ▶️ Usage

1. The camera continuously monitors for elephant presence.
2. If an elephant is detected: GSM alert is sent via Twilio & deterrent mechanism is triggered.
3. Logs and images are saved locally for review.

## 🤝 Contributing

Contributions are welcome! 🎉
If you’d like to improve Eleguard, please fork the repository and submit a pull request.

## 📜 License

This project is licensed under the [MIT License](https://github.com/alvin-dennis/EleGuard/blob/main/LICENSE)