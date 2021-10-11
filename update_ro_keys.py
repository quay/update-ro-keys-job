import os
import pymysql
from urllib.parse import unquote
import traceback
import json
from datetime import datetime, timedelta

password_decoded = unquote(os.environ.get('DB_PASSWORD'))

conn = pymysql.connect(host=os.environ.get('DB_HOST'),
            user=os.environ.get('DB_USER'),
            password=password_decoded,
            db=os.environ.get('DB_NAME'),
            cursorclass=pymysql.cursors.DictCursor)

KEY_NAME = os.environ.get('KEY_NAME', 'quay-readonly')

# Default expiry 1 year
EXPIRY_DATE = os.environ.get('EXPIRY_DATE',(datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')) + " 00:00:00" 



def update_ro_keys():
    kid_data = open("/conf/stack/quay-readonly.kid").read()
    jwk_data = open("/conf/stack/quay-readonly.pem").read()
    # kid_data = "kid_data"
    # jwk_data = "jwk_data"
    
    try:
        with conn.cursor() as cur:
            # Insert the key data
            # Fetch the servickey id of the newly inserted key
            cur.execute("SELECT id from servicekey WHERE name=%s " , (KEY_NAME))
            servicekey = cur.fetchone()
 
            if servicekey:
                # Update
                q = ("UPDATE servicekey "
                        "SET expiration_date=%s WHERE name=%s")
                cur.execute(q, (EXPIRY_DATE, KEY_NAME))
                conn.commit()

            else:
                # New key 
                q = ("INSERT INTO servicekey "
                     "(name, service, metadata, kid, jwk, expiration_date) "
                    'VALUES (%s, "quay", "{}", %s, %s, %s)')
                cur.execute(q , (KEY_NAME, kid_data, jwk_data, EXPIRY_DATE))
                conn.commit()
                
                # Fetch the servickey id of the newly inserted key
                cur.execute("SELECT id from servicekey WHERE name=%s " , (KEY_NAME))
                servicekey = cur.fetchone()
                print(servicekey)
                servicekey_id = servicekey['id']

                NOTES = 'Quay RO service key %s' % KEY_NAME
                cur.execute("INSERT INTO servicekeyapproval (approval_type, notes) VALUES ('Super User API', %s)", (NOTES))
                conn.commit()

                # Fetch the approval id of the newly inserted key
                cur.execute("SELECT id from servicekeyapproval WHERE notes=%s",  (NOTES))
                approvalkey = cur.fetchone()
                print(approvalkey)
                approvalkey_id = approvalkey['id']

                cur.execute("""UPDATE servicekey set approval_id=%d where id=%d""" % (approvalkey_id, servicekey_id))
                conn.commit()

    except Exception as e:
        print(cur._last_executed)
        print("ERROR: Unable to Add service key")
        print(e)
        traceback.print_exc()
    finally:
        conn.close()


update_ro_keys()
