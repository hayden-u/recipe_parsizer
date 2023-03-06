from recipe_scrapers import scrape_me

scraper = scrape_me('https://elavegan.com/gluten-free-vegan-spring-rolls/', wild_mode = True)

print(scraper.host())
print(scraper.total_time())
print(scraper.ingredients())
print(scraper.instructions())
print(scraper.instructions_list())
