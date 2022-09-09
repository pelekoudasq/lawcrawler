import argparse
import bs4
import pprint
import requests


parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=(
        "Drafts or proposed laws that have been tabled in Parliament but have"
        "not yet started their discussion in Parliamentary Committees"
    ),
)
parser.add_argument(
    "--page", default=1, type=int, help="The default value is 1"
)

base_url = (
    "https://www.hellenicparliament.gr/Nomothetiko-Ergo/"
    "Katatethenta-Nomosxedia?pageNo=%s"
)

def crawl_laws_page(args):
    target_url = base_url % (args.page)

    r = requests.get(target_url)
    if not r.status_code == 200:
        raise 

    html_doc = r.content
    soup = bs4.BeautifulSoup(html_doc, 'html.parser')

    table = soup.find(summary="laws katatethenta")
    if not table:
        print("No laws found")
        return

    all_elements = []
    for tr in table.find_all("tr"):
        elements = [td.get_text().strip() for td in tr.find_all("td")]
        if elements not in [[], None]:
            all_elements.append(elements)

    final_elements = []
    for element in all_elements[:-1]:
        in_dict = dict(zip(["date", "title", "type", "ministry"], element))
        final_elements.append(in_dict)

    pprint.pprint(final_elements)


if __name__ == "__main__":
    args = parser.parse_args()
    crawl_laws_page(args)
