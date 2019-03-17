import os
import json
import requests
from flask import Flask, jsonify, make_response, request, send_file
from flask_api import status
from flask_cors import CORS, cross_origin

application = Flask(__name__)
cors = CORS(application)
application.config['CORS_HEADERS'] = 'Content-Type'

books_base_url = "https://www.googleapis.com/books/v1/volumes"

SEARCH_PARAM = "key_words"
PARAM_SORT = "sorted"
PARAM_START_INDEX = "start_index"
PARAM_MAX_RESULTS = "max_results"

@application.route("/v1/books")
@cross_origin()
def query_books():
    try:
        if (not request.args.has_key(SEARCH_PARAM)):
            return get_response({"message" : "Se debe ingresar algun parametro de busqueda valido!"}, status.HTTP_400_BAD_REQUEST)

        query_param = "q={}".format(request.args.get(SEARCH_PARAM))

        response = requests.get(books_base_url + "?{}".format(query_param), headers = {"key" : os.environ['BOOKS_API_TOKEN']})
        book_list = response.json()["items"] if (response.json()["totalItems"] > 0) else []
        start_index = 0 if (not request.args.has_key(PARAM_START_INDEX)) else int(request.args[PARAM_START_INDEX])
        print(len(book_list))

        if (start_index >= len(book_list)):
            return get_response({"items" : []}, status.HTTP_200_OK)

        if (request.args.has_key(PARAM_SORT) and request.args[PARAM_SORT]):
            book_list = sorted(book_list, key=lambda book: book["volumeInfo"]["title"])

        new_end_index = len(book_list) if ((not request.args.has_key(PARAM_MAX_RESULTS)) or len(book_list) < int(request.args[PARAM_MAX_RESULTS])) else (start_index + int(request.args[PARAM_MAX_RESULTS]))
        new_end_index = len(book_list) if (new_end_index > len(book_list)) else new_end_index
        
        return get_response({"items" : book_list[start_index : new_end_index]}, status.HTTP_200_OK)
    except ValueError as e:
        return get_response({"message" : "La busqueda que intenta realizar no es valida! : {}".format(e.message)}, status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return get_response({"message" : "Se produjo un error inesperado: {}".format(e.message)}, status.HTTP_500_INTERNAL_SERVER_ERROR)

def get_response(request_response_obj, response_status):
    return make_response(json.dumps(request_response_obj), response_status)
