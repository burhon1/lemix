def youtube_link_formatter(video_url):
    if 'youtu.be' in video_url:
        lnk = video_url.split('/')[3]
        return f'https://www.youtube.com/embed/{lnk}'
    elif 'youtube.com' in video_url and 'embed' in video_url:
        return video_url
    elif 'youtube.com/watch?v=' in video_url:
        lnk = video_url.split('/')[3].split('?v=')[1].split('&')[0]
        return f'https://www.youtube.com/embed/{lnk}'
    else:
        video_url
        