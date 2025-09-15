<p align="center">
  <img src="https://skillicons.dev/icons?i=python,opencv,tk" alt="logo python opencv tk" width="25%">
  <br><br>
  <i>Camera Classifier with live video feed,<br>
  custom Tkinter GUI, and CNN model trained on user images.</i>
</p>

---

# 📖 Index

* 📌 [Overview](#-overview)
* 📥 [Download & Installation](#-download--installation)
* 📷 [Usage Examples](#-usage-examples)
* 📄 [License](#-license)

---

# 📌 Overview

**Camera Classifier** is a **Python application** that allows users to capture images from a live camera, label them, train a **Convolutional Neural Network (CNN)** model, and predict classes in real-time.

The project combines a **CustomTkinter GUI**, **OpenCV camera handling**, and a **CNN built with TensorFlow/Keras**, providing a complete interactive experience for image classification.

Key features:

* **Custom class setup**: The user chooses the number of classes (2–10) and assigns their names.
* **Image collection**: Captured images are automatically stored in **numbered folders** (e.g., `1`, `2`, `3`, …) corresponding to the classes.
* **CNN training**: Images are preprocessed and augmented. Since this is a CNN, training may take some time if many images are collected. During training, the **video feed will freeze**: this is normal and helps optimize performance.
* **Real-time prediction**: The model can predict classes from the live camera feed using either the **Prediction** or **Auto Prediction** modes. These functions are quite sensitive, so accurate results require a large and balanced image set. For best performance, try to maintain consistent lighting, environment, and camera distance.
* **Reset functionality**: Clears the model and deletes all saved images, but keeps the empty class folders. These can be removed manually if not needed.

This tool is ideal for small-scale image classification experiments, live demonstrations, and learning CNN fundamentals.

---

# 📥 Download & Installation

**⚠️ Python 3.x is required on the machine to run this project.**

1. Download the latest **CameraClassifier** folder (includes all files and the batch file).
2. Make sure **Python 3.x** is installed and added to your system PATH.
3. Open the folder and double-click `run_camera_classifier.bat` to start the application.
   On first run, the batch file will automatically install all required Python packages (from `requirements.txt`).

---

# 📷 Usage Examples

* The program prompts for class number and names.
<br>![App Screenshot](img/setup.png)<br>
<br>![App Screenshot](img/class.png)<br>
* Captured images are stored in numbered folders (e.g., `1`, `2`, …) that match the chosen classes.
* Train the CNN model with the collected images. **Note:** while training, the application will temporarily freeze and the live image will stop updating until training is completed.
* Use the **"Predict"** or **"Auto Prediction"** buttons to classify the live camera feed.
* The **"Reset"** button deletes all collected images but leaves the folders intact (they can be removed manually if desired).
* The status bar and labels display prediction results in real-time.


---

# 📄 License

Released under the MIT License.
Feel free to use, modify, and share 🚀
