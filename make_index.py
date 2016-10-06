#!/usr/bin/python3

import os
import re
import html
import calendar

nums = list(int(s) for s in os.listdir("predictionbook"))
nums.sort()

print('''

<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
	<title>All public predictions on predictionbook.com</title>
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<style>
		body {
			font-family: sans-serif;
		}
		a {
			text-decoration: none;
			color: #0645ad;
		}
		table, td {
			border: 0;
		}
		td {
			white-space: nowrap;
		}
	</style>
</head>
<body>
<table>
<tr><td>#</td><td>predicted</td><td>known</td><td>user</td><td>prediction</td></tr>
''')

def get_ymd_and_url(date):
	ymd  = date.split()[0]
	year, month, day = ymd.split('-')
	day = day.lstrip('0')
	month_name = calendar.month_name[int(month)]
	date_url = 'https://en.wikipedia.org/wiki/Portal:Current_events/%s_%s_%s' % (year, month_name, day)
	return ymd, date_url

for n in nums:
	with open("predictionbook/%s" % (n,)) as f:
		content = f.read()
		if '<div id="notice">You are not authorized to perform that action</div>' in content:
			continue
		try:
			title = re.findall("<title>(.*?)</title>", content)[0]
		except IndexError:
			continue
		title = html.unescape(title)
		prediction = title.replace("PredictionBook: ", "", 1)
		user_url, username = re.findall('<a class="user" href="(.*?)">(.*?)</a>', content)[0]
		user_url = 'http://predictionbook.com' + user_url

		url = 'http://predictionbook.com/predictions/%s' % (n,)

		predicted_date = re.findall('<span title="(.*?)" class="date">', content)[0]
		predicted_ymd, date_url = get_ymd_and_url(predicted_date)

		known_date = re.findall('known <span title="(.*?)" class="date">', content)[0]
		known_ymd, _ = get_ymd_and_url(known_date)

		print('<tr><td><a href="%s">%s</a></td><td><a href="%s">%s</a></td><td>%s</td><td><a href="%s">%s</a></td><td><a href="%s">%s</a></td></tr>' % (
			url, n, date_url, predicted_ymd, known_ymd, user_url, username, url, html.escape(prediction)))

print('''
</table>
</body>
</html>
''')
