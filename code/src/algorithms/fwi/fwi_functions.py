import math

#Calculates the FFMC
def FFMC(temp, relative_humidity, wind, rain, FFMCPrev):
    # mo          -initial fine fuel MC 
    # m           -final  MC 
    # mr          -fine fuel moisture content after rain
    # ed          -EMC for  drying 
    # ew          -EMC for wetting  
    # ko and kl   -intermediate steps to  kd and kw 
    # kd          -log  drying rate for hourly computation, log  to  base 10 
    # kw          -log  wetting rate  for  hourly computation, log  to  base  10 
    
    relative_humidity = min(100.0, relative_humidity)
    mo = 147.2 * (101 - FFMCPrev)/(59.5 + FFMCPrev)

    if rain > .5:
        rainfall = rain - .5
        if mo <= 150.0:
            mr = mo + 42.5 * rainfall * math.exp(-100.0 / (251.0 - mo)) * (1.0-math.exp(-6.93 / rainfall))
        else:
            mr = mo + 42.5 * rainfall * math.exp(-100.0 / (251.0 - mo)) * (1.0-math.exp(-6.93 / rainfall)) + \
                0.0015 * pow(mo - 150.0, 2) * pow(rainfall, .5)

        if mr > 250.0:
            mr = 250.0
        mo=mr

    ed = 0.942 * pow(relative_humidity, 0.679) + 11.0 * math.exp((relative_humidity - 100.0) / 10.0) + 0.18 * \
        (21.1 - temp) * (1.0 - math.exp(-0.115 * relative_humidity))

    if mo > ed:
        ko = 0.424 * (1.0 - pow(relative_humidity / 100.0, 1.7)) + 0.0694 * pow(wind, .5) * \
            (1.0 - pow(relative_humidity / 100.0, 8))
        kd = ko * 0.581 * math.exp(0.0365 * temp)
        m = ed + (mo - ed) * pow(10.0,-kd)
    else:
        ew = 0.618 * pow(relative_humidity,0.753) + \
             10.0 * math.exp((relative_humidity - 100.0) / 10.0) + \
             0.18 * (21.1 - temp) * (1.0 - math.exp(-0.115 * relative_humidity))
        if mo < ew:
            k1 = 0.424 * (1.0 - pow((100.0 - relative_humidity) / 100.0, 1.7)) + \
                 0.0694 * pow(wind, .5) * (1.0 - pow((100.0 - relative_humidity) / 100.0, 8))
            kw = k1 * 0.581 * math.exp(0.0365 * temp)

            m = ew - (ew - mo) * pow(10.0, -kw) 
        else:
            m = mo
            
    return 59.5 * (250.0 - m) / (147.2 + m)

def DMC(temp, relative_humidity, rain, DMCPrev, month):
    # mo - duff moisture content from previous day
    # mr - duff moisture content after rain
    # m  - duff moisture content after drying
    # k  - log drying rate in DMC, log10 M/day
    # le - effective day length in DMC, hours
    # b  - slope variable in DMC rain effect
    # pr - DMC after rain
    # re - effective rainfall
    relative_humidity = min(100.0, relative_humidity)
    if rain > 1.5:
        re = 0.92 * rain - 1.27

        mo = 20.0 + math.exp(5.6348 - DMCPrev / 43.43)

        if DMCPrev <= 33.0:
            b = 100.0 / (0.5 + 0.3 * DMCPrev)
        else:
            if DMCPrev <= 65.0:
                b = 14.0 - 1.3 * math.log(DMCPrev)
            else:
                b = 6.2 * math.log(DMCPrev) - 17.2
        
        mr = mo + 1000.0 * re / (48.77 + b * re)

        pr = 244.72 - 43.43 * math.log(mr - 20.0)

        if pr > 0.0:
            DMCPrev = pr
        else:
            DMCPrev = 0.0
    if temp > -1.1:
        le = dayLength(month)

        k = 1.894 * (temp + 1.1) * (100.0 - relative_humidity) * float(le) * 0.000001

    else:
        k = 0.0

    return DMCPrev + 100.0 * k

def DC(temp, rain, DCPrev, month):
    #q      - moisture equivalent of DC, units of 0.254mm
    #qo     - moisture equivalent of previous day's DC
    #qr     - moisture equivalent after rain
    #v      - potential evapotranspiration, units of 0.254mm
    #lf     - day length adjustment in DC
    #dr     - DC after rain
    #rd     - effective rainfall DC
    if rain > 2.8:
        rd = 0.83 * rain - 1.27
        qo = 800.0 * math.exp(-DCPrev / 400.0)
        qr = qo + 3.937 * rd
        dr = 400.0 * math.log(800.0 / qr)

        if dr > 0.0:
            DCPrev = dr
        else:
            DCPrev = 0.0
    
    lf = dryingFactor(month)
    
    if temp > -2.8:
        v = 0.36 * (temp+2.8) + lf
    else:
        v = lf
    
    if v < 0.0:
        v = 0.0
    
    return DCPrev + 0.5 * v

def ISI(wind, FFMC):
    #fw - wind function
    #ff - fine fuel moisture function
    #m  - fine fuel moisture content 
    fw = math.exp(0.05039 * wind)

    m = 147.2 * (101.0 - FFMC) / (59.5 + FFMC)

    ff = 91.9 * math.exp(-0.1386 * m) * (1.0 + pow(m, 5.31) / 49300000.0)

    return 0.208 * fw * ff

def BUI(DMC, DC):
    #u - build up index
    if DMC <= 0.4 * DC:
        u = 0.8 * DMC * DC / (DMC + 0.4 * DC)
    else:
        u = DMC - (1.0 - 0.8 * DC / (DMC + 0.4 * DC)) * \
            (0.92 + pow(0.0114 * DMC, 1.7))

    return max(u,0.0)

def FWI(ISI,BUI):
    #fd - duff moisture function
    #b - FWI intermediate form
    #s - FWI final form
    if BUI <= 80.0:
        fd = 0.626 * pow(BUI, 0.809) + 2.0
    else:
        fd = 1000.0 / (25.0 + 108.64 * math.exp(-0.023 * BUI))

    b = 0.1 * ISI * fd

    if b > 1.0:
        s = math.exp(2.72 * pow(0.434 * math.log(b), 0.647))
    else:
        s = b

    return s

def DSR(FWI):
    return 0.0272 * pow(FWI, 1.77)

def dryingFactor(month):

    LfN = [-1.6, -1.6, -1.6, 0.9, 3.8, 5.8, 6.4, 5.0, 2.4, 0.4, -1.6, -1.6]
    
    return LfN[(month-1)%12]

def dayLength(month):
    DayLength46N = [ 6.5,  7.5,  9.0, 12.8, 13.9, 13.9, 12.4, 10.9,  9.4,  8.0,  7.0,  6.0]
  
    return DayLength46N[(month-1)%12]
