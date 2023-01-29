from Controller.controller import Controller


# TODO - In UML add notions for state and methods -> + for public, - for private, and inside method brackets in, out and inout
# TODO - add validation for dates i.e. 31 feb
# TODO - after implementing online database see if calls for getting names and number from show_day can be optimnised into a single db request, instead of one request for each iteration
# TODO - convert daily_notes_ids and daily_notes into array of tuples in model
# TODO = when documenting check for getter metheods and remove them
# TODO - change parameter date to result of date to string wherever is used only to display which should be everywhere
# TODO - KEEP IN MIND CURRENTLY DATABASE GIVES SWAPPED SKINTYPE AND MAIL, FIX IN NEW DATABASE
# TODO - make possible to validate data when editing client 1 by 1 field
# TODO - Make the needed changes so when fillers are created theyre assigned customer_id = 1, also check if that will make it easier for methods such as are_fillers
# TODO - rework is_free so it works without separate is_free databse call and fix showing busy if for example extending treatment
# TODO - make validation method remove whitespaces
# TODO - allow bookings from within worktime to exceed worktime durationwise
class MclsMain:
    def __init__(self):
        self.controller = Controller()
        self.controller.view.mainloop()

        # tk = Tk()
        # root = Frame(tk)
        #
        # fonts1 = list(font.families())[210:240]
        # fonts2 = list(font.families())[240:270]
        # fonts3 = list(font.families())[280:310]
        #
        # print(len(list(font.families())))
        # labels1 = []
        # labels2 = []
        # labels3 = []
        #
        # for index, f in enumerate(fonts1):
        #
        #     labels1.append(Label(text = 'Човек е дълго изречение, написано с много любов ' + fonts1[index], font = (fonts1[index], 16)))
        #     labels1[index].grid(row = index, column = 0)
        #
        #     labels2.append(Label(text = 'Човек е дълго изречение, написано с много любов ' + fonts2[index], font = (fonts2[index], 16)))
        #     labels2[index].grid(row = index, column = 1)
        #
        #     labels3.append(Label(text = 'Човек е дълго изречение, написано с много любов ' + fonts3[index], font = (fonts3[index], 16)))
        #     labels3[index].grid(row = index, column = 2)
        #
        #
        # tk.mainloop()
