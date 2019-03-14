# 7547.Taller de desarrollo de Proyectos 2 - TP0: Server.

# Run
	> docker build --tag=${container-name} .
	> docker run -p ${local_port}:${exp_port} ${container-name}

# API

	To search for books make a GET request to /v1/books?key_words=${kw} with the desired query key words. 

	To retrieve a specific book's data make a GET request to /v1/books?id=${book_id} providing the specified book id. 
