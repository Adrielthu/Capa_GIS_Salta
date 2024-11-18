"""
Este script procesa un archivo CSV que contiene información de lugares populares, corrige tipos
de lugares basados en el nombre del lugar y filtra ciertos tipos no deseados.

El flujo del script incluye las siguientes operaciones:

1. Carga del archivo CSV de entrada.
2. Corrección de tipos de lugares erróneos utilizando patrones en los nombres de los lugares.
3. Filtrado y eliminación de lugares basados en tipos específicos no deseados.
4. Exportación de los resultados procesados a archivos CSV, tanto los lugares filtrados como los no filtrados.
5. Manejo de tipos importantes como hospitales, universidades y escuelas, que son separados y almacenados en un archivo
aparte.

Funciones:
    - load_file(): Carga los datos desde un archivo CSV y los almacena en un DataFrame.
    - save_file(df): Guarda los datos procesados en un archivo CSV de salida.
    - save_filtered_out_file(filtered_out_df): Guarda los lugares filtrados en un archivo CSV separado.
    - replace_wrong_types(df): Corrige los tipos de lugares erróneos basados en los nombres de los lugares.
    - delete_and_export_big_3(df, important_types): Elimina los tipos importantes (hospital, universidad, escuela)
    y los guarda por separado.
    - filter_types(df): Elimina y corrige lugares con tipos específicos que no son deseados en el conjunto de datos.

Variables globales:
    - INPUT_FILE: Ruta del archivo CSV de entrada.
    - OUTPUT_FILE: Ruta del archivo CSV de salida para los datos procesados.
    - FO_OUTPUT_FILE: Ruta del archivo CSV donde se almacenarán los lugares filtrados.
"""

import pandas as pd
import string
import unidecode

# Archivos de entrada y salida
INPUT_FILE = '../3_filtro_por_cercania/Divisor_de_csv/PopularPlaces_FilledType.csv'
OUTPUT_FILE = 'PopularPlaces.csv'
FO_OUTPUT_FILE = 'PopularPlaces-FO.csv'

# Función para cargar los datos utilizando pandas
def load_file():
    """Carga los datos desde el archivo CSV y los almacena en un DataFrame."""
    try:
        df = pd.read_csv(INPUT_FILE)
        print(f"Archivo {INPUT_FILE} cargado exitosamente.")
        return df
    except FileNotFoundError:
        print(f"Error: El archivo {INPUT_FILE} no fue encontrado.")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
        return pd.DataFrame()

# Función para guardar el DataFrame filtrado utilizando pandas
def save_file(df):
    """Guarda los lugares filtrados en un archivo CSV."""
    try:
        df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')
        print(f"Lugares guardados en {OUTPUT_FILE}.")
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")

# Función para guardar los lugares filtrados fuera del set principal
def save_filtered_out_file(filtered_out_df):
    """Guarda los lugares filtrados en un archivo separado."""
    try:
        filtered_out_df.to_csv(FO_OUTPUT_FILE, index=False, encoding='utf-8')
        print(f"Lugares filtrados guardados en {FO_OUTPUT_FILE}.")
    except Exception as e:
        print(f"Error al guardar el archivo filtrado: {e}")


