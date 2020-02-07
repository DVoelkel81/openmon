import uuid
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone



# Create your models here.

class subcustomer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #Unique DB ID
    customerid = models.CharField(max_length=25, default='None', editable=True, verbose_name="Customer ID") # ID of Customer
    customername = models.CharField(max_length=50, default='None', editable=True, verbose_name="Customer Name") # ID of Customer
    insertby = models.CharField(max_length=50, default='None', editable=True, verbose_name="insert by") # ID of Customer
    inserttime = models.DateTimeField('Inserttime') #Date of Inserting CHP # ID of Customer
    
    class Meta:
        """
        Set the name of table to identify in admin console.
        """        
        verbose_name = u'1 - Customer'
        verbose_name_plural = u'1 - Customers'
        
    # Methods
    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of MyModelName.
        """
        return reverse('model-detail-view', args=[str(self.customerid)])

    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return self.customername     

class devices(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #Unique DB ID
    deviceid = models.CharField(max_length=25, verbose_name="Device ID", unique=True) # ID of Customer
    devicename =models.CharField(max_length=25, verbose_name="Device Name") # ID of Customer
    device_type = models.ForeignKey('devicestype', on_delete=models.CASCADE,)
    devicedescription = models.TextField(verbose_name="Description") #General Informaition for Users
    customerid = models.CharField(max_length=25, verbose_name="Customer ID") # ID of Customer    
    insertby = models.CharField(max_length=50, default='None', editable=True, verbose_name="insert by") # ID of Customer
    inserttime = models.DateTimeField('Inserttime') #Date of Inserting CHP # ID of Customer    
        
    class Meta:
        """
        Set the name of table to identify in admin console.
        """        
        verbose_name = u'2 - Devices'
        verbose_name_plural = u'2 - Devices'
            
    # Methods
    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of MyModelName.
        """
        return reverse('model-detail-view', args=[str(self.deviceid)])
    
    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return self.deviceid 

