
#b::
	HTTP := ComObjCreate("WinHttp.WinHttpRequest.5.1")
	HTTP.open("GET", "http://localhost:23119/better-bibtex/cayw?format=pandoc")
	HTTP.Send()
	Data := HTTP.ResponseText
	Sleep, 200
	SendInput %Data%
	return