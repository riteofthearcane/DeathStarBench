.PHONY: proto data run

# NEVER Run Proto
# To run edited go code just use the run command below
proto:
	for f in services/**/proto/*.proto; do \
		protoc --go_out=plugins=grpc:. $$f; \
		echo compiled: $$f; \
	done

data:
	go-bindata -o data/bindata.go -pkg data data/*.json

setup:
	docker kill $(docker container ps -a -q)
	eval $(luarocks path --bin)
	
run:
	docker-compose build
	docker-compose up --remove-orphans -d
