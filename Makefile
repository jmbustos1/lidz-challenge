.PHONY: django postgres dockerup

django:
	docker exec -it lidz-django /bin/bash

postgres:
	docker exec -it lidz-postgres /bin/bash

dockerup:
	sudo docker-compose up
