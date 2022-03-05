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
                review.find("a", class_="no_hover").text.strip()
            )
            review_dict["num_critic_reviews"] += 1
            count += 1
        if count == 10:
            break
    return pd.DataFrame([review_dict])


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
                review.find("span", class_="blurb blurb_expanded").text.strip()
            )
        else:
            review_dict["user_reviews"].append(
                review.find("div", class_="review_body").find("span").text.strip()
            )
        review_dict["num_user_reviews"] += 1
        count += 1
        if count == 10:
            break
    return pd.DataFrame([review_dict])


if __name__ == "__main__":
    ## testing ##
    title = "dune"
    critic_reviews = get_critic_reviews(title)
    user_reviews = get_user_reviews(title)
    print(critic_reviews)
