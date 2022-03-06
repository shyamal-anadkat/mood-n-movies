from bs4 import BeautifulSoup
import requests
import pandas as pd

##############################
## Author: Shyamal Anadkat ###
##############################
def get_critic_reviews(movie_title):
    review_dict = {
        "critic_reviews": [],
        "movie_title": [],
        "metacritic_url": [],
        "num_critic_reviews": 0,
    }
    review_dict["movie_title"] = movie_title
    metacritic_url = f"https://www.metacritic.com/movie/{movie_title}/critic-reviews"
    review_dict["metacritic_url"] = metacritic_url
    user_agent = {"User-agent": "Mozilla/5.0"}
    response = requests.get(metacritic_url, headers=user_agent)
    # time.sleep(rand.randint(3,30))
    soup = BeautifulSoup(response.text, "html.parser")
    count = 0
    for review in soup.find_all("div", class_="review pad_top1 pad_btm1"):
        if review.find("a", class_="no_hover"):
            review_dict["critic_reviews"].append(
                "<review>"
                + review.find("a", class_="no_hover").text.strip()
                + "</review>"
            )
            review_dict["num_critic_reviews"] += 1
            count += 1
        if count == 10:
            break
    # return pd.DataFrame([review_dict])
    return review_dict


def get_user_reviews(movie_title):
    review_dict = {
        "user_reviews": [],
        "movie_title": [],
        "metacritic_url": [],
        "num_user_reviews": 0,
    }
    review_dict["movie_title"] = movie_title
    metacritic_url = f"https://www.metacritic.com/movie/{movie_title}/user-reviews?sort-by=most-helpful&num_items=50"
    review_dict["metacritic_url"] = metacritic_url
    user_agent = {"User-agent": "Mozilla/5.0"}
    response = requests.get(metacritic_url, headers=user_agent)
    # time.sleep(rand.randint(3,30))
    soup = BeautifulSoup(response.text, "html.parser")
    count = 0
    for review in soup.find_all("div", class_="review pad_top1"):
        if review.find("span", class_="blurb blurb_expanded"):
            review_dict["user_reviews"].append(
                "<review>"
                + review.find("span", class_="blurb blurb_expanded").text.strip()
                + "</review>"
            )
        else:
            review_dict["user_reviews"].append(
                "<review>"
                + review.find("div", class_="review_body").find("span").text.strip()
                + "</review>"
            )
        review_dict["num_user_reviews"] += 1
        count += 1
        if count == 10:
            break
    # return pd.DataFrame([review_dict])
    return review_dict


def reviews_fetch_and_fill(imdb_df):
    count = 0
    data = []
    for _, row in imdb_df.iterrows():
        record = dict()
        title = row["mc_link"].split("movie", 1)[1].split("?")[0].split("/")[1]
        try:
            critic_reviews = get_critic_reviews(title)
            user_reviews = get_user_reviews(title)

            record["mc_link"] = row["mc_link"]
            record["title"] = title

            record["mc_link_critic"] = critic_reviews["metacritic_url"]
            record["mc_link_user"] = user_reviews["metacritic_url"]

            record["user_reviews"] = user_reviews["user_reviews"]
            record["critic_reviews"] = critic_reviews["critic_reviews"]

            record["num_user_reviews"] = user_reviews["num_user_reviews"]
            record["num_critic_reviews"] = critic_reviews["num_critic_reviews"]
            data.append(record)
            count += 1
        except Exception as e:  # pylint: disable=broad-except
            print(f"Unable to fetch reviews for {title}:{e}. Continuing.")
    print(f":: All done! Processed {count} records ::")
    return data


if __name__ == "__main__":
    imdbdata = pd.read_csv("../data/processed/IMBD_top_1000_clean.csv")
    print(f"IMDB clean data, no. of records: {len(imdbdata)}")
    reviewsdata = reviews_fetch_and_fill(imdbdata)
    finaldf = pd.DataFrame(reviewsdata)
    path = "../data/raw/reviews_data_raw.csv"
    finaldf.to_csv(path, index=False)
    print(f":: Saved in {path} ::")
