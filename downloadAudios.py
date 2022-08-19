import dropbox
import os
from time import sleep

sleep(120)

folders = [
    '/button2/', 
    '/button3/', 
    '/button4/',
    '/button5/',
    '/button6/',
    '/button7/',
    '/button8/',
    '/button9/'
]

dbx = dropbox.Dropbox(
            app_key = 	# ADD YOUR DROPBOX APP KEY (ex. 'xxxxxxxxxxx')
            app_secret = # ADD YOUR DROPBOX APP KEY (ex. 'xxxxxxxxxxxxxxxxxxx')
            oauth2_refresh_token = # ADD YOUR DROPBOX oauth2 refresh token here (ex. 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
                                   # see https://developers.dropbox.com/oauth-guide
        )

def process_folder_entries(current_state, entries):
    for entry in entries:
        if isinstance(entry, dropbox.files.FileMetadata):
            current_state[entry.path_lower] = entry
        elif isinstance(entry, dropbox.files.DeletedMetadata):
            current_state.pop(entry.path_lower, None) # ignore KeyError if missing
    return current_state

def fileDownload():
    for folder in folders:
        response = dbx.files_list_folder(path=folder)
        files = process_folder_entries({}, response.entries)
        dirList = os.listdir('/home/pizero/recorder' + folder)
        downloads = []
        for entry in files.values():
            p = entry.name
            if p not in dirList:
                print(p + ' downloading...')
                dbx.files_download_to_file(download_path='/home/pizero/recorder' + folder + 'D' + p, path=folder + p, rev=None)
                os.rename('/home/pizero/recorder' + folder + 'D' + p, '/home/pizero/recorder' + folder + p)
                print('Done!')
            downloads.append(p)
            print(downloads)

        for d in dirList:
            if d not in downloads:
                os.remove('/home/pizero/recorder' + folder + d)
                print(d + " deleted.")
    
    downloads = []
    print("All new files have been downloaded.")

if __name__ == "__main__": fileDownload()
