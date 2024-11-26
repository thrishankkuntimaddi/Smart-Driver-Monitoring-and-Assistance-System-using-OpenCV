# Smart Driver Monitoring and Assistance System using OpenCV 🚘

This repository contains a Python-based **Smart Driver Monitoring and Assistance System** that leverages computer vision to enhance road safety. Using technologies like **OpenCV**, **dlib**, and **Twilio**, the system monitors the driver in real-time to detect signs of:

- **Drowsiness**
- **Closed eyes**
- **Inattention**

It provides visual alerts on-screen and can optionally send **SMS notifications** for immediate intervention, ensuring a safer driving experience.

---

## 🔧 Features

- **Real-Time Facial Monitoring**: Tracks facial landmarks to identify drowsiness and signs of inattention.
- **Customizable Alerts**: Configure thresholds for detection sensitivity.
- **Twilio Integration**: Sends SMS alerts to a predefined number for prompt action.
- **Open-Source**: Adapt and enhance the project for your use case.

---

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/thrishankkuntimaddi/Smart-Driver-Monitoring-and-Assistance-System-using-OpenCV.git
   cd Smart-Driver-Monitoring-and-Assistance-System-using-OpenCV
   ```

2. **Install dependencies**:
   Make sure you have Python installed. Then, install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Twilio**:
   - Update the Twilio credentials in `main.py` to enable SMS notifications.

4. **Run the script**:
   ```bash
   python main.py
   ```

---

## ⚙️ Configuration

- **Detection Thresholds**: You can adjust the detection thresholds in `main.py` to make the system more or less sensitive to signs of drowsiness or inattention.
- **Twilio Credentials**: To enable SMS alerts, you will need to provide your Twilio Account SID, Auth Token, and phone numbers in the script.

---

## 📂 Project Structure

- `main.py` - The main script for running the driver monitoring system.
- `requirements.txt` - Contains the list of dependencies required to run the project.
- `utils/` - Contains helper functions for facial landmark detection and alert mechanisms.

---

## 📈 Future Enhancements

- **Voice Alerts**: Add voice alerts to warn the driver without requiring them to look at the screen.
- **Driver Statistics**: Collect and analyze driver behavior data to improve the detection accuracy.
- **Extended Platform Support**: Expand the system to run on mobile devices or embedded systems for better usability.

---

## 🤝 Contributing

This project is open for contributions! Feel free to fork the repository, make changes, and submit a pull request. Suggestions and enhancements are always welcome.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## 📞 Contact

For any questions or support, feel free to reach out to [Thrishank Kuntimaddi](https://github.com/thrishankkuntimaddi).
