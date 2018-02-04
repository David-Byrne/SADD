cd /docker-entrypoint-initdb.d/

passwordline=`grep -oE '"dbPassword":"(.*?[^\\])"' secrets.json`
# Reads the dbPassword entry in secrets.json, via regex

password=${passwordline:14:`expr length $passwordline - 15`}
# Extracts out the password from that line

psql -U postgres -d postgres -c "alter user postgres with password '$password;'"
