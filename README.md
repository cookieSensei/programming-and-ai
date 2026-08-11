# AI Lab Docker Environment

This repository provides a **GPU-enabled Docker environment** containing multiple isolated Python environments for different AI workflows.

The container is based on **CUDA 12.1 + Ubuntu 22.04** and includes environments for:

* TensorFlow research
* PyTorch deep learning
* Data science workflows
* Resume OCR + ATS scoring with Transformers

---

# Environments Overview

The container contains **four virtual environments** located in:

```
/opt/envs/
```

| Environment   | Path              | Purpose                               |
| ------------- | ----------------- | ------------------------------------- |
| TensorFlow    | `/opt/envs/tf`    | TensorFlow experiments and research   |
| PyTorch       | `/opt/envs/torch` | Deep learning, computer vision, YOLO  |
| Data Science  | `/opt/envs/ds`    | Classical ML and analytics            |
| ATS Resume AI | `/opt/envs/ats`   | OCR, NLP, resume parsing, ATS scoring |

---

---

# Activating Python Environments

Each environment can be activated manually using `source`.

---

## TensorFlow Environment

Activate:

```bash
source /opt/envs/tf/bin/activate
```

Verify:

```bash
python -c "import tensorflow as tf; print(tf.__version__)"
```

Deactivate:

```bash
deactivate
```

---

## PyTorch Environment

Activate:

```bash
source /opt/envs/torch/bin/activate
```

Verify GPU:

```bash
python -c "import torch; print(torch.cuda.is_available())"
```

Deactivate:

```bash
deactivate
```

---

## Data Science Environment

Activate:

```bash
source /opt/envs/ds/bin/activate
```

Test:

```bash
python -c "import pandas, sklearn, xgboost"
```

Deactivate:

```bash
deactivate
```

---

## ATS Resume AI Environment

This environment is designed for:

* Resume OCR
* EasyOCR
* Transformers
* Sentence embeddings
* ATS scoring

Activate:

```bash
source /opt/envs/ats/bin/activate
```

Test OCR:

```bash
python -c "import easyocr; print('EasyOCR ready')"
```

Deactivate:

```bash
deactivate
```

---

# Running Python Without Activating

You can also directly call Python from an environment:

```bash
/opt/envs/torch/bin/python script.py
```

Example:

```bash
/opt/envs/ats/bin/python resume_parser.py
```

---

# Available Jupyter Kernels

If using JupyterLab inside the container, the following kernels are available:

* **Python (TensorFlow)**
* **Python (PyTorch)**
* **Python (Data Science)**
* **Python (ATS Resume AI)**

Start JupyterLab:

```bash
/opt/envs/ds/bin/jupyter lab --ip=0.0.0.0 --port=8888 --allow-root
```

---

# Workspace Directory

The container uses:

```
/workspace
```

as the main working directory.

Any files in your host project directory will appear here inside the container.

---

# GPU Support

The container supports CUDA-enabled GPUs.

Verify inside the container:

```bash
nvidia-smi
```

or:

```bash
python -c "import torch; print(torch.cuda.is_available())"
```

---

# Included Technologies

The container includes support for:

* TensorFlow
* PyTorch
* HuggingFace Transformers
* Sentence Transformers
* EasyOCR
* Tesseract OCR
* OpenCV
* YOLOv8
* Streamlit / Gradio / FastAPI
* Pandas / Scikit-learn / XGBoost
* JupyterLab

---





## 🌐 Running Streamlit Apps

The container supports running **Streamlit applications** for building interactive ML demos.

---

### ▶️ Run a Streamlit App

Activate the desired environment (example: Data Science):

```bash
source /opt/envs/ds/bin/activate
```

Run the app:

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

If the above command gives error on file uploads, give extra permissions using the following command:

```
streamlit run app.py \
    --server.address 0.0.0.0 \
    --server.port 8501 \
    --server.enableXsrfProtection false \
    --server.enableCORS false
```

---

### 🌍 Access the App

- **Local:**
  ```
  http://localhost:8501
  ```

- **Remote (Coder / VM / Cloud):**
  - Forward port **8501**
  - Open the forwarded URL

---

### ⚠️ Notes

- `0.0.0.0` is required for Docker/remote environments  
- Default port is **8501**  
- Change port if needed:

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8080
```



------------------------------------------------------------------------

# 🧠 Creating Your Langchain Virtual Environment 

Students can create their own LangChain/GenAI environment.

## 🚀 Setup

    bash setup.sh
    source .venv/bin/activate

## 🧪 Verify

    python -c "import langchain; print('LangChain ready')"

## 📓 Jupyter

Select:

    Python (langchain-env)

## 🧹 Reset Environment

    rm -rf .venv
    bash setup.sh

------------------------------------------------------------------------

# 📁 Workflow

    git clone <repo>
    cd project
    bash setup.sh
    source .venv/bin/activate
    python app.py

------------------------------------------------------------------------

# Workspace Directory

    /workspace

------------------------------------------------------------------------

# GPU Support

    nvidia-smi

---



---

# 🧠 Creating Your Own Virtual Environment (Recommended for Students)

Students should create their own environment for projects (especially GenAI / LangChain).

---

## 🚀 Step-by-Step Setup

### 1. Go to your project folder

```bash
cd my-project
```

---

### 2. Create virtual environment

```bash
python3 -m venv .venv
```

---

### 3. Activate it

```bash
source .venv/bin/activate
```

---

### 4. Install dependencies

#### Option A (Recommended)

```bash
pip install -r requirements.txt
```

#### Option B (Manual install)

```bash
pip install langchain openai chromadb streamlit python-dotenv
```

---

### 5. Verify setup

```bash
python -c "import langchain; print('LangChain ready')"
```

---

### 6. Deactivate

```bash
deactivate
```

---

# ⚡ One-Command Setup (Easiest)

If provided, run:

```bash
bash setup.sh
source .venv/bin/activate
```

---

# 🔁 Reset Environment (If Something Breaks)

```bash
rm -rf .venv
bash setup.sh
```

---

# 📓 Jupyter Notebook Support

After setup:

```bash
python -m ipykernel install --user --name=langchain-env
```

Then select kernel:

```
Python (langchain-env)
```

---

# 💻 VS Code / Coder Users

1. Open Command Palette (`Ctrl + Shift + P`)
2. Select:

   ```
   Python: Select Interpreter
   ```
3. Choose:

   ```
   .venv/bin/python
   ```

---



---

# 🎯 Best Practices

### ✅ Do

* Create `.venv` per project
* Use `requirements.txt`
* Activate environment before running code

### ❌ Don’t

* Don’t install packages globally
* Don’t reuse environments across projects

---

# 🚀 Example Workflow

```bash
git clone <your-repo>
cd project

bash setup.sh
source .venv/bin/activate

python app.py
```

---

# 📜 License

MIT License


