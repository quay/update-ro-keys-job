# Update RO Keys

This script updates the Quay.io DB to add RO keys. The Keys 
to be added are passed in as a `Secret` monted on the container

Environment variables

| Variable  | Description |
| --- | --- |
|DB_HOST| Database hostname |  
|DB_USER | Database username | 
|DB_PASSWORD | Database password
|KEY_NAME| Name of the key that needs to be inserted | 
|EXPIRY_TIME | Expiry time of key in `YYYY-MM-DD` fromat | 