class devicestype(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #Unique DB ID
    devicetypeid = models.CharField(max_length=25, verbose_name="Device ID", unique=True) # ID of Customer
    devicetypename =models.CharField(max_length=25, verbose_name="Device Name") # ID of Customer
    devicetypedescription = models.TextField(verbose_name="Description") #General Informaition for Users
    insertby = models.CharField(max_length=50, default='None', editable=True, verbose_name="insert by") # ID of Customer
    inserttime = models.DateTimeField('Inserttime') #Date of Inserting CHP # ID of Customer    
            
    class Meta:
        """
        Set the name of table to identify in admin console.
        """        
        verbose_name = u'3 - Devicetype'
        verbose_name_plural = u'3 - Devicetype'
                
    # Methods
    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of MyModelName.
        """
        return reverse('model-detail-view', args=[str(self.devicetypeid)])
        
    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return self.devicetypeid
    

class errorlog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #Unique DB ID
    deviceid = models.ForeignKey('devices', on_delete=models.CASCADE,)
    alarmtime = models.DateTimeField('Insert') #Date of the last Dataupdate
    alarm1 = models.CharField(max_length=25, default=' ', editable=True, verbose_name="Alarm Pos1") #Alarm1
    alarm2 = models.CharField(max_length=25, default=' ', editable=True, verbose_name="Alarm Pos2") #Alarm2
    alarm3 = models.CharField(max_length=25, default=' ', editable=True, verbose_name="Alarm Pos3") #Alarm3
    alarm4 = models.CharField(max_length=25, default=' ', editable=True, verbose_name="Alarm Pos4") #Alarm4
    alarm5 = models.CharField(max_length=25, default=' ', editable=True, verbose_name="Alarm Pos5") #Alarm5
    alarmInfo = models.TextField(default='',verbose_name="Info") #General Informaition for Users
    
        
    # Label fuer Tabellenname
    class Meta:
        verbose_name = u'4 - Alarmmessage'
        verbose_name_plural = u'4 - Alarmmessage'
        #verbose_name_plural = u'Erzeugte Leistung'
    
    # Methods
    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of MyModelName.
        """
        return reverse('model-detail-view', args=[str(self.id)])
            
    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return str(self.deviceid)    

#heating, cooling, Air condition, santaery
class hcasdata(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #Unique DB ID
    deviceid = models.ForeignKey('devices', on_delete=models.CASCADE,)
    evaporationtemp = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="evaporation temperatur") #Verdampfungstemperatur
    condensationtemp = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="condensation temperatur") #Verflüssigungstemperatur
    compressortemp = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="compressor temperatur") #compressortemperatur
    hotgastemp = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="hotgas temperatur") #heissgastemperatur
    fluidtemp =  models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="fluid temperatur") #Medium temperatur
    roomtempdevice = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="room temperatur") #room temperatur Anlage
    devicevoltage = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="device voltage") #Spannung Anlag
    compressorcurrent = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="compressor current") #stromaufnahme anlage
    devicepower = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="device power") #device power
    deviceconsumption = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="device consumption") #Verbrauch anlage
    serverroomtemp = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="temperatur serverroom") #Temperatur Serverraum
    serverroomhumidity = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="humidity serverroom") #Luftfeuchtigkeit Serverraum
    runhours = models.IntegerField(default=0, verbose_name="Runhours") # Betreibsstundenzaehler
    inserttime = models.DateTimeField('Inserttime') #Date of Inserting CHP # ID of Customer    
                
    class Meta:
        """
        Set the name of table to identify in admin console.
        """        
        verbose_name = u'5 - Hcasdata'
        verbose_name_plural = u'5 - Hcasdata'
                    
    # Methods
    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of MyModelName.
        """
        return reverse('model-detail-view', args=[str(self.deviceid)])
            
    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return self.deviceid
        
#CHP controller
class chpdata(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #Unique DB ID
    deviceid = models.ForeignKey('devices', on_delete=models.CASCADE,)
    hcltemp = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="hct temperatur") #Heizkreis Vorlauf Temperatur
    hcctemp = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="hcc temperatur") ##Heizkreis Nachlauf Temperatur
    boilertoptemp = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="boiler temp top") #Kessel Temperatur oben
    boilermidtemp = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="boiler temp mid") #Kessel Temperatur mitte
    boilerbuttemp = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="boiler temp but") #Kessel Temperatur buttom
    coolingtemp = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="cooling temp") #Kühlwasser Temperatur
    motorintemp = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="motor in temp") #Motoreintritt Temperatur
    motorouttemp = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="motor out temp") #Motoraustritt Temperatur
    wastgastemppri = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="wastgas pri temp") #Abgastemperatur Temperatur
    wastgastempsec = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="wastgas sec temp") #Abgastemperatur Temperatur
    oiltemp = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="oil temp") #Oil Temperatur
    oilpressure = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="Oil pressure") #Oil pressure
    exhaustgastemp = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="exhaustgas temp") #AWT Temperatur
    voltagel1 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="voltage L1") #Voltage Phase 1
    voltagel2 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="voltage L2") #Voltage Phase 2
    voltagel3 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="voltage l3") #Voltage Phase 3
    voltage12 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="voltage 1-2") #Voltage Phase 12
    voltage23 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="voltage 2-3") #Voltage Phase 23
    voltage31 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="voltage 3-1") #Voltage Phase 31
    currentl1 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="current L1") #Current Phase L1
    currentl2 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="current L2") #Current Phase L2
    currentl3 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="current L3") #Current Phase L3
    startcounter = models.IntegerField(default=0, verbose_name="startcounter") # Startzähler
    unsuccesstartcounter = models.IntegerField(default=0, verbose_name="unsuccessful starts") # fehlerhafte starts
    runhours = models.IntegerField(default=0, verbose_name="Runhours") # Betreibsstundenzaehler
    khwcount = models.IntegerField(default=0, verbose_name="kwhhours") # Betreibsstundenzaehler
    kvarcount = models.IntegerField(default=0, verbose_name="kvarhours") # Betreibsstundenzaehler
    stateerror = models.PositiveSmallIntegerField(default=0, verbose_name="state error") # Status chp has an error
    statewarning = models.PositiveSmallIntegerField(default=0, verbose_name="state warning") # Status chp has a warning
    staterunning = models.PositiveSmallIntegerField(default=0, verbose_name="state running") # Status chp is running
    statestop = models.PositiveSmallIntegerField(default=0, verbose_name="state stop") # Status CHP is Stoped
    modeauto = models.PositiveSmallIntegerField(default=0, verbose_name="mode auto") # Status CHP in Automatic mode
    modeman = models.PositiveSmallIntegerField(default=0, verbose_name="mode manual") # Status CHP in Manual Mode
    modestop = models.PositiveSmallIntegerField(default=0, verbose_name="mode stop") # Status CHP in Stop Mode
    gcbstate = models.PositiveSmallIntegerField(default=0, verbose_name="gcb state") # Status generator circuit breaker
    mcbstate = models.PositiveSmallIntegerField(default=0, verbose_name="mcb state") # Status mains circuit breaker
    modepowerderate = models.PositiveSmallIntegerField(default=0, verbose_name="power derate") # Status powerderate by supplyer
    inserttime = models.DateTimeField('Inserttime') #Date of Inserting CHP # ID of Customer    
                
    class Meta:
        """
        Set the name of table to identify in admin console.
        """        
        verbose_name = u'6 - CHPdata'
        verbose_name_plural = u'6 - CHPdata'
                    
    # Methods
    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of MyModelName.
        """
        return reverse('model-detail-view', args=[str(self.id)])
            
    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return str(self.deviceid)
        
