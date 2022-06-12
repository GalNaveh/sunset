import cgitb 
cgitb.enable()

cgitb.start_response('200 OK', [('Content-Type', 'text/html')])

print("<b> Hello, World</b>")