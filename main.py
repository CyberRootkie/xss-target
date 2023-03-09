'''
TODO
- Ne pas crawler si on est sur le même domaine 
- Mettre des couleurs
- Enregistrer les résultats KO
'''

import requests 
from bs4 import BeautifulSoup as bs
import tldextract
import os

f = open('urls.txt', 'r')
dic_dom_tested = {}

for url in f:
    url = url.strip()
    print(f'Crawling {url}...')
    try:
        r = requests.get(url, timeout=10)
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
            tmp = tldextract.extract(url)
            dom = f"{tmp.domain}.{tmp.suffix}"
            if dom in dic_dom_tested:
                pass
            else:
                r_ping = os.system(f"ping -c 1 {dom} > /dev/null")
                if not r_ping:
                    print(dom, 'OK')
                    dic_dom_tested[dom] = 'OK'
                else:
                    print(dom, 'KO')
                    dic_dom_tested[dom] = 'KO'

f.close()