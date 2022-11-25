from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField,SubmitField)
from wtforms.validators import InputRequired, Length

class Provisioning(FlaskForm):
    deviceManufacturer = StringField('Manufacturer', validators=[InputRequired(),Length(min=1,max=30)]),
    deviceModel = StringField('Model', validators=[InputRequired(),Length(min=1,max=20)]),
    assetTag = StringField('Asset Tag', validators=[InputRequired(),Length(min=1,max=10)]),
    windowsUpdates = BooleanField('Windows Updates', validators=[InputRequired()]),
    Bitlocker = BooleanField('Bitlocker 100% enrypted', validators=[InputRequired()]),
    InstalluserSoftware = BooleanField('Install User Software', validators=[InputRequired()]),
    ADGroups = BooleanField('AD groups replicated', validators=[InputRequired()]),
    StandardDesktopIcons = BooleanField('Standard icons are showing on desktop', validators=[InputRequired()]),
    VPNInstalled = BooleanField('VPN Installed', validators=[InputRequired()]),
    HardwareWorking = BooleanField('Hardware in working order', validators=[InputRequired()]),
    ProvisioningSignOff = StringField('Provisioning User', validators=[InputRequired(),Length(min=1,max=20)]),
    submit = SubmitField('Submit')
    

    
class DesktopSupport(FlaskForm):
    contactedUser = BooleanField('Contacted User'),
    collectOldDevice = BooleanField('Collect Old Device'),
    Changebitlocker = BooleanField('Change bitlocker pin'),
    checkIP = BooleanField('Check for existing IP reservation and update if required'),
    collectOldDevice = BooleanField('Collect Old Device'),
    desktopSignOff = StringField('Desktop Staff Member', validators=[InputRequired(),Length(min=1,max=10)])
    submit = SubmitField('Submit')


class User(FlaskForm):
    UserSignOff = BooleanField('I declare that on receiving this device, I am responsible for the SBU IT asset. Any changes in ownership within my department must first be authorised with my line manager. Once agreed, I will log a call on the IT Service Desk for this to be authorised and actioned by the SBU IT team. If this device is no longer required, I will log a call on the IT Service Desk for it to be returned to IT. If I am leaving SBUHB or leaving my current role I will log a call on the IT Service Desk, stating my final day of work in the HB/Department and my current line manager. Any damages incurred are the responsibility of the department. A departmental cost code will be required in the event of accidental damage and a call will be logged with SBU IT, immediately. ',validators=[InputRequired()]),
    submit = SubmitField('Submit')