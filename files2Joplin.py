'''
Create a RAW directory for import into Joplin using the files in a given attachment directory.
Sub-directories are ignored.
The RAW directory is named joplin and is created as a sub-directory of the attachment directory.
One note is created for each file where the file name not including the extension is the title and
the body consists of only a link(s) to the attached file.

Required command line inputs:
1) joplin_directory. The absolute path for the Joplin directory.
   It is the directory you are syncing to, not the local directory.
   This is needed to check if randomly generated file names already exist.
2) files_directory. The path for the attachment directory with the files to add to the
   RAW directory. Can be relative to the current directory.

Optional command line inputs:
1) -l or --link_type. Type of link for attachments. Either 'joplin' to add the file to
   joplin_directory/.resource and use a Joplin link in the note, or 'file' to copy the file to
   attach_directory and use a file:// link(s) in the note. Default is 'joplin'. Note that Joplin
   currently does not sync attachments that it manages ('joplin' type links).
   See https://github.com/laurent22/joplin/issues/279. If you know you will want to edit the
   attachments, you probably currently want to use the 'file' type links. However, be aware that the
   files will not be managed by Joplin and therefore not encrypted by Joplin.
2) -a or --attach_dir_file. File containing sets of link names, absolute paths for directories
   (one link name and one directory per line, comma separated) for links with type 'file'.
   Multiple directories may be needed for multiple computers, particularly for different OSs.
   The files are moved to the directory path on the first line, so that directory must make sense
   for the computer you are running this from. This directory will be created if it does not exist.
   Good options for the directories would be sub-directories of the directories Joplin is synced to
   on each computer. Link names should identify the computers corresponding to the directory path.
   Must be specified if link_type is file and ignored otherwise.
'''


import argparse
from datetime import datetime, timezone
import glob
import mimetypes
import os
import shutil
import sys


def split_file_name(file):
    '''
    Description
    ----
    Split file name into name and extension

    Inputs
    ----
    :file: File name with extension.

    Outputs
    ----
    :extension: File name extension.
    :file_name: File name without extension.
    '''

    split = file.split('.')
    extension = '.' + split[-1]
    file_name = '.'.join(split[:-1])

    return (extension, file_name)


