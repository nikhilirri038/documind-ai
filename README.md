# 📄 DocuMind AI — AI-Powered Personal Document Assistant

DocuMind AI is a Python-based web application that allows users to upload PDF documents, extract their text, and ask questions about the document using Google's Gemini AI.

Instead of manually searching through lengthy documents, users can interact with their PDF through a simple chat interface and receive easy-to-understand answers based on the document's content.

## ✨ Features

- **PDF Upload:** Upload PDF documents directly through the web interface.
- **Text Extraction:** Extract readable text from PDFs using PyMuPDF.
- **AI-Powered Question Answering:** Ask questions about uploaded documents using the Gemini API.
- **Interactive Chat:** Ask follow-up questions while maintaining conversation history.
- **Extracted Text Preview:** View extracted document text before asking questions.
- **Error Handling:** Display helpful messages when API requests fail or temporary service errors occur.
- **Retry Support:** Retry questions when Gemini encounters temporary availability or rate-limit errors.
- **Cloud Deployment:** Deploy the Streamlit application on an Amazon EC2 instance.
- **Environment Variable Configuration:** Keep API credentials outside the application source code.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application programming |
| Streamlit | Interactive web interface |
| PyMuPDF | PDF text extraction |
| Google Gemini API | AI-powered question answering |
| python-dotenv | Load environment variables during local development |
| Git and GitHub | Version control and source code management |
| Amazon EC2 | Cloud hosting and deployment |
| Ubuntu Linux | Server operating system |

## 🏗️ Architecture

```text
                  User
                   |
                   v
          Streamlit Web Interface
                   |
                   v
             Upload PDF
                   |
                   v
             PyMuPDF
          Extract PDF Text
                   |
                   v
          User Asks a Question
                   |
                   v
          Prepare AI Prompt
       + Conversation History
                   |
                   v
            Gemini API
                   |
                   v
          Generate an Answer
                   |
                   v
          Display in Chat UI
```

### Deployment Architecture

```text
User's Browser
      |
      | HTTP
      v
Amazon EC2 Instance
      |
      v
Ubuntu Linux
      |
      v
Python Virtual Environment
      |
      v
Streamlit Application
      |
      v
Google Gemini API
```

## 📂 Project Structure

```text
documind-ai/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .gitignore          # Files excluded from Git
├── .env                # API key configuration (not committed)
└── README.md           # Project documentation
```

## ⚙️ Prerequisites

Before running the project, install or prepare the following:

- Python 3.10 or later, compatible with the installed dependencies
- Git
- A Google Gemini API key
- An internet connection
- A Google AI Studio account with access to a supported Gemini model

For cloud deployment, an AWS account with permission to create and manage EC2 resources is also required.

## 🚀 Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/documind-ai.git
cd documind-ai
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a Virtual Environment

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux or Ubuntu:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

Create a `requirements.txt` file containing:

```text
streamlit
pymupdf
google-genai
python-dotenv
```

Install the packages:

```bash
pip install -r requirements.txt
```

### 4. Configure the Gemini API Key

Create a `.env` file in the project root:

```text
GEMINI_API_KEY=your_actual_gemini_api_key
```

Get an API key through [Google AI Studio](https://aistudio.google.com/).

**Security note:** Replace the example value with your actual key. Never commit `.env` to GitHub or share your API key publicly.

### 5. Run the Application

Start the Streamlit server:

```bash
streamlit run app.py
```

Open the local URL shown in the terminal, typically:

```text
http://localhost:8501
```

## ☁️ Deploying on Amazon EC2

The application can be hosted on an Ubuntu EC2 instance.

### Deployment Steps

1. Launch an Ubuntu EC2 instance.
2. Configure SSH access through the instance's security group.
3. Connect to the instance.
4. Install Git, Python, pip, and the Python virtual environment package.
5. Clone the GitHub repository.
6. Create and activate a virtual environment.
7. Install the dependencies using `pip install -r requirements.txt`.
8. Configure `GEMINI_API_KEY` securely on the instance.
9. Configure the EC2 security group to allow application traffic on port `8501`, restricted to trusted IP addresses during testing.
10. Start the application.

Example commands for Ubuntu:

```bash
sudo apt update
sudo apt install -y git python3-pip python3-venv

git clone https://github.com/YOUR_USERNAME/documind-ai.git
cd documind-ai

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

streamlit run app.py \
  --server.address 0.0.0.0 \
  --server.port 8501
```

Open the following address in your browser:

```text
http://YOUR_EC2_PUBLIC_IP:8501
```

Replace `YOUR_EC2_PUBLIC_IP` with the public IPv4 address of your instance.

For production use, configure HTTPS, restrict network access, and run Streamlit as a managed service rather than relying on an interactive terminal session.

## 💬 How to Use

1. Open DocuMind AI in your browser.
2. Upload a PDF document.
3. Wait for the application to extract readable text.
4. Expand the extracted-text section if you want to inspect the content.
5. Enter a question in the chat box.
6. Read the AI-generated answer.
7. Ask follow-up questions about the same document.
8. Clear the chat when you want to start a new conversation.

### Example Questions

- What is this document about?
- Explain the main concepts in simple English.
- What are the important points?
- Summarize the document.
- Explain a particular topic mentioned in the PDF.

The quality of the answers depends on the readability of the PDF, the amount of text included in the prompt, and the availability of the Gemini API.

## 🔐 Security and Privacy

- Keep API keys in environment variables rather than source code.
- Add `.env` and `.venv/` to `.gitignore`.
- Avoid uploading confidential or sensitive documents.
- Remember that extracted PDF text is sent to Google's Gemini API for answer generation.
- Restrict access to the EC2 instance using security groups.
- Use HTTPS and appropriate access controls before exposing the application publicly.

## ⚠️ Limitations

- Scanned PDFs may require OCR because ordinary text extraction might not recognize their content.
- The current application sends a limited portion of the extracted text to Gemini, so answers may miss information outside that portion.
- Gemini may temporarily return service availability errors or rate limits.
- API quotas and pricing depend on the model and Google account terms.
- EC2 hosting may incur AWS charges depending on instance usage, storage, and account eligibility.
- The application is designed as a lightweight document assistant; it does not guarantee that every generated answer is correct.

## 🔮 Future Improvements

- Add OCR support for scanned PDFs.
- Improve retrieval so relevant sections can be found in very large documents.
- Add support for multiple document formats.
- Implement document summarization and keyword extraction.
- Add user authentication and document access controls.
- Improve citation and page-number references in AI responses.
- Add automated tests and CI/CD using GitHub Actions.
- Configure HTTPS and a custom domain for cloud deployment.
- Explore a serverless backend using AWS Lambda and API Gateway.

## 🎯 Learning Outcomes

This project provides practical experience with:

- Building an interactive application using Python and Streamlit.
- Extracting text from PDF documents with PyMuPDF.
- Integrating an external generative AI API.
- Managing API credentials using environment variables.
- Maintaining code with Git and GitHub.
- Setting up a Python environment on Ubuntu Linux.
- Deploying and running a web application on Amazon EC2.
- Troubleshooting API errors and cloud application issues.

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Open a pull request describing your improvements.

## 📜 License

This project is available for educational and portfolio purposes. If you intend to distribute it publicly, consider adding an appropriate open-source license, such as the MIT License.

## 👨‍💻 Author

**Your Name**

GitHub: https://github.com/YOUR_USERNAME

LinkedIn: Add your LinkedIn profile URL here.

---

If you find this project useful, consider giving the repository a ⭐ on GitHub.
