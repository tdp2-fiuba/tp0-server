# 7547.Taller de desarrollo de Proyectos 2 - TP0: Server.

Try this app at: https://tp0-server.herokuapp.com.

# Run
	> docker build --tag=${container-name} .
	> docker run -p ${local_port}:${exp_port} ${container-name}

# API

	To search for books make a GET request to /v1/books?key_words=${kw} with the desired query key words. 

	OPTIONAL PARAMETERS:
		- start_index: return query results starting from the indicated index.
		- max_results: maximum amount of results to be returned.
		- sorted: if set to true, this will ensure the resulting book list is ordered by title alphabetically.
