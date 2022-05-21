serve:
	uvicorn pack.example_fastapi:app --port 8001 --reload

lint:
	pyflakes pack
	mypy --check-untyped-defs -p pack

get:
	http --json get localhost:8001/items/

post:
	http --json post localhost:8001/items/ name=foo price=12

bad-post:
	http --json post localhost:8001/items/ shame=foo
