from flask import Flask, render_template, request, Response
import os
import subprocess
import tempfile
import io
import shutil

# Set non-interactive Matplotlib backend BEFORE importing pyplot
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        spotify_url = request.form.get("spotify_url")
        if not spotify_url:
            return "Please provide a valid Spotify URL", 400
            
        temp_dir = None
        try:
            # Create a temporary directory for processing
            temp_dir = tempfile.mkdtemp()
            
            # Run spotdl to download the audio file
            subprocess.run(["spotdl", "download", spotify_url, "--output", temp_dir], check=True)
            
            # Find the downloaded file in the temp directory
            downloaded_files = os.listdir(temp_dir)
            if not downloaded_files:
                return "No files were downloaded", 500
                
            # Get the path to the downloaded file
            audio_file = os.path.join(temp_dir, downloaded_files[0])
            
            # Generate spectrogram
            spectrogram_data = generate_spectrogram(audio_file)
            
            # Return the spectrogram image
            return Response(spectrogram_data, mimetype='image/png')
        except Exception as e:
            return f"An error occurred: {str(e)}", 500
        finally:
            # Always clean up temporary files, even if an error occurs
            if temp_dir and os.path.exists(temp_dir):
                try:
                    shutil.rmtree(temp_dir)
                except:
                    pass
    
    return render_template("index.html")

def generate_spectrogram(audio_file):
    """Generate a spectrogram from the audio file"""
    # Load the audio file
    y, sr = librosa.load(audio_file)
    
    # Create a figure and axes
    plt.figure(figsize=(12, 8))
    
    # Generate spectrogram
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log')
    
    # Add a colorbar
    plt.colorbar(format='%+2.0f dB')
    
    # Add title and labels
    plt.title('Spectrogram')
    plt.xlabel('Time')
    plt.ylabel('Frequency (Hz)')
    plt.tight_layout()
    
    # Save the figure to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    
    return buf.getvalue()

if __name__ == "__main__":
    app.run(debug=True)
