"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db
from flask import render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
from app.models import Movie
from app.forms import MovieForm
from flask_wtf.csrf import generate_csrf


###
# Routing for your application.
###
@app.route('/api/v1/movies', methods=['POST'])
def movies():
    """
    Handles POST requests to add a new movie to the database.
    Validates the form data, saves the uploaded poster file, and adds the movie details to the database.
    Returns a JSON response indicating success or failure.
    """
    # Check if the request is a POST request
    if request.method == 'POST':
        # Initialize the form with the request data
        form = MovieForm()
        
        # Validate the form data
        if form.validate_on_submit():
            try:
                # Get the file from the form
                poster = form.poster.data
                filename = secure_filename(poster.filename)

                # Ensure the upload folder exists
                app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                
                # Save the file to the upload folder
                poster_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                poster.save(poster_path)
                
                # Create a new movie instance
                new_movie = Movie(
                    title=form.title.data,
                    description=form.description.data,
                    poster=filename
                )
                
                # Add the new movie to the database
                db.session.add(new_movie)
                db.session.commit()
                
                # Return success message
                return jsonify({
                    "message": "Movie Successfully added",
                    "title": new_movie.title,
                    "poster": new_movie.poster,
                    "description": new_movie.description
                }), 201
        
            except Exception as e:
                # Handle unexpected errors
                return jsonify({"error": "An error occurred while processing the request."}), 500
            
        else:
            # Return validation errors
            return jsonify({
                "errors": form_errors(form)
            }), 400
    
    # If the request is not a POST request, return method not allowed
    return jsonify({"error": "Method Not Allowed"}), 405



#CSRF token endpoint
@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})


@app.route('/')
def index():
    return render_template('index.html')




###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"error": "Page not found"}), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({"error": "Internal server error"}), 500