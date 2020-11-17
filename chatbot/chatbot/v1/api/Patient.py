class Patient:
    def __init__(self, name):
        self.name = name
        self.hiDone = False
        self.getAllDentists = False
        self.dentistName = None
        self.time = None
        self.confirmation = False

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

    def confirm_appointment(self):
        self.confirmation = True

    def decline_appointment(self):
        self.confirmation = False



