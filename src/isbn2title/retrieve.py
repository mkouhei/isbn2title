# -*- coding: utf-8 -*-
"""
    Copyright (C) 2012 Kouhei Maeda <mkouhei@palmtb.net>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import os.path
import urllib2
import re
import lxml.html
import time
from __init__ import __apiurl__
from __init__ import __sleep__

APIURL = __apiurl__
SLEEP = __sleep__
INFILE = '~/booklist.csv'
OUTFILE = '/tmp/booklist.csv'


def retrieve_title(api_url, isbn):
    res = urllib2.urlopen(api_url + isbn)
    data = res.read().decode('shift-jis')

    pat_multiple_ln = re.compile('\n(\s*)\n*')
    replaced_data = pat_multiple_ln.sub('\n', data)

    root = lxml.html.fromstring(data)

    # for new product
    divs = root.xpath('//div')
    # for second used
    spans = root.xpath('//span')

    if [span.attrib.get('title')
        for span in spans
        if span.attrib.get('title')]:
        # for second used
        title = [span.attrib.get('title')
                 for span in spans
                 if span.attrib.get('title')][0]
    else:
        # for new product
        try:
            div_title = [div
                         for div in divs
                         if div.attrib.get('class') == 'productTitle'][0]
            title_str = div_title.xpath('a')[0].text.replace('^\s+', '')
            pat_space = re.compile('^\s+')
            title = pat_space.sub('', title_str)
        except IndexError as e:
            title = ''

    time.sleep(SLEEP)
    return title


def main():
    with open(os.path.expanduser(INFILE)) as f:
        lines = {line.split(',')[0]: line for line in f}
        isbn_l = [line for line in lines]

    isbn_title_dict = {isbn: retrieve_title(APIURL, isbn)
                       for isbn in isbn_l}

    with open(OUTFILE, 'w') as f:
        for i in isbn_title_dict:
            f.write('"%s",%s' % (isbn_title_dict[i].encode('utf-8'), lines[i]))


if __name__ == '__main__':
    main()
