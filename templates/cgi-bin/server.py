#!/usr/bin/python
# coding=utf-8
# Import modules for CGI handling
import cgi, os
import cgitb;

cgitb.enable()
form = cgi.FieldStorage()
# Get filename here.
fileitem = form['uploadfile']
# Test if the file was uploaded
if fileitem.filename:
    # directory traversal attacks
    fn = os.path.basename(fileitem.filename)
    # get store path  and save it
    open(os.getcwd() + '/files/' + fn, 'wb').write(fileitem.file.read())

    message = 'The file "' + fn + '" was uploaded successfully'

else:
    message = 'No file was uploaded'

print('Content-type:text/html \n\n')
print('file %s' % message)
