# -*- coding: utf-8 -*-

import string
import unidecode

INPUT_FILE = 'C:/Users/adrie/Desktop/TUPED/capa_GIS/Geo_Salta_24/4_busqueda_places_tipo/PopularPlacesFull-.csv'
OUTPUT_FILE = 'C:/Users/adrie/Desktop/TUPED/capa_GIS/Geo_Salta_24/5_filtrar_por_tipo/PopularPlaces.csv'
FO_OUTPUT_FILE = 'C:/Users/adrie/Desktop/TUPED/capa_GIS/Geo_Salta_24/5_filtrar_por_tipo/PopularPlaces-FO.csv'

CSV_HEADER = 'Name,type,ratings,latitude,longitude,place_id\n' # Header que le gusta a Google Maps

ids = []
names = []
types = []
ratings = []
lats = []
lngs = []

filtered_out = []

def load_file():
    in_file = open(INPUT_FILE, encoding='utf-8')
    in_file.readline() # header
    for line in in_file.readlines():
        splited = line[:-1].split(',') # borrar /n
        if len(splited) < 6:
            continue
        #
        name = splited[0]
        type = splited[1]
        rating = splited[2]
        lat = splited[3]
        lng = splited[4]
        idp = splited[5]
        #
        ids.append(idp)
        names.append(name)
        types.append(type)
        ratings.append(int(rating))
        lats.append(float(lat))
        lngs.append(float(lng))
        #
    in_file.close()

def save_file():
    out_file = open(OUTPUT_FILE, 'w', encoding='utf-8')
    out_file.write(CSV_HEADER)
    for i in range(len(ids)):
        out_file.write(f'{names[i]},{types[i]},{ratings[i]},{lats[i]},{lngs[i]},{ids[i]}\n') # Guardo los datos minimos
    out_file.close()

def save_filtered_out_file():
    out_file = open(FO_OUTPUT_FILE, 'w', encoding='utf-8')
    out_file.write(CSV_HEADER)
    for line in filtered_out:
        out_file.write(line)
    out_file.close()

def save_place_info(idx):
    filtered_out.append(f'{names[idx]},{types[idx]},{ratings[idx]},{lats[idx]},{lngs[idx]},{ids[idx]}\n')

def delete_item(index):
    try:
        del ids[index]
        del names[index]
        del types[index]
        del ratings[index]
        del lats[index]
        del lngs[index]
    except Exception as e:
        print(e)

def delete_items(indexes):
    indexes.sort(reverse = True)
    for i in indexes:
        delete_item(i)
    indexes.clear()

def replace_wrong_types():
    # Reemplazar types erroneos o faltantes
    print('Corrigiendo types erroneos: ', end = '')
    table = str.maketrans(dict.fromkeys(string.punctuation))
    fixed = 0
    for i in range(len(ids)):
        type = types[i]
        prev_type = type
        _ = unidecode.unidecode(names[i].lower())
        _ = _.translate(table)
        #
        if 'carniceria' in _ and 'butcher_shop' not in type:
            type = 'butcher_shop'
        elif ('polleria' in _ or 'aves' in _) and 'poultry_store' not in type:
            type = 'poultry_store'
        elif ('verduleria' in _ or 'fruteria' in _) or ('fruta' in _ or 'verdura' in _):
            if 'fruit_and_vegetable_store' not in type and ('carniceria' not in _ and 'sindicato' not in _):
                type = 'fruit_and_vegetable_store'
        elif ('despensa' in _ or 'almacen' in _) and ('liquor_store' not in type and 'grocery' not in type):
            type = 'grocery_store'
        elif (('panaderia' in _ and 'panaderias' not in _) or 'confiteria' in _ or 'panific' in _) and 'bakery' not in type:
            type = 'bakery'
        elif 'drugstore' in _ and 'drugstore' not in type:
            type = 'drugstore'
        elif ('kios' in _ or 'quios' in _) and 'empanada' not in _ and 'drugstore' not in type:
            type = 'kiosk'
        elif 'farmacia' in _ and 'pharmacy' not in type:
            type = 'pharmacy'
        elif 'regaleria' in _ and 'gift_shop' not in type:
            type = 'gift_shop'
        elif 'panaler' in _ and 'diaper_service' not in type:
            type = 'diaper_service'
        elif ('vivero' in _ or 'plantas' in _) and 'garden_center' not in type:
            type = 'garden_center'
        elif 'car_repair' in type:
            if 'respuesto' in _ or 'autoparte' in _:
                type = 'auto_parts_store'
            elif 'accesorio' in _:
                type = 'car_accessories_store'
        elif 'moving_company+storage' in type:
            if 'flete' not in _:
                type = 'storage'
            else:
                type = 'moving_company'
        #
        elif 'abertura' in _ and 'door_supplier' not in type:
            type = 'door_supplier'
        elif 'gimnasio' in _ and 'gym' not in type:
            type = 'gym'
        elif 'peinados' in _ and 'beauty_salon' not in type:
            type = 'beauty_salon'
        elif 'sanitarios' in _ and 'hardware_store' not in type:
            type = 'hardware_store'
        #
        elif 'centro medico' in _ and 'hospital' in type:
            type = 'medical_center'
        elif 'centro de salud' in _ and 'hospital' in type:
            type = 'community_health_center'
        elif 'clinica' in _ and 'hospital' in type:
            type = 'medical_clinic'
        elif 'jardin' in _ and 'school' in type:
            type = 'nursery_school'
        elif 'primaria' in _ and 'school' in type:
            type = 'primary_school'
        elif 'secundar' in _ and 'school' in type:
            type = 'secondary_school'
        #
        elif 'bus_station' in type and 'terminal' not in _: # paradas de cole
            type = 'transit_station'
        #
        if prev_type != type:
            types[i] = type
            fixed += 1
    print(fixed)

