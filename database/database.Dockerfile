FROM postgres:10.1
COPY secrets.json /docker-entrypoint-initdb.d/
COPY database/create-sentiment-table.sql /docker-entrypoint-initdb.d/
COPY database/create-tweet-table.sql /docker-entrypoint-initdb.d/
COPY database/set-up-account.sh /docker-entrypoint-initdb.d/
EXPOSE 5432
