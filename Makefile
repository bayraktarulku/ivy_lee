run:
	@python3 run.py

install:
	@pip3 install -r requirements.txt

reset:
	@rm -f app/storage/sqlite_db.py