def delete_empty_types():
    # Elimina los que tienen coordinadas repetidas
    print('Eliminando types vacios:', len(ids), end = '')
    no_type = list([i for i,type in enumerate(types) if not type])
    # Exporta por las dudas los que tengan algo de rating
    filtered_out.append('# TYPE NULO\n')
    [save_place_info(i) for i in no_type if ratings[i] > 4]
    #
    delete_items(no_type)
    print(' >', len(ids))

def delete_and_export_shady_types():
    # Elimina los 'importantes' que no concuerdan con el typo
    print('Separando types dudosos:', len(ids), end = '')
    table = str.maketrans(dict.fromkeys(string.punctuation))
    del_index = []
    #
    filtered_out.append('# TYPE DUDOSO\n')
    for i in range(len(ids)):
        type = types[i]
        _ = unidecode.unidecode(names[i].lower())
        _ = _.translate(table)
        #
        if 'hospital' in type and ('hospital' not in _ or 'sanatorio' in _ or 'clinica' in _): # hospitales dudosos
            del_index.append(i)
        elif 'university' in type and ('facultad' not in _ or 'universidad' in _): # universidades dudosas
            del_index.append(i)
        elif '+school' in type and ('colegio' not in _ or 'escuela' not in _ or 'esc' not in _ or 'instituto' not in _): # escuelas dudosas
            del_index.append(i)
        else:
            continue
        save_place_info(i)
    #
    delete_items(del_index)
    print(' >', len(ids))

def delete_and_export_big_3():
    # Separa los types importantes: hospital, university, school para filtrarlos manualmente
    print('Separando types importantes:', len(ids), end = '')
    del_index = []
    filtered_out.append('# TYPE IMPORTANTES\n')
    for i,type in enumerate(types):
        for ts in type.split('+'):
            if ts in ['hospital','university','school']:
                del_index.append(i)
                save_place_info(i)
                break
    #
    delete_items(del_index)
    print(' >', len(ids))

