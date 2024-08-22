Google_News = "Google"
Search_Google_News = "Search_Google_News"

Yahoo_News = "Yahoo"
Search_Yahoo_News = "Search_Yahoo_News"

Bing_News = "Bing"
Search_Bing_News = "Search_Bing_News"

Duck_News = "Duck"
Search_Duck_News = "Search_Duck_News"

#####################################################
BBC_News = "BBC"
Search_BBC_News = "Search_BBC_News"

CNN_News = "CNN"
Search_CNN_News = "Search_CNN_News"

Global_News = "Global News"
Search_Global_News = "Search_Global_News"

NewYork_Times_News = "NewYork Times"
Search_NewYork_Times_News = "Search_NewYork_Times_News"

USA_Today_News = "USA Today"
Search_USA_Today_News = "Search_USA_Today_News"

####################################################

Youm7_News = "El youm 7"
Search_Youm7_News = "Search_Youm7_News"

Daily_Egypt_News = "Daily Egypt"
Search_Daily_Egypt_News = "Search_Daily_Egypt_News"

Egyptian_Streets_News = "Egyptian Streets"
Search_Egyptian_Streets_News = "Search_Egyptian_Streets_News"

Masr_Elyoum_News = "Masr Elyoum"
Search_Masr_Elyoum_News = "Search_Masr_Elyoum_News"

Masrawy_News = "Masrawy"
Search_Masrawy_News = "Search_Masrawy_News"

Ahram_Gate_News = "Ahram Gate"
Search_Ahram_Gate_News = "Search_Ahram_Gate_News"

####################################################
Single_Article_Scraping = "Single_Article_Scraping"
####################################################
ENGINE_SCRAPPING_SERVICES = {
    Search_Google_News: Google_News,
    Search_Yahoo_News: Yahoo_News,
    Search_Bing_News: Bing_News,
    Search_Duck_News: Duck_News,
}

GLOBAL_NEWS_SCRAPPING_SERVICES = {
    Search_BBC_News: BBC_News,
    Search_CNN_News: CNN_News,
    Search_Global_News: Global_News,
    Search_NewYork_Times_News: NewYork_Times_News,
    Search_USA_Today_News: USA_Today_News,
}

EGYPTIAN_NEWS_SCRAPPING_SERVICES = {
    Search_Youm7_News: Youm7_News,
    Search_Daily_Egypt_News: Daily_Egypt_News,
    Search_Egyptian_Streets_News: Egyptian_Streets_News,
    Search_Masr_Elyoum_News: Masr_Elyoum_News,
    Search_Masrawy_News: Masrawy_News,
    Search_Ahram_Gate_News: Ahram_Gate_News,
}

ALL_NEWS_SCRAPPING_SERVICES = {
    **ENGINE_SCRAPPING_SERVICES,
    **GLOBAL_NEWS_SCRAPPING_SERVICES,
    **EGYPTIAN_NEWS_SCRAPPING_SERVICES,
}
