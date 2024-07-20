import time
from .utils import create_chromium_driver, scrap_subcategory
def scrape_expat_dakar(website_url):
    driver = create_chromium_driver()
    driver.get(website_url)
    category_info = []
    time.sleep(10)
    categories_list =  driver.eles(".home-categories__item")
    print("element text---", len(categories_list))
    for category in categories_list:
        main_category_title = category.s_ele(".home-category__header__title").text
        subcategory_list = category.eles(".home-category__list-item__link")
        subcategories = [
            {
                "title": subcategory.text,
                "href": subcategory.attr('href')
            }
            for subcategory in subcategory_list
        ]
        category_info.append({
            "main_category_title": main_category_title,
            "subcategories": subcategories
        })

    # Navigate through stored category information
    for category in category_info:
        print("Main category:", category["main_category_title"])
        for subcategory in category["subcategories"]:
            subcategory_title = subcategory["title"]
            subcategory_href = subcategory["href"]
            print("Subcategory title:", subcategory_title)
            print("Subcategory href:", subcategory_href)
            driver.get(subcategory_href)
            time.sleep(5)
            print("driver title===", driver.title)
            # Call your scraping function here
            scrap_subcategory(driver, subcategory_href, f'{category["main_category_title"]}>{subcategory_title}')
            
            driver.back()
            time.sleep(2)

    # for category in categories_list:
    #     main_category_title = category.s_ele(".home-category__header__title").text
    #     subcategory_list = category.eles(".home-category__list-item__link")
    #     print("total vehicle list----", len(subcategory_list))
    #     for subcategory in subcategory_list:
    #         print("subcategory====", subcategory)
    #         subcategory_title = subcategory.text
    #         subcategory_href = subcategory.attr('href')
    #         print("subcategory herf---", subcategory_title)
    #         print("subcategory herf---", subcategory_href)
    #         driver.get(subcategory_href)
    #         time.sleep(5)
    #         driver.back()
    #         time.sleep(2)
    #         categories_list = driver.eles(".home-categories__item")
    #         print("subcategory-----", categories_list)
    #         print("category-----", category)
    #         category = categories_list[categories_list.index(category)]
    #         subcategory_list = category.eles(".home-category__list-item__link")
            
        driver.back()
        time.sleep(2)
            
            
