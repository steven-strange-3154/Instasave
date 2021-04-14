"""Instagram public post downloader by crawling instasaveonline.com"""
__name__ = "instasave"
__author__ = "Steven Strange"
__email__ = "stevenstrange31545nk74@gmail.com"
__version__ = "1.0"

from urllib.request import Request, URLError, HTTPError, urlopen
from urllib.parse import urlencode
from bs4 import BeautifulSoup as BS
import argparse, re, os, humanize

parser = argparse.ArgumentParser(description="Instagram post downloader using instasaveonline.com")
parser.add_argument('url', help="Post link")
args = parser.parse_args()

if args.url.startswith('https://www.instagram.com'):
    header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
    fetcher = 'https://instasaveonline.com'
    data = {'link': args.url, 'submit': True}
    data = urlencode(data).encode()

    try:
        print('Fetching file links from instasaveonline.com')
        req = Request(fetcher, data, header)
        page = urlopen(req)
    except (URLError, HTTPError) as err:
        print("An error occured, halting")
        exit(1)
    else:
        data = page.read().decode('utf-8')
        data = BS(data, 'html.parser')
    finally:
        data = data.find('div', {'class': 'dlsection'})
        if data:
            links = data.findAll('a')
            links = [x['href'] for x in links]
            file_name = re.compile('(\d+_\d+_\d+_n.jpg)')
            for link in links:
                name = file_name.search(link)
                if name:
                    try:
                        image = Request(link, None, header)
                        image = urlopen(image).read()
                    except (URLError, HTTPError) as err:
                        print(f'Failed to download {name.group()}')
                        continue
                    else:
                        with open(name.group(), 'wb') as wf:
                            wf.write(image)
                            print(f'Saved: {name.group()} ({humanize.naturalsize(len(image))})')
                            wf.close()
            os.system('termux-media-scan ./')
 