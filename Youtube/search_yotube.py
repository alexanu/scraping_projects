# pip install youtube-search-python


regions = ['AR','AT','AU','BR','CA','CH','CN','DE','ES','FI','FR','GB','GR','HK','IL','IN','IT','KR','KZ','NL','NO','NZ','PL','PT','RO','SE','SI','SK','TH','TR','UA','US']
search_words =['Azure Function', 'Logic App', 'Power App', 'Alpaca Trading']

# regions = ['AR','AT','AU']
# search_words =['Azure Function']

from youtubesearchpython import *
import pandas as pd

def main():
    search_result = pd.DataFrame([])
    for word in search_words:
        for reg in regions:
            titles = []
            publ = []
            dur = []
            links = []
            customSearch = CustomSearch(word, VideoUploadDateFilter.thisMonth,region = reg)
            for video in customSearch.result()['result']:
                titles.append(video['title'])
                publ.append(video['publishedTime'])
                dur.append(video['duration'])
                links.append(video['link'])
                # print(f"{video['title']} ({video['publishedTime']}, {video['duration']}, {video['link']})")
            temp_df=pd.DataFrame({'Topic': word, 'Title':titles, 'Published':publ, 'Duration':dur, 'Link':links, 'Region':reg})
            search_result =pd.concat([search_result, temp_df])

    search_result.drop_duplicates(subset='Title', keep="last", inplace=True)
    search_result.reset_index(inplace=True, drop=True)
    search_result.to_csv('youtube_search_res.csv')

if __name__ == '__main__':
    main()