
.PHONY: example
example:
	cat example.skema | skema gen typescript > play.ts
	cat example.skema | skema gen python > play.py
	cat example.skema | skema gen jsonschema > play.json
	cat example.skema | skema gen graphql > play.graphql