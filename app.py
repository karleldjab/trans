from flask import Flask, request, jsonify, render_template
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Aucun fichier envoyé'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Aucun fichier sélectionné'}), 400

        # Enregistrer le fichier temporairement
        file_path = os.path.join("temp_files", file.filename)
        file.save(file_path)
        
        # Appeler Whisper.cpp pour transcrire le fichier audio
        result = subprocess.run(
            ["./main", "-f", file_path], 
            capture_output=True, 
            text=True
        )
        
        # Récupérer la sortie de Whisper.cpp
        transcription = result.stdout.strip()
        
        # Supprimer le fichier temporaire après transcription
        os.remove(file_path)
        
        return jsonify({'transcription': transcription})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    if not os.path.exists("temp_files"):
        os.makedirs("temp_files")
    app.run(debug=True)
