from flask import Flask, request, render_template
from db import db
from models import Media, Artist
from tools import get_itunes_media, populate_data_into_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'love_si507'
db.init_app(app)


@app.before_first_request  # called before first user request
def create_tables():
    db.create_all()
    sample_keyword = "Hello"  # add 10 sample data when it runs for the first time
    media_data = get_itunes_media(sample_keyword, 10)
    populate_data_into_db(media_data['results'])
    

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/all')
def all():
    all_media = Media.query.all()
    all_media_str= list(map(lambda x: str(x), all_media))  # call __repr__() on each media to get strings
    return render_template('all.html', results = all_media_str)


@app.route('/search')
def before_search():
    return render_template('searchform.html')


@app.route('/searchresult') 
def after_search():
    if request.method == 'GET':
        keyword = request.args.get('keyword')
        no = request.args.get('no')
        keyword = keyword if keyword else 'Born this way'
        no = no if no else 10  # use 10 as default value
        media_data = get_itunes_media(keyword, no)
        populate_data_into_db(media_data['results'])  # call those two funcs from tools.py
        return render_template('searchresult.html', 
            keyword = keyword, 
            results = media_data['results'])
    return '<h1>Please use the form to visit this link</h1>'  # just in case user use another request method

if __name__ == '__main__':
    app.run(port=5000, debug=True)

