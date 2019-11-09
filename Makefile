
.PHONY: example
example:
	cat example.skema | python -m skema gen typescript > play.ts
	cat example.skema | python -m skema gen python > play.py
	cat example.skema | python -m skema gen jsonschema > play.json
	cat example.skema | python -m skema gen graphql > play.graphql