from flask import Flask, request, jsonify
from models import init_db, register_voter, get_voter_photo, has_voted, mark_voted
from face_recognition import verify_voter
from blockchain import add_vote_block, get_vote_counts
import base64
import io
from PIL import Image

app = Flask(__name__)
init_db()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    photo_path = data.get('photo_path')  # Assume photo is stored on server
    register_voter(name, photo_path)
    return jsonify({"message": "Registration successful"}), 201

@app.route('/vote', methods=['POST'])
def vote():
    data = request.get_json()
    voter_id = data.get('voter_id')
    candidate = data.get('candidate')
    live_photo_base64 = data.get('live_photo')  # now expecting base64 data
    
    # Retrieve the registered photo for facial recognition
    registered_photo_path = get_voter_photo(voter_id)
    if not registered_photo_path:
        return jsonify({"message": "Voter not found"}), 404

    # Optionally, convert the base64 image to a temporary image file or PIL Image object
    try:
        header, encoded = live_photo_base64.split(",", 1)
        live_image_data = base64.b64decode(encoded)
        live_image = Image.open(io.BytesIO(live_image_data))
        # You can save live_image if needed:
        # live_image.save("live_capture.jpg")
        # For now, assume you modify verify_voter to work with PIL Image or temporary file
        live_photo_path = "temporary_live_capture.jpg"
        live_image.save(live_photo_path)
    except Exception as e:
        return jsonify({"message": "Failed to decode live image", "error": str(e)}), 400

    # Facial verification using DeepFace
    if not verify_voter(registered_photo_path, live_photo_path):
        return jsonify({"message": "Facial verification failed"}), 401

    # Check if the voter has already voted
    if has_voted(voter_id):
        return jsonify({"message": "You have already voted"}), 400

    # Add vote to our blockchain simulation and mark the voter as having voted
    add_vote_block(voter_id, candidate)
    mark_voted(voter_id)
    
    return jsonify({"message": "Vote cast successfully"}), 200
@app.route('/dashboard', methods=['GET'])
def dashboard():
    counts = get_vote_counts()
    return jsonify(counts), 200

if __name__ == '__main__':
    app.run(debug=True)
