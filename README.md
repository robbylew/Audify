# Audify

## Project Status

I've completely scrapped my previous implementation of the Spotify algorithm and am rebuilding it from scratch using Flask.

## Current Implementation

The current version of Audify is a simple web application that generates spectrograms from Spotify tracks. Users can:

1. Enter a Spotify song URL
2. View a spectrogram visualization of the audio

## Technical Details

This implementation uses:
- Flask as the web framework
- Spotify track downloads via spotdl
- Librosa for audio processing
- Matplotlib for spectrogram generation

## Running the Application

To run the application:

1. Install requirements:

```
pip install flask librosa matplotlib numpy spotdl
```

2. Run the Flask app:

```
python app.py
```

3. Open a browser and navigate to `http://127.0.0.1:5000`

## Note

This is a work in progress as I rebuild the application with a new architecture.
