from flask import Flask, render_template, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

# Define the download folder
DOWNLOAD_FOLDER = 'downloads/'

# Ensure the download directory exists
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

def download_music(url):
    """Function to download music using yt-dlp."""
    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),  # Save the music in the download folder
        'format': 'bestaudio/best',  # Download the best quality audio
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)  # Try to download the music
            return True, info_dict['title']  # Return success
    except Exception as e:
        return False, str(e)  # Return failure message

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    """Handle the music download request."""
    url = request.form.get('url')  # Get the URL from the form
    
    # Check if the URL is valid
    if not url:
        return jsonify({"message": "URL is required!"}), 400
    
    # Start downloading the music
    success, message = download_music(url)
    
    # Return response based on success or failure
    if success:
        return jsonify({"message": f"Download successful! '{message}' has been saved."})
    else:
        return jsonify({"message": f"Download failed. Error: {message}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
