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

The project combines **CustomTkinter GUI**, **OpenCV camera handling**, and a **CNN built with TensorFlow/Keras**, providing a full interactive experience for image classification.

Key features:

* **Custom class setup**: The user chooses the number of classes (2–10) and their names.
* **Image collection**: Captured images are saved inside automatically created **numbered folders** (e.g., `1`, `2`, `3`, …) corresponding to the classes.
* **CNN training**: Images are preprocessed and augmented. Since this is a CNN, training may take time if many images are collected. During training the **video feed freezes**: this is normal and avoids unnecessary slowdowns.
* **Real-time prediction**: Predicts class of live frames with optional automatic prediction mode. The **Auto Prediction** function is very sensitive, so better results require a large and balanced image set.
* **Reset functionality**: Clears the model and deletes all saved images, but keeps the empty class folders, which must be removed manually if not needed.

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
* Captured images are stored in numbered folders (e.g., `1`, `2`, …) that match the chosen classes.
* Train the CNN model with the collected images. **Note:** while training, the application will temporarily freeze and the live image will stop updating until training is completed.
* Use the **"Predict"** or **"Auto Prediction"** buttons to classify the live camera feed.

  * The **Auto Prediction** mode is very sensitive and requires a high number of well-distributed images for good performance.
* The **"Reset"** button deletes all collected images but leaves the folders intact (they can be removed manually if desired).
* The status bar and labels display prediction results in real-time.

**Example Prediction Output:**

* ⚫ *"IDLE"* → when the camera is active but no prediction.
* 🔴 *"TRAIN FIRST!"* → if prediction is attempted before training.
* 🟢 *Predicted class with confidence* → when the model is trained.

---

# 📄 License

Released under the MIT License.
Feel free to use, modify, and share 🚀

---
Ottimo, vedo che hai già messo insieme **Overview** e **Download & Installation + Usage** in un formato più compatto 👍.
Per renderlo ancora più chiaro e leggibile in stile README, ti propongo di sistemare leggermente la struttura: tenere la parte di **Download & Installation** solo per l’installazione, e spostare tutte le spiegazioni pratiche in **Usage Examples**, così non si ripetono cose e l’indice rimane coerente.

Ecco la versione riordinata:

---


