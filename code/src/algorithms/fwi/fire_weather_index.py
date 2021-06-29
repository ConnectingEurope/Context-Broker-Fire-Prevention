import algorithms.fwi.fwi_functions as fwi

#FWI class to store the needed parameters
class FireWeatherIndex():
    def __init__(self, temperature, relative_humidity, wind, rain, FFMCPrev, DMCPrev, DCPrev, month):
        self.temperature = temperature
        self.relative_humidity = relative_humidity
        self.wind = wind
        self.rain = rain
        self.FFMCPrev = FFMCPrev
        self.DMCPrev = DMCPrev
        self.DCPrev = DCPrev
        self.month = month
        self.FFMC = 0.0
        self.DMC = 0.0
        self.DC = 0.0
        self.ISI = 0.0
        self.BUI = 0.0
        self.FWI = 0.0
        self.DSR = 0.0
    
    #This method calculate the fire weather index taking into account the itermediate indexes
    def calculate_fire_weather_index(self):
        self.FFMC = fwi.FFMC(self.temperature, self.relative_humidity, self.wind, self.rain, self.FFMCPrev)
        self.DMC = fwi.DMC(self.temperature, self.relative_humidity, self.rain, self.DMCPrev, self.month)
        self.DC = fwi.DC(self.temperature, self.rain, self.DCPrev, self.month)
        self.ISI = fwi.ISI(self.wind, self.FFMC)
        self.BUI = fwi.BUI(self.DMC, self.DC)
        self.FWI = fwi.FWI(self.ISI, self.BUI)

    def calculate_daily_severity_rating(self):
        self.DSR = fwi.DSR(self.FWI)
