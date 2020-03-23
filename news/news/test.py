import re

url = 'https://www.jiemian.com/video/AGQCOAhmB24BOlVg.html'
# url = 'https://www.jiemian.com/lists/280.html'

# content = re.findall('.*lists/(.*\d)_1\.html', video_url)
if 'video' in url:
    content = re.findall('.*video/(.*).html', url)[0]
else:
    content = re.findall('.*article.(.*\d).html', url)[0]
print (content)
