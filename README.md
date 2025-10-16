# Multi-Agent Task Management System

A sophisticated multi-agent system built with Microsoft Semantic Kernel that handles task management, company information queries, and email notifications through intelligent agent orchestration.

## 🚀 Features

- **Intelligent Agent Routing**: TriageAgent automatically routes requests to specialized agents
- **Task Management**: Create, assign, list, and complete tasks with database persistence
- **Company Information**: Query company policies and HR guidelines using Azure Cognitive Search with vector search on uploaded documents
- **Email Notifications**: Automatic email notifications for task updates via Gmail SMTP
- **Chat History**: Persistent conversation history with session management
- **Hybrid Search**: Combines keyword, vector, and semantic search for accurate information retrieval

## 🏗️ Architecture

The system consists of four specialized agents:

1. **TriageAgent**: Routes incoming requests to appropriate specialized agents
2. **DBAgent**: Manages task creation, assignment, and completion with database operations
3. **InformativeAgent**: Provides company policies and HR information using Azure Cognitive Search with vector search on uploaded documents
4. **MCPAgent**: Handles email notifications for task-related updates

## 📋 Prerequisites

- Python 3.8 or higher
- Azure OpenAI Service
- Azure Cognitive Search Service
- Azure Blob Storage (for document storage)
- Gmail account with App Password
- Git (for cloning the repository)

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/MultiAgent-SemanticKernel-Python.git
cd MultiAgent-SemanticKernel-Python
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example configuration file and update it with your credentials:

```bash
cp config.env.example config.env
```

Edit `config.env` with your actual values:

```env
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=your_deployment_name
AZURE_OPENAI_CHAT_DEPLOYMENT=your_chat_deployment_name

# Azure Search Configuration
AZURE_SEARCH_ENDPOINT=https://your-search-service.search.windows.net
AZURE_SEARCH_INDEX=your_index_name
AZURE_SEARCH_API_KEY=your_search_api_key

# Email Configuration
SENDER_EMAIL=your-email@gmail.com
APP_PASSWORD=your_gmail_app_password
```

### 5. Set Up Gmail App Password

1. Enable 2-Factor Authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a new app password for "Mail"
   - Use this password in your `config.env` file

## 🚀 Usage

### 1. Start the MCP Server

In a separate terminal, start the email notification server:

```bash
python MCPServer.py
```

### 2. Run the Main Application

```bash
python main.py
```

### 3. Interact with the System

The system will start and you can interact with it through the command line:

```
Multi-Agent Task Management System
========================================
Enter your request (type 'exit' to quit):

User > Add a task for John to complete the quarterly report by Friday
```

## 📝 Example Interactions

### Task Management
```
User > Add a task for Sarah to review the budget proposal
User > List all pending tasks for Sarah
User > Mark task 1 as completed
```

### Company Information
```
User > What is our remote work policy?
User > How many vacation days do employees get?
User > What is the process for requesting time off?
User > What are the company's cybersecurity guidelines?
User > Tell me about our employee benefits package
```

### System Features
- **Automatic Routing**: The system automatically routes your requests to the appropriate agent
- **Email Notifications**: Task updates trigger automatic email notifications
- **Persistent Storage**: All tasks and conversations are stored in a SQLite database
- **Intelligent Search**: Company information queries use hybrid semantic search
- **Document Vector Search**: Upload any documents to Azure Blob Storage for intelligent querying
- **Multi-Format Support**: Works with PDFs, Word documents, and other text-based files

## 🗂️ Project Structure

```
MultiAgent-SemanticKernel-Python/
├── main.py                 # Main application entry point
├── orchestrator.py         # Agent orchestration and handoff logic
├── db.py                   # Database operations and chat history
├── MCPServer.py           # Email notification MCP server
├── config.env              # Environment configuration
├── requirements.txt        # Python dependencies
├── Agents/
│   └── agent_set.py        # Agent definitions and configuration
└── plugins/
    ├── DBAgentPlugin.py    # Database operations plugin
    ├── InformativeAgentPlugin.py  # Azure Search plugin
    └── MCPPlugin.py        # MCP connection plugin
```

## 🔧 Configuration

### Azure OpenAI Setup
1. Create an Azure OpenAI resource in the Azure portal
2. Deploy a GPT-4 model for chat completions
3. Deploy a text-embedding-3-small model for embeddings
4. Update the configuration in `config.env`

### Azure Cognitive Search Setup
1. Create an Azure Cognitive Search service
2. Create an Azure Blob Storage account
3. Upload your company documents (PDFs, Word docs, etc.) to Blob Storage
4. Create a search index with your company documents
5. Configure semantic search capabilities with vector search
6. Update the search configuration in `config.env`

### Document Upload Process
1. **Prepare your documents**: Company policies, HR guidelines, procedures, etc.
2. **Upload to Azure Blob Storage**: Place your documents in a container
3. **Configure search index**: Set up the index to process your documents
4. **Enable vector search**: Configure semantic search for better results
5. **Test the system**: Ask questions about your uploaded content

### Supported Document Types
- **PDF files**: Company handbooks, policy documents, procedures
- **Word documents**: HR guidelines, training materials, procedures
- **Text files**: Plain text documents, markdown files
- **HTML files**: Web-based documentation, intranet content

### Best Practices for Document Upload
- **Organize by category**: Group related documents in Blob Storage containers
- **Use descriptive names**: Name files clearly for easy identification
- **Include metadata**: Add tags or descriptions to improve search results
- **Regular updates**: Keep documents current and remove outdated versions
- **Test queries**: Verify that your documents are searchable after upload


**Happy coding! 🎉**