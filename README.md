# 🎵 Spotify-Advance

Advanced tools and utilities for interacting with Spotify, featuring a web interface and various automation scripts.

## 🚀 Features

- Web interface for Spotify interaction
- Example scripts for common Spotify operations
- Jupyter notebook playground for experimentation
- Docker support for easy deployment
- Pre-commit hooks for code quality

## 📋 Prerequisites

- Python 3.x
- Spotify Developer Account and API Credentials
- Docker (optional)

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/haviv1idan/Spotify-Advance.git
cd Spotify-Advance
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up pre-commit hooks:
```bash
pre-commit install
```

## 🐳 Docker Setup

Build and run using Docker:

```bash
docker build -t spotify-advance .
docker run -p 8000:8000 spotify-advance
```

## 📁 Project Structure

```
spotify-advance/
├── src/               # Source code
├── examples_scripts/  # Example usage scripts
├── templates/         # Web interface templates
├── playground.ipynb   # Jupyter notebook for testing
├── web.py            # Web application
├── Dockerfile        # Docker configuration
└── requirements.txt  # Python dependencies
```

## 🎮 Usage

1. Configure your Spotify API credentials
2. Run the web interface:
```bash
python web.py
```
3. Visit `http://localhost:8000` in your browser

## 🧪 Development

1. Make sure to install development dependencies
2. Run pre-commit hooks before committing
3. Use the playground.ipynb for testing new features

## 📝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Idan Haviv**
- GitHub: [@haviv1idan](https://github.com/haviv1idan)

## ⭐ Show your support

Give a ⭐️ if this project helped you!