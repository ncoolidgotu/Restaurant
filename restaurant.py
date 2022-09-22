# pwease don't s-s-steaw ouw code
### Nate Coolidge 					100749708
### Saief Shams Murad 				100836639
### Christina Cho 					100816275
### Jia Chen(Anthony Chen Chen)		100572516
try:
    import sys
    from sqlalchemy import create_engine, Column, String, DateTime, Integer #For Object Relational Mapping
    from sqlalchemy.orm import sessionmaker, exc as ormexc #For Object Relational Mapping
    from sqlalchemy.ext.declarative import declarative_base #For Object Relational Mapping
    from sqlalchemy import exc #import the exceptions for sqlalchemy
    from datetime import datetime #For datetime formatting
    from PyQt6 import QtWidgets #For Changing GUI Screens
    from PyQt6.QtCore import QDate, QDateTime
    from PyQt6.QtWidgets import QApplication, QMainWindow, QErrorMessage, QMessageBox #For GUI Functionality
    from PyQt6.uic import loadUi #For UI importing
    import pygame   #For background music
    databaseEngine = create_engine('sqlite:///restaurant.db', echo = False) #Load Restaurant SQL database into ORM engine
    RestaurantSession = sessionmaker(bind=databaseEngine) #Bind ORM to restaurant.db
    restaurantSession  = RestaurantSession()    # Hidden class for SQL operations
    restaurantDatabase = declarative_base()   # Construct a class for mapping objects to the SQL database (This class accesses SQL but supports methods in the derived class we will specify)

    # Error Handlers
    class Error(Exception):
        # The base exception class
        pass

    class EmailCheck(Error):
        # Rasies the error when the email condition is not met
        pass

    class StringCheck(Error):
        # Raises the error when the string value is not of type string
        pass

    class LengthCheck(Error):
        # Raises the error when the password length is less than 8 characters
        pass

    class EmptyInputErrorForPeople(Error):
        # Raises an error if the input value for the number of people is empty or not
        pass

    class EmptyInputErrorForRoom(Error):
        # Raises an error if the input value for the number of room is empty or not
        pass

    class DateInThePastError(Error):
        # Raises an error if the date value is in the past
        pass

    class ToBeforeFromDateError(Error):
        # Raises an error if the end date is before the starting date
        pass

    class NoAccountError(Error):
        # Raises an error if the account does not exist
        pass

    class DuplicateAccountError(Error):
        # Raises an error when a user to attempting to make duplicated accounts with the same email address
        pass

    class NoReservationError(Error):
        # Raises an error when the user is trying to view, modify or cancel reservations where there are no reservations
        pass

    class Account(restaurantDatabase): #Derived class from "restaurantDatabase" ORM class
        __tablename__ = 'accounts' #Bind the SQL Table (will create a table if there is not an existing table. Otherwise, it will map to existing table)
        email = Column(String(50), primary_key=True) #Bind the SQL Columns (will create a column if there is not an existing column. Otherwise, it will map to existing column)
        first_name = Column(String(50))              #Make email a primary key for the accounts database
        last_name = Column(String(50))
        password = Column(String(50))
        date_of_birth = Column(String(50))

        def __init__(self, email, first_name, last_name, password, date_of_birth): #Initialize attributes for account
            self.email = email
            self.first_name = first_name
            self.last_name = last_name
            self.password = password # Wanted to make this private but sql had issues with it
            self.date_of_birth = date_of_birth

        # getter methods for all the attributes
        def get_email(self):
            return self.email

        def get_first_name(self):
            return self.first_name

        def get_last_name(self):
            return self.last_name

        def get_password(self):
            return self.password

        def get_date_of_birth(self):
            return self.date_of_birth

    class Reservation(restaurantDatabase): #Derived class from "restaurantDatabase" ORM class
        __tablename__ = 'reservation' #Bind the SQL Table (will create a table if there is not an existing table. Otherwise, it will map to existing table)
        reservationID = Column(Integer, primary_key=True, autoincrement = True) #Bind the SQL Columns (will create a column if there is not an existing column. Otherwise, it will map to existing column)
        email = Column(String(50))                        #Make reservationID a primary key for the reservation database
        numOfDays = Column(String(50))
        fromD = Column(String(50))
        toD = Column(String(50))
        numOfPer = Column(String(50))
        numOfRoom = Column(String(50))

        def __init__(self, email, fromD, toD, numOfDays, numOfPer, numOfRoom): #Initialize attributes for reservation
            self.email = email
            self.numOfDays = numOfDays
            self.fromD = fromD
            self.toD = toD
            self.numOfPer = numOfPer
            self.numOfRoom = numOfRoom

        # getter methods for all the attributes
        def get_email(self):
            return self.email

        def get_ID(self):
            return self.reservationID

        def get_numOfDays(self):
            return self.numOfDays

        def get_fromD(self):
            return self.fromD

        def get_toD(self):
            return self.toD

        def get_numOfPer(self):
            return self.numOfPer

        def get_numOfRoom(self):
            return self.numOfRoom

    class MainMenu(QMainWindow): #Derived class of QMainWindow to control functionality inside the windows
        def __init__(self):
            super(MainMenu,self).__init__()
            loadUi("MainMenu.ui",self)  # Loads the window from main menu .ui file
            self.RegisterSignup.clicked.connect(manager.goToRegisterMenu)   # When this button is clicked, it takes the user to the register menu
            self.Login.clicked.connect(manager.goToLoginMenu)               # When this button is clicked, it takes the user to the login menu
            self.Exit.clicked.connect(manager.closeProgram)                 # When this button is clicked, it allows the user to exist the program


    class LoginMenu(QMainWindow):
        def __init__(self):
            super(LoginMenu,self).__init__()
            loadUi("Login.ui", self)    # Loads the login window from .ui file
            self.CancelBt.clicked.connect(manager.goToMainMenu)             # When this button is clicked, it takes the user back to the main menu
            self.SubmitBt.clicked.connect(self.submitData)                  # When this button is clicked, it allows the user to submit the data entered

        # Function to submit the data from the input boxes
        def submitData(self):
            try:
                self.email = self.EmailField.text()
                if not self.email.find("@" and ".") != -1:   # Checks for an @ and a . in the email
                    raise EmailCheck                         # Initiates EmailCheck class to raise faulty email error
                else:
                    pass

            except EmailCheck:                               # Functionality of EmailCheck
                email_error_msg = QMessageBox()
                email_error_msg.setWindowTitle("Error!")
                email_error_msg.setText("The email entered is invalid. Please re-enter.")
                email_error_msg.exec()

            try:
                self.password = self.PassField.text()       # Verifies password integrity
                if not len(self.password) >= 8:
                    raise LengthCheck
                else:
                    validation = manager.login(self.email, self.password)
                    self.EmailField.clear()
                    self.PassField.clear()
                    if validation == True:                  # After checking login credentials, the program logs the user in
                        msg = QMessageBox()
                        msg.setText("Login Successful!")
                        msg.setWindowTitle("Rick Astley's Bar and Grill")
                        msg.exec()
                        manager.goToReservationMenu()       # loads the Reservation Menu
                    else:
                        raise NoAccountError                # if the account is not found this error is raised

            except LengthCheck:                             # checks the length of the password
                pass_error_msg = QMessageBox()
                pass_error_msg.setWindowTitle("Rick Astley's Bar and Grill")
                pass_error_msg.setText("The password entered is too short. Please re-enter.")
                pass_error_msg.exec()

            except NoAccountError:                          # Functionality of NoAccountError
                msg = QMessageBox()
                msg.setText("The credentials you provided are invalid! Please try again!")
                msg.setWindowTitle("Rick Astley's Bar and Grill")
                msg.exec()

    # class for the registration menu
    class RegisterMenu(QMainWindow):
        def __init__(self):
            super(RegisterMenu,self).__init__()
            loadUi("RegisterMenu.ui", self)                 # Loadin the Register Menu UI file
            self.CancelBt.clicked.connect(manager.goToMainMenu)      # When this button is clicked, it takes the user back to the main menu
            self.SubmitBt.clicked.connect(self.submitData)           # When this button is clicked, it allows the user to submit the data entered

        def submitData(self): #Save the reservation to the SQL Database
            try:
                self.password = self.PassField.text() #Read the on-screen fields
                self.fName = self.FNameField.text()
                self.lName = self.LNameField.text()
                self.email = self.EmailField.text()
                if not self.email.find("@" and ".") != -1: #Check for data integrity, faulty email address
                    raise EmailCheck
                elif self.email.find(" ") != -1:
                    raise EmailCheck                        # raised when incorrect email is entered
                elif not self.fName.isalpha() or not self.lName.isalpha():
                    raise StringCheck                       # raised when email id contains numbers
                elif not len(self.password)>=8:             # checks password character length
                    raise LengthCheck
                else:                                       # Data is submitted, and all of the fields are cleared
                    self.bDay = datetime.strptime(self.DoBField.text(), "%d/%m/%Y")
                    manager.createAccount(self.email, self.fName, self.lName, self.password, self.bDay)
                    self.EmailField.clear()
                    self.PassField.clear()
                    self.FNameField.clear()
                    self.LNameField.clear()

            except StringCheck:                             # functionality of StringCheck error exception
                self.FNameField.clear()
                self.LNameField.clear()
                fname_error_msg = QMessageBox()
                fname_error_msg.setWindowTitle("Rick Astley's Bar and Grill")
                fname_error_msg.setText("The name entered is invalid. Please re-enter.")
                fname_error_msg.exec()

            except LengthCheck:                             # functionality of LengthCheck error exception
                self.PassField.clear()
                pass_error_msg = QMessageBox()
                pass_error_msg.setWindowTitle("Error!")
                pass_error_msg.setText("The password entered is too short. Please re-enter.")
                pass_error_msg.exec()

            except EmailCheck:                              # functionality of EmailCheck error exception
                self.EmailField.clear()
                email_error_msg = QMessageBox()
                email_error_msg.setWindowTitle("Error!")
                email_error_msg.setText("The email entered is invalid. Please re-enter.")
                email_error_msg.exec()


    class ReservationMenu(QMainWindow): #GUI Window for Reservation Menu
        def __init__(self):
            super(ReservationMenu,self).__init__()
            loadUi("ReservationMenu.ui", self)              # Loads the reservation menu
            self.addReservation.clicked.connect(manager.goToReserveMenu)        # When this button is clicked, it takes the user to the reservation menu to add a reservation
            self.viewReservation.clicked.connect(manager.goToViewReservation)   # When this button is clicked, it allows the user to view the reservation made previously
            self.modifyReservation.clicked.connect(manager.goToModifyReservation)   # When this button is clicked, it takes the user to the menu that allows the user to modify the previouly made reservation
            self.cancelReservation.clicked.connect(manager.goToCancelReservation)   # When this button is clicked, it takes the user to the menu that allows the user to calcel the previously made reservations
            self.logout.clicked.connect(manager.goToMainMenu)                   # When this button is clicked, it logs the user out and lose access to the account

        def setUser(self): #Set username in header
            self.label_2.setText(f"Hello {manager.currentAccount.get_first_name()} {manager.currentAccount.get_last_name()}!")


    class ReserveMenu(QMainWindow): #GUI Menu to make a reservation
        def __init__(self):
            super(ReserveMenu,self).__init__()
            loadUi("Reserve.ui", self)                      # loads the reserve menu UI file
            self.SubmitBt.clicked.connect(self.submitData)                      # When this button is clicked, it allows the user to submit the data entered to make a reservation
            self.BackBt.clicked.connect(manager.goToReservationMenu)            # When this button is clicked, it takes the user back to the reservation menu
            self.currentDate = QDate.currentDate()          # date fields are defaulted to current date
            self.qdate = QDate(self.currentDate.year(), self.currentDate.month(), self.currentDate.day())
            self.FromDate.setDate(self.qdate)
            self.FromDate.show()
            self.ToDate.setDate(self.qdate)
            self.ToDate.show()
            self.NofP.setValue(1)                           # number of room and person set to 1 by default. bcz person/room cant be 0
            self.NofR.setValue(1)


        def submitData(self): #Submit the reservation to the database
            try:                                        # Read on-screen fields
                self.numOfP = self.NofP.text()
                self.numOfR = self.NofR.text()
                self.fromD = datetime.strptime(self.FromDate.text(), "%d/%m/%Y").date()
                self.toD = datetime.strptime(self.ToDate.text(), "%d/%m/%Y").date()
                # Check data integrity
                if not self.numOfP > '0':
                    raise EmptyInputErrorForPeople
                elif not self.numOfR > '0':
                    raise EmptyInputErrorForRoom
                elif self.fromD < self.currentDate:
                    raise DateInThePastError
                elif self.toD < self.fromD:
                    raise ToBeforeFromDateError
                else:                                    # Calculate "To Date" from the dates selected.
                    self.numOfDays = (self.toD - self.fromD).days
                    if self.numOfDays == 0:              # most restaurant count same day reservation as 1 day, so we implemented this into the code
                        self.numOfDays = 1

                    manager.createReservation(self.numOfDays, self.fromD, self.toD, self.numOfP, self.numOfR) #Add the reservation to the database
                    self.NofP.setValue(1)   # Set default value for no. of people/rooms to 1
                    self.NofR.setValue(1)
                    msg = QMessageBox()
                    msg.setText("Reservation Successful!")
                    msg.setWindowTitle("Rick Astley's Bar and Grill")
                    msg.exec()
                    manager.goToReservationMenu()       # after successfull reservation, goes back to previos menu

            except ToBeforeFromDateError:               # raised when date entered is wrong
                toD_error_msg = QMessageBox()
                toD_error_msg.setWindowTitle("Error!")
                toD_error_msg.setText("Please enter a valid END date.")
                toD_error_msg.exec()

            except DateInThePastError:                  # raised when date entered is in the past
                fromD_error_msg = QMessageBox()
                fromD_error_msg.setWindowTitle("Error!")
                fromD_error_msg.setText(f"Please enter a valid upcoming date.\nCurrent Date: {datetime.now().date()}")
                fromD_error_msg.exec()

            except EmptyInputErrorForRoom:              # raised when room number entered is wrong
                self.NofR.setValue(1)
                NofR_error_msg = QMessageBox()
                NofR_error_msg.setWindowTitle("Error!")
                NofR_error_msg.setText("Please enter the number of rooms expected.")
                NofR_error_msg.exec()

            except EmptyInputErrorForPeople:            # raised when people number entered is wrong
                self.NofP.setValue(1)
                NofP_error_msg = QMessageBox()
                NofP_error_msg.setWindowTitle("Error!")
                NofP_error_msg.setText("Please enter the number of people expected.")
                NofP_error_msg.exec()


    class ViewReservation(QMainWindow): #GUI Menu to view reservations
        def __init__(self):
            super(ViewReservation,self).__init__()
            loadUi("ViewReservation.ui", self)          # loads the view reservation menu UI file
            self.BackBt.clicked.connect(self.exit)             # When this button is clicked, it takes the user back to the reservation menu
            self.RefreshBt.clicked.connect(self.loadData)      # When this button is clicked, it allows the user to refresh the data listed on the table

        def exit(self):     # Exit the menu. all fields are cleared
            self.dataTable.clear()
            manager.goToReservationMenu()
            self.dataTable.setRowCount(1)

        def loadData(self): #Load the reservations from SQL database into the on-screen table
            try:
                manager.viewReservation() #Retrieve reservations
                row = 0
                if manager.reservations.count()<1: #Let user know there are no reservations
                    raise NoReservationError
                else:
                    self.dataTable.setRowCount(manager.reservations.count())    # Format the Table
                    self.columns = ["Res. ID","From Date","Days","To Date","No. of Guests","No. of Rooms"]
                    self.dataTable.setHorizontalHeaderLabels(self.columns)
                    for reservation in manager.reservations: #Populate the on-screen table
                        self.dataTable.setItem(row, 0, QtWidgets.QTableWidgetItem(str(reservation.get_ID())))
                        self.dataTable.setItem(row, 1, QtWidgets.QTableWidgetItem(reservation.get_fromD()))
                        self.dataTable.setItem(row, 2, QtWidgets.QTableWidgetItem(reservation.get_numOfDays()))
                        self.dataTable.setItem(row, 3, QtWidgets.QTableWidgetItem(reservation.get_toD()))
                        self.dataTable.setItem(row, 4, QtWidgets.QTableWidgetItem(reservation.get_numOfPer()))
                        self.dataTable.setItem(row, 5, QtWidgets.QTableWidgetItem(reservation.get_numOfRoom()))
                        row += 1
            except NoReservationError:
                msg = QMessageBox()
                msg.setText("You have no reservations stored in the database!")
                msg.setWindowTitle("Rick Astley's Bar and Grill")
                msg.exec()

    class CancelReservation(QMainWindow): #GUI menu to cancel reservations for the logged in user
        def __init__(self):
            super(CancelReservation,self).__init__()
            loadUi("CancelReservation.ui", self)           # loads the cancel reservation menu UI file
            self.BackBt.clicked.connect(self.exit)         # When this button is clicked, it takes the user back to the reservation menu
            self.CancelBt.clicked.connect(self.cancel)     # When this button is clicked, the specified reservation ID is deleted

        def exit(self):         # Exits the menu and clears all field
            self.dataTable.clear()
            manager.goToReservationMenu()
            self.dataTable.setRowCount(0)
            self.ResID.clear()

        def cancel(self):       # Operations to cancel reservation
            manager.cancelReservation()
            self.ResID.clear()
            self.dataTable.clear()
            self.loadData()

        def loadData(self):     # Load data from reservation table
            try:                # works same as the view reservation menu for the most part
                manager.viewReservation()
                row = 0
                if manager.reservations.count()<1:
                    raise NoReservationError
                else:
                    self.dataTable.setRowCount(manager.reservations.count())
                    self.columns = ["Res. ID","From Date","Days","To Date","No. of Guests","No. of Rooms"]
                    self.dataTable.setHorizontalHeaderLabels(self.columns)
                    for reservation in manager.reservations:
                        self.dataTable.setItem(row, 0, QtWidgets.QTableWidgetItem(str(reservation.get_ID())))
                        self.dataTable.setItem(row, 1, QtWidgets.QTableWidgetItem(reservation.get_fromD()))
                        self.dataTable.setItem(row, 2, QtWidgets.QTableWidgetItem(reservation.get_numOfDays()))
                        self.dataTable.setItem(row, 3, QtWidgets.QTableWidgetItem(reservation.get_toD()))
                        self.dataTable.setItem(row, 4, QtWidgets.QTableWidgetItem(reservation.get_numOfPer()))
                        self.dataTable.setItem(row, 5, QtWidgets.QTableWidgetItem(reservation.get_numOfRoom()))
                        self.ResID.addItem(str(reservation.get_ID()))       # Populate reservation ID dropdown list
                        row += 1

            except NoReservationError:          # Raised when logged user has no reservation
                msg = QMessageBox()
                msg.setText("You have no reservations stored in the database!")
                msg.setWindowTitle("Rick Astley's Bar and Grill")
                msg.exec()

    class ModifyReservation(QMainWindow): #GUI menu to modify a reservation
        def __init__(self):
            super(ModifyReservation,self).__init__()
            loadUi("ModifyReservation.ui", self)        # loads the modify reservation menu UI file
            self.SubmitBt.clicked.connect(self.submitData)
            self.BackBt.clicked.connect(manager.goToReservationMenu)
            self.PullBt.clicked.connect(self.selectData)
            self.currentDate = QDate.currentDate()
            self.qdate = QDate(self.currentDate.year(), self.currentDate.month(), self.currentDate.day())
            self.FromDate.setDate(self.qdate)
            self.FromDate.show()
            self.ToDate.setDate(self.qdate)
            self.ToDate.show()

        def pullData(self):
            self.ResID.clear()
            manager.viewReservation()
            for reservation in manager.reservations:
                self.ResID.addItem(str(reservation.get_ID()))
    # <<<<<------------------------------------------------------------------------------------------------
        def selectData(self):
            try:
                manager.selectReservation()
                fromDateString = QDate.fromString(manager.currentReservation.get_fromD(), "yyyy-MM-dd")
                fromDateString = QDate(fromDateString.year(),fromDateString.month(),fromDateString.day())
                self.FromDate.setDate(fromDateString)
                self.FromDate.show()
                toDateString = QDate.fromString(manager.currentReservation.get_toD(), "yyyy-MM-dd")
                toDateString = QDate(toDateString.year(),toDateString.month(),toDateString.day())
                self.ToDate.setDate(toDateString)
                self.ToDate.show()
                self.NofP.setValue(int(manager.currentReservation.get_numOfPer()))
                self.NofP.show()
                self.NofR.setValue(int(manager.currentReservation.get_numOfRoom()))
                self.NofR.show()
            except AttributeError as NoReservationError:
                msg = QMessageBox()
                msg.setText("You have no reservations stored in the database!")
                msg.setWindowTitle("Rick Astley's Bar and Grill")
                msg.exec()

        def submitData(self):
            try:
                self.numOfP = self.NofP.text()
                self.numOfR = self.NofR.text()
                self.fromD = datetime.strptime(self.FromDate.text(), "%d/%m/%Y").date()
                self.toD = datetime.strptime(self.ToDate.text(), "%d/%m/%Y").date()

                if not self.numOfP > '0':
                    raise EmptyInputErrorForPeople
                elif not self.numOfR > '0':
                    raise EmptyInputErrorForRoom
                elif self.fromD < self.currentDate:
                    raise DateInThePastError
                elif self.toD < self.fromD:
                    raise ToBeforeFromDateError
                else:
                    self.numOfDays = (self.toD - self.fromD).days
                    if self.numOfDays == 0:
                        self.numOfDays = 1

                    manager.modifyReservation(self.numOfDays, self.fromD, self.toD, self.numOfP, self.numOfR)
                    self.NofP.setValue(1)
                    self.NofR.setValue(1)
                    manager.goToReservationMenu()

            except ToBeforeFromDateError:
                toD_error_msg = QMessageBox()
                toD_error_msg.setText("Please enter a valid END date.")
                toD_error_msg.setWindowTitle("Error!")
                toD_error_msg.exec()

            except DateInThePastError:
                fromD_error_msg = QMessageBox()
                fromD_error_msg.setWindowTitle("Error!")
                fromD_error_msg.setText(f"Please enter a valid upcoming date.\nCurrent Date: {datetime.now().date()}")
                fromD_error_msg.exec()

            except EmptyInputErrorForRoom:
                self.NofR.setValue(1)
                NofR_error_msg = QMessageBox()
                NofR_error_msg.setWindowTitle("Error!")
                NofR_error_msg.setText("Please enter the number of rooms expected.")
                NofR_error_msg.exec()

            except EmptyInputErrorForPeople:
                self.NofP.setValue(1)
                NofP_error_msg = QMessageBox()
                NofP_error_msg.setWindowTitle("Error!")
                NofP_error_msg.setText("Please enter the number of people expected.")
                NofP_error_msg.exec()

            except AttributeError as NoReservationError:
                msg = QMessageBox()
                msg.setText("You have no reservations stored in the database!")
                msg.setWindowTitle("Rick Astley's Bar and Grill")
                msg.exec()


    class GUI: #Class to control GUI windows
        def __init__(self):
            self.app = QtWidgets.QApplication(sys.argv) #Widgets is used to organize GUI windows
            self.screen =  QtWidgets.QStackedWidget() #Stacked widgets allows multiple windows to be created
            self.mainMenu = MainMenu() #Set first window to Main Menu UI
            self.registerMenu = RegisterMenu() #Set second window to Register Menu UI
            self.loginMenu = LoginMenu() #Set third window to Login Menu UI
            self.reservationMenu = ReservationMenu() #Set fourth window to Reservation Menu UI
            self.reserveMenu = ReserveMenu()
            self.viewReservation = ViewReservation()
            self.cancelReservation = CancelReservation()
            self.modifyReservation = ModifyReservation()

        def buildGUI(self): #Build the GUI
            self.screen.addWidget(self.mainMenu) #Screen Index 0
            self.screen.addWidget(self.registerMenu) #Screen Index 1
            self.screen.addWidget(self.loginMenu) #Screen Index 2
            self.screen.addWidget(self.reservationMenu) #Screen Index 3
            self.screen.addWidget(self.reserveMenu) #Screen Index 4
            self.screen.addWidget(self.viewReservation) #Screen Index 5
            self.screen.addWidget(self.cancelReservation) #Screen Index 6
            self.screen.addWidget(self.modifyReservation) #Screen Index 7
            self.screen.setFixedHeight(580) #constrain window dimensions
            self.screen.setFixedWidth(800)
            self.screen.show() #Display window
            self.app.exec() #Execute GUI


    class Manager: #aggregation class ("has" relationship with account and reservation)
        def createReservation(self, numOfDays, fromD, toD, numOfPer, numOfRoom):
            self.myReservation = Reservation(self.currentAccount.email, fromD, toD, numOfDays, numOfPer, numOfRoom) #Temporary instance for object relational mapping
            restaurantSession.add(self.myReservation) #add data to SQL table (synchronize object)
            restaurantSession.commit() #Commit the changes to the database

        def createAccount(self, email, fName, lName, password, bDay): #Method to add account to restaurant Database
            try:
                self.myAccount = Account(email, fName, lName, password, bDay) #Temporary instance for object relational mapping
                restaurantSession.add(self.myAccount) #add data to SQL table (synchronize object)
                restaurantSession.commit() #Commit the changes to the database
                success_resgiter_msg = QMessageBox()
                success_resgiter_msg.setWindowTitle("Rick Astley's Bar and Grill")
                success_resgiter_msg.setText("Registered Successfully!")
                success_resgiter_msg.exec()
                manager.goToMainMenu()

            except exc.IntegrityError as DuplicateAccountError: #Make sure account email is unique
                msg = QMessageBox()
                msg.setText("This account already exists!")
                msg.setWindowTitle("Rick Astley's Bar and Grill")
                restaurantSession.rollback()
                msg.exec()

        def viewReservation(self): #Query reservations for a specific user from the database based on current logged in user
            try:
                self.reservations = restaurantSession.query(Reservation).filter(Reservation.email == self.currentAccount.email) #Query the SQLite Database using a filter and map entries that match the filter to multiple instances of Reservation
            except AttributeError:
                return False

        def cancelReservation(self): #Delete reservation based on current ID selected in GUI
            try:
                self.currentReservation = restaurantSession.query(Reservation).filter(Reservation.reservationID == gui.cancelReservation.ResID.currentText()).first() #Query the SQLite Database using a filter and map entries that match the filter to an instance of Account
                restaurantSession.delete(self.currentReservation) #Delete reservation from database
                restaurantSession.commit() #Commit changes to database
                msg = QMessageBox()
                msg.setText("Reservation cancelled successfully!")
                msg.setWindowTitle("Rick Astley's Bar and Grill")
                msg.exec()

            except ormexc.UnmappedInstanceError as NoReservationError: #Except error when no reservations exist
                pass

        def selectReservation(self):
            self.currentReservation = restaurantSession.query(Reservation).filter(Reservation.reservationID == gui.modifyReservation.ResID.currentText()).first() #Query the SQLite Database using a filter and map entries that match the filter to an instance of Reservation

        def modifyReservation(self, numOfDays, fromD, toD, numPeople, numRoom):
            self.currentReservation.numOfDays = numOfDays
            self.currentReservation.fromD = fromD
            self.currentReservation.toD = toD
            self.currentReservation.numOfPer = numPeople
            self.currentReservation.numOfRoom = numRoom
            restaurantSession.commit()
            msg = QMessageBox()
            msg.setText("Reservation updated successfully!")
            msg.setWindowTitle("Rick Astley's Bar and Grill")
            msg.exec()

        def login(self, email, password): #Validates login credentials of user. Saves logged in user to a currentAccount instance for future reference
            try:
                self.currentAccount = restaurantSession.query(Account).filter(Account.email == email, Account.password == password).first() #Query the SQLite Database using a filter and and map entries that match the filter to the object
                if self.currentAccount == None:
                    return False
                else:
                    return True
            except AttributeError:
                return False

        def accessDatabase(self): #Method used to initially launch the database
            #Commit the data
            restaurantDatabase.metadata.create_all(databaseEngine)
            restaurantSession.commit()

        def goToMainMenu(self): #Below methods are used to navigate between menu screens
            gui.screen.setCurrentIndex(0) #Index number indicates the current screen in QWidgets

        def goToRegisterMenu(self):
            gui.screen.setCurrentIndex(1)

        def goToLoginMenu(self):
            gui.screen.setCurrentIndex(2)

        def goToReservationMenu(self):
            gui.screen.setCurrentIndex(3)
            gui.reservationMenu.setUser()

        def goToViewReservation(self):
            gui.screen.setCurrentIndex(5)
            gui.viewReservation.loadData()

        def goToCancelReservation(self):
            gui.screen.setCurrentIndex(6)
            gui.cancelReservation.loadData()

        def goToModifyReservation(self):
            gui.screen.setCurrentIndex(7)
            gui.modifyReservation.pullData()

        def goToReserveMenu(self):
            gui.screen.setCurrentIndex(4)

        def closeProgram(self):
            restaurantSession.close()
            msg = QMessageBox()
            msg.setText("Thank you for choosing Rick Astley's Bar and Grill!\n We will never give you up and never let you down.")
            msg.setWindowTitle("Rick Astley's Bar and Grill")
            msg.exec()
            exit()


    if __name__ == "__main__":
        manager = Manager()
        pygame.mixer.init()     # loads the background music
        pygame.mixer.music.load("bgm.mp3")
        pygame.mixer.music.play()
        gui = GUI()
        manager.accessDatabase()
        gui.buildGUI()

except Exception:
    print("An unexpected error occured.\nMake sure required dependencies are installed:\nsqlalchemy\npygame\nPyQt6")
