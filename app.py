from flask import Flask, request, jsonify, render_template
import subprocess
import os

app = Flask(__name__)

WHISPER_PATH = "/home/kali/whisper.cpp"  # Path to the Whisper.cpp directory
WHISPER_BINARY = os.path.join(WHISPER_PATH, "main")  # Path to the Whisper binary

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Save the file temporarily
        file_path = os.path.join("temp_files", file.filename)
        file.save(file_path)
        
        # Call Whisper.cpp to transcribe the audio file
        result = subprocess.run(
            [WHISPER_BINARY, "-f", file_path], 
            capture_output=True, 
            text=True,
            cwd=WHISPER_PATH  # Ensure the command runs in the correct directory
        )
        
        # Get the transcription result
        transcription = result.stdout.strip()
        
        # Delete the temporary file after transcription
        os.remove(file_path)
        
        return jsonify({'transcription': transcription})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    if not os.path.exists("temp_files"):
        os.makedirs("temp_files")
    app.run(debug=True)
