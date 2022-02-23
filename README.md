**Install PostgresSQL client, on Mac:**

`brew install libpq`

**First Launch**

Edit env according to your needs.

Launch docker-compose:

`docker-compose -f docker-compose.prod.yml up -d --build `

`docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
`

project is going to be available on http://0.0.0.0:8000/shorten_url/

Bring down containers (and the associated volumes with the -v flag):


`docker-compose -f docker-compose.prod.yml down -v `
