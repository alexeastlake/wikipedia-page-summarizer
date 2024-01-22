import os
from utils import wikipedia_api_utils
from utils import pdf_utils

def main():
    try:
        # Searches for a wikipedia article using user input
        article_title = wikipedia_api_utils.search_article_titles()

        # Retrieves various article info
        article_url = wikipedia_api_utils.get_article_url(article_title)
        article_text = wikipedia_api_utils.get_article_text(article_title)
        article_thumbnail = wikipedia_api_utils.get_article_thumbnail(article_title)
        article_images = wikipedia_api_utils.get_article_images(article_title, 3)

        # Exports article data to PDF
        output_dir = os.path.join(os.path.normpath(os.path.join(os.path.dirname(__file__), "..")), "output")
        pdf_utils.export_pdf(dir = output_dir, title = article_title, text = article_text, thumbnail = article_thumbnail, images = article_images, url = article_url)
    except Exception as e:
        print(e)
        exit()

if __name__ == "__main__":
    main()