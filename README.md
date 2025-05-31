# Psychological Expert System

A sophisticated AI-powered platform designed to facilitate therapeutic interactions through specialized psychological expert agents. The system supports both short-term and long-term therapeutic relationships, with experts specializing in various psychological domains.

## 🌟 Features

### Expert Domain Model
- Multiple specialization areas (Anxiety, Depression, Trauma, etc.)
- Various therapeutic approaches (CBT, Psychodynamic, DBT, etc.)
- Different session types (Initial Assessment, Regular Session, Crisis Intervention, etc.)

### Session Management
- Real-time session state tracking
- Progress monitoring and risk assessment
- Homework management
- Session history and summaries

### Data Source Management
- Research databases integration (PubMed, PsycINFO)
- Professional guidelines (APA, WHO)
- Treatment protocols (CBT, DBT)
- Clinical documentation
- Case studies
- Ethical guidelines

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- FastAPI
- Pydantic
- MongoDB (optional)
- Sentence Transformers (for RAG)

### Installation
```bash
# Clone the repository
git clone https://github.com/mentrics/psychological-expert-system.git
cd psychological-expert-system

# Install dependencies
pip install -r requirements.txt

# Start the API server
uvicorn src.main:app --reload
```

## 📁 Project Structure
```
psychological-expert-system/
│
├── data/                  # Data files
│   └── psychological_experts.json
│
├── src/
│   ├── api/              # API routes
│   ├── config/           # Configuration
│   ├── domain/           # Core business logic
│   └── main.py          # FastAPI entry point
│
└── docs/                 # Documentation
    └── PSYCHOLOGICAL_EXPERT_SYSTEM.md
```

## 🔧 Configuration

### Data Sources
The system supports multiple data sources for expert knowledge:
- Research Databases
- Professional Guidelines
- Treatment Protocols
- Clinical Documentation
- Case Studies
- Ethical Guidelines

### Expert Configuration
Experts are configured with:
- Specialization areas
- Therapeutic approaches
- Communication styles
- Session protocols
- Ethical guidelines

## 📚 Documentation

For detailed documentation, please refer to:
- [System Overview](docs/PSYCHOLOGICAL_EXPERT_SYSTEM.md)
- API Documentation (available at `/docs` when running the server)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- American Psychological Association (APA)
- World Health Organization (WHO)
- Various research databases and treatment protocols

## 🔗 Links

- [API Documentation](http://localhost:8000/docs) (when running locally)
- [GitHub Repository](https://github.com/mentrics/psychological-expert-system)
