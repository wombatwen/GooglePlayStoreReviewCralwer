
import re
import json
import requests
import logging

class GooglePlayStoreCrawler(object):

    base_url = 'https://play.google.com/store/apps/details'
    get_review_url = 'https://play.google.com/store/getreviews'

    review_pattern = r'.*?<span class="responsive-img author-image" style="background-image:url\((.*?)\).*? <span class="responsive-img-hdpi"> <span class="responsive-img author-image" style="background-image:url\((.*?)\).*?<div class="review-info">.*?<span class="author-name">(.*?)<\/span>.*?<span class="review-date">(.*?)<\/span> <a class="reviews-permalink" href="(.*?)".*?<div class="current-rating" jsname="jIIjq" style="width: (.*?)%;">.*?<span class="review-title">(.*?)<\/span>(.*?)<div class="review-link" style="display:none">'
    review_sort_order = {
        "newest": 0,
        "rating": 1,
        "helpfulness": 2
    }

    def logger(self):
        name = self.__class__.__name__
        return logging.getLogger(name)

    def __init__(self):

        return

    def get_raw_data(self, url=None, data=None):

        r = requests.post(url, data=data)
        if r.status_codes == requests.codes.ok:
            return r.content
        else:
            return ''

    def get_reviews(self, app_id=None, host_lang=None, page_num=0, sort_order="newest"):

        if app_id == None:
            self.logger.error("empty app_id.\n")
            return

        data = {
            'reviewType': 0,
            'pageNum': page_num,
            'id': app_id,
            'reviewSortOrder' : self.review_sort_order[sort_order],
            'xhr': 1
        }
        if host_lang != None:
            data['hl'] = host_lang

        url = self.get_review_url
        raw_data = self.get_raw_data(url=url, data=data)
        raw_data = json.loads(raw_data[4:])[0][2]

        reviews = []
        for block in raw_data.split('<div class="single-review" tabindex="0">')[1:]:

            match = re.match(self.review_pattern, block)
            if match != None:
                review = {
                    "background_image_ldpi": match.group(1),
                    "background_image_hdpi": match.group(2),
                    "author_name": match.group(3),
                    "date": match.group(4),
                    "link": match.group(5),
                    "rating": int(match.group(6))/20,
                    "title": match.group(7),
                    "content": match.group(8)
                }
                print match.group(1)
                print match.group(2)
                print match.group(3)
                print match.group(4)
                print match.group(5)
                print match.group(6)
                print match.group(7)
                print match.group(8)
                reviews.append(review)

        return reviews

    def get_newest_reviews(self, app_id=None, host_lang=None, page_num=0):

        return self.get_reviews(app_id, host_lang, page_num, sort_order="newest")


if __name__ == '__main__':

    api_client = GooglePlayStoreApiClient()
    api_client.get_newest_reviews(app_id='com.google.android.apps.docs', host_lang='en')

