import pandas
import requests
import boto3

# Replace the text 'TODO' for the OMDB API key
OMDB_API_KEY = "TODO"
MOVIES_FILE = "movies.csv"
OMDB_URL = "http://www.omdbapi.com"
# List of attributes to update on html
MOVIE_INFO_LIST = [ "Year", "Genre", "Director", "Writer", "Actors", "Awards", "Plot" ]
# S3 bucket to upload html file, replace 'TODO' for your bucket name
BUCKET_NAME = "TODO"

def get_movie_info(movie_title):
    """Function to search a movie information on website OMDB (Open Movie Database), using the 
    title of a movie as search parameter
    
    The search will return a json with the movie informations. If the title don't match any movie, will return a json like:
    {'Response': 'False', 'Error': 'Movie not found!'}
    Args:
        movie_title (String): Name of a movie (in English)
    """
    response = requests.get(f'{OMDB_URL}/?t={movie_title}&apikey={OMDB_API_KEY}')
    return response.json() if response.status_code == 200 and eval(response.json()['Response']) else None

def add_html_card(html_file, movie_list):
    """Function to create a html card of movies from a list

    Args:
        html_file (file): html file that will be created
        movie_list (list): list that contain information of movies (dictionaries)
    """
    html_file.write('<div class="card-deck">\n')
    
    for movie in movie_list:
        html_file.write('\t<div class="card m-2" style="width: 200px;">\n')
        html_file.write('\t\t<img src="' + movie["Poster"] + '" alt="' + movie["Title"] + '"/>\n')
        html_file.write('\t\t\t<div class="card-body">\n')
        html_file.write('\t\t\t\t<h2 class="card-title">' + movie["Title"] + '</h2>\n')
        
        for info in MOVIE_INFO_LIST:
            if info in movie:
                html_file.write('\t\t\t\t<b>' + info + ':</b> ' + movie[info] + '<br><br>\n')

        html_file.write('\t\t\t\t<a href="https://www.imdb.com/title/' + movie['imdbID'] + '" class="btn btn-secondary">Learn more</a>\n')
        html_file.write('\t\t\t</div>\n')
        html_file.write('\t</div>\n')
        
    html_file.write('</div>\n')


def create_html_file(movie_list):
    """Function to create a simple html of movies from a list

    Args:
        movie_list (list): list that contain information of movies (dictionaries)
    """
    html_file = open("index.html", "w+")
    html_file.write('<!doctype html>\n')
    html_file.write('<html lang="en">\n')
    html_file.write('<head>\n')
    html_file.write('<meta charset="utf-8">\n')
    html_file.write('<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">\n')
    html_file.write('<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css">\n')
    html_file.write('<title>Movie List</title>\n')
    html_file.write('</head>\n')
    html_file.write('<body>\n')
    html_file.write('<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"></script>\n')
    html_file.write('<script src="https://cdn.jsdelivr.net/npm/popper.js@1.14.7/dist/umd/popper.min.js"></script>\n')
    html_file.write('<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/js/bootstrap.min.js"></script>\n')
    
    add_html_card(html_file, movie_list[:5])
    add_html_card(html_file, movie_list[5:])
  
    html_file.write('</body>\n')
    html_file.write('</html>\n')
    html_file.close()

def upload_file_s3(file_name, bucket):
    """Upload html to AWS S3 bucket

    Args:
        file_name (str): Name of the file that will be updated
        bucket (str): Bucket name
    """
    s3_client = boto3.client('s3')
    s3_client.upload_file(file_name, bucket, file_name, ExtraArgs={'ContentType':'text/html', 'ACL': 'public-read'})
    
    
# Get the movie list form the file 'movies.csv'
movies_title = pandas.read_csv(MOVIES_FILE)['Movie'].tolist()
# Gather the information of movies on OMDB
movies_info = [movie for title in movies_title if (movie := get_movie_info(title)) is not None]
# Creates a simple html file with the movie information provide from OMDB
create_html_file(movies_info)
# Upload html to AWS S3 Bucket
upload_file_s3("index.html", BUCKET_NAME)

