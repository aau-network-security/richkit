## Symantec Web Service 

This is generated to get categories of given urls, normally it fetches category from symantec web service then saves it to local file which is called `categorized_urls` under `dat/retrieve/data/`



### How to use 

Import necesseary functions and make a call as demonstrated given below 

```python
from dat.retrieve.symantec import fetch_from_internet
from dat.retrieve.symantec import LocalCategoryDB

urls = ["www.aau.dk","www.github.com","www.google.com"]

local_db = LocalCategoryDB()
for url in urls:
    url_category=local_db.get_category(url)
    if url_category=='':
        url_category=fetch_from_internet(url)
    print(url_category)

```

