from selectolax.parser import HTMLParser, Node
from playwright.async_api import async_playwright
import pandas as pd
from httpx import get
import json
import asyncio
from datetime import datetime
import re

CONFIG='config.json'

def get_config():
    with open(CONFIG) as c:
        return json.load(c)
    
async def playwright_get_html(container_selector, url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)

        await page.wait_for_load_state("networkidle")
        await page.evaluate("() => window.scroll(0, document.body.scrollHeight)")
        await page.wait_for_selector(container_selector)
        

        return await page.inner_html('body')

def get_containers(html, container, container_selector):
    tree = HTMLParser(html)
    
    if container['match'] == 'all':
        containers = tree.css(container_selector)
    elif container['match'] == 'first':
        containers = [tree.css_first(container_selector)]

    if container['type'] == 'node':
        return containers
    elif container['type'] == 'text':
        return [container.text() for container in containers]

def get_parsed_info(node, selectors):
    parsed = {}

    for s in selectors:
        if s['match'] == 'all':
            elems = node.css(s['selector'])
        elif s['match'] == 'first':
            elems = [node.css_first(s['selector'])]

        if s['type'] == 'text':
            elems = [el.text() for el in elems]
        else:
            elems = [el.attributes[s['type']] for el in elems]

        if len(elems) == 1:
            parsed[s['name']] = elems[0]
        else:
            parsed[s['name']] = elems

    return parsed

def reformat_date(date, from_format, out_format):
    new_date = datetime.strptime(date, from_format)
    return datetime.strftime(new_date, out_format)

def get_price(price):
    regex = re.compile('(\d*,\d*)')
    match = regex.match(price)
    return match.group(0)

def transform(parsed:dict):
    parsed['category_tags'] = parsed['category_tags'][:5]
    parsed['nr_reviews'] = parsed['nr_reviews'].split(' ')[1]
    parsed['release_date'] = reformat_date(parsed['release_date'], from_format='%b %d, %Y', out_format='%Y-%m-%d')
    parsed['currency'] = parsed['original_price'][-1]
    parsed['original_price'] = get_price(parsed['original_price'])
    parsed['discounted_price'] = get_price(parsed['discounted_price'])

def main():
    config = get_config()

    url = config['url']
    container = config['container']
    selectors = config['item']
    out_file = config['output_file']

    container_selector = container['selector']

    html = asyncio.run(playwright_get_html(container_selector=container_selector, url=url))
    containers = get_containers(html, container, container_selector)

    parsed = [get_parsed_info(c, selectors) for c in containers]
    [transform(pars) for pars in parsed]

    final = parsed

    df = pd.DataFrame(final)
    df.to_csv(out_file, index=False)

if __name__=='__main__':
    main()