#Emergency genset controller
class egcdata(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #Unique DB ID
    deviceid = models.ForeignKey('devices', on_delete=models.CASCADE,)
    coolingtemp = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="cooling temp") #Kühlwasser Temperatur
    oiltemp = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="cooling temp") #Oil Temperatur
    oilpressure = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="cooling temp") #Oil Temperatur
    voltagel1 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="voltage L1") #Voltage Phase 1
    voltagel2 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="voltage L2") #Voltage Phase 2
    voltagel3 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="voltage l3") #Voltage Phase 3
    voltage12 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="voltage 1-2") #Voltage Phase 12
    voltage23 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="voltage 2-3") #Voltage Phase 23
    voltage31 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="voltage 3-1") #Voltage Phase 31
    currentl1 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="current L1") #Current Phase L1
    currentl2 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="current L2") #Current Phase L2
    currentl3 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="current L3") #Current Phase L3
    startcounter = models.IntegerField(default=0, verbose_name="startcounter") # Startzähler
    unsuccesstartcounter = models.IntegerField(default=0, verbose_name="unsuccessful starts") # fehlerhafte starts
    runhours = models.IntegerField(default=0, verbose_name="Runhours") # Betreibsstundenzaehler
    khwcount = models.IntegerField(default=0, verbose_name="kwhhours") # Betreibsstundenzaehler
    kvarcount = models.IntegerField(default=0, verbose_name="kvarhours") # Betreibsstundenzaehler
    stateerror = models.PositiveSmallIntegerField(default=0, verbose_name="state error") # Status chp has an error
    statewarning = models.PositiveSmallIntegerField(default=0, verbose_name="state warning") # Status chp has a warning
    staterunning = models.PositiveSmallIntegerField(default=0, verbose_name="state running") # Status chp is running
    statestop = models.PositiveSmallIntegerField(default=0, verbose_name="state stop") # Status CHP is Stoped
    modeauto = models.PositiveSmallIntegerField(default=0, verbose_name="mode auto") # Status CHP in Automatic mode
    modeman = models.PositiveSmallIntegerField(default=0, verbose_name="mode manual") # Status CHP in Manual Mode
    modestop = models.PositiveSmallIntegerField(default=0, verbose_name="mode stop") # Status CHP in Stop Mode
    modetest = models.PositiveSmallIntegerField(default=0, verbose_name="test mode") # Status mains circuit breaker
    gcbstate = models.PositiveSmallIntegerField(default=0, verbose_name="gcb state") # Status generator circuit breaker
    mcbstate = models.PositiveSmallIntegerField(default=0, verbose_name="mcb state") # Status mains circuit breaker
    operstate = models.PositiveSmallIntegerField(default=0, verbose_name="Operation state") # 1 = standby 2 = island 3 = parallel 4 = testmode
    mainsfail = models.PositiveSmallIntegerField(default=0, verbose_name="mainsfailstate") # mainsfail
    inserttime = models.DateTimeField('Inserttime') #Date of Inserting CHP # ID of Customer    
                
    class Meta:
        """
        Set the name of table to identify in admin console.
        """        
        verbose_name = u'7 - Emergency genset data'
        verbose_name_plural = u'7 - Emergency genset data'
                    
    # Methods
    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of MyModelName.
        """
        return reverse('model-detail-view', args=[str(self.deviceid)])
            
    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return self.deviceid
        
#Mediumvoltage protection device
class mvpdata(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #Unique DB ID
    deviceid = models.ForeignKey('devices', on_delete=models.CASCADE,)
    voltagel1 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="voltage L1") #Voltage Phase 1
    voltagel2 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="voltage L2") #Voltage Phase 2
    voltagel3 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="voltage l3") #Voltage Phase 3
    voltage12 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="voltage 1-2") #Voltage Phase 12
    voltage23 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="voltage 2-3") #Voltage Phase 23
    voltage31 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="voltage 3-1") #Voltage Phase 31
    currentl1 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="current L1") #Current Phase L1
    currentl2 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="current L2") #Current Phase L2
    currentl3 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="current L3") #Current Phase L3
    cbclosecounter = models.IntegerField(default=0, verbose_name="cb close counter") # Startzähler
    runhours = models.IntegerField(default=0, verbose_name="Runhours") # Betreibsstundenzaehler
    khwcount = models.IntegerField(default=0, verbose_name="kwhhours") # Betreibsstundenzaehler
    kvarcount = models.IntegerField(default=0, verbose_name="kvarhours") # Betreibsstundenzaehler
    stateerror = models.PositiveSmallIntegerField(default=0, verbose_name="state error") # Status chp has an error
    statewarning = models.PositiveSmallIntegerField(default=0, verbose_name="state warning") # Status chp has a warning
    modeauto = models.PositiveSmallIntegerField(default=0, verbose_name="mode auto") # Status CHP in Automatic mode
    modeman = models.PositiveSmallIntegerField(default=0, verbose_name="mode manual") # Status CHP in Manual Mode
    modestop = models.PositiveSmallIntegerField(default=0, verbose_name="mode stop") # Status CHP in Stop Mode
    modetest = models.PositiveSmallIntegerField(default=0, verbose_name="test mode") # Status mains circuit breaker
    cb1state = models.PositiveSmallIntegerField(default=0, verbose_name="gcb state") # Status generator circuit breaker
    cb2state = models.PositiveSmallIntegerField(default=0, verbose_name="mcb state") # Status mains circuit breaker
    cb3state = models.PositiveSmallIntegerField(default=0, verbose_name="mcb state") # Status mains circuit breaker
    cb4state = models.PositiveSmallIntegerField(default=0, verbose_name="mcb state") # Status mains circuit breaker
    inserttime = models.DateTimeField('Inserttime') #Date of Inserting CHP # ID of Customer    
                
    class Meta:
        """
        Set the name of table to identify in admin console.
        """        
        verbose_name = u'8 - mvpdata'
        verbose_name_plural = u'8 - mvpdata'
                    
    # Methods
    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of MyModelName.
        """
        return reverse('model-detail-view', args=[str(self.deviceid)])
            
    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return self.deviceid
        