def filter_types():
    # Reemplazar types erroneos o faltantes
    print('Corrigiendo / eliminando segun types:', len(ids), end = '')
    types_to_delete = [
'transit_station', # parada de cole, no es lugar de permanencia
'parking', # playa de estac, no es lugar de permanencia
'emergency_room',
'masonry_contractor',
'ambulance_service',
'tent_rental_service',
'food_manufacturer',
'awning_supplier',
'distance_learning_center',
'roofing_contractor',
'dive_club',
'life_coach',
'drinking_water_fountain',
'importer',
'exhibition_and_trade_center',
'glass_repair_service',
'commercial_agent',
'observatory',
'personal_trainer',
'housing_complex',
'boarding_house',
'home_health_care_service',
'student_housing_center',
'e_commerce_service',
'training_center',
'vocational_training_school',
'painter',
'arts_organization',
'assisted_living_facility',
'well_drilling_contractor',
'business_broker',
'haunted_house',
'industrial_gas_supplier',
'business_center',
'swimming_basin',
'dog_trainer',
'student_dormitory',
'gift_basket_store',
'custom_home_builder',
'entertainer',
'temp_agency',
'house_sitter',
'scenic_spot',
'country_house',
'green_energy_supplier',
'bicycle_club',
'arena',
'gasfitter',
'engineer',
'condominium_complex',
'housing_society',
'historical_landmark',
'tourist_attraction',
'handyman',
'dj',
'plumber',
'bridge',
'apartment_complex',
'adventure_sports']
    types_to_change = {
'technical_school':'secondary_school',
'debt_collecting':'money_transfer_service',
'home_goods_store+clothing_store':'clothing_store',
'movie_rental+furniture_store':'home_goods_store+electronics_store',
'pharmacy+veterinary_care':'veterinary_care',
'convenience_store+book_store':'convenience_store',
'meal_takeaway+restaurant':'meal_takeaway',
'library+book_store':'library',
'haberdashery':'notions_store',
'grocery_or_supermarket+storage':'grocery_or_supermarket',
'electronics_store+furniture_store':'electronics_store',
'bakery+grocery_or_supermarket':'bakery',
'bakery+meal_takeaway':'bakery',
'bakery+restaurant':'bakery',
'neon_sign_shop':'sign_shop',
'clothes_market':'clothing_store',
'rugby':'rugby_club',
'alternative_fuel_station':'gas_station',
'dance_hall':'night_club',
'army_base':'military_base',
'wood_stove_shop':'firewood_supplier',
'phone_repair_service':'mobile_phone_repair_shop',
'cleaners':'cleaning_products_supplier',
'plastic_bag_supplier':'packaging_supply_store',
'motorcycle_shop':'motorcycle_dealer',
'gambling_house':'betting_agency',
'pharmaceutical_lab':'corporate_office',
'shipping_equipment_industry':'moving_company',
'tool_rental_service':'tool_store',
'customs_broker':'lawyer',
'foundation':'non_profit_organization',
'paintings_store':'digital_printer',
'child_care_agency':'nursery_school',
'motorsports_store':'car_dealer',
'computer_hardware_manufacturer':'computer_accessories_store',
'cheese_shop':'cold_cut_store',
'specialized_clinic':'medical_clinic',
'frozen_food_manufacturer':'meal_takeaway',
'paralegal_services_provider':'law_firm',
'sewing_shop':'clothing_store',
'livery_company':'association_or_organization',
'sewing_machine_repair_service':'machine_shop',
'indoor_playground':'childrens_party_service',
'woodworking_supply_store':'furniture_store',
'adult_day_care_center':'association_or_organization',
'elevator_service':'industrial_equipment_supplier',
'marina':'club',
'printer_repair_service':'computer_accessories_store',
'vehicle_shipping_agent':'bus_company',
'video_arcade':'children_amusement_center',
'blood_testing_service':'medical_lab',
'machine_workshop':'repair_service',
'art_studio':'handicraft',
'wedding_photographer':'photographer',
'charity':'non_profit_organization',
'mortgage_lender':'loan_agency',
'airport_shuttle_service':'transportation_service',
'video_production_service':'media_company',
'chemistry_lab':'medical_lab',
'information_services':'software_company',
'aquarium':'pet_store',
'wholesale_drugstore':'drugstore',
'cosmetic_products_manufacturer':'cosmetics_store',
'hobby_store':'gift_shop',
'woodworker':'furniture_store',
'livestock_breeder':'agricultural_service',
'delivery_service':'bar',
'fire_protection_equipment_supplier':'store',
'financial_consultant':'loan_agency',
'electronic_parts_supplier':'electronics_store',
'fireworks_store':'store',
'organic_store':'store',
'art_handcraft':'art_school',
'gun_shop':'hunting_and_fishing_store',
'swimming_pool':'swimming_pool_contractor',
'holding_company':'corporate_office',
'solar_hot_water_system_supplier':'solar_energy_equipment_supplier',
'chocolate_cafe':'candy_store',
'soup_kitchen':'community_center',
'battery_store':'store',
'confectionery':'bakery',
'portrait_studio':'photography_studio',
'building_consultant':'building_firm',
'metal_fabricator':'metal_workshop',
'electronics_manufacturer':'electronics_company',
'sheet_metal_contractor':'service',
'bullring':'park',
'fish_processing':'fish_store',
'employment_agency':'civil_registry',
'paper_mill':'packaging_company',
'heating_contractor':'repair_service',
'antique_furniture_restoration_service':'repair_service',
'marble_contractor':'furniture_manufacturer',
'food_court':'bar',
'cultural_association':'community_center',
'blueprint_service':'service',
'residents_association':'community_center',
'box_lunch_supplier':'meal_takeaway',
'ophthalmology_clinic':'doctor',
'counselor':'engineering_consultant'}
    manual_check = [] # agregar types para chequear manualmente

    del_index = []
    fixed = 0
    for i in range(len(ids)):
        type = types[i]
        prev_type = type
        #
        if type in types_to_change:
            type = types_to_change[type]
        #
        splited_types = type.split('+')
        if len(splited_types) == 1:
            if type in types_to_delete:
                del_index.append(i)
        else:
            deleted = False
            for ti in reversed(range(len(splited_types))):
                if splited_types[ti] in types_to_delete:
                    del splited_types[ti]
                    deleted = True
            if deleted:
                if not splited_types: # se borraron todos
                    del_index.append(i)
                else:
                    type = '+'.join(splited_types) # no es necesario join ya que tienen maximo 2 types
        #
        if type in manual_check:
            names[i] += '***'
        if prev_type != type:
            types[i] = type
            fixed += 1
    #
    delete_items(del_index)
    print(' >', len(ids))

#
load_file()
full_count = len(ids)

replace_wrong_types()
delete_empty_types()
delete_and_export_shady_types()
delete_and_export_big_3()
filter_types()

save_file()
save_filtered_out_file()

print('Total:', full_count)
print('Guardados:', len(ids))