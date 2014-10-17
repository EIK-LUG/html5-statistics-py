from urllib.request import urlopen, URLError
from socket import timeout
import json


#Probably missing some tags
HTML5_TAGS = ["<!DOCTYPE_html", "<audio", "<video", "<article", "<header", "<footer", "<canvas", "<aside", "<bdi",
              "<details", "<dialog", "<figcaption", "<figure", "<main", "<mark", "<menuitem", "<meter", "<nav",
              "<progress", "<rp", "<rt", "<ruby", "<section", "<summary", "<time", "<wbr", "<datalist", "<keygen",
              "<output", "<svg", "<embed", "<source", "<track", "<video"]

report = {}


def get_urls(file):
    """Opens a file of urls, each url expected to be on a new line. These are read into a list.
    :param file Path to file
    :return List of urls
    """
    lines = open(file, "r").readlines()
    new_lines = []
    for line in lines:
        new_lines.append(line.replace("\n", ""))
    return new_lines


def get_html(url):
    """Attempts to download html at url. In case of download taking more than 1 seconds, 'No Response is returned.'
    :param url Some url
    :return html as string or 'No Response'"""
    try:
        return urlopen(url, timeout=1).read().decode('utf-8')
    except URLError:
        return "Invalid URL"
    except timeout:
        return "Timeout"
    except UnicodeDecodeError:
        return "Unable to decode, not utf-8"
    except Exception as e:
        return "Some other error: " + str(e)


def contains_html5(url):
    """Checks if the html at url contains any HTML5 tags.
    :param url Some url
    :return Does the html at url contain any html5 tags"""
    response = get_html(url)
    if response.find("<") == -1:
        return response
    for tag in HTML5_TAGS:
        if response.find(tag):
            return True
    return False

if __name__ == "__main__":
    urls = get_urls("urls.txt")
    url_nr = 0
    nr_of_urls = len(urls)
    #Modest sample size of 100 urls
    for url in urls[0:100]:
        print("url:" + str(url_nr) + "/" + str(nr_of_urls))
        report[url] = contains_html5(url)
        url_nr += 1
    json.dump(report, open("report", "w"), sort_keys=True, indent=4, separators=(',', ': '))
