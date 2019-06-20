# HufsIME
This is HUFS IME Question page

## Required Packages

```
pip install django-taggit

pip install django-taggit-templatetags

pip install beautifulsoup

pip install allauth
```

## Characteristics of our site

1. Social Login
>- We used Google API & Allauth. It might secure our page.
2. Crawling
>- We used beautifulsoup to displaying notices of IME official page.
3. Tag function
>- We used Taggit for this function. By this function, user's interest can be known through the activity history of the user. And it allows to freely find the questions associated with the tag.

5. Like function
>- We asynchronously put "Like" function based on AJAX & Jquery.

6. Recommend function
>- It is created by accumulating records from user activities such as posting, commenting, and composing replies. For current version, it is applied different weight for each elements.

7. View Count
>- This function was made on an IP-based basis, so an view data can be accumulated once a day for a single post by one IP.

8. Google Visualization
>- Based on the tag data, user can check the activity of oneself's at a glance by pie chart.
