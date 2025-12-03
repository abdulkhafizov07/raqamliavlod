from pytube import YouTube

yt = YouTube("https://www.youtube.com/watch?v=0hEwudQlknM")
print(dir(yt))
print(yt.initial_data['contents']['twoColumnWatchNextResults']['results']['results']['contents'][1]['videoSecondaryInfoRenderer']['attributedDescription']['content'])