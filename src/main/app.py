import os
import json
import requests
from flask import Flask, jsonify, make_response, request
from flask_api import status
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

books_base_url = "https://www.googleapis.com/books/v1"
#books_api_token = "AIzaSyCOeFB-k532HjyVfsYJK9pKKx9UGDoqq5g"

SEARCH_PARAM = "key_words"
ID_PARAM = "id"

@app.route("/v1/books")
@cross_origin()
def query_books():
    if (not (request.args.has_key(SEARCH_PARAM) or request.args.has_key(ID_PARAM))):
        return get_response({"message" : "Se debe ingresar algun parametro de busqueda valido!"}, status.HTTP_400_BAD_REQUEST)

    try:
        url = books_base_url + "/volumes"
        query_param = request.args.get(SEARCH_PARAM, request.args.get(ID_PARAM))

        if (request.args.has_key(SEARCH_PARAM)):
            response = requests.get(url + "?q={}".format(query_param), headers = {"key" : os.environ['BOOKS_API_TOKEN']});
            book_list = response.json()["items"] if (response.json()["totalItems"] > 0) else []
            return get_response({"items" : book_list}, status.HTTP_200_OK)
        response = requests.get(url + "/" + query_param, headers = {"key" : os.environ['BOOKS_API_TOKEN']});
        return get_response({"data" : response.json()}, status.HTTP_200_OK)
    except ValueError:
        return get_response({"message" : "La busqueda que intenta realizar no es valida!"}, status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return get_response({"message" : "Se produjo un error inesperado: {}".format(e.message)}, status.HTTP_500_INTERNAL_SERVER_ERROR)

def get_response(request_response_obj, response_status):
    return make_response(json.dumps(request_response_obj), response_status)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
