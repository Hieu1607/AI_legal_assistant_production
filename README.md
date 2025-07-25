# AI Legal Assistant Production

🤖 **AI Legal Assistant** - Hệ thống trợ lý pháp lý thông minh sử dụng RAG (Retrieval-Augmented Generation) với ChromaDB và sentence transformers.

## 📋 Tính năng

- **🔍 Tìm kiếm văn bản pháp lý**: Tìm kiếm thông minh trong cơ sở dữ liệu văn bản luật
- ** Vector Database**: Sử dụng ChromaDB để lưu trữ và tìm kiếm embeddings
- **🚀 API RESTful**: FastAPI với documentation tự động
- **🐳 Docker**: Containerized deployment với double warm-up tự động
- **⚡ RAG System**: Retrieval-Augmented Generation cho tìm kiếm chính xác

## 🛠️ Tech Stack

- **Backend**: FastAPI, Python 3.11
- **AI/ML**: Sentence Transformers (all-MiniLM-L6-v2), Google Generative AI
- **Database**: ChromaDB (Vector Database)
- **Containerization**: Docker, Docker Compose
- **Data Processing**: BeautifulSoup, Pandas
- **Logging**: Structured logging với ColoredLogs

## 🚀 Quick Start

### Prerequisites

Đảm bảo máy của bạn đã cài đặt:
- [Git](https://git-scm.com/)
- [Python 3.11+](https://python.org/)
- [Docker Desktop](https://docker.com/products/docker-desktop/) - **Lưu ý: Phải khởi động Docker Desktop trước khi chạy**
- `gdown` (for Google Drive downloads): `pip install gdown`

**Quan trọng**: Đảm bảo Docker Desktop đang chạy trước khi thực hiện setup!

### Option 1: One-Click Install (Windows)

```powershell
Invoke-Expression (Invoke-WebRequest -Uri "https://raw.githubusercontent.com/Hieu1607/AI_legal_assistant_production/main/install.ps1").Content
```

### Option 1b: One-Click Install (Linux/macOS)

```bash
curl -sSL https://raw.githubusercontent.com/Hieu1607/AI_legal_assistant_production/main/install.sh | bash
```

### Option 2: Manual Setup

#### Linux/macOS:
```bash
# Clone repository
git clone https://github.com/Hieu1607/AI_legal_assistant_production.git
cd AI_legal_assistant_production

# Run setup script
chmod +x setup.sh
./setup.sh
```

#### Windows:
```powershell
# Clone repository
git clone https://github.com/Hieu1607/AI_legal_assistant_production.git
cd AI_legal_assistant_production

# Run setup script
.\setup.ps1
```

### Option 3: Step-by-Step

```bash
# 1. Clone repository
git clone https://github.com/Hieu1607/AI_legal_assistant_production.git
cd AI_legal_assistant_production

# 2. Download data
python scripts/download_gdown.py

# 3. Build and run with Docker
docker-compose build
docker-compose up -d
```

## 📱 Usage

Sau khi khởi động thành công, bạn có thể truy cập:

- **🌐 API Documentation**: http://localhost:8000/docs
- **💚 Health Check**: http://localhost:8000/
- **🔍 Search Endpoint**: http://localhost:8000/retrieve

### Example API Calls

```bash
# Health check
curl http://localhost:8000/

# Search legal documents
curl -X POST "http://localhost:8000/retrieve" \
  -H "Content-Type: application/json" \
  -d '{"query": "quyền lợi người lao động", "top_k": 5}'
```

## 📁 Project Structure

```
AI_legal_assistant_production/
├── app/                    # FastAPI application
├── src/                    # Source code modules
│   ├── embedding/          # Embedding generation
│   ├── store_vector/       # ChromaDB operations
│   ├── retrieval/          # Data fetching
│   └── preprocess/         # Data preprocessing
├── scripts/                # Utility scripts
│   ├── warmup_chromadb.py  # Database warm-up
│   ├── download_gdown.py   # Data download
│   └── start_with_warmup.sh # Container startup
├── configs/                # Configuration files
├── data/                   # Data storage
│   └── processed/          # Processed data & vector store
├── logs/                   # Application logs
├── docker-compose.yml      # Docker services
├── Dockerfile             # Container definition
└── requirements.txt       # Python dependencies
```

## 🔧 Development

### Local Development Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Install gdown for Google Drive downloads
pip install gdown

# Set environment variables
cp .env_example .env
# Edit .env with your actual API keys:
# - Replace your_openai_api_key_here with your OpenAI API key
# - Replace your_gemini_api_key_here with your Gemini API key

# Initialize ChromaDB and load sample data
cd scripts
python download_data_and_build_vector_store.py
cd ..

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Database Management

```bash
# Initialize ChromaDB
python src/store_vector/init_index.py

# Build embeddings
python src/embedding/build_embeddings_with_local_model.py

# Index embeddings
python src/store_vector/index_embeddings_streaming.py
```

## 🐳 Docker Commands

```bash
# Build image
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild from scratch
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

## 📊 Monitoring & Logs

- **Container logs**: `docker-compose logs -f ai-legal-assistant`
- **Application logs**: `./logs/app.log`
- **Error logs**: `./logs/errors.log`
- **Health check**: http://localhost:8000/health

## 🔒 Security

- Non-root user trong container
- Security vulnerabilities được scan và mitigate
- Environment variables cho sensitive data
- CORS protection enabled

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## � Troubleshooting

### Common Issues

**1. gdown installation fails:**
```bash
# Try upgrading pip first
pip install --upgrade pip
pip install gdown

# Or install with user flag
pip install --user gdown
```

**2. Google Drive download fails:**
```bash
# Manual download if automated fails
# Download from: https://drive.google.com/your-file-id
# Place in data/ directory
```

**3. ChromaDB permission issues:**
```bash
# Check data directory permissions
chmod 755 data/
chmod 755 data/processed/
```

**4. Docker container fails to start:**
```bash
# Check if Docker Desktop is running
docker info

# If Docker is not running, start Docker Desktop:
# Windows: Start Docker Desktop from Start menu
# macOS: Open Docker Desktop application
# Linux: sudo systemctl start docker

# Check port availability
netstat -tulpn | grep 8000
```

**5. Docker daemon not running:**
```bash
# Windows: 
# - Open Docker Desktop from Start menu
# - Wait for the whale icon to become stable in system tray

# Linux:
sudo systemctl start docker
sudo systemctl enable docker

# macOS:
# - Open Docker Desktop application
# - Wait for Docker to start completely
```

## �📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Hieu1607/AI_legal_assistant_production/issues)
- **Documentation**: [API Docs](http://localhost:8000/docs)
- **Email**: [Contact](mailto:your-email@example.com)

## 🙏 Acknowledgments

- [ChromaDB](https://chromadb.ai/) for vector database
- [Sentence Transformers](https://sentence-transformers.net/) for embeddings
- [FastAPI](https://fastapi.tiangolo.com/) for web framework
- [Docker](https://docker.com/) for containerization