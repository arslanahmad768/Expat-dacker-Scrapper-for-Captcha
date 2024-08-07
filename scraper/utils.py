from DrissionPage import ChromiumOptions, ChromiumPage
import time
import re


def scrap_subcategory(driver, subcategory_href, category):
    ID = url_add = site = email = first_name = last_name = phone = title = description = bared_price = sales_price = type_ = condition = region = \
    address = loc_latitude = loc_longitude = images = categories = Ad_Année_de_construction = Ad_Année_modèle = Ad_Ascenseur = Ad_Boîte_de_vitesse = \
    Ad_Capacité_de_stockage = Ad_Carburant = Ad_Catégorie = Ad_Classe_énergie = ad_couleur = Ad_Couleur_véhicule = Ad_Cylindrée = Ad_Etat = Ad_Expérience = \
    ad_extérieur = ad_kilométrage = ad_marque_auto = ad_marque_moto = ad_modèle_phone = ad_métier = ad_meublé = Ad_Niveau_d_études = ad_nombre_de_chambresv = \
    Ad_Nombre_de_niveaux = Ad_Nombre_de_pièces = Ad_Nombre_de_places = Ad_Nombre_de_portes = ad_nombre_de_salle = Ad_Permis = ad_places_de_parking = \
    Attachments_Path = ad_salaire = ad_secteur_d = Ad_Sous_type = Ad_Surface_habitable = Ad_Surface_totale = ad_travail = Ad_Type_de_billet = \
    ad_type_de_contrat = Ad_Type_de_produit = ad_type_de_véhicule = Ad_Type_moto = Ad_Type_nautisme = ""

    # print("driver data====", driver.html)
    original_page_source = driver.html
    subcategory_content_list = driver.eles('.listings-cards__list-item ')
    subcategory_info = []
    for subcategory_content in subcategory_content_list:
        subCategory_content_href = subcategory_content.s_ele('.listing-card__inner').attr('href')
        subcategory_info.append(subCategory_content_href)

    for subCategory_content_url in subcategory_info:
        # subcategory_content = subcategory_content_list[index]
        # print("sobcatgeory===", subcategory_content)
        # subCategory_content_href = subcategory_content.s_ele('.listing-card__inner')
        # subCategory_content_url = subCategory_content_href.attr('href')
        # print("content href===", subCategory_content_href.attr('href'))
        print("url of subcategory==", subCategory_content_url)
        driver.get(subCategory_content_url)
        time.sleep(5)

        pattern = r"(\d+)$"
        match_ = re.search(pattern, subCategory_content_url)
        if match_:
            ID = match_.group(1)
            print("ID---", ID)
        url_add = subCategory_content_url
        site = "https://www.expat-dakar.com/"
        name_tag = driver.s_ele('.listing-item-transparency__title').text
        name = re.sub(r'[^a-zA-Z\s]', '', name_tag)
        full_name = name.split(" ")
        if len(full_name) == 2:
            print("fullname---", full_name)
            first_name, last_name = full_name[0], full_name[1]
        elif len(full_name) >= 3:
            print("fullname---", full_name)
            first_name = f'{full_name[0]} {full_name[1]}'
            last_name = ' '.join(full_name[2:])
        else:
            print("fullname---", full_name)
            first_name, last_name = full_name[0], ''
        print("first name====", first_name, "last name===", last_name)
        phone_tag = driver.s_ele('.listing-item-contact__contact-phone__number').attr('href')
        phone = phone_tag.replace("tel:","")
        print("phone number is===", phone)
        title = driver.title
        print("title===", title)
        description = driver.s_ele(".listing-item__description").text
        print("description====", description)
        price =  driver.s_ele(".listing-item__price")
        if price:
            sales_price_tag = price.s_ele(".listing-card__price__deal")
            if sales_price_tag:
                sales_price = sales_price_tag.text
                bared_price = price.s_ele(".listing-card__price__value 1").text
            else:
                sales_price = price.text

        print("Sales price===", sales_price)
        type_ = 6 if 'location' in subCategory_content_url else 1
        print("type===", type_)
        # condition
        region = driver.s_ele(".listing-item__address-region").text
        print("region===", region)
        address = driver.s_ele(".listing-item__address-location").text
        print("address===", address)
        images_ = driver.s_ele(".gallery gallery--main ")
        images_tag = images_.eles('.gallery__image__resource vh-img')
        image_urls = []
        count = 0
        for img in images_tag:
            img_url = img.attr('src')
            image_urls.append(img_url)
            count += 1
            if count >=5:
                break
        if image_urls:
            images = '||'.join(image_urls)
        print("images===", images)
        Ad_Année_modèle = description_detail(driver, "Année Modèle")
        print("model year===", Ad_Année_modèle)
        category_description = driver.s_ele('.listing-item__description').text
        if  "ascenseur" in  category_description:
            Ad_Ascenseur = "oui"
        else:
            Ad_Ascenseur = "non"
        print("Ad_Ascenseur", Ad_Ascenseur)
        Ad_Boîte_de_vitesse = description_detail(driver, "Transmission")
        print("bolte de vitassa===", Ad_Boîte_de_vitesse)

        Ad_Capacité_de_stockage = description_detail(driver, "Stockage")
        print("Ad_Capacité_de_stockage===", Ad_Capacité_de_stockage)

        Ad_Carburant = description_detail(driver, "Carburant")
        print("Ad_Carburant===", Ad_Carburant)

        ad_couleur = description_detail(driver, "Couleur")
        if not ad_couleur:
            ad_couleur = "Autre"

        Ad_Couleur_véhicule = "Autre"
        colors = ["blanc", "bleu", "gris clair", "gris poivre", "jaune", "marron", "meuve", "noir", "orange", "rose", "rouge", "vert", "violet"]
        if category_description:
            # Search for the color in the text content
            for possible_color in colors:
                if possible_color in category_description.lower():
                    Ad_Couleur_véhicule = possible_color
                    break
        print("vehicle color===", Ad_Couleur_véhicule)
        Ad_Etat = description_detail(driver, 'Etat')
        print("Ad_Etat===", Ad_Etat)
        if category_description:
            Ad_Expérience = get_experience(category_description)
            ad_places_de_parking = check_parking(category_description)
        print("Ad_Expérience===", Ad_Expérience)

        Ad_Extériour_sample = ["balcon", "jardin", "térasse"]
        if category_description:
            lower_text = category_description.lower()
            results = {word: word.lower() in lower_text for word in Ad_Extériour_sample}
            Ad_Extérieur_ = [word for word, found in results.items() if found]
            if Ad_Extérieur_:
                ad_extérieur = str(Ad_Extérieur_)
        print("Ad_Extérieur====", ad_extérieur)
        ad_kilométrage = description_detail(driver, 'Kilométrage')
        print("Ad_Kilométrage====", ad_kilométrage)
        if "Voitures" in category:
            ad_marque_auto = description_detail(driver, "Marque")
        elif "Motos & scooters" in category:
            ad_marque_moto = description_detail(driver, "Marque")
        elif "Téléphones" in category:
            ad_modèle_phone = description_detail(driver, "Marque")
        ad_métier_sample = [
                            "Administrateur", "Avocat", "Commercial & Vente", "Comptabilité & Gestion", "Conseil & Audit", "Direction générale"
                            "Étude & Recherche & Ingénierie", "Formation & Etude", "Informaticien", "Juriste", "Logistique & Transport", "Marketing & Communication",
                            "Médecine & Santé", "Ménage & Entretien", "Musique", "Ouvrier & Artisan", "Production & Opération", "Ressources Humaines",
                            "Sécurité & Défense & Gardiennage", "Service client & Accueil"
                            ]
        detail_tag = driver.s_ele('.listing-item__header')
        if detail_tag:
            detail_txt = detail_tag.text.lower()
            if "Services" in category:
                ad_metier_list = detail_txt.split(" ")
                for metier_data in ad_metier_list:
                    for sample_metier_data in ad_métier_sample:
                        if sample_metier_data.lower() in metier_data:
                            ad_métier = sample_metier_data
            if "meublé" in detail_txt:
                ad_meublé = "oui"
            else:
                ad_meublé = "non"
        ad_nombre_de_chambresv = description_detail(driver, 'Chambres')
        ad_nombre_de_salle = description_detail(driver, 'Salle de Bain')
        ad_salaire_tag = driver.s_ele('.listing-card__price__value 1')
        if ad_salaire_tag:
            ad_salaire = ad_salaire_tag.text
        ad_sector_activity = ["Agriculture", "Automobile", "Autre", "Banque & Assurance & Finance", "BTP Construction", "Commerce & Distribution", "Elevage",
                              "Environnement", "Immobilier", "Industrie", "Restaurant & Hôtellerie", "Secteurs publics", "Service", "Services", "Sport",
                              "Télécom & Internet & Média", "Textile & Mode & Luxe", "Tourisme", "Transport & Logistique"]
        ad_sector = description_detail(driver, "Secteur d'activité")
        if ad_sector:
            data = ad_sector.lower().split(" ")
            for sector in data:
                for sample_sector in ad_sector_activity:
                    if sector in sample_sector.lower():
                        ad_secteur_d = sample_sector
                        break
        Ad_Surface_totale = description_detail(driver, "Mètres carrés")
        ad_type_de_contrat = description_detail(driver, "Type de contrat")
        print("ad_type_de_contrat===", ad_type_de_contrat)
        ad_type_de_véhicule = description_detail(driver, "Carrosserie")
        print("ad_type_de_véhicule===", ad_type_de_véhicule)
        # driver.get(subcategory_href)
        # time.sleep(5)
        # driver.load_mode(original_page_source)
        # Refresh the elements list to continue iterating correctly
        # subcategory_content_list = driver.eles('.listings-cards__list-item ')

