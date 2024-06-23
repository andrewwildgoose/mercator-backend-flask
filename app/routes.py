from flask import request, jsonify, session, current_app as app
from app import app
from app.database import create_user, get_user_by_email
from app.gpx_service import save_gpx_file, save_file_share, delete_gpx_file_from_db
from app.models import GpxFile, FileShare, Track, TrackPoint


@app.route('/')
def home():
    return "Hello World"

@app.route('/register', methods=['POST'])
def register():
    email = request.json.get('email')
    password = request.json.get('password')
    name = request.json.get('name')

    if not email or not password or not name:
        return jsonify({'message': 'Email, password and name are required'}), 400

    if get_user_by_email(email):
        return jsonify({'message': 'Email address already registered'}), 400

    create_user(email, password, name)

    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    user = get_user_by_email(email)

    if user is None or not user.check_password(password):
        return jsonify({'message': 'Invalid email or password'}), 401

    # Log in the user (for session-based authentication)
    session['user_id'] = user.id

    return jsonify({'message': 'Logged in successfully'}), 200

@app.route('/logout', methods=['POST'])
def logout():
    if 'user_id' not in session:
        return jsonify({'message': 'User already logged out'}), 200

    # Clear the session data
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/upload-gpx', methods=['POST'])
def upload_gpx():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        try:
            is_public = request.form.get('is_public', 'false').lower() == 'true'
            gpx_file_id = save_gpx_file(file, session['user_id'], is_public)
            return jsonify({'message': 'File uploaded and data stored successfully', 'gpx_file_id': gpx_file_id}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return jsonify({'error': 'File not allowed'}), 400

@app.route('/my-gpx-files', methods=['GET'])
def get_my_gpx_files():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    user_id = session['user_id']
    gpx_files = GpxFile.query.filter_by(owner_id=user_id).all()
    shared_files = GpxFile.query.join(FileShare).filter(FileShare.shared_with_user_id == user_id).all()
    
    files = gpx_files + shared_files
    files_data = [{'id': f.id, 'filename': f.filename, 'upload_time': f.upload_time.isoformat(), 'is_public': f.is_public} for f in files]

    return jsonify(files_data)

@app.route('/public-gpx-files', methods=['GET'])
def get_public_gpx_files():
    public_files = GpxFile.query.filter_by(is_public=True).all()
    files_data = [{'id': f.id, 'filename': f.filename, 'upload_time': f.upload_time.isoformat()} for f in public_files]

    return jsonify(files_data)

@app.route('/share-gpx-file', methods=['POST'])
def share_gpx_file():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    user_id = session['user_id']
    file_id = request.json.get('file_id')
    share_with_email = request.json.get('share_with_email')
    share_with_user = get_user_by_email(share_with_email)

    if not share_with_user:
        return jsonify({'error': 'User to share with not found'}), 404

    gpx_file = GpxFile.query.filter_by(id=file_id, owner_id=user_id).first()
    if not gpx_file:
        return jsonify({'error': 'File not found or you do not have permission to share this file'}), 404

    file_share_id = save_file_share(gpx_file, share_with_user)

    return jsonify({'message': 'File shared successfully', 'file_share': file_share_id}), 200

@app.route('/gpx-file/<uuid:file_id>', methods=['GET'])
def get_gpx_file(file_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    user_id = session['user_id']
    gpx_file = GpxFile.query.filter((GpxFile.id == file_id) and 
                                    ((GpxFile.owner_id == user_id) or 
                                    (GpxFile.is_public == True) or 
                                    (FileShare.shared_with_user_id == user_id))).first()

    if not gpx_file:
        return jsonify({'error': 'File not found or you do not have permission to view this file'}), 404

    if gpx_file:
        tracks = gpx_file.tracks
        all_track_points_data = []
        for t in tracks:
            track = t.id
            track_points = t.track_points
            track_points_data = [{'id': tp.id, 'latitude': tp.latitude, 'longitude': tp.longitude, 'elevation': tp.elevation} for tp in track_points]
            all_track_points_data.append({'track': track, 'track_points': track_points_data})

    file_data = {
        'id': gpx_file.id,
        'filename': gpx_file.filename,
        'upload_time': gpx_file.upload_time.isoformat(),
        'is_public': gpx_file.is_public,
        'tracks': [{'id': t.id, 'name': t.name, 'description': t.description} for t in gpx_file.tracks],
        'all_track_points': all_track_points_data,
        'waypoints': [{'id': w.id, 'name': w.name, 'latitude': w.latitude, 'longitude': w.longitude, 'elevation': w.elevation} for w in gpx_file.waypoints]
    }

    return jsonify(file_data)

@app.route('/gpx-files/<uuid:gpx_file_id>', methods=['DELETE'])
def delete_gpx_file(gpx_file_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    message = delete_gpx_file_from_db(gpx_file_id)

    return jsonify({'message': message}), 200

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'gpx'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS