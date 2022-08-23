# app.py


from config import *
from schema import *
from create_data import *
from flask_restx import Api, Resource

api = Api(app)

bs_movie = api.namespace('movies')
bs_director = api.namespace('directors')
bs_genre = api.namespace('genres')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)
@bs_movie.route('/')
class MoviesView(Resource):
    movie_schema = MovieSchema(many=True)

    def get(self):
        movies = Movie.query
        args = request.args
        director_id = args.get('director_id')
        if director_id is not None:
            movies = movies.filter(Movie.director_id == director_id)
        genre_id = args.get('genres_id')
        if genre_id is not None:
            movies = movies.filter(Movie.genre_id == genre_id)
        movies = movies.all()

        return movies_schema.dump(movies), 200

    def post(self):
        movie = movie_schema.load(request.json)
        new_movie = Movie(**movie)
        with db.session.begin():
            db.session.add(new_movie)
        return 'All OK', 201


@bs_movie.route('/<int:movie_id>')
class MovieViews(Resource):
    def get(self, movie_id):
        try:
            film = Movie.query.filter(Movie.id == movie_id).one()
            return movie_schema.dump(film), 200
        except Exception:
            return f'Not so movie_id like {movie_id}'

    def put(self, movie_id):
        Movie.query.filter(Movie.id == movie_id).update(request.json)
        db.session.commit()

        return '', 200

    def delete(self, movie_id):
        Movie.query.filter(Movie.id == movie_id).delete()
        db.session.commit()

        return None, 200


@bs_director.route('/')
class DirectorsViews(Resource):
    def get(self):
        directors = Director.query.all()

        return directors_schema.dump(directors)
    def post(self):
        director = director_schema.load(request.json)
        new_director = Director(**director)
        with db.session.begin():
            db.session.add(new_director)
        return 'All Ok', 201




@bs_director.route('/<director_id>')
class DirectorViews(Resource):
    def get(self, director_id):
        try:
            director = Director.query.filter(Director.id == director_id).one()
            return director_schema.dump(director), 200
        except Exception:
            return f'Not so director_id like {director_id}'
    def put(self,director_id):
        Director.query.filter(Director.id == director_id).update(request.json)
        db.session.commit()

        return None, 200

    def delete(self, director_id):
        Director.query.filter(Director.id == director_id).delete()
        db.session.commit()

        return None, 200


@bs_genre.route('/')
class GenresViews(Resource):
    def get(self):
        genres = Genre.query.all()
        return genres_schema.dump(genres)
    def post(self):
        genre = genre_schema.load(request.json)
        new_genre = Genre(**genre)
        with db.session.begin():
            db.session.add(new_genre)
        return 'All Ok', 201



@bs_genre.route('/<genre_id>')
class GenreViews(Resource):
    def get(self, genre_id):
        try:
            genre = Genre.query.filter(Genre.id == genre_id).one()
            return genre_schema.dump(genre)
        except Exception:
            return f'Not so genre_id like {genre_id}'
    def put(self, genre_id):
        Genre.query.filter(Genre.id == genre_id).update(request.json)
        db.session.commit()

        return None, 200
    def delete(self,genre_id):
        Genre.query.filter(Genre.id == genre_id).delete()
        db.session.commit()

        return None, 200


if __name__ == '__main__':
    app.run(debug=True)
