import sys
from PIL import Image
import os
import io

#arguments
#full name admin AD (admin@domain.local)
admin_login = str(sys.argv[1])
#password admin AD
admin_pass = str(sys.argv[2])
#user login for change foto
user_login = str(sys.argv[3])
#path for foto.jpg
foto = str(sys.argv[4])

image = Image.open(foto)
#thumbnail photo
image.thumbnail(size=(96,96))
#image.thumbnail(size=(300,300))

#jpg to OctetString
buf = io.BytesIO()
image.save(buf,'jpeg')
img = buf.getvalue()
#bytes to OctetString !!!
bimg = [img]

img_size = len(img)
if img_size > 102400 :
    print("Big size of picture: ",foto ,img_size ," > 100 kB")
    sys.exit(1)

###work to AD
from ms_active_directory import ADDomain
domain = ADDomain(domain='domain.local',site='domain.local',ldap_servers_or_uris=['dc1.domain.local','dc2.domain.local'])

try:
    #create connect
    session = domain.create_session_as_user(admin_login, admin_pass) 
    #save foto to AD
    success = session.overwrite_attribute_for_user(user_login,'thumbnailPhoto',bimg)
    print(success)
except Exception as e:
    #print(type(e))
    print(e.args)