def write_attachment_file(file, rand_attach, now):
    '''
    Description
    ----
    Move attachment to RAW directory. Write attachment markdown file.

    Inputs
    ----
    :file: Attachment File name before adding to Joplin
    :rand_attach: Attachment file name after adding to Joplin
    :extension: Attachment file extension
    :now: Current date & time in Joplin format
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


def write_note_file(joplin_directory, file, now, joplin_attach=None, file_attach_list=None):
    '''
    Description
    ----
    Write note markdown file with link to attachment.

    Inputs
    ----
    :file: Attachment file name before adding to Joplin with extension
    :rand_md: Random markdown file name for note
    :now: Current date & time in Joplin format
    :joplin_attach: Attachment file name after adding to Joplin for joplin link type.
    :file_attach_list: List of link names and directories for file link type.
    '''

    assert (not joplin_attach) + (not file_attach_list) == 1, \
        'Must specify exactly one of joplin_attach for joplin type attachments or ' + \
        'file_attach_list for file type attachments'

    (extension, file_name) = split_file_name(file)

    # Random markdown file name
    rand_md = os.urandom(16).hex()
    while os.path.exists(joplin_directory + '/' + rand_md + '.md'):
        rand_md = os.urandom(16).hex()

    with open('joplin/' + rand_md + '.md', 'w') as fid:

        # Title
        fid.write(file_name + '\n\n')

        # Image types which will display in Joplin are given image links.
        if extension in ['.png', '.jpeg', '.jpg']:
            start = '!['
        else:
            start = '['

        # Link(s) to attachment.
        if joplin_attach:

            fid.write(start + file + '](:/' + joplin_attach + ')\n\n')

        else:

            # Make directory if it does not exist
            dir_name = file_attach_list[0][1].strip()
            if not os.path.exists(dir_name):
                os.mkdir(dir_name)

            for attach in file_attach_list:

                # Link text
                link_name = attach[0].strip()

                # Directory name
                dir_name = attach[1].strip()
                if '/' in dir_name and dir_name[-1] != '/':
                    dir_name += '/'
                if '\\' in dir_name and dir_name[-1] != '\\':
                    dir_name += '\\'

                # Replace spaces file name for link
                file = file.replace(' ', '%20')

                # Write file link
                fid.write(start + link_name + '](file://' + dir_name + file + ')\n')

            fid.write('\n')

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


def get_attach_dir_list(attach_dir_file):
    '''
    Description
    ----
    Read link names and directories for file for file type links

    Inputs
    ----
    :attach_dir_file: File name

    Outputs
    ----
    :attach_dir_list: List of lists with each sub-list containing a link name and its directory
    '''

    attach_dir_list = []
    with open(attach_dir_file, 'r') as fid:
        for line in fid:
            attach_dir_list.append(line.strip().split(','))

    return attach_dir_list


def main(joplin_directory, files_directory, link_type='joplin', attach_dir_file=None):
    '''
    main
    '''

    # Get attachment directory list
    if link_type == 'file':
        attach_dir_list = get_attach_dir_list(attach_dir_file)

    # Change directory
    os.chdir(files_directory)

    # List of files
    file_list = glob.glob('*.*')

    # Stop if joplin directory exists. Don't just delete since user may not have imported yet.
    assert not os.path.isdir('joplin'), \
        'joplin directory exists. Import it if necessary, remove it, and run again.'

    # Make RAW directory
    os.mkdir('joplin')
    if link_type == 'joplin':
        os.mkdir('joplin/resources')

    # Current time in Joplin format. Might use file upated times instead of just current time?
    now = datetime.now(timezone.utc).isoformat()[:23] + 'Z'

    # Loop over attachment files
    for file in file_list:

        if link_type == 'joplin':

            # Random markdown file name for attachment
            rand_attach = os.urandom(16).hex()
            while os.path.exists(joplin_directory + '/' + rand_attach + '.md'):
                rand_attach = os.urandom(16).hex()

            # Move attachment to RAW directory. Write attachment markdown file.
            write_attachment_file(file, rand_attach, now)

            # Write note file
            write_note_file(joplin_directory, file, now, joplin_attach=rand_attach)

        else:

            # Move file to first directory in list
            # Rename if there is a file with the same name in that directory
            file_split = file.split('.')
            file_prefix = '.'.join(file_split[:-1])
            file_ext = file_split[-1]
            directory = attach_dir_list[0][1].strip()
            file_path = directory + '/' + file
            cnt = 1
            while os.path.exists(file_path):
                file_new = file_prefix + '_' + str(cnt) + '.' + file_ext
                file_path = directory + '/' + file_new
                cnt += 1
            shutil.move(file, file_path)

            if file_new:
                file = file_new

            write_note_file(joplin_directory, file, now, file_attach_list=attach_dir_list)


if __name__ == '__main__':

    # Command line arguments
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('joplin_directory',
                        help='The absolute path for the Joplin directory. It is the directory ' + \
                             'you are syncing to, not the local directory. This is needed to ' + \
                             'check if randomly generated file names already exist.')
    PARSER.add_argument('files_directory',
                        help='The absolute path for the attachment directory with the files to ' + \
                             'add to the RAW directory.')
    PARSER.add_argument('-l', '--link_type', default='joplin', choices=['joplin', 'file'],
                        help="Type of link for attachments. Either 'joplin' to add the file " + \
                             "to joplin_directory/.resource and use a Joplin link in the note, " + \
                             "or 'file' to copy the file to attach_directory and use a " + \
                             "file:// link in the note. Default is 'joplin'.")
    PARSER.add_argument('-a', '--attach_dir_file', default=None,
                        help="File containing sets of link names, absolute paths for directories " \
                             "(one link name and one directory per line, comma separated) for " + \
                             "links with type 'file'. Multiple directories may be needed for " + \
                             "multiple computers, particularly for different OSs. " + \
                             "The files are moved to the directory path on the first line, " + \
                             "so that directory must make sense for the computer you are " + \
                             "running this from. This directory will be created if it does " + \
                             "not exist. Good options for the directories would be " + \
                             "sub-directories of the directories Joplin is synced to on each " + \
                             "computer. Link names should identify the computers corresponding " + \
                             "to the directory paths.")
    ARGS = PARSER.parse_args()

    if ARGS.link_type == 'file':
        assert ARGS.attach_dir_file, \
            'Name of file (attach_dir_file) with list of directories must be specified for ' + \
            'file link type'

    main(ARGS.joplin_directory, ARGS.files_directory, ARGS.link_type, ARGS.attach_dir_file)
