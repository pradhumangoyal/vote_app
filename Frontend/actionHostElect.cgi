import cgi

if __name__ == '__main__':
	form = cgi.FieldStorage()
	title = form.getvalue('elec')
	hostId = form.getvalue('vtr')
	startTime = form.getvalue('stime')
	endTime = form.getvalue('etime')

	print("startTime ==> ")
	print(startTime)