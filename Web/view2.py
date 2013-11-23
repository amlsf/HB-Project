"GET /incoming/sms HTTP/1.0"

FORM ImmutableMultiDict([])

ARGS ImmutableMultiDict([
	('FromZip', u'08722'), 
	# ('From', u'+17328413670'), 
	('FromCountry', u'US'), 
	('FromCity', u'METUCHEN'), 
	('ApiVersion', u'2010-04-01'), 
	('To', u'+17327346228'), 
	('NumMedia', u'0'), 
	('AccountSid', u'ACcd18bc05976f7bea45e9a39729140644'), 
	('SmsSid', u'SM05488d6f8fad0e2741b884b4c89b9760'), 
	('ToCity', u'WOODBRIDGE'), 
	('FromState', u'NJ'), 
	('SmsMessageSid', u'SM05488d6f8fad0e2741b884b4c89b9760'), 
	# ('Body', u'Hey'), 
	('MessageSid', u'SM05488d6f8fad0e2741b884b4c89b9760'), 
	('SmsStatus', u'received'), 
	('ToZip', u'07095'), 
	('ToCountry', u'US'), 
	('ToState', u'NJ')
])

"GET /incoming/sms?AccountSid=ACcd18bc05976f7bea45e9a39729140644&MessageSid=SM05488d6f8fad0e2741b884b4c89b9760&Body=Hey&ToZip=07095&ToCity=WOODBRIDGE&FromState=NJ&ToState=NJ&SmsSid=SM05488d6f8fad0e2741b884b4c89b9760&To=%2B17327346228&ToCountry=US&FromCountry=US&SmsMessageSid=SM05488d6f8fad0e2741b884b4c89b9760&ApiVersion=2010-04-01&FromCity=METUCHEN&SmsStatus=received&NumMedia=0&From=%2B17328413670&FromZip=0872