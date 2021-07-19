"""Arguments for request parser"""
from flask_restplus import reqparse

sorting = reqparse.RequestParser()
sorting.add_argument("start", default=1, required=False, help="Start page")
sorting.add_argument("limit", default=10, required=False, help="Per_page")
sorting.add_argument("sort_data", required=False, choices=["Rating", "Date Release"])
sorting.add_argument("sort_by", required=False, choices=["Descending", "Ascending"])
sorting.add_argument("Director", required=False, help="Director of film")
sorting.add_argument("from", required=False, help="Film From")
sorting.add_argument("to", required=False, help="To")
sorting.add_argument(
    "genre_film",
    required=False,
    choices=["action", "fighting", "comedy", "kids-movie", "drama", "horror"],
)
sorting.add_argument("search", required=False, help="Type title or word")

