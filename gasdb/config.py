# URI for db connection TODO: dockerize and use that as db
DB_URI = 'postgres+psycopg2://postgres:postgres@db:5432/gasdb'
CSV_PLACE = 'Data/impianti.csv'  # source for both csv
# TODO: replace both with the URL source, maybe pass this as env variable
CSV_PRICE = 'Data/prezzi.csv'
