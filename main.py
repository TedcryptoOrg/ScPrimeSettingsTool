import argparse
import yaml
import asyncio
import re

from bs4 import BeautifulSoup
from lxml import etree
from pyppeteer import launch


async def main():
    browser = await launch(
        ignoreHTTPSErrors=True,
        headless=True,
        args=[
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--headless',
            '--disable-gpu',
            '--ignore-certificate-errors'
        ]
    )
    page = await browser.newPage()
    await page.setViewport({'width': 1920, 'height': 1280})
    response = await page.goto(args.url, {'waitUntil': 'networkidle0'})

    if response.status != 200:
        raise Exception("[Pyppeteer] HTTP Code:" + str(response.status), response.status)

    if args.screenshot:
        await page.screenshot({'path': 'screenshot.png', 'fullPage': True})

    html = await page.content()
    soup = BeautifulSoup(html, 'html.parser')

    dom = etree.HTML(str(soup))
    for element_name in configs['elements']:
        element = configs['elements'][element_name]

        if args.update_settings:
            is_element_asked = element_name in args.update_settings
            is_element_command_asked = 'command' in element and element['command'] in args.update_settings
            if not is_element_asked and not is_element_command_asked:
                continue

        dom_element = dom.xpath(element['xpath'])

        if not dom_element:
            # fallback to search by name for the element
            dom_element = soup.find(text=re.compile(re.escape(element['label']))).parent.next_sibling.div
            if not dom_element:
                print('Element %s not found. Debug with --screenshot or check your configuration file!' % element_name)
                continue
            else:
                element_value = dom_element.contents[0].text
        else:
            element_value = dom_element[0].text

        if args.commands and 'command' in element:
            print('spc host config %s %s%s' % (element['command'], element_value, element['unit']))
        elif not args.commands:
            print('%s %s%s' % (element['label'], element_value, element['unit'] if 'unit' in element else ''))

    await browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process grafana settings')
    parser.add_argument('--config', '-c', help='Path to config file', required=False, default='config.yaml')
    parser.add_argument('--url', '-u', help='Grafana provider url', required=False)
    parser.add_argument('--provider-id', '-p', help='Grafana provider id', required=False)
    parser.add_argument('--commands', help='Prints commands that need to be run', required=False, default=False, action='store_true')
    parser.add_argument('--screenshot', help='Saves a screenshot of grafane for debug purposes', required=False, default=False, action='store_true')
    parser.add_argument(
        '--update_settings',
        help='Which settings should be automatically updated', required=False, default=[])

    args = parser.parse_args()
    if args.update_settings:
        args.update_settings = args.update_settings.split(',')

    if not args.url and not args.provider_id:
        print("Please provide a grafana url or a provider id")
        exit(1)

    if not args.url:
        args.url = 'https://grafana.scpri.me/d/Cg7V28sMk/provider-detail?var-provider=' + args.provider_id

    with open(args.config, "r") as stream:
        try:
            configs = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    asyncio.get_event_loop().run_until_complete(main())
