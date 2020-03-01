# files2Joplin
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
