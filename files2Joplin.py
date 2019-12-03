'''
Create a RAW directory for import into Joplin using the files in an given attachment directory.
Sub-directories are ignored.
The RAW directory is named joplin and is created as a sub-directory of the attachment directory.
One note is created for each file where the file name not including the extension is the title and
the body consists of only a link to the attached file.

Command line inputs:
    The Joplin directory is needed to check if randomly generated file names already exist.
    The attachment directory with the files to add to the RAW directory.
'''

from datetime import datetime, timezone
import glob
import os
import shutil
import sys

# Inputs
joplin_directory = sys.argv[1]
files_directory = sys.argv[2]

# Change directory
os.chdir(files_directory)

# List of files
file_list = glob.glob('*.*')

# Make RAW directory
try:
    os.mkdir('joplin')
    os.mkdir('joplin/resources')
except FileExistsError:
    # Stop if joplin directory exists. Don't just delete since user may not have imported it yet.
    print('joplin directory exists. Import it if necessary, remove it, and run again.')

# Current time in Joplin format. Might use file attributes for times instead of just current time?
now = datetime.now(timezone.utc).isoformat()[:23] + 'Z'

# Loop over attachment files
for file in file_list:

    # Attachment file name and extension
    split = file.split('.')
    extension = split[-1]
    file_name = '.'.join(split[:-1])

    # Attachment file size
    file_size = os.path.getsize(file)

    # Attachment markdown file

    # Random markdown file name
    rand_attach = os.urandom(16).hex()
    while os.path.exists(joplin_directory + '/' + rand_attach + '.md'):
        rand_attach = os.urandom(16).hex()

    # Move attachment to RAW directory.
    # Extension here is mainly for testing purposes.
    # Attachments in Joplin don't have extensions and extension seems to be ignored on import.
    shutil.move(file, 'joplin/resources/' + rand_attach + '.' + extension)

    # Write markdown file
    with open('joplin/' + rand_attach + '.md', 'w') as f:

        f.write(file + '\n\n')
        f.write('id: ' + rand_attach + '\n')

        if extension == 'pdf':
            f.write('mime: application/pdf\n')
        elif extension == 'txt':
            f.write('mime: text/plain\n')
        else:
            f.write('mime: \n')

        f.write('filename: ' + file + '\n')

        f.write('created_time: ' + now + '\n')
        f.write('updated_time: ' + now + '\n')
        f.write('user_created_time: ' + now + '\n')
        f.write('user_updated_time: ' + now + '\n')

        f.write('file_extension: \n')

        f.write('encryption_cipher_text: \n')
        f.write('encryption_applied: 0\n')
        f.write('encryption_blob_encrypted: 0\n')

        f.write('size: ' + str(file_size) + '\n')
        f.write('type_: 4')

    # Markdown file with link to attachment

    # Random markdown file name
    rand_md = os.urandom(16).hex()
    while os.path.exists(joplin_directory + '/' + rand_attach + '.md'):
        rand_md = os.urandom(16).hex()

    # Write markdown file
    with open('joplin/' + rand_md + '.md', 'w') as f:

        # Title and link to attachment
        f.write(file_name + '\n\n')
        f.write('[' + file + '](:/' + rand_attach + ')\n\n')

        # Other data
        f.write('id: ' + rand_md + '\n')
        f.write('parent_id: \n') # ' + parent_id + '

        f.write('created_time: ' + now + '\n')
        f.write('updated_time: ' + now + '\n')

        f.write('is_conflict: 0\n')

        f.write('latitude: 0.00000000\n')
        f.write('longitude: 0.00000000\n')
        f.write('altitude: 0.0000\n')

        f.write('author: \n')
        f.write('source_url: \n')

        f.write('is_todo: 0\n')
        f.write('todo_due: 0\n')
        f.write('todo_completed: 0\n')

        f.write('source: joplin-desktop\n')
        f.write('source_application: net.cozic.joplin-desktop\n')
        f.write('application_data:\n')
        f.write('order: 0\n')

        f.write('user_created_time: ' + now + '\n')
        f.write('user_updated_time: ' + now + '\n')

        f.write('encryption_cipher_text: \n')
        f.write('encryption_applied: 0\n')

        f.write('markup_language: 1\n')
        f.write('type_: 1')
