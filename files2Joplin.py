'''
Create a RAW directory for import into Joplin using the files in a given attachment directory.
Sub-directories are ignored.
The RAW directory is named joplin and is created as a sub-directory of the attachment directory.
One note is created for each file where the file name not including the extension is the title and
the body consists of only a link to the attached file.

Command line inputs:
1) The absolute path for the Joplin directory.
   It is the directory you are syncing to, not the local directory.
   This is needed to check if randomly generated file names already exist.
2) The absolute path for the attachment directory with the files to add to the RAW directory.

**WARNING: If you plan on editing attachments, you should check that Joplin actually syncs
attachments after they are edited before using this. I have had problems with that in
Joplin 1.0.175 & 1.0.178. If your attachments are not syncing after editing, an alternative would
be to link to the files directly using file:// in front of the file paths. I may add an option for
this if Joplin does not fix this.**
'''

from datetime import datetime, timezone
import glob
import mimetypes
import os
import shutil
import sys


def split_file_name(file):
    '''
    Split file name into name and extension
    '''

    # Attachment file name and extension
    split = file.split('.')
    extension = '.' + split[-1]
    file_name = '.'.join(split[:-1])

    return (extension, file_name)


def write_attachment_file(file, rand_attach, now):
    '''
    Move attachment to RAW directory. Write attachment markdown file.

    Inputs
    ---
    :file: Attachment File name before adding to Joplin
    :rand_attach: Attachment file name after adding to Joplin
    :extension: Attachment file extension
    :now: Current date & time
    '''

    (extension, _) = split_file_name(file)

    # Attachment file size
    file_size = os.path.getsize(file)

    # Move file
    shutil.move(file, 'joplin/resources/' + rand_attach)

    # Write markdown file
    with open('joplin/' + rand_attach + '.md', 'w') as fid:

        fid.write(file + '\n\n')
        fid.write('id: ' + rand_attach + '\n')

        try:
            mimetype = mimetypes.types_map[extension]
        except KeyError:
            mimetype = ''

        fid.write('mime: ' + mimetype + '\n')

        fid.write('filename: ' + file + '\n')

        fid.write('created_time: ' + now + '\n')
        fid.write('updated_time: ' + now + '\n')
        fid.write('user_created_time: ' + now + '\n')
        fid.write('user_updated_time: ' + now + '\n')

        fid.write('file_extension: \n')

        fid.write('encryption_cipher_text: \n')
        fid.write('encryption_applied: 0\n')
        fid.write('encryption_blob_encrypted: 0\n')

        fid.write('size: ' + str(file_size) + '\n')
        fid.write('type_: 4')


def write_note_file(joplin_directory, file, rand_attach, now):
    '''
    Write note markdown file with link to attachment.

    Inputs
    ---
    :file: Attachment file name before adding to Joplin without extension
    :rand_md: Random markdown file name for note
    :rand_attach: Attachment file name after adding to Joplin
    :extension: Attachment file extension
    :now: Current date & time
    '''

    (extension, file_name) = split_file_name(file)

    # Random markdown file name
    rand_md = os.urandom(16).hex()
    while os.path.exists(joplin_directory + '/' + rand_md + '.md'):
        rand_md = os.urandom(16).hex()

    with open('joplin/' + rand_md + '.md', 'w') as fid:

        # Title and link to attachment.
        # Image types which will display in Joplin are given image links.
        fid.write(file_name + '\n\n')
        if extension in ['.png', '.jpeg', '.jpg']:
            fid.write('![' + file + '](:/' + rand_attach + ')\n\n')
        else:
            fid.write('[' + file + '](:/' + rand_attach + ')\n\n')

        # Other data
        fid.write('id: ' + rand_md + '\n')
        fid.write('parent_id: \n') # ' + parent_id + '

        fid.write('created_time: ' + now + '\n')
        fid.write('updated_time: ' + now + '\n')

        fid.write('is_conflict: 0\n')

        fid.write('latitude: 0.00000000\n')
        fid.write('longitude: 0.00000000\n')
        fid.write('altitude: 0.0000\n')

        fid.write('author: \n')
        fid.write('source_url: \n')

        fid.write('is_todo: 0\n')
        fid.write('todo_due: 0\n')
        fid.write('todo_completed: 0\n')

        fid.write('source: joplin-desktop\n')
        fid.write('source_application: net.cozic.joplin-desktop\n')
        fid.write('application_data:\n')
        fid.write('order: 0\n')

        fid.write('user_created_time: ' + now + '\n')
        fid.write('user_updated_time: ' + now + '\n')

        fid.write('encryption_cipher_text: \n')
        fid.write('encryption_applied: 0\n')

        fid.write('markup_language: 1\n')
        fid.write('type_: 1')


def main(joplin_directory, files_directory):
    '''
    main
    '''

    # Change directory
    os.chdir(files_directory)

    # List of files
    file_list = glob.glob('*.*')

    # Stop if joplin directory exists. Don't just delete since user may not have imported yet.
    assert not os.path.isdir('joplin'), \
        'joplin directory exists. Import it if necessary, remove it, and run again.'

    # Make RAW directory
    os.mkdir('joplin')
    os.mkdir('joplin/resources')

    # Current time in Joplin format. Might use file upated times instead of just current time?
    now = datetime.now(timezone.utc).isoformat()[:23] + 'Z'

    # Loop over attachment files
    for file in file_list:

        # Random markdown file name for attachment
        rand_attach = os.urandom(16).hex()
        while os.path.exists(joplin_directory + '/' + rand_attach + '.md'):
            rand_attach = os.urandom(16).hex()

        write_attachment_file(file, rand_attach, now)
        write_note_file(joplin_directory, file, rand_attach, now)


if __name__ == '__main__':

    # Inputs
    JOPLIN_DIRECTORY = sys.argv[1]
    FILES_DIRECTORY = sys.argv[2]

    main(JOPLIN_DIRECTORY, FILES_DIRECTORY)
