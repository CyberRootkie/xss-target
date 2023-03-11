'''
TODO
- Utiliser une méthode plus efficace que le ping (trop de faux positifs)
- Factoriser le code
- Gérer des paramètres ligne de commande
'''

import requests 
from bs4 import BeautifulSoup as bs
import tldextract
import os
from colorama import init
from termcolor import colored

f = open('list_dom.txt', 'r')
f2 = open('results.txt', 'w')
dic_dom_tested = {}

headers = {'user-agent': 'XSS_Bot', 'Referer': 'https://www.google.fr'}
try:
    for domain_name in f:
        domain_name = domain_name.strip()
        url = f"http://www.{domain_name}"
        print(f'Crawling {url}...')
        try:
            r = requests.get(url, timeout=10, headers=headers)
        except requests.exceptions.ConnectTimeout:
            continue
        except requests.exceptions.SSLError:
            continue
        except:
            continue
        html = r.text
        soup = bs(html, "html.parser")  


        for script in soup.find_all('script'):
            url_script = script.attrs.get('src')
            if url_script is not None:
                tmp = tldextract.extract(url_script)
                dom_externe = f"{tmp.domain}.{tmp.suffix}"
                statut = 'OK'
                if dom_externe in dic_dom_tested:
                    statut = dic_dom_tested[dom_externe]
                elif domain_name == dom_externe:
                    pass
                else:
                    r_ping = os.system(f"ping -c 1 {dom_externe} > /dev/null")
                    if not r_ping:
                        statut = 'OK'
                        dic_dom_tested[dom_externe] = 'OK'
                    else:
                        statut = 'KO'
                        dic_dom_tested[dom_externe] = 'KO'
                if statut == 'OK':
                    print(colored(f"{dom_externe} in {domain_name}", 'green'))
                else:
                    f2.write(f"{dom_externe};{domain_name}\n")
                    f2.flush()
                    print(colored(f"{dom_externe} in {domain_name}", 'red'))
except KeyboardInterrupt:
    print('[!] Detected CTRL+C ! ')
    f.close()
    f2.close()
    exit()

f.close()
f2.close()