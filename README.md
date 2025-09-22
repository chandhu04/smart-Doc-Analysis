# Smart Doc Analysis 🎯

## AI-Powered Document Analysis Platform - Team ResearchAI

> *"We built this comprehensive document analysis platform to revolutionize how you process, analyze, and extract insights from documents!"*

### The Problem 😤
As professionals and researchers, we waste HOURS manually analyzing documents, extracting key information, and finding related content. Existing tools are either too expensive, too complicated, or lack comprehensive analysis capabilities.

### Our Solution ✨
An AI-powered document analysis platform that:
- Automatically analyzes and summarizes uploaded documents
- Extracts key topics and provides intelligent insights
- Integrates live data sources for related content
- Provides real-time billing with usage tracking
- Works with PDFs, Word docs, and text files

## What Makes It Special 🚀

### Built by Developers, For Professionals
- 📄 **Document Processing**: Extract and analyze text from PDF, DOCX, and TXT files
- 🤖 **AI Analysis**: Intelligent summarization and topic extraction
- 🌐 **Live Data Integration**: Real-time content matching with Pathway integration
- 💰 **Billing System**: Flexprice integration with per-operation charging
- 📊 **Real-time Dashboard**: Live usage tracking and statistics
- 🌐 **Web Interface**: Professional web-based platform

### Key Benefits
- ✅ Automatic document analysis with AI-powered summaries
- ✅ Intelligent topic extraction and key insights identification
- ✅ Real-time integration with live data sources and news
- ✅ Usage-based billing with transparent cost tracking
- ✅ Professional web interface with real-time updates
- ✅ Comprehensive document processing with related content matching

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download** the project:
```bash
cd smart_research_assistant
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the web application**:
```bash
python simple_web.py
```

4. **Open your browser** to `http://localhost:8000`

## Usage Examples

### Web Interface
1. **Start the server**:
```bash
python simple_web.py
```

2. **Open http://localhost:8000 in your browser**

3. **Upload documents**: Drag and drop PDF, DOCX, or TXT files

4. **Get instant analysis**: AI automatically analyzes content, extracts topics, and finds related live data

5. **Track usage**: Real-time billing dashboard shows credits, usage, and costs

### Command Line Mode
```bash
# Upload and research in one command
python src/smart_research_assistant.py -u document.pdf -q "climate change impacts" -o report.txt

# Disable online sources
python src/smart_research_assistant.py -q "your query" --no-online

# Different citation styles
python src/smart_research_assistant.py -q "your query" --citation-style apa

# JSON output format
python src/smart_research_assistant.py -q "your query" -f json -o report.json
```

### Advanced Usage
```bash
# Show usage statistics
python src/smart_research_assistant.py --stats

# Custom data directory
python src/smart_research_assistant.py --data-dir ./custom_data -i

# Multiple document upload
python src/smart_research_assistant.py -u *.pdf *.txt -i
```

## Project Structure

```
smart_research_assistant/
├── simple_web.py               # Main web application
├── src/                        # Source code modules
│   ├── smart_research_assistant.py # Core AI engine
│   ├── document_processor.py       # Document text extraction
│   ├── search_engine.py           # Search functionality
│   ├── flexprice_billing.py       # Billing integration
│   ├── pathway_integration.py     # Live data integration
│   └── citation_system.py         # Citation formatting
├── web_data/                   # Runtime data (auto-created)
├── uploads/                    # Document uploads (auto-created)
├── requirements.txt            # Python dependencies
└── README.md                  # This file
```

## Features

The Smart Doc Analysis platform includes:

- **Document Processing**: PDF, DOCX, TXT support with intelligent text extraction
- **AI Analysis**: Automatic summarization, topic extraction, and content insights
- **Live Data Integration**: Real-time news and blog content matching via Pathway
- **Billing System**: Flexprice integration with per-operation charging ($0.25/question, $0.50/report)
- **Web Dashboard**: Real-time usage tracking, credit management, and live statistics

## Supported File Formats

- **Text Files** (`.txt`): Plain text documents
- **PDF Documents** (`.pdf`): Portable Document Format files
- **Word Documents** (`.docx`): Microsoft Word documents

## Live Data Sources

- **News Sources**: Real-time news articles and breaking updates
- **Industry Blogs**: Technology and research blog posts
- **Pathway Integration**: Continuous data ingestion with background updates
- *Extensible*: Easy to add more sources via configuration

## Citation Styles

- **Simple**: `[document.pdf, p.5]` or `[wikipedia.org]`
- **APA**: Author (Year). Title. Retrieved from domain
- **MLA**: Author. "Title". Web. domain. Date

## Usage Statistics & Billing

The system tracks:
- Query count and processing time
- Document processing statistics
- User satisfaction ratings
- Peak usage patterns
- Cost calculation for billing integration

## API Integration Ready

The MVP is designed to be extended with:
- REST API endpoints
- Web interface
- Database integration
- Advanced AI/ML features
- Custom online sources

## Development

### Running Tests
```bash
# Install development dependencies
pip install pytest pytest-cov

# Run tests (when test files are added)
pytest
```

### Code Formatting
```bash
# Install formatting tools
pip install black flake8

# Format code
black src/
flake8 src/
```

### Adding New Features

The modular design makes it easy to extend:

1. **New Document Types**: Extend `document_processor.py`
2. **Additional Sources**: Add to `online_integration.py`
3. **Citation Formats**: Extend `citation_system.py`
4. **Search Algorithms**: Enhance `search_engine.py`

## Troubleshooting

### Common Issues

**"Module not found" errors:**
```bash
# Make sure you're in the project directory
cd smart_research_assistant

# Install dependencies
pip install -r requirements.txt
```

**PDF processing fails:**
```bash
# Install PyPDF2
pip install PyPDF2

# For better PDF support, optionally install:
pip install PyMuPDF
```

**Online search timeout:**
- Check internet connection
- Increase timeout in `config.yaml`
- Use `--no-online` flag to disable online sources

### Performance Tips

- **Large Documents**: Process one at a time for very large files
- **Many Documents**: Use SSD storage for better performance
- **Online Queries**: Be patient - online sources can be slow
- **Memory Usage**: Monitor memory with many large documents

## Contributing

This is an MVP (Minimum Viable Product) designed for demonstration and extension. Key areas for improvement:

1. **Enhanced AI Integration**: Add LLM-powered summarization
2. **Web Interface**: Build React/Vue.js frontend
3. **Database Support**: Add PostgreSQL/MongoDB integration
4. **Advanced Search**: Implement semantic search
5. **Mobile App**: Create mobile companion app
6. **Collaboration**: Multi-user support and sharing

## License

This project is provided as-is for educational and demonstration purposes.

## Support

For questions or issues with this MVP:
1. Check the troubleshooting section above
2. Review the configuration files
3. Examine the source code - it's well-documented
4. Test with simple examples first

---

**Smart Doc Analysis Platform** - Transforming how you analyze and extract insights from documents! 🎯📊
