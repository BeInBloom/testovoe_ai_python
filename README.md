# Короткое саммари от меня, а не от нейро хрючего.

Пришлось парсить все файлы "руками", так как нейронки перегружены бесплатные.
По этому картинка, где плохой текст, распозналась плохо. Так же gemeni сделала норм распознование
когда я кидал в нее на прямую. Так же есть проблемы с логированием и флагом --verbose, но этим
мне уже лень заниматься. Так же есть бак с таск баром, который то появляется, то нет.
Этим тоже мне лень заниматься. Сама структура модульная, но из-за объема кода и сжатого времени
много что было сделано нейронкой.

# AI Document Summarizer

A Python CLI application that analyzes documents in a folder and generates summaries using AI (LLM).

## Features

- 🤖 **Multi-format support**: txt, md, pdf, jpg, png, gif, webp
- 🔌 **Plugin-based skill system**: extensible via YAML/TOML
- 💉 **Dependency injection**: clean architecture with dependency-injector
- 🔄 **Automatic retry**: Tenacity-based retry with exponential backoff
- ⚡ **Multimodal AI**: Send text, PDFs, and images to LLM
- 📁 **Recursive folder scanning**: Iterative algorithm (stack-based)
- ⚙️ **Configurable**: Environment variables via pydantic-settings

## Installation

1. Install `uv` (if not installed):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Create virtual environment and install dependencies:

```bash
uv venv
uv sync
```

3. Activate virtual environment:

```bash
source .venv/bin/activate
```

4. Configure environment variables:

```bash
cp .env.example .env
# Edit .env with your OpenRouter API key
```

## Usage

Run the application:

```bash
python main.py /path/to/folder
```

If no folder path is provided, the current directory is used:

```bash
python main.py
```

## Configuration

Create a `.env` file with the following variables:

```env
OPENROUTER_API_KEY=your-api-key-here
OPENROUTER_MODEL=z-ai/glm-4.5-air:free
MAX_FILE_SIZE_MB=10
SKILLS_PATH=src/skills/.config/happy_smile
RECURSIVE_SCAN=true
REQUEST_TIMEOUT=10
MAX_RETRIES=3
```

### Configuration Options

| Variable             | Description                          | Default                          |
| -------------------- | ------------------------------------ | -------------------------------- |
| `OPENROUTER_API_KEY` | Your OpenRouter API key              | Required                         |
| `OPENROUTER_MODEL`   | Model to use for summarization       | `z-ai/glm-4.5-air:free`          |
| `MAX_FILE_SIZE_MB`   | Maximum file size to process (MB)    | `10`                             |
| `SKILLS_PATH`        | Path to skills configuration         | `src/skills/.config/happy_smile` |
| `RECURSIVE_SCAN`     | Scan subfolders recursively          | `true`                           |
| `REQUEST_TIMEOUT`    | HTTP request timeout (seconds)       | `10`                             |
| `MAX_RETRIES`        | Maximum retry attempts for API calls | `3`                              |

## Architecture

The application follows a contract-based architecture with dependency injection:

```
ai/
├── main.py                      # CLI entry point
├── config.py                    # Pydantic Settings
├── src/
│   ├── core/                    # Core application logic
│   │   ├── logger.py           # Custom logger
│   │   ├── app.py              # Application contract + SimpleApplication
│   │   ├── main_app.py         # Main App class
│   │   ├── cli.py              # CLI utilities
│   │   ├── runner.py           # Application runner
│   │   ├── folder_scanner.py   # Iterative folder scanner
│   │   ├── document_collector.py # Document collector
│   │   ├── summary_generator.py # Summary generator
│   │   └── skill_selector.py   # Skill selection
│   ├── domain/                  # Domain models
│   │   ├── models.py           # Pydantic models
│   │   └── exceptions.py       # Domain exceptions
│   ├── readers/                 # Document readers
│   │   ├── contracts.py        # DocumentReader Protocol
│   │   ├── factory.py          # ReaderFactory
│   │   ├── txt_reader.py       # Text file reader
│   │   ├── pdf_reader.py       # PDF reader (base64)
│   │   └── image_reader.py     # Image reader (base64)
│   ├── llm/                     # LLM integration
│   │   ├── contracts.py        # LLMProvider Protocol
│   │   ├── openrouter.py       # OpenRouter client with retry
│   │   └── prompts.py          # Prompt templates
│   ├── skills/                  # Skill system
│   │   ├── base.py             # Skill contract
│   │   ├── registry.py         # Skill loader
│   │   └── .config/happy_smile/
│   │       └── folder_analysis.yaml
│   └── output/                  # Output formatting
│       └── formatter.py        # Output formatter
└── src/dependencies.py          # DI Container
```

## Flow

1. **Folder Scanning**: Iteratively scans folder (stack-based, no recursion)
2. **Document Collection**: Reads files via appropriate readers
3. **Summary Generation**: Sends documents to OpenRouter LLM
4. **Output**: Formats and displays summary

## Retry Logic

The application uses Tenacity for automatic retry:

- **Exponential backoff + jitter**: 1s → 10s max
- **Retry conditions**: HTTP errors, rate limits (429), timeouts
- **Max retries**: 3 attempts
- **Rate limit handling**: Respects `Retry-After` header

## Supported File Types

| Type   | Extensions                               | Method                        |
| ------ | ---------------------------------------- | ----------------------------- |
| Text   | `.txt`, `.md`, `.markdown`               | Text content                  |
| PDF    | `.pdf`                                   | Base64 → OpenRouter file      |
| Images | `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp` | Base64 → OpenRouter image_url |

## Development

To add a new document reader:

1. Implement `DocumentReader` Protocol
2. Add `supports()`, `read()`, `get_supported_extensions()` methods
3. Register in `src/dependencies.py`

To add a new skill:

1. Create YAML/TOML file in skills directory
2. Define skill configuration
3. Implement skill class

## Requirements

- Python 3.13+
- OpenRouter API key (free tier available)

## License

MIT
