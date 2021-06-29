import os
import time
from imbox import Imbox # pip3 install imbox
import traceback

import config.config as cnf

config = cnf.Config()

HOST = config.mail_host
USERNAME = config.mail_user
PASSWORD = config.mail_password
MAIL_FROM = config.mail_from
SAVE_FOLDER_CAMERA = config.save_image_folder
CHECK_MAIL_SECONDS = config.seconds_check_email

if __name__ == "__main__":
    module_name = "camera_receiver"
    print("START - EXECUTION EVERY {0} seconds.".format(CHECK_MAIL_SECONDS))

    while True:
        # enable less secure apps on your google account
        # https://myaccount.google.com/lesssecureapps

        try:
            if not os.path.isdir(SAVE_FOLDER_CAMERA):
                os.makedirs(SAVE_FOLDER_CAMERA, exist_ok=True)
                
            mail = Imbox(HOST, username=USERNAME, password=PASSWORD, ssl=True, ssl_context=None, starttls=False)
            #messages = mail.messages() # defaults to inbox
            messages = mail.messages(unread=True, sent_from=MAIL_FROM)

            for (uid, message) in messages:
                mail.mark_seen(uid) # optional, mark message as read

                for idx, attachment in enumerate(message.attachments):
                    try:
                        att_fn = attachment.get('filename')
                        download_path = f"{SAVE_FOLDER_CAMERA}/{att_fn}"
                        print(download_path)
                        with open(download_path, "wb") as fp:
                            fp.write(attachment.get('content').read())
                    except:
                        print(traceback.print_exc())

            mail.logout()
        except Exception as ex:
            error_text = "Exception in {0}: {1}".format(module_name, ex)
            print(error_text)
        
        print("SLEEP {0}".format(CHECK_MAIL_SECONDS))
        time.sleep(CHECK_MAIL_SECONDS)