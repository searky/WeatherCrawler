# WeatherCrawler
Get weather information from www.weather.com.cn<br>
You can reference the article from this URL: https://www.lao-wang.com/?p=80<br>
## data table struct
### weather_city
Name | Type | Extra
------------ | ------------- | -------------
wid | int | AI, PK
cityid | int | 
city | varchar(64) | 

### weather_items
Name | Type | Extra
------------ | ------------- | -------------
wid | int | AI, PK
cityid | int | 
weather | varchar(5) | 
temp | int | 
humidity | int | 
wd | varchar(16) | 
ws | varchar(10) | 
rain | float | 
aqi | int | 
udate | date | 
utime | time | 


### weather_wcode
Name | Type | Extra
------------ | ------------- | -------------
wid | int | AI, PK
code | varchar(5) | 
name | varchar(10) | 
