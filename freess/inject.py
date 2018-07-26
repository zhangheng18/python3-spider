import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
from bs4 import BeautifulSoup
from mitmproxy import ctx

# load in the javascript to inject
# with open('content.js', 'r') as f:
#     content_js = f.read()

content_js = ('Object.defineProperty(navigator, "webdriver", {'
              'value: false,'
              'configurable: true'
              '});')


def response(flow):
    # only process 200 responses of html content
    if not flow.response.status_code == 200:
        return
    if "<!DOCTYPE HTML>" not in flow.response.text:
        return
    # inject the script tag
    html = BeautifulSoup(flow.response.text, 'lxml')
    container = html.head or html.body
    if container:
        script = html.new_tag('script')
        script.string = content_js

        container.insert(0, script)
        flow.response.text = str(html)
        ctx.log.info('Successfully injected the content.js script.')