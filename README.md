# GhostMusic - AI Audio Generation Platform

GhostMusic is a web application that leverages AI to generate unique audio content based on text prompts. Built with Flask and the Hugging Face API, it provides a user-friendly interface for creating AI-generated music and sounds.

## Features

- **User Authentication**: Secure login and signup system
- **AI Audio Generation**: Generate audio content from text descriptions using the MusicGen model
- **Dark/Light Theme**: Toggle between dark and light modes for comfortable viewing
- **Audio Playback**: Built-in audio player for immediate playback
- **Download Capability**: Download generated audio files in WAV format
- **Responsive Design**: Works seamlessly across desktop and mobile devices

## Technologies Used

- **Backend**:
  - Flask (Python web framework)
  - SQLAlchemy (Database ORM)
  - FFmpeg (Audio processing)
  - Hugging Face API (AI model integration)

- **Frontend**:
  - HTML5/CSS3
  - JavaScript
  - Font Awesome (Icons)
  - Inter Font Family

## Prerequisites

- Python 3.7+
- FFmpeg
- Hugging Face API key
- SQLite

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ghostmusic.git
cd ghostmusic
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
export HF_API_KEY=your_huggingface_api_key  # On Windows: set HF_API_KEY=your_huggingface_api_key
```

5. Initialize the database:
```bash
flask db upgrade
```

## Usage

1. Start the Flask development server:
```bash
python app.py
```

2. Open a web browser and navigate to:
```
http://127.0.0.1:5000
```

3. Create an account or log in
4. Enter a text prompt describing the audio you want to generate
5. Click "Generate Audio" and wait for the generation to complete
6. Play the generated audio or download it

## Project Structure

```
ghostmusic/
├── app.py              # Main application file
├── templates/          # HTML templates
│   ├── index.html     # Main page template
│   ├── login.html     # Login page template
│   └── signup.html    # Signup page template
├── static/            # Static files (CSS, JS, images)
├── instance/         # Instance-specific files
│   └── users.db      # SQLite database
└── requirements.txt   # Python dependencies
```

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Hugging Face](https://huggingface.co/) for providing the AI model API
- [Facebook's MusicGen](https://huggingface.co/facebook/musicgen-small) for the audio generation model
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [FFmpeg](https://ffmpeg.org/) for audio processing capabilities

## Support

For support, please open an issue in the GitHub repository or contact [jhamb.aarav@gmail.com].
```
