'''
   e.g. run with

   $ python dg_test.py /home/alan/dgtech/aggregator/getnews/test/spiders/wechat_sogou/wechat_sogou_3.html
'''

from scrapy.http import Request, HtmlResponse
from newspaper import *
import copy
from newspaper.cleaners import DocumentCleaner
import sys
import csv

DUMMY_URL="http://test.dealglobe.com"

def fake_response_from_file(file_path):
    """
    Create a Scrapy fake HTTP response from a HTML file
    @param file_name: The relative filename from the responses directory,
                      but absolute paths are also accepted.
    @param url: The URL of the response.
    returns: A scrapy HTTP response which can be used for unittesting.
    """
    request = Request(url=DUMMY_URL)
    file_content = open(file_path, 'r').read()
    response = HtmlResponse(url=DUMMY_URL,
        request=request,
        body=file_content,
        encoding='utf-8')
    return response

def get_article_nodes(a):
    html = a.config.get_parser().fromstring(a.html)
    html_copy = copy.deepcopy(html)
    doc = DocumentCleaner(a.config).clean(html_copy)
    ex = a.extractor
    text_nodes = ex.nodes_to_check(doc) # <p>, <td>, <pre>
    return text_nodes

def create_article(response):
    a = Article(DUMMY_URL,language="zh")
    a.set_html(response.body)
    return a

def write_csv(node_stats):
    with open("output.csv","w") as f:
        w = csv.writer(f)
        w.writerow(["Text","Score","Is link heavy"])
        for n in node_stats:
            text_content = n[0]
            if text_content and text_content.strip() != "":
                w.writerow(n)

def stats_from_file(fname):
    resp = fake_response_from_file(fname)
    article = create_article(resp)
    nodes = get_article_nodes(article)
    stats = article.extractor.node_stats_ex(nodes)
    return stats
 
if __name__ == '__main__':
    fname = sys.argv[1]
    results = stats_from_file(fname)
    write_csv(results)