#controlling chp device
class controlchp(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #Unique DB ID
    deviceid = models.ForeignKey('devices', on_delete=models.CASCADE,)
    ipaddr = models.CharField(max_length=25, default=' ', editable=True, verbose_name="IP-address") #IP Adress
    activpowerreq = models.IntegerField(default=0, verbose_name="requested power") # Status mains circuit breaker
    reactivpowerreq = models.IntegerField(default=0, verbose_name="requested reactive power") # Status mains circuit breaker
    tempreq = models.PositiveSmallIntegerField(default=0, verbose_name="requested temperatur request") # Status mains circuit breaker
    resetcmd = models.PositiveSmallIntegerField(default=0, verbose_name="reset cmd") # Status mains circuit breaker
    requestinfo = models.TextField(verbose_name="Info") #General Informaition for Users
    inserttime = models.DateTimeField('Inserttime') #Date of Inserting CHP # ID of Customer    
                
    class Meta:
        """
        Set the name of table to identify in admin console.
        """        
        verbose_name = u'9 - controlchp'
        verbose_name_plural = u'9 - controlchp'
                    
    # Methods
    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of MyModelName.
        """
        return reverse('model-detail-view', args=[str(self.deviceid)])
            
    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return self.deviceid
     
#controlling hvac device
class controlhvas(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #Unique DB ID
    deviceid = models.ForeignKey('devices', on_delete=models.CASCADE,)
    ipaddr = models.CharField(max_length=25, default=' ', editable=True, verbose_name="IP-address") #IP Adress
    resetcmd = models.PositiveSmallIntegerField(default=0, verbose_name="reset command") # reset command
    operationmodecmd = models.PositiveSmallIntegerField(default=0, verbose_name="operation Mode") # change mode command cooling, heating, breath
    devicemodecmd = models.PositiveSmallIntegerField(default=0, verbose_name="device Mode") # auto manual stop
    requestinfo = models.TextField(verbose_name="Info") #General Informaition for Users
    inserttime = models.DateTimeField('Inserttime') #Date of Inserting CHP # ID of Customer    
                
    class Meta:
        """
        Set the name of table to identify in admin console.
        """        
        verbose_name = u'10 - controlhvas'
        verbose_name_plural = u'10 - controlhvas'
                    
    # Methods
    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of MyModelName.
        """
        return reverse('model-detail-view', args=[str(self.deviceid)])
            
    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return self.deviceid
          
#controlling egc device
class controlegc(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #Unique DB ID
    deviceid = models.ForeignKey('devices', on_delete=models.CASCADE,)
    ipaddr = models.CharField(max_length=25, default=' ', editable=True, verbose_name="IP-address") #IP Adress
    resetcmd = models.PositiveSmallIntegerField(default=0, verbose_name="reset command") # reset command
    operationmodecmd = models.PositiveSmallIntegerField(default=0, verbose_name="operation Mode") # change start/stop/standby
    devicemodecmd = models.PositiveSmallIntegerField(default=0, verbose_name="device Mode") # auto manual stop
    requestinfo = models.TextField(verbose_name="Info") #General Informaition for Users
    inserttime = models.DateTimeField('Inserttime') #Date of Inserting CHP # ID of Customer    
                    
    class Meta:
        """
        Set the name of table to identify in admin console.
        """        
        verbose_name = u'11 - controlegc'
        verbose_name_plural = u'11 - controlegc'
                        
    # Methods
    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of MyModelName.
        """
        return reverse('model-detail-view', args=[str(self.deviceid)])
                
    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return self.deviceid

#controlling mvp device
class controlmvp(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #Unique DB ID
    deviceid = models.ForeignKey('devices', on_delete=models.CASCADE,)
    ipaddr = models.CharField(max_length=25, default=' ', editable=True, verbose_name="IP-address") #IP Adress
    resetcmd = models.PositiveSmallIntegerField(default=0, verbose_name="reset command") # reset command
    CB1cmd = models.PositiveSmallIntegerField(default=0, verbose_name="CB1 Open/close") # change start/stop/standby
    CB2cmd = models.PositiveSmallIntegerField(default=0, verbose_name="CB2 Open/close") # auto manual stop
    CB3cmd = models.PositiveSmallIntegerField(default=0, verbose_name="CB3 Open/close") # auto manual stop
    CB4cmd = models.PositiveSmallIntegerField(default=0, verbose_name="CB4 Open/close") # auto manual stop
    requestinfo = models.TextField(verbose_name="Info") #General Informaition for Users
    inserttime = models.DateTimeField('Inserttime') #Date of Inserting CHP # ID of Customer    
                        
    class Meta:
        """
        Set the name of table to identify in admin console.
        """        
        verbose_name = u'12 - controlmvp'
        verbose_name_plural = u'12 - controlmvp'
                            
    # Methods
    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of MyModelName.
        """
        return reverse('model-detail-view', args=[str(self.deviceid)])
                    
    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return self.deviceid

#systemalarms
class systemalarms(models.Model):
    bstate = [(1,"test1"),(2,"test2")]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #Unique DB ID
    deviceid = models.ForeignKey('devices', on_delete=models.CASCADE,)
    measurevalue = models.CharField(max_length=25, default=' ', editable=True, verbose_name="Requested temp or state") #IP Adress
    boardercondition = models.PositiveSmallIntegerField(choices=bstate,default=1, verbose_name="requested boarder",help_text="Please choose border value higer or lower") # auto manual stop
    boardervalue = models.IntegerField(default=0, verbose_name="Boarder Value",help_text="Please insert boarder value") # auto manual stop
    boarderinfo = models.TextField(verbose_name="Info") #General Informaition for Users
    inserttime = models.DateTimeField('Inserttime') #Date of Inserting CHP # ID of Customer    
                            
    class Meta:
        """
        Set the name of table to identify in admin console.
        """        
        verbose_name = u'13 - systemalarms'
        verbose_name_plural = u'13 - systemalarms'
                                
    # Methods
    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of MyModelName.
        """
        return reverse('model-detail-view', args=[str(self.deviceid)])
                        
    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return self.deviceid