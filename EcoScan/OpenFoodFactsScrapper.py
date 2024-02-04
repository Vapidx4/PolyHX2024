from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from . import Barcode

# https://world.openfoodfacts.org/

def runSelenium():
    global source
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    source = driver.page_source
    driver.quit()

def scrapWebsite():
    dataDict = {}
    doc = BeautifulSoup(source, "html.parser")

    titleTag = doc.find("title")

    if titleTag:
        productName = titleTag.text.strip()
        if productName == "Error":
            print("No data is available for this barcode")
            return
        dataDict["Product Name"] = productName

    packaging_p = doc.find("p", id="field_packaging")

    if packaging_p:
        packagings = packaging_p.find_all("a", class_="tag well_known")

        if packagings:

            packagingsList = []

            for packaging in packagings:
                packagingsList.append(packaging.get_text(strip=True))
            dataDict["Packagings"] = packagingsList

    ingredientsOrigin_p = doc.find("p", id="field_origins")

    if ingredientsOrigin_p:
        ingredientsOrigin = ingredientsOrigin_p.find_all("a")

        if ingredientsOrigin:

            ingredientsOriginList = []

            for ingredient in ingredientsOrigin:
                ingredientsOriginList.append(ingredient.get_text(strip=True))

            dataDict["Origin of Ingredients"] = ingredientsOriginList

    manufacturer_p = doc.find("p", id="field_manufacturing_places")

    if manufacturer_p:
        manufacturer = manufacturer_p.find("a")
        if manufacturer:
            dataDict["Manufacturer"] = manufacturer.get_text(strip=True)

    productScores = doc.find("div", class_="v-space-short", id="product_summary")

    if productScores:
        scores = productScores.find_all("h4")

        if scores:

            scoresList = []

        for score in scores:
            scoreData = score.get_text(strip=True)
            scoresList.append(scoreData)

        dataDict["Scores"] = scoresList

    carbonFootprint_ul = doc.find("ul", class_="panel_accordion accordion", id="panel_carbon_footprint")

    if carbonFootprint_ul:
        carbonFootprint = carbonFootprint_ul.find_next("h5").get_text(strip=True)

        if carbonFootprint:
            dataDict["Carbon Footprint"] = carbonFootprint

    packagingImpact_a = doc.find("a", {"href": "#panel_packaging_recycling_content", "class": "panel_title"})

    if packagingImpact_a:
        packagingImpact = packagingImpact_a.find("h4").get_text(strip=True)

        if packagingImpact_a:
            dataDict["Packaging Impact"] = packagingImpact

    ingredientsImpact_a = doc.find("a", {"href": "#panel_origins_of_ingredients_content", "class": "panel_title"})

    if ingredientsImpact_a:
        ingredientsImpact = ingredientsImpact_a.find("h5").get_text(strip=True)
        if ingredientsImpact:
            dataDict["Ingredients Impact"] = ingredientsImpact

    return dataDict

def getBarecodeData(img):
    global url
    barcodeData = Barcode.readBarcode(img)
    if barcodeData:
        barcodeCode = barcodeData[0]
        print(barcodeData)
        url = f"https://world.openfoodfacts.org/product/{barcodeCode}"
        runSelenium()
        dataDict = scrapWebsite()
        return dataDict
    else:
        print("The barcode couldn't be read")