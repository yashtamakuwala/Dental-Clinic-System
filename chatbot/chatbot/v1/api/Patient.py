class Patient:
    def __init__(self):
        self.name = None
        self.hiDone = False
        self.getAllDentists = False
        self.dentistName = None
        self.time = None
        self.confirmation = False
        self.wantingToCancel = False
        self.bookingId = None
        self.cancelDentist = None
        self.cancelTime = None
        self.cancelDone = False

    def set_patient_name(self, ptName: str):
        self.name = ptName

    def shown_dentists(self):
        self.getAllDentists = True
        self.confirmation = False
        self.time = None
        self.dentistName = None
        self.confirmation = False

    def got_dentist_name(self, dentistName):
        self.getAllDentists = True
        self.dentistName = dentistName
        self.time = None
        self.confirmation = False

    def asked_appointment_time(self, hh):
        self.getAllDentists = True
        self.time = hh
        self.confirmation = False

    def confirm_appointment(self, bookingId):
        self.confirmation = True
        self.bookingId = bookingId
        self.getAllDentists = False
        self.dentistName = None
        self.time = None
        self.wantingToCancel = False
        self.cancelDentist = None
        self.cancelTime = None
        self.cancelDone = False

    def decline_appointment(self):
        self.confirmation = False



