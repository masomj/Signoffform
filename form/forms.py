from flask_wtf import Form
from wtforms import StringField, RadioField,SubmitField
from wtforms.validators import InputRequired, Length

class Provisioning(Form):
    deviceManufacturer = StringField('Manufacturer', validators=[InputRequired(),Length(min=1,max=30)]),
    deviceModel = StringField('Model', validators=[InputRequired(),Length(min=1,max=20)]),
    assetTag = StringField('Asset Tag', validators=[InputRequired(),Length(min=1,max=10)]),
    windowsUpdates = RadioField('Windows Updates',choices=['Yes','No']),
    Bitlocker = RadioField('Bitlocker 100% enrypted',choices=['Yes','No']),
    InstalluserSoftware = RadioField('Install User Software',choices=['Yes','No']),
    ADGroups = RadioField('AD groups replicated',choices=['Yes','No']),
    StandardDesktopIcons = RadioField('Standard icons are showing on desktop',choices=['Yes','No']),
    VPNInstalled = RadioField('VPN Installed',choices=['Yes','No']),
    HardwareWorking = RadioField('Hardware in working order' ,choices=['Yes','No']),
    ProvisioningSignOff = StringField('Provisioning User', validators=[InputRequired(),Length(min=1,max=20)]),
    submit = SubmitField('Submit')
    
class DesktopSupport(Form):
    contactedUser = RadioField('Contacted User',choices=['Yes','No']),
    collectOldDevice = RadioField('Collect Old Device',choices=['Yes','No']),
    Changebitlocker = RadioField('Change bitlocker pin',choices=['Yes','No']),
    checkIP = RadioField('Check for existing IP reservation and update if required',choices=['Yes','No']),
    collectOldDevice = RadioField('Collect Old Device',choices=['Yes','No']),
    desktopSignOff = StringField('Desktop Staff Member', validators=[InputRequired(),Length(min=1,max=10)])
    submit = SubmitField('Submit')



class User(Form):
    UserSignOff = RadioField('Sign', choices=['Yes','No']),
    submit = SubmitField('Submit')