.PHONY: run
run:
	docker compose up -d

.PHONY: rerun
rerun:
	docker compose up --build --force-recreate -d