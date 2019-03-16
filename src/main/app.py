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
PARAMETER_MAP = { "start_index" : "startIndex", "max_results" : "maxResults" }

@application.route("/v1/books")
@cross_origin()
def query_books():
    try:
        if (not request.args.has_key(SEARCH_PARAM)):
            return get_response({"message" : "Se debe ingresar algun parametro de busqueda valido!"}, status.HTTP_400_BAD_REQUEST)

        query_param = "q={}".format(request.args.get(SEARCH_PARAM))

        for param, value in request.args.items():
            if PARAMETER_MAP.has_key(param):
                query_param += "&{}={}".format(PARAMETER_MAP[param], value);

        response = requests.get(books_base_url + "?{}".format(query_param), headers = {"key" : os.environ['BOOKS_API_TOKEN']});
        book_list = response.json()["items"] if (response.json()["totalItems"] > 0) else []
        return get_response({"items" : book_list}, status.HTTP_200_OK)
    except ValueError as e:
        return get_response({"message" : "La busqueda que intenta realizar no es valida! : {}".format(e.message)}, status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return get_response({"message" : "Se produjo un error inesperado: {}".format(e.message)}, status.HTTP_500_INTERNAL_SERVER_ERROR)

def get_response(request_response_obj, response_status):
    return make_response(json.dumps(request_response_obj), response_status)
