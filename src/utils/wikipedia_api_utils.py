import requests
import random

API_URL = "https://en.wikipedia.org/w/api.php"

def get_article_titles(article_title):
    try:
        if not article_title:
            raise

        print("Getting articles for {}...".format(article_title))

        request_params = {
            "action": "query",
            "list": "search",
            "srsearch": article_title,
            "srlimit": 10,
            "redirects": True,
            "format": "json"
        }

        response = requests.get(API_URL, request_params)
        response_json = response.json()

        pages = (response_json.get("query").get("search"))

        if len(pages) <= 0:
            raise

        titles = [page.get("title") for page in pages]

        print("Retrieved articles {}\n".format(", ".join(titles)))

        return titles
    except Exception as e:
        print("Failed to retrieve articles: {\n}".format(e))

        return []

def search_article_titles():
    try:
        while True:
            search_title = input("Enter a title, or press Enter to exit: ")

            if not search_title:
                exit()

            article_titles = get_article_titles(search_title)
            
            if len(article_titles) == 1:
                return article_titles[0]
            elif len(article_titles) <= 0:             
                continue
            elif len(article_titles) > 1:
                for i, title in enumerate(article_titles):
                    if search_title.lower() == title.lower():
                         if input("A retrieved article has title: {}. Confirm this article (y/n)? ".format(article_titles[i])) == "y":
                            return article_titles[i]
               
                print("More than 1 article found, narrow your title search\n")
                continue
    except Exception as e:
        print("Failed to search articles: {}".format(e))

def get_article_text(article_title):
    try:
        print("Getting article text...")

        request_params = {
            "action": "query",
            "titles": article_title,
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
            "exsectionformat": "wiki",
            "redirects": True,
            "format": "json"
        }

        response = requests.get(API_URL, request_params)
        response_json = response.json()

        page_text = next(iter((response_json.get("query").get("pages").values()))).get("extract")
        print("Retrieved article text\n")

        return page_text
    except Exception as e:
        print("Failed to retrieve article text: {}\n".format(e))

def get_url_content(url):
    try:
        return requests.get(url = url, headers = {"User-Agent": "Script"}, allow_redirects = True).content
    except Exception as e:
        raise e

def get_article_image(image_title):
    try:
        print("Getting article image {}...".format(image_title))
    
        request_params = {
            "action": "query",
            "titles": image_title,
            "prop": "imageinfo",
            "iiprop": "url",
            "format": "json"
        }

        response = requests.get(API_URL, request_params)
        response_json = response.json()

        image_url = next(iter((response_json.get("query").get("pages").values()))).get("imageinfo")[0].get("url")
        image = get_url_content(image_url)
        print("Retrieved article image\n")

        return image
    except Exception as e:
        print("Failed to retrieve article image: {}\n".format(e))

def get_article_images(article_title, num_images):
    try:
        print("Getting {} article {} image(s)...".format(num_images, article_title))

        request_params = {
            "action": "query",
            "titles": article_title,
            "prop": "images",
            "imlimit": "max",
            "redirects": True,
            "format": "json"
        }

        response = requests.get(API_URL, request_params)
        response_json = response.json()

        valid_file_types = [".jpg", ".jpeg", ".png"]

        page = next(iter((response_json.get("query").get("pages").values())))

        if "images" not in page.keys():
            raise ValueError("No images found for page")

        page_images = page.get("images")
        page_image_titles = [image.get("title") for image in page_images]
        filtered_page_image_titles = [title for title in page_image_titles if any(title.lower().endswith(file_type) for file_type in valid_file_types)]
        chosen_indexes = random.sample(range(0, len(filtered_page_image_titles)), min(len(filtered_page_image_titles), num_images))
        chosen_page_image_titles = [filtered_page_image_titles[i] for i in chosen_indexes]
        
        images = []

        for image_title in chosen_page_image_titles:
            if len(images) >= num_images: break

            images.append(get_article_image(image_title))

        print("Retrieved {} article image(s)\n".format(len(images)))
        
        return images
    except Exception as e:
        print("Failed to retrieve article image(s): {}\n".format(e))

def get_article_thumbnail(article_title):
    try:
        print("Getting article {} thumbnail...".format(article_title))

        request_params = {
            "action": "query",
            "titles": article_title,
            "prop": "pageimages",
            "piprop": "thumbnail",
            "pithumbsize": 200,
            "redirects": True,
            "format": "json"
        }

        response = requests.get(API_URL, request_params)
        response_json = response.json()

        page = next(iter((response_json.get("query").get("pages").values())))

        if "thumbnail" not in page.keys():
            raise ValueError("No thumbnail found for page")

        thumbnail = page.get("thumbnail")
        thumbnail_url = thumbnail.get("source")

        thumbnail_image = get_url_content(thumbnail_url)
        print("Retrieved article thumbnail\n")

        return thumbnail_image
    except Exception as e:
        print("Failed to retrieve article thumbnail: {}\n".format(e))

def get_article_url(article_title):
    try:
        print("Getting article {} URL...".format(article_title))

        request_params = {
            "action": "query",
            "titles": article_title,
            "prop": "info",
            "inprop": "url",
            "redirects": True,
            "format": "json"
        }

        response = requests.get(API_URL, request_params)
        response_json = response.json()

        url = next(iter((response_json.get("query").get("pages").values()))).get("fullurl")
        print("Retrieved article URL\n")

        return url
    except Exception as e:
        print("Failed to retrieve article {} URL".format(article_title))