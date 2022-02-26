import pandas as pd
import requests
from bs4 import BeautifulSoup

page = 1
movie_df = pd.DataFrame()

## Credits to Yulin Zheng for some of the logic that we used to adapt the code ##
while True:
    url = (
        "https://www.imdb.com/search/title/?groups=top_1000&languages=en&count=100&start="
        + str(page)
        + "&ref_=adv_nxt"
    )
    data_page = requests.get(url, headers={"Accept-Language": "en-US"})
    print(url)
    titles = []
    title_hrefs = []
    mc_links = []
    certificates = []
    ratings = []
    genres = []
    votes = []
    metascores = []
    runtime_list = []
    directors_list = []
    stars_list = []
    grosses_list = []  #
    introduction_list = []
    produce_year_list = []
    soup = BeautifulSoup(data_page.text)
    list_item_content = soup.findAll("div", class_="lister-item-content")
    print("number of movies on page: " + str(len(list_item_content)))
    for movie_content in list_item_content:
        list_muted_text = movie_content.findAll("p", class_="text-muted")
        introduction_list.append(list_muted_text[1].text.replace("\n ", ""))
        item_header = movie_content.find("h3", class_="lister-item-header")
        title = item_header.find("a")
        title_href = item_header.find("a", href=True)["href"]

        # get metacritic link/title
        critic_url = f"https://www.imdb.com{title_href}criticreviews"
        mc_page = requests.get(critic_url, headers={"Accept-Language": "en-US"})
        mc_soup = BeautifulSoup(mc_page.text)
        mc_link_elem = mc_soup.select_one("a[href*=https://www.metacritic.com/movie/]")
        if mc_link_elem:
            mc_link = mc_link_elem["href"]
        else:
            mc_link = ""
            print(f"MC link not available for {title}-{title_href}")

        rating = movie_content.find("strong")
        certificate = movie_content.find("span", class_="certificate")
        vote = movie_content.find("p", class_="sort-num_votes-visible")
        genre = movie_content.find("span", class_="genre")
        metascore = movie_content.find("span", class_="metascore favorable")
        runtime = movie_content.find("span", class_="runtime")
        p_content = movie_content.find("p", class_="")
        produce_year = movie_content.find("span", class_="lister-item-year")
        produce_year = produce_year.text.replace("(", "")
        produce_year = produce_year.replace(")", "")
        produce_year_list.append(produce_year)
        if p_content != None:
            p_content_split = p_content.text.split("|")
            directors = p_content_split[0].replace("\n", "")
            directors = directors.replace("Director:", "")
            directors = directors.replace("Directors:", "")
            stars = p_content_split[1].replace("\n", "")
            stars = stars.replace("Stars:", "")
            stars_list.append(stars)
            directors_list.append(directors)
        else:
            directors_list.append(None)
            stars_list.append(None)
        if certificate != None:
            certificates.append(certificate.text.strip())
        else:
            certificates.append(certificate)
        if "|" in vote.text:
            vote_gross = vote.text.split("|")
            vote_value = vote_gross[0]
            vote_value = vote_value.replace("\n", "")
            vote_value = vote_value.replace(",", "")
            vote_value = vote_value.replace("Votes:", "")
            gross_value = vote_gross[1]
            gross_value = gross_value.replace("\n", "")
            gross_value = gross_value.replace("Gross:", "")
            gross_value = gross_value.replace("$", "")
            gross_value = gross_value.replace("M", "")
            gross_value = gross_value.replace(" ", "")
            votes.append(vote_value)
            grosses_list.append(gross_value)
        else:
            vote_value = vote.text.replace("\n", "")
            vote_value = vote_value.replace("Votes:", "")
            vote_value = vote_value.replace(",", "")
            votes.append(vote_value)
            grosses_list.append(None)
        if rating != None:
            ratings.append(rating.text.strip())
        else:
            ratings.append(rating)
        title_hrefs.append(title_href)
        if title != None:
            titles.append(title.text.strip())
        else:
            titles.append(title)
        if mc_link != None:
            mc_links.append(mc_link)
        if genre != None:
            genres_text = genre.text.replace(" ", "")
            genres_text = genres_text.strip()
            genres.append(genres_text)
        else:
            genres.append(genre)
        if metascore != None:
            metascores.append(metascore.text.strip())
        else:
            metascores.append(metascore)
        if runtime != None:
            runtime_text = runtime.text.strip()
            runtime_text = runtime_text.replace(" min", "")
            runtime_list.append(runtime_text)
        else:
            runtime_list.append(runtime)

    df = pd.DataFrame(
        {
            "title": titles,
            "title_href": title_hrefs,
            "mc_link": mc_links,
            "genre": genres,
            "certificate": certificates,
            "votes": votes,
            "metascore": metascores,
            "directors": directors_list,
            "stars": stars_list,
            # "gross":grosses_list,
            "introduction": introduction_list,
            "produce_year": produce_year_list,
            "runtime": runtime_list,
            "rating": ratings,
        }
    )
    movie_df = movie_df.append(df)
    page = page + 100
    if page > 1000:
        break

movie_df.to_csv("imdb_top_1000.csv", index=False)
