import csv
import random
import datetime
import pgeocode

# csv_file_companies = open('roadconstructioncompanies_ga.csv', 'r')
csv_file_companies = open(
    'roadconstructioncompanies.csv', 'r')

csv_file_telematics_data = open(
    'data/telematics_data_test.csv', 'w')

csv_companies = csv.reader(csv_file_companies)
csv_writer = csv.writer(csv_file_telematics_data)
csv_writer.writerow(['VIN', 'Activity Group Id', 'Date', 'Ops Time', 'Company', 'Product Category',
                     'Product', 'Sensor Category', 'Parameter', 'Description', 'Value', 'State', "Purchase Type", "Age", "Latitude", "Longitude"])


# Setup values
index = -1
initial_state = 'normal_ops'
time_step = 5
end_time = 240
activitiesPerVehicle = 2


def getParameterValue(time, time_step, parameter, value, state, product):
    if "Temp" in parameter:
        new_value = tempFunction(time, time_step, value, state)
    elif parameter == 'Fuel Usage':
        if time == 0:
            new_value = fuelUsageFunction(product)
        else:
            new_value = value * random.uniform(0.99, 1.01)
    elif parameter == 'Oil Pressure':
        if time == 0:
            new_value = oilPressureFunction(product)
        else:
            new_value = value * random.uniform(0.99, 1.01)
    elif parameter == 'Distance':
        new_value = random.uniform(35, 100)
    elif parameter == 'Speed':
        new_value = random.uniform(5, 25)
    elif parameter == 'Grade' or parameter == 'Slope':
        if time == 0:
            new_value = random.uniform(0, 2.5)
        elif value > 2:
            new_value = random.uniform(2.1, 2.5)
        elif value > 1:
            new_value = random.uniform(1.1, 1.9)
        else:
            new_value = random.uniform(0, 0.9)
    else:
        new_value = 0
    return new_value


def tempFunction(current_time, time_step, last_value, state):
    normal_ops_temp = 200
    anomaly_temp = 250
    cooldown_temp = 60
    warmup_time = end_time * 0.2
    cool_down_time = end_time * 0.8
    if current_time > cool_down_time:
        state = 'cooldown'
    if state == 'normal_ops':
        if current_time < warmup_time and last_value < normal_ops_temp:
            temp = last_value + time_step * 5 * random.random()
        if last_value > normal_ops_temp - time_step / 2:
            temp = normal_ops_temp + 2 * random.random() - 2.5
        else:
            temp = last_value + time_step * \
                random.uniform(0.8, 1) - time_step / 2
    elif state == 'anomaly':
        if last_value > anomaly_temp:
            temp = anomaly_temp + 5 * random.random() - 2.5
        else:
            temp = last_value + time_step * 2 * random.random()
    elif state == 'cooldown':
        if last_value < cooldown_temp:
            temp = last_value
        else:
            temp = last_value - time_step * 5 * random.random()
    return temp


productCategories = ['Asphalt Paver',
                     'Asphalt Screed', 'Material Transfer Vehicle', 'Asphalt Milling Machine']


def fuelUsageFunction(product):
    for category in productCategories:
        productChoices = getProductChoices(category)
        if product in productChoices:
            index = productChoices.index(product)
            oilPressure = (index + 1) * 10
            break
    return oilPressure


def oilPressureFunction(product):
    for category in productCategories:
        productChoices = getProductChoices(category)
        if product in productChoices:
            index = productChoices.index(product)
            oilPressure = (index + 1) * 10
            break
    return oilPressure


anomaly_counter = 1


def getState(last_state):
    if last_state == 'anomaly':
        state = last_state
    else:
        number = random.random()
        if number < 0.995:
            state = 'normal_ops'
        else:
            state = 'anomaly'
            print('New Anomaly ' + str(anomaly_counter))
            # anomaly_counter = anomaly_counter + 1
            # print('Anomaly Counter = ' + anomaly_counter)
    return state


def getPurchaseType():
    purchaseChoices = ['New', 'Used', 'Rebuild']
    purchaseType = random.choice(purchaseChoices)
    return purchaseType


def getProductAge():
    productAge = random.randint(1, 9)
    return productAge


def getProductChoices(productCategory):
    if productCategory == 'Asphalt Paver':
        productChoices = ["RP-170e/ex", "RP-175e/ex",
                          "RP-250e", "RP-190e/ex", "RP-195e/ex", "SP-100e", "SP-200e/ex"]
    if productCategory == 'Asphalt Screed':
        productChoices = ["S-8", "S-10", "EZ-IV-8", "EZ-IV-10",
                          "Eagle-8", "Eagle-10", "EZ-R2-10", "EZ-V-10"]
    if productCategory == 'Material Transfer Vehicle':
        productChoices = ["MTV-1100e/ex", "SB-1500e/ex",
                          "SB-2500e/ex", "MTV-1105e", "SB-3000"]
    if productCategory == 'Asphalt Milling Machine':
        productChoices = ["RX-300e/ex", "RX-505",
                          "RX-600e/ex", "RX-600eLR", "RX-700e/ex", "RX-900e/ex"]
    if productCategory == 'Broom':
        productChoices = ["FB-100e", "CB-100"]
    if productCategory == 'CIR Recycling':
        productChoices = ["CIR Milling Machine", "RT-500"]
    if productCategory == 'Stabilizer/Reclaimer':
        productChoices = ["SX-5e", "SX-6e", "SX-8e", 'Grade']
    return productChoices


