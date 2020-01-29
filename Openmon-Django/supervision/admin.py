from django.contrib import admin
from .models import subcustomer
from .models import devices
from .models import devicestype
from .models import errorlog
from .models import hcasdata, controlhvas
from .models import chpdata, controlchp
from .models import egcdata, controlegc
from .models import mvpdata, controlmvp
from .models import systemalarms


# Register your models here.
class subcustomeradmin(admin.ModelAdmin):
    fieldsets = [
        ('Customer Data', {'fields':['customerid','customername']}),
        ('Date information',{'fields':['insertby','inserttime']}),
    ]

class devicesadmin(admin.ModelAdmin):
    fieldsets = [
        ('Device Data', {'fields':['customerid','deviceid','devicename','device_type','devicedescription']}),
        ('Date information',{'fields':['insertby','inserttime']}),
    ]

class devicestypeadmin(admin.ModelAdmin):
    fieldsets = [
        ('Device Data', {'fields':['devicetypeid','devicetypename','devicetypedescription']}),
        ('Date information',{'fields':['insertby','inserttime']}),
    ]
    
class errorlogadmin(admin.ModelAdmin):
    fieldsets = [
        ('Device Data', {'fields':['deviceid','alarm1','alarm2','alarm3','alarm4','alarm5','alarmInfo']}),
        ('Date information',{'fields':['alarmtime']}),
    ]

class hcasdataadmin(admin.ModelAdmin):
    fieldsets = [
        ('Device Data', {'fields':['deviceid','runhours']}),
        ('Temperatur Information', {'fields':['evaporationtemp','condensationtemp','compressortemp','hotgastemp','fluidtemp','roomtempdevice','serverroomtemp']}),
        ('Energy Information',{'fields':['devicevoltage','compressorcurrent','devicepower','deviceconsumption']}),
        ('Date information',{'fields':['inserttime']}),
    ]

class chpdataadmin(admin.ModelAdmin):
    fieldsets = [
        ('Device data', {'fields':['deviceid','runhours','startcounter','unsuccesstartcounter','oilpressure']}),
        ('Mode information',{'fields':['modepowerderate','modeauto','modeman','modestop']}),
        ('Temperatur information', {'fields':['hcltemp','hcctemp','boilertoptemp','boilermidtemp','boilerbuttemp','coolingtemp','motorintemp','motorouttemp','wastgastemppri','wastgastempsec','oiltemp','exhaustgastemp']}),
        ('Energy information',{'fields':['voltagel1','voltagel2','voltagel3','voltage12','voltage23','voltage31','currentl1','currentl2','currentl3','khwcount','kvarcount']}),
        ('State information',{'fields':['stateerror','statewarning','staterunning','statestop','gcbstate','mcbstate']}),
        ('Date information',{'fields':['inserttime']}),
    ]

class egcdataadmin(admin.ModelAdmin):
    fieldsets = [
        ('Device data', {'fields':['deviceid','runhours','startcounter','unsuccesstartcounter','coolingtemp','oilpressure','oiltemp']}),
        ('Mode information',{'fields':['modeauto','modeman','modestop']}),
        ('Energy information',{'fields':['voltagel1','voltagel2','voltagel3','voltage12','voltage23','voltage31','currentl1','currentl2','currentl3','khwcount','kvarcount']}),
        ('State information',{'fields':['operstate','mainsfail','gcbstate','mcbstate','stateerror','statewarning','staterunning','statestop']}),
        ('Date information',{'fields':['inserttime']}),
    ]
    
class mvpdataadmin(admin.ModelAdmin):
    fieldsets = [
        ('Device data', {'fields':['deviceid','runhours','cbclosecounter']}),
        ('Mode information',{'fields':['modeauto','modeman','modestop','modetest']}),
        ('Energy information',{'fields':['voltagel1','voltagel2','voltagel3','voltage12','voltage23','voltage31','currentl1','currentl2','currentl3','khwcount','kvarcount']}),
        ('State information',{'fields':['stateerror','statewarning','cb1state','cb2state','cb3state','cb4state']}),
        ('Date information',{'fields':['inserttime']}),
    ]

class controlchpadmin(admin.ModelAdmin):
    fieldsets = [
        ('Device data', {'fields':['deviceid','ipaddr','requestinfo']}),
        ('Requests',{'fields':['activpowerreq','reactivpowerreq','tempreq','resetcmd']}),
        ('Date information',{'fields':['inserttime']}),
    ]

class controlhvasadmin(admin.ModelAdmin):
    fieldsets = [
        ('Device data', {'fields':['deviceid','ipaddr','requestinfo']}),
        ('Commands',{'fields':['resetcmd','operationmodecmd','devicemodecmd']}),
        ('Date information',{'fields':['inserttime']}),
    ]

class controlegcadmin(admin.ModelAdmin):
    fieldsets = [
        ('Device data', {'fields':['deviceid','ipaddr','requestinfo']}),
        ('Commands',{'fields':['resetcmd','operationmodecmd','devicemodecmd']}),
        ('Date information',{'fields':['inserttime']}),
    ]

class controlmvpadmin(admin.ModelAdmin):
    fieldsets = [
        ('Device data', {'fields':['deviceid','ipaddr','requestinfo']}),
        ('Commands',{'fields':['resetcmd','CB1cmd','CB2cmd','CB3cmd','CB4cmd']}),
        ('Date information',{'fields':['inserttime']}),
    ]

class csystemalarmadmin(admin.ModelAdmin):
    fieldsets = [
        ('Alarm data', {'fields':['deviceid','boarderinfo']}),
        ('Commands',{'fields':['measurevalue','boardercondition','boardervalue']}),
        ('Date information',{'fields':['inserttime']}),
    ]

admin.site.register(subcustomer, subcustomeradmin)
admin.site.register(devices, devicesadmin)
admin.site.register(devicestype, devicestypeadmin)
admin.site.register(errorlog, errorlogadmin)
admin.site.register(hcasdata, hcasdataadmin)
admin.site.register(chpdata, chpdataadmin)
admin.site.register(egcdata, egcdataadmin)
admin.site.register(mvpdata, mvpdataadmin)
admin.site.register(controlchp, controlchpadmin)
admin.site.register(controlhvas, controlhvasadmin)
admin.site.register(controlegc, controlegcadmin)
admin.site.register(controlmvp, controlmvpadmin)
admin.site.register(systemalarms, csystemalarmadmin)