# files2Joplin
Create a RAW directory for import into Joplin using the files in a given attachment directory.
Sub-directories are ignored.
The RAW directory is named joplin and is created as a sub-directory of the attachment directory.
One note is created for each file where the file name not including the extension is the title and
the body consists of only a link to the attached file.

Command line inputs:
1) The Joplin directory is needed to check if randomly generated file names already exist.
2) The attachment directory with the files to add to the RAW directory.