def getProductAndSensorCategories(productCategory):
    if productCategory == 'Asphalt Paver':
        productChoices = getProductChoices(productCategory)
        product = random.choice(productChoices)
        sensorCategories = ['Engine', 'GPS', 'Grade']
    if productCategory == 'Asphalt Screed':
        productChoices = getProductChoices(productCategory)
        product = random.choice(productChoices)
        sensorCategories = ['Engine', 'Screed', 'GPS', 'Grade']
    if productCategory == 'Material Transfer Vehicle':
        productChoices = getProductChoices(productCategory)
        product = random.choice(productChoices)
        sensorCategories = ['Engine', 'GPS', 'Grade']
    if productCategory == 'Asphalt Milling Machine':
        productChoices = getProductChoices(productCategory)
        product = random.choice(productChoices)
        sensorCategories = ['Engine', 'GPS', 'Grade']
    if productCategory == 'Broom':
        productChoices = getProductChoices(productCategory)
        product = random.choice(productChoices)
        sensorCategories = ['Engine', 'GPS', 'Grade']
    if productCategory == 'CIR Recycling':
        productChoices = getProductChoices(productCategory)
        product = random.choice(productChoices)
        sensorCategories = ['Engine', 'GPS', 'Grade']
    if productCategory == 'Stabilizer/Reclaimer':
        productChoices = getProductChoices(productCategory)
        product = random.choice(productChoices)
        sensorCategories = ['Engine', 'GPS', 'Grade']
    return product, sensorCategories


def getDate():
    start_date = datetime.date(2020, 1, 1)
    end_date = datetime.date(2020, 2, 1)
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return random_date


# sensorCategories = ['Engine', 'Hydraulic System',
#                     'Grade Control', 'Machine Codes', 'Screed']
# sensorCategories = ['Engine', 'Screed', 'GPS']
# parameters = {'Screed': {'Screed Heat': {'description': 'Deg F', 'initial value': 40}}, {'Engine':  {'Fuel Usage': {'description': 'mpg', 'initial value': 22.1}}}

# parameters = {'Screed Heat': {'description': 'Deg F', 'initial value': 40},
# 'Fuel Usage': {'description': 'mpg', 'initial value': 22.1}}

parameters = {
    "Screed": {
        "Sensor 1 Temp": {"description": "Deg F", "initial value": 40},
        "Sensor 2 Temp": {"description": "Deg F", "initial value": 40},
        "Sensor 3 Temp": {"description": "Deg F", "initial value": 40},
        "Sensor 4 Temp": {"description": "Deg F", "initial value": 40},
    },
    "Engine": {
        "Fuel Usage": {"description": "gph", "initial value": 0},
        "Oil Pressure": {"description": "kPa", "initial value": 0},
    },
    "GPS": {
        "Distance": {"description": "ft", "initial value": 0},
        "Speed": {"description": "mph", "initial value": 0},
    },
    "Grade": {
        "Grade": {"description": "deg", "initial value": 0},
        "Slope": {"description": "deg", "initial value": 0},
    },
    # "Electrical": {
    #     "System Voltage": {"description": "V", "initial value": 0},
    #     "Battery": {"description": "V", "initial value": 0},
    # },
    # "Hydraulic": {
    #     "Flow Sensor #1": {"description": "Boolean", "initial value": 0},
    #     "Flow Sensor #2": {"description": "Boolean", "initial value": 0},
    # },
    # "Machine Codes": {
    #     "Conveyor": {"description": "Boolean", "initial value": 0},
    #     "Propel": {"description": "Boolean", "initial value": 0},
    # },
    # "Machine Speeds": {
    #     "Conveyor": {"description": "Boolean", "initial value": 0},
    #     "Propel": {"description": "Boolean", "initial value": 0},
    # }
}

# parameters = {
#     "Screed": {"Panel 1 Temp": {"description": "Deg F", "initial value": 40}}, "Engine": {"Fuel Usage": {"description": "mpg", "initial value": 22.1}}
# }

# print(type(parameters['Screed']))
# print(parameters['Screed']['Panel 1 Temp'])


def getCompanyNameAndCity(row):
    company = f"{row[0].strip()} ({row[2].strip()}, {row[3].strip()})"
    return company


def getCompanyLatLon(row):
    nomi = pgeocode.Nominatim('us')
    geoinfo = nomi.query_postal_code(row[4].strip())
    latitude = geoinfo['latitude']
    longitude = geoinfo['longitude']
    return latitude, longitude


testMode = True
vin = 0
activity_group_id = 0
for row in csv_companies:
    if index == -1:
        index = 0
        continue
    # value = initial_temp + 10*random.random()
    company = getCompanyNameAndCity(row)
    lat, lon = getCompanyLatLon(row)
    for productCategory in productCategories:
        product, sensorCategories = getProductAndSensorCategories(
            productCategory)
        purchaseType = getPurchaseType()
        productAge = getProductAge()
        for activity in range(0, activitiesPerVehicle):
            print("vin =", vin)
            print("activity_group_id=", activity_group_id)
            date = getDate()
            for sensorCategory in sensorCategories:
                # print(parameters[sensorCategory])
                for parameter, param_set in parameters[sensorCategory].items():
                    description = param_set['description']
                    value = param_set['initial value']
                    # print(description, value)
                    state = getState(initial_state)
                    for time in range(0, end_time, time_step):
                        opsTime = time
                        state = getState(state)
                        value = getParameterValue(
                            time, time_step, parameter, value, state, product)
                        csv_writer.writerow([vin, activity_group_id, date, opsTime,
                                             company, productCategory, product, sensorCategory, parameter, description, value, state, purchaseType, productAge, lat, lon])
                        index = index + 1
            activity_group_id = activity_group_id + 1
        vin = vin + 1
    if testMode == True and vin > 30:
        break
print("Number of data points=", index)
