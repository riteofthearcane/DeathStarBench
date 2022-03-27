.PHONY: proto data run

# DO NOT RUN PROTO
proto:
	for f in services/**/proto/*.proto; do \
		protoc --go_out=plugins=grpc:. $$f; \
		echo compiled: $$f; \
	done

data:
	go-bindata -o data/bindata.go -pkg data data/*.json

setup:
	docker kill $$(docker container ls -q)

run:
	docker-compose build
	docker-compose up --remove-orphans -d

# RUN THIS TO FIX LUA ISSUE: eval $(luarocks path --bin)
