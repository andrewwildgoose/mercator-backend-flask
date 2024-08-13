import gpxpy
from datetime import datetime
from werkzeug.utils import secure_filename
from app.database import db
from app.models import GpxFile, Track, TrackPoint, Waypoint, FileShare
from sqlalchemy.orm import subqueryload

def save_gpx_file(file, owner_id, is_public):
    gpx = gpxpy.parse(file)
    filename = secure_filename(file.filename)
    
    gpx_file = GpxFile(filename=filename, upload_time=datetime.now(), owner_id=owner_id, is_public=is_public)
    db.session.add(gpx_file)
    db.session.commit()

    # Extract and store tracks and track points
    for track in gpx.tracks:
        track_record = Track(gpx_file_id=gpx_file.id, name=track.name, description=track.description)
        db.session.add(track_record)
        db.session.commit()

        track_points_data = [
            TrackPoint(track_id=track_record.id, latitude=point.latitude, longitude=point.longitude, elevation=point.elevation, time=point.time)
            for segment in track.segments for point in segment.points
        ]
        db.session.bulk_save_objects(track_points_data)
        db.session.commit()

    # Extract and store waypoints
    waypoints_data = [
        Waypoint(gpx_file_id=gpx_file.id, name=waypoint.name, latitude=waypoint.latitude, longitude=waypoint.longitude, elevation=waypoint.elevation, time=waypoint.time)
        for waypoint in gpx.waypoints
    ]
    db.session.bulk_save_objects(waypoints_data)
    db.session.commit()

    return gpx_file.id

def save_file_share(gpx_file_id, shared_with_user_id):
    file_share = FileShare(gpx_file_id=gpx_file_id, shared_with_user_id=shared_with_user_id)
    db.session.add(file_share)
    db.session.commit()

    return file_share.id

def delete_gpx_file_from_db(gpx_file_id):
    gpx_file = GpxFile.query.get(gpx_file_id)
    if not gpx_file:
        return 'GPX file cannot be located'

    # Simply delete the GPXFile object
    db.session.delete(gpx_file)
    db.session.commit()

    return 'GPX file and related records deleted successfully'