def description_detail(driver, text):
    element = driver.s_ele(f'text:{text}')
    if element:
        next_sibling = element.s_ele('xpath=following-sibling::*[1]')
        vehicle_description = next_sibling.text
        return vehicle_description
    return ''

def check_parking(description):
    ad_places_de_parking = 0
    parking_pattern = re.search(r'(\d*)\s*parking', description, re.IGNORECASE)

    if parking_pattern:
        if parking_pattern.group(1):
            ad_places_de_parking = int(parking_pattern.group(1))
        else:
            ad_places_de_parking = 1

    return ad_places_de_parking

def get_experience(input_string):
    # Use regex to find a digit followed by optional space and "ans" or "an"
    match = re.search(r'(\d+)\s*(ans?|an)\b', input_string)

    if match:
        # Extract the digit and convert it to an integer
        digit = int(match.group(1))

        # Check if the digit is greater than 10
        if digit > 10:
            return '10 ans et plus'
        elif digit == 1:
            return f'{digit} an'
        else:
            return f'{digit} ans'

    return ''


def extract_region_and_address(location_string):
  # Split the string by comma
  parts = location_string.split(',')

  # Strip leading/trailing whitespace from each part
  parts = [part.strip() for part in parts]
  print("parts----", parts)
  # Assign region and address based on the number of parts
  if len(parts) == 3:
      address, region  = parts[0], parts[1]
  elif len(parts) == 2:
      address, region  = "", parts[0]
  else:
      address, region = '', parts[0] if parts else ''

  return region, address  
        


def create_chromium_driver():
    """
    Creates a Chromium driver instance and navigates to the specified URL.
    @return:
    ChromiumPage: A Chromium driver instance.
    """
    options = ChromiumOptions()
    arguments = [
        "-no-first-run",
        "-force-color-profile=srgb",
        "-metrics-recording-only",
        "-password-store=basic",
        "-use-mock-keychain",
        "-export-tagged-pdf",
        "-no-default-browser-check",
        "-disable-background-mode",
        "-enable-features=NetworkService,NetworkServiceInProcess,LoadCryptoTokenExtension,PermuteTLSExtensions",
        "-disable-features=FlashDeprecationWarning,EnablePasswordsAccountStorage",
        "-deny-permission-prompts",
        "-disable-gpu"
    ]
    for argument in arguments:
        options.set_argument(argument)
        
    # Adjusting the instantiation to match the expected parameters
    driver = ChromiumPage(addr_or_opts=options)
    return driver

