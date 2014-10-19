#!/usr/bin/python3
from requests import Session
from lxml import html
from re import compile, findall, match
from os import makedirs
from os.path import exists, getmtime
from calendar import timegm
from time import strptime

AUTH_NONE = 0
AUTH_MOODLE = 1

_regex = compile('https\:\/\/www\.moodle\.tum\.de\/mod\/resource\/view\.php\?id\=\d{6}')
_is_file = compile('\.(pdf|txt|py|c|jar)')

def create_filepath(filepath):
	if not exists(filepath):
		makedirs(filepath)

def download_file(session, url, filepath):
	filename = filepath + url[url.rindex('/'):] #ugly as fuck

	if not exists(filename):
		print('[+] ' + filename)
		req = session.get(url)
		with open(filename, 'wb') as fh:
			for chunk in req.iter_content():
				fh.write(chunk)
	else:
		last_mod_file = getmtime(filename)
		last_mod_www = timegm(strptime(session.head(url).headers['Last-Modified'], '%a, %d %b %Y %H:%M:%S %Z'))

		if last_mod_www > last_mod_file:
			print('[M] ' + filename)
			req = session.get(url)
			with open(filename, 'wb') as fh:
				for chunk in req.iter_content():
					fh.write(chunk)

def resolve_direct_link(session, url):
	return session.head(url).headers['Location']

def get_file_links(session, url, base=''):
	links = []
	handle = session.get(url).text

	if url.startswith('https://www.moodle.tum.de/course/'):
		for match in findall(_regex, handle):
			links.append(resolve_direct_link(session, match))
	else:
		hrefs = html.fromstring(handle).xpath('//a/@href')
		for href in hrefs:
			if _is_file.findall(href) != []: # is file link?
				links.append(base + href)

	return links

def get_moodle_session(user, passwd):
	session = Session()

	session.get('https://www.moodle.tum.de/Shibboleth.sso/Login?providerId=https://tumidp.lrz.de/idp/shibboleth&target=https://www.moodle.tum.de/auth/shibboleth/index.php')
	resp = session.post('https://tumidp.lrz.de/idp/Authn/UserPassword', data={'j_username':user, 'j_password':passwd})

	parsed = html.fromstring(resp.text)

	session.post('https://www.moodle.tum.de/Shibboleth.sso/SAML2/POST', data={'RelayState':parsed.forms[0].fields['RelayState'], 'SAMLResponse':parsed.forms[0].fields['SAMLResponse']})

	return session

def main(AUTH_MOODLE, user, passwd, url, files):
	session = get_moodle_session(user, passwd)
	links = get_file_links(session, url)

	for link in links:
		for ft in files:
			reg = compile(ft[0])
			match = reg.findall(link)
			if match != []:
				create_filepath(ft[1])
				download_file(session, link, ft[1] + '/' + match[0])

def main(mode, url, files, user='', passwd='', base=''):
	session = None
	if mode == AUTH_MOODLE:
		session = get_moodle_session(user, passwd)
	else:
		session = Session()

	links = get_file_links(session, url, base)

	for link in links:
		for ft in files:
			reg = compile(ft[0])
			match = reg.findall(link)
			if match != []:
				create_filepath(ft[1])
				download_file(session, link, ft[1])
