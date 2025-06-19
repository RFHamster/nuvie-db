format:
	@blue .
	@isort .

migrations:
	@sh scripts/make_migrations.sh -e ".env" -n "$(name)" -s "$(schema)"

apply:
	@sh scripts/apply_migrations.sh -e ".env"

test:
		$(shell pytest --test-alembic)