import requests
import operator
from bs4 import BeautifulSoup

congresspeople_urls = []
url_dict = {}
contributor_totals = {}


def get_congresspeople(url):
    # Finds links for each congressperson's profile page and adds it to an array
    page = requests.get(url)
    content = BeautifulSoup(page.content, "html.parser")
    all_members = content.find("div", {"class": "Congress"})
    all_letters = all_members.find_all("p")

    for letter in all_letters:
        congresspeople = letter.find_all("a")
        for congressperson in congresspeople:
            url_dict[congressperson.text.strip()] = "https://opensecrets.org" + congressperson.get('href')

            congresspeople_urls.append("https://opensecrets.org" + congressperson.get('href'))


def get_contributors(url):
    # Find url of contributions page within individual congressperson's profile page.
    page = requests.get(url)
    content = BeautifulSoup(page.content, "html.parser")
    nav_tab = content.find("div", {"class": "TabNav"})
    nav_item_list = nav_tab.find("ul")
    nav_items = nav_item_list.find_all("li")
    for nav_item in nav_items:
        curr = nav_item.text.strip()
        if curr == "Contributors":
            link = nav_item.find("a")
            con_page = "https://opensecrets.org" + link.get('href')

    # Find page for contributions for entire career.
    page = requests.get(con_page)
    content = BeautifulSoup(page.content, "html.parser")
    dropdown_menu = content.find("div", {"class": "StickyFilters-cycle"})
    dropdown_links = dropdown_menu.find_all("option")
    for year in dropdown_links:
        curr = year.text.strip()
        if curr == "Career":
            career_link = "https://opensecrets.org" + year.get('value')

    # Find contributor names and amounts and return it in a dictionary.
    curr_contributors_list = {}
    page = requests.get(career_link)
    content = BeautifulSoup(page.content, "html.parser")
    cont_table = content.find("tbody")
    contributors = cont_table.find_all("tr")

    for contributor in contributors:
        name_and_total = contributor.find_all('td')[0::1]
        # Remove dollar sign and commas
        total = name_and_total[1].text.strip().replace("$", "")
        total = int(total.replace(",", ""))
        # Add it to the dictionary for the current contributor
        curr_contributors_list[name_and_total[0].text.strip()] = total

    return curr_contributors_list


def get_totals(url):
    # Total up all contributions for every contributor by searching top contributor lists of every congressperson.
    get_congresspeople(url)
    # Iterate through every congressperson's profile link
    for name in url_dict:
        url = url_dict.get(name)
        print("Current Congressperson: " + name)
        # Create dictionary of contributor totals for current congressman
        curr = get_contributors(url)

        # If contributor is not already in the overall dictionary, add it. Otherwise, add tot the total.
        for contributor in curr:
            if contributor not in contributor_totals:
                contributor_totals[contributor] = curr.get(contributor)
            else:
                contributor_totals[contributor] += curr.get(contributor)
        print(contributor_totals)


def sort_dict(d, reverse):
    # Sorts and returns a dictionary in forward or reverse order of value.
    if not reverse:
        sorted_d = sorted(d.items(), key=operator.itemgetter(1))
    else:
        sorted_d = sorted(d.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_d


def main():
    full_list = "https://www.opensecrets.org/members-of-congress/members-list?cong_no=117&cycle=2020"
    get_totals(full_list)

    sort_dict(contributor_totals, False)


if __name__ == '__main__':
    main()
