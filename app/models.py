import uuid
from sqlalchemy.dialects.postgresql import UUID
from app.database import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class GpxFile(db.Model):
    __tablename__ = 'gpx_files'
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4)
    filename = db.Column(db.String(255), nullable=False)
    upload_time = db.Column(db.DateTime, nullable=False)
    owner_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)
    is_public = db.Column(db.Boolean, nullable=False, default=False)

    owner = db.relationship('User', backref=db.backref('gpx_files', lazy=True))

class Track(db.Model):
    __tablename__ = 'tracks'
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4)
    gpx_file_id = db.Column(UUID(as_uuid=True), db.ForeignKey('gpx_files.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    gpx_file = db.relationship('GpxFile', backref=db.backref('tracks', lazy=True, cascade='all, delete-orphan'))

class TrackPoint(db.Model):
    __tablename__ = 'track_points'
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4)
    track_id = db.Column(UUID(as_uuid=True), db.ForeignKey('tracks.id', ondelete='CASCADE'), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    elevation = db.Column(db.Float)
    time = db.Column(db.DateTime)
    track = db.relationship('Track', backref=db.backref('track_points', lazy=True, cascade='all, delete-orphan'))

class Waypoint(db.Model):
    __tablename__ = 'waypoints'
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4)
    gpx_file_id = db.Column(UUID(as_uuid=True), db.ForeignKey('gpx_files.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(255))
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    elevation = db.Column(db.Float)
    time = db.Column(db.DateTime)
    gpx_file = db.relationship('GpxFile', backref=db.backref('waypoints', lazy=True, cascade='all, delete-orphan'))

class FileShare(db.Model):
    __tablename__ = 'file_shares'
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4)
    gpx_file_id = db.Column(UUID(as_uuid=True), db.ForeignKey('gpx_files.id', ondelete='CASCADE'), nullable=False)
    shared_with_user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    shared_with_user = db.relationship('User', backref=db.backref('shared_files', lazy=True, cascade='all, delete-orphan'))
    gpx_file = db.relationship('GpxFile', backref=db.backref('shared_with', lazy=True, cascade='all, delete-orphan'))