# Función para reemplazar tipos incorrectos basados en el nombre del lugar
def replace_wrong_types(df):
    """Corrige los tipos incorrectos basados en el nombre del lugar."""
    table = str.maketrans(dict.fromkeys(string.punctuation))
    fixed = 0

    for i, row in df.iterrows():
        type = row['type']
        prev_type = type
        name_norm = unidecode.unidecode(row['Name'].lower()).translate(table)

        if 'carniceria' in name_norm and 'butcher_shop' not in type:
            type = 'butcher_shop'
        elif ('polleria' in name_norm or 'aves' in name_norm) and 'poultry_store' not in type:
            type = 'poultry_store'
        elif ('verduleria' in name_norm or 'fruteria' in name_norm) or ('fruta' in name_norm or 'verdura' in name_norm):
            if 'fruit_and_vegetable_store' not in type and ('carniceria' not in name_norm and 'sindicato' not in name_norm):
                type = 'fruit_and_vegetable_store'
        elif ('despensa' in name_norm or 'almacen' in name_norm) and ('liquor_store' not in type and 'grocery' not in type):
            type = 'grocery_store'
        elif ('panaderia' in name_norm or 'confiteria' in name_norm or 'panific' in name_norm) and 'bakery' not in type:
            type = 'bakery'
        elif 'drugstore' in name_norm and 'drugstore' not in type:
            type = 'drugstore'
        elif ('kios' in name_norm or 'quios' in name_norm) and 'empanada' not in name_norm and 'drugstore' not in type:
            type = 'kiosk'
        elif 'farmacia' in name_norm and 'pharmacy' not in type:
            type = 'pharmacy'
        elif 'regaleria' in name_norm and 'gift_shop' not in type:
            type = 'gift_shop'
        elif 'panaler' in name_norm and 'diaper_service' not in type:
            type = 'diaper_service'
        elif ('vivero' in name_norm or 'plantas' in name_norm) and 'garden_center' not in type:
            type = 'garden_center'
        elif 'car_repair' in type:
            if 'respuesto' in name_norm or 'autoparte' in name_norm:
                type = 'auto_parts_store'
            elif 'accesorio' in name_norm:
                type = 'car_accessories_store'
        elif 'moving_company+storage' in type:
            if 'flete' not in name_norm:
                type = 'storage'
            else:
                type = 'moving_company'
        #
        elif 'abertura' in name_norm and 'door_supplier' not in type:
            type = 'door_supplier'
        elif 'gimnasio' in name_norm and 'gym' not in type:
            type = 'gym'
        elif 'peinados' in name_norm and 'beauty_salon' not in type:
            type = 'beauty_salon'
        elif 'sanitarios' in name_norm and 'hardware_store' not in type:
            type = 'hardware_store'
        #
        elif 'centro medico' in name_norm and 'hospital' in type:
            type = 'medical_center'
        elif 'centro de salud' in name_norm and 'hospital' in type:
            type = 'community_health_center'
        elif 'clinica' in name_norm and 'hospital' in type:
            type = 'medical_clinic'
        elif 'jardin' in name_norm and 'school' in type:
            type = 'nursery_school'
        elif 'primaria' in name_norm and 'school' in type:
            type = 'primary_school'
        elif 'secundar' in name_norm and 'school' in type:
            type = 'secondary_school'
        #
        elif 'bus_station' in type and 'terminal' not in name_norm: # paradas de cole
            type = 'transit_station'
        #
        # Añadir más reemplazos según sea necesario

        if prev_type != type:
            df.at[i, 'type'] = type
            fixed += 1

    print(f"{fixed} tipos corregidos.")
    return df

# Función para eliminar y exportar los tipos importantes
def delete_and_export_big_3(df, important_types=['hospital', 'university', 'school']):
    print(f"Separando tipos importantes: {len(df)} registros.")
    filtered_out_df = df[df['type'].apply(lambda x: any(t in x for t in important_types))]
    df = df[~df.index.isin(filtered_out_df.index)]
    print(f"Después de eliminar tipos importantes: {len(df)} registros restantes.")
    return df, filtered_out_df

def filter_types(df):
    """Elimina y corrige lugares según tipos específicos."""
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

    df_filtered = df[~df['type'].apply(lambda x: any(t in x for t in types_to_delete))]

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

    df_filtered['type'] = df_filtered['type'].replace(types_to_change)

    print(f"Filtrado completado: {len(df)} registros -> {len(df_filtered)} registros restantes.")
    return df_filtered


if __name__ == "__main__":
    # Cargar archivo
    df_places = load_file()

    if not df_places.empty:
        # Reemplazar tipos incorrectos
        df_places = replace_wrong_types(df_places)

        # Eliminar y exportar tipos importantes
        #df_places, df_filtered_out = delete_and_export_big_3(df_places)

        # Filtrar tipos no deseados
        df_places = filter_types(df_places)

        # Guardar resultados
        save_file(df_places)
        #save_filtered_out_file(df_filtered_out)