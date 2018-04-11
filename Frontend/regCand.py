import cgi
form = cgi.FieldStorage()
searchterm =  form.getvalue('name')
manifesto = form.getvalue('manifesto')
election = form.getvalue('elect')
