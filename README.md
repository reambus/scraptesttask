# Run command beelow to crawl links
scrapy crawl linkcollector -s FEED_URI='/home/roman/projects/tmp/links.csv' -s FEED_FORMAT=csv

# Run command beelow to crawl profiles
scrapy crawl profilecollector --logfile /tmp/scrap.log -a filename='/home/roman/projects/tmp/links.csv' -s FEED_URI='/home/roman/projects/tmp/profiles.csv' -s FEED_FORMAT=csv 