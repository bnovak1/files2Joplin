# files2Joplin
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
Joplin 1.0.175. If your attachments are not syncing after editing, an alternative would be to link
to the files directly using file:// in front of the file paths. I may add an option for this if the
next version of Joplin does not fix this.**
