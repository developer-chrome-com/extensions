#!/usr/bin/env python

from HTMLParser import HTMLParser
import logging
import os
import os.path
import re
from shutil import rmtree
from urllib import urlretrieve
import xml.etree.ElementTree as ET

origin_url = 'https://developer.chrome.com'
extensions_path = '/extensions'
url_suffix = '/index.html'
css_list = [
    '/static/css/out/site.css',
    '/static/css/print.css',
    '/static/css/prettify.css'
]
ignore_list = [
    '/extensions/whats_new'
]
logging.basicConfig(filename='example.log', level=logging.DEBUG)


class MyHTMLParser(HTMLParser):
    hrefs = []

    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if attr[0] == 'href':
                href = attr[1]
                href = re.sub(r'#.*$', '', href)
                self.hrefs.append(href)


def download_file(url, filename):
    print('Downloading {u} to {f}'.format(u=url, f=filename))
    return urlretrieve(url, filename)


def clean_dest(dest_path):
    if os.path.exists(dest_path):
        rmtree(dest_path)
    os.mkdir(dest_path)


def parse_html(index_html, subpath):
    with open(index_html, 'r') as f:
        html_string = f.read()
    parser = MyHTMLParser()
    parser.feed(html_string)
    download_list = []
    for href in parser.hrefs:
        if re.search(r'\.[^\.]{1,4}$', href):
            continue
        if href.startswith('http'):
            continue
        if href.startswith('/extensions/'):
            download_list.append(href)
        if not href.startswith('/'):
            download_list.append(subpath + '/' + href)
    return list(set(download_list))


def modify_css_href(dest_html):
    with open(dest_html, 'r') as f:
        html_lines = f.readlines()
    i = 0
    while(i < len(html_lines)):
        if (re.search(r'<link', html_lines[i])):
            html_lines[i] = re.sub(
                r'href="([^"]+)"',
                r'href="' + extensions_path + r'\1"',
                html_lines[i])
        i += 1
    with open(dest_html, 'w') as f:
        f.writelines(html_lines)


if __name__ == '__main__':
    root_path = os.getcwd()
    dest_path = root_path + extensions_path

    clean_dest(dest_path)

    download_list = [extensions_path]
    downloaded = {}
    while len(download_list) > 0:
        subpath = download_list.pop()
        if subpath in ignore_list:
            continue
        subpath_base = os.path.basename(subpath)
        if subpath_base in downloaded.keys():
            logging.debug('Ignoring {s} due to existing {e}'.format(
                s=subpath, e=downloaded[subpath_base]
            ))
            continue
        dest_html = root_path + subpath
        if not dest_html.endswith('.html'):
            dest_html += url_suffix
        if not os.path.exists(os.path.dirname(dest_html)):
            os.makedirs(os.path.dirname(dest_html))
        download_file(origin_url + subpath, dest_html)
        downloaded[subpath_base] = subpath

        if dest_html.endswith('.html'):
            append_list = sorted(
                list(
                    set(parse_html(dest_html, subpath)) -
                    set(download_list)
                ),
                reverse=True
            )
            logging.debug('{s} appends following list:\n{l}'.format(
                s=subpath, l='\n'.join(append_list)))
            download_list = append_list + download_list
            modify_css_href(dest_html)

    for css in css_list:
        dest_css = root_path + extensions_path + css
        if not os.path.exists(os.path.dirname(dest_css)):
            os.makedirs(os.path.dirname(dest_css))
        download_file(origin_url + css, dest_css)
