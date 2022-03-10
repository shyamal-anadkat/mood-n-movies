# import required modules
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re


def is_right_wikipg(href, imdb_soup):
    retVal = False
    href_id = re.findall(r".(tt[0-9]*)", href)[0]
    imdb_link_elem = imdb_soup.select_one(
        f'a[href*="https://www.imdb.com/title/{href_id}"]'
    )
    if imdb_link_elem:
        imdb_link, *rest = imdb_link_elem[  # pylint: disable=unused-variable
            "href"
        ].split(  # pylint: disable=unused-variable
            "?"
        )
        imdb_link_id = re.findall(r".(tt[0-9]*)", imdb_link)[1]
        # imdb_link = imdb_link.replace('awards', '').replace('business', '') # make this more generic
        # to_compare = f"https://www.imdb.com{href}"
        # print(f"{imdb_link}#######{to_compare}")
        if imdb_link_id == href_id:
            retVal = True

    return retVal


def sensible_title_caps(title):
    no_caps_list = ["in", "the"]
    words = []
    for word in title.split():
        if word not in no_caps_list:
            word = word.capitalize()
        words.append(word)
    return " ".join(words)


def create_df_with_plots(imdb_df):
    movie_title = imdb_df[["title", "title_href", "mc_link", "produce_year"]].values
    num_missing_link = 0

    # example link dune.. https://en.wikipedia.org/wiki/Dune_(2021_film)
    plots_dicts = list()
    for title, href, mc_link, year in movie_title:
        # get URL
        wiki_title = (
            title.strip()
            .replace(" ", "_")
            .replace(".", "")
            .replace("_In_", "_in_")
            .strip()
        )
        # note - capitalize first letter only if not like a, in
        wiki_link = f"https://en.wikipedia.org/wiki/{wiki_title}"
        # print(wiki_link)
        page = requests.get(wiki_link)

        # scrape webpage
        soup = BeautifulSoup(page.content, "html.parser")
        imdb_soup = BeautifulSoup(page.text, "html.parser")

        is_right_wikipage = is_right_wikipg(href, imdb_soup)
        if not is_right_wikipage:
            # get the wiki page with like the year and film pattern
            # I wanna set the soup to that new page if I find it.  West_Side_Story_(2021_film)
            suffix = f"_({year}_film)"
            wiki_link = f"https://en.wikipedia.org/wiki/{wiki_title}{suffix}"
            page = requests.get(wiki_link)
            soup = BeautifulSoup(page.content, "html.parser")
            imdb_soup = BeautifulSoup(page.text, "html.parser")

            is_right_wikipage = is_right_wikipg(href, imdb_soup)
            if not is_right_wikipage:
                suffix = "_(film)"
                wiki_link = f"https://en.wikipedia.org/wiki/{wiki_title}{suffix}"
                page = requests.get(wiki_link)
                soup = BeautifulSoup(page.content, "html.parser")
                imdb_soup = BeautifulSoup(page.text, "html.parser")
                mc_link = list()
                mc_link.append(
                    imdb_soup.select_one('a[href*="https://www.imdb.com/title/"]')
                )
                is_right_wikipage = is_right_wikipg(href, imdb_soup)
                if not is_right_wikipage:
                    num_missing_link += 1
                    missing_movies = list()
                    missing_movies.append(wiki_title)
                    print(f"IMDB link not available for {wiki_title}, link:{wiki_link}")

        if is_right_wikipage:
            # create title object
            title = soup.find(id="firstHeading").text
            title_movie = list()
            title_movie.append(title)

            plots = []
            plot = []
            plot_section = [soup.findAll("h2")[1]]
            for header in plot_section:
                for elem in header.next_siblings:
                    if elem.name and elem.name.startswith("h2"):
                        # stop at next header
                        break
                    if elem.name == "p":
                        plot.append(elem.get_text().replace("\n", ""))

            plots.append(plot)
            plots_dic = {
                "title": title_movie,
                "wiki_link": wiki_link,
                "plot": plots,
                "mc_link": mc_link,
            }
            print(f"{title}-{year}")
            plots_dicts.append(plots_dic)
    print("======================================")
    print(f"# of Missing links = {num_missing_link}")
    print("======================================")
    return pd.DataFrame(plots_dicts, columns=["title", "wiki_link", "plot", "mc_link"])


if __name__ == "__main__":
    in_path = "../data/processed/IMDB_top_1000_clean.csv"
    out_path = "../data/processed/with_plot_summary.csv"
    print(
        f":: Scraping plots for wikipedia using input CSV: {in_path}, please wait...::"
    )
    df = pd.read_csv(in_path)
    create_df_with_plots(df).to_csv(out_path, index=False)
    print(f":: All done. Saved in {out_path} ::")
