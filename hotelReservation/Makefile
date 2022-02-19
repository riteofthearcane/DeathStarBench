.PHONY: proto data run

# NEVER RUN THE proto COMMAND
# To compile code just edit the go files in the service folder 
# and build with the run command
proto:
	for f in services/**/proto/*.proto; do \
		protoc --go_out=plugins=grpc:. $$f; \
		echo compiled: $$f; \
	done

data:
	go-bindata -o data/bindata.go -pkg data data/*.json

run:
	docker-compose build
	docker-compose up --remove-orphans -d
