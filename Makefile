
.PHONY: example
example:
	cat example.skema | python -m skema gen typescript > play.ts
	cat example.skema | python -m skema gen python > play.py
	cat example.skema | python -m skema gen jsonschema > play.json
	cat example.skema | python -m skema gen graphql > play.graphql

jsonschema:
	cat jsonschema.skema | python -m skema gen python > skema/reconstruct/schema_types.py
	cat jsonschema.skema | python -m skema gen jsonschema > play_sjon.json

print:
	cat jsonschema.skema | python -m skema tree

pipes:
	cat play.graphql | python -m skema from graphql