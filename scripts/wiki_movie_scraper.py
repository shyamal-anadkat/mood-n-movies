# import required modules
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

# @author: AIPI 540 Team #5


def is_right_wikipg(href, imdb_soup):
    """Determine if the wikipedia page is correct

    Checks to see if the wikipedia page is right based on External links
    matching the IMDB movie link href. The href is an HTML attribute that
    specifies the URL of the page the link redirects to.
    https://www.w3schools.com/tags/att_a_href.asp

    :param href: string containing title_href id(title/tt1160419)
    :param imdb_soup: object with constructor and parser

    :returns: bool of whether imdb link matched href link
    """
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
    """Capitalize the title of a movie

    This function capitalizes the first character in movie titles while
    leaving out certain words to not be capitalized

    :param title: string of the movie title name

    :return: string containing the movie title with capitalized first
    letters except certain words
    """
    no_caps_list = ["in", "the"]
    words = []
    for word in title.split():
        if word not in no_caps_list:
            word = word.capitalize()
        words.append(word)
    return " ".join(words)


def create_df_with_plots(imdb_df):
    """A dataframe is created

    The dataframe consists of movie title, metacritic link, wikipedia
    link, and movie plot. A dataframe is two-dimensional, size-mutable,
    potentially heterogeneous tabular data.
    https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html

    :param imdb_df: {title:str, title_href:str, mc_link:str, produce_year:int}

    :return: Final dataframe with movie title, metacritic link, wikipedia
    link, and movie plot summary.
    """
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
