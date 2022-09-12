import sqlite3
from pathlib import Path

hp_die = {'Fighter': 10, 'Paladin': 10, 'Ranger': 8, 'Barbarian': 12, 'Rogue': 6, 'Bard': 6, 'Cleric': 8, 'Druid': 8,
          'Wizard': 4, 'Sorcerer': 4, 'Warlock': 4}  # the hit dice value for each class for calculating hit points

attribute_mod = {'1': -5, '2': -4, '3': -4, '4': -3, '5': -3, '6': -2, '7': -2, '8': -1, '9': -1, '10': 0, '11': 0,
                 '12': 1, '13': 1, '14': 2, '15': 2, '16': 3, '17': 3, '18': 4, '19': 4,
                 '20': 5}  # attribute modifiers for calculating stat bonuses

menu_input = []
mod_menu_input = []


class char_hitpoints:  # used to calculate hit points

    def __init__(self, con_mod, level, hit_die):
        self.con_mod = con_mod
        self.char_level = level
        self.hit_die = hit_die

    def calc_hp(self, con_mod, level, hit_die):
        char_hp = level * hit_die + con_mod * level
        return char_hp


def create_char_database():  # creates the database for a new character and adds the necessary tables
    connection = sqlite3.connect(f"{first_name}.db")

    connection.execute("CREATE TABLE Stats (Name,Surname,Class,Level,Strength,Dexterity,Constitution, Intelligence, "
                       "Wisdom, Charisma, HitPoints)")

    connection.execute("CREATE TABLE Weapons (Weapon,DmgType,MinDmg,MaxDmg,Reach,Finesse)")

    connection.execute("CREATE TABLE Armor (Armor,Type, AC, MaxDex,StealthDis)")

    connection.execute("CREATE TABLE Inventory (Item,EffectType,EffMin,EffMax,Charges,Cost)")

    connection.close()


def create_stats():  # adds stats for character creation
    connection = sqlite3.connect(f"{first_name}.db")

    cursor = connection.cursor()

    cursor.execute("INSERT INTO Stats (Name,Surname,Class,Level,Strength,Dexterity,Constitution, Intelligence, "
                   f"Wisdom, Charisma,HitPoints) VALUES (?,?,?,?,?,?,?,?,?,?,?)", (
                       first_name, surname, char_class, char_level, input_str, input_dex, input_con, input_int,
                       input_wis,
                       input_cha, char_hp))
    connection.commit()
    connection.close()


def modify_stats():  # allows for modification of stats by the user
    connection = sqlite3.connect(f"{first_name}.db")
    cursor = connection.cursor()
    cursor.execute(f"UPDATE Stats SET {stat_select} = {mod_stat}")
    connection.commit()
    connection.close()


def create_weapon():  # this creates adds a weapon to a character's inventory. Uses stats from the 'data.db' database
    # and transfers those to the character's database
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM Weapons WHERE Name = '{input_weapon}' ")
    result = cursor.fetchone()
    connection.close()

    connection = sqlite3.connect(f"{first_name}.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Weapons (Weapon, DmgType, MinDmg, MaxDmg, Reach, Finesse) VALUES (?,?,?,?,?,?)",
                   (result[0], result[1], result[2], result[3], result[4], result[5]))
    connection.commit()
    connection.close()


def delete_weapon():  # deletes a weapon from a character's database
    connection = sqlite3.connect(f"{first_name}.db")
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM Weapons WHERE Weapon = '{input_weapon}'")
    connection.commit()
    connection.close()


def create_armor():  # same as weapon above
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM Armor WHERE Name = '{input_armor}' ")
    result = cursor.fetchone()
    connection.close()

    connection = sqlite3.connect(f"{first_name}.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Armor (Armor, Type, AC, MaxDex, StealthDis) VALUES (?,?,?,?,?)",
                   (result[0], result[1], result[2], result[3], result[4]))
    connection.commit()
    connection.close()


def delete_armor():  # same as weapon above
    connection = sqlite3.connect(f"{first_name}.db")
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM Armor WHERE Armor = '{input_armor}'")
    connection.commit()
    connection.close()


def create_inventory():  # creates a table for
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM Items WHERE Item = '{input_item}' ")
    result = cursor.fetchone()
    connection.close()

    connection = sqlite3.connect(f"{first_name}.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Inventory (Item, EffectType, EffMin, EffMax, Charges, Cost) VALUES (?,?,?,?,?,?)",
                   (result[0], result[1], result[2], result[3], result[4], result[5]))
    connection.commit()
    connection.close()


def delete_inventory():
    connection = sqlite3.connect(f"{first_name}.db")
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM Inventory WHERE Item = '{input_item}'")
    connection.commit()
    connection.close()


def list_weapons():  # lists all the available weapons in the database
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM Weapons")
    result = cursor.fetchall()

    for listweap in result:
        print(listweap[0])

    connection.close()


def list_armor():  # lists all the available armor in the database
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM Armor")
    result = cursor.fetchall()

    for listarmor in result:
        print(listarmor[0])

    connection.close()


def display_char():  # uses the first name of a character to pull up the character information from the database
    connection = sqlite3.connect(f"{first_name}.db")
    cursor = connection.cursor()

    cursor.execute(f"SELECT * FROM Stats")
    result_stats = cursor.fetchall()

    cursor.execute(f"SELECT * FROM Weapons")
    result_weapons = cursor.fetchall()

    cursor.execute(f"SELECT * FROM Armor")
    result_armor = cursor.fetchall()

    cursor.execute(f"SELECT Item FROM Inventory")
    result_item = cursor.fetchall()
    connection.close()

    print(f'''Character Name: {result_stats[0][0]} {result_stats[0][1]}
          Character Class: {result_stats[0][2]}
          Character Level: {result_stats[0][3]}
          Character Attributes:
          Strength:{result_stats[0][4]}
          Dexterity: {result_stats[0][5]}
          Constitution: {result_stats[0][6]}
          Intelligence: {result_stats[0][7]} 
          Wisdom: {result_stats[0][8]}
          Charisma: {result_stats[0][9]}''')

    print("Weapons:")  # runs through all the weapons
    for w in result_weapons:
        print(w[0])
        print(w[1])
        print(f"{w[2]}D{w[3]}")
        print("")

    for a in result_armor:  # runs through all the armor
        print(f"Armor:", a[0])
        print(f"Armor Class:", a[2])
        print("")

    print("Inventory:")  # runs through the misc inventory
    for i in result_item:
        print(i[0])


while menu_input != "Q":  # main body for menu prompts
    print("***********************************************************")
    print("This program allows you to create and store D&D characters.")
    print("***********************************************************")
    menu_input = input("Select what you want to do: [C]reate Char, [D]isplay Char, [M]odify Char, or [Q]uit")

    if menu_input == "C":
        first_name = input("Enter your character's first name: ").capitalize()
        char_database = f"{first_name}.db"  # inputs database name into a variable for checking if database exists
        database_check = Path(char_database)
        if database_check.is_file():  # performs check to see if file exists to prevent overwriting existing characters
            print("")
            print("")
            print(
                "This character already exists! Please either make a new character or modify your existing character.")
        else:
            create_char_database()
            surname = input("Enter your character's surname: ").capitalize()
            char_class = input("Enter your character's class: ").capitalize()
            char_level = int(input("Enter your character's level: "))
            input_str = int(input("Enter your Strength: "))
            input_dex = int(input("Enter your Dexterity: "))
            input_con = int(input("Enter your Constitution: "))
            input_int = int(input("Enter your Intelligence: "))
            input_wis = int(input("Enter your Wisdom: "))
            input_cha = int(input("Enter your Charisma: "))

            s_input_con = str(input_con)
            stat_mod = attribute_mod[f"{s_input_con}"]
            hit_dice = hp_die[f"{char_class}"]
            hit_points = char_hitpoints(f"{stat_mod}", f"{char_level}", f"{hit_dice}")
            char_hp = hit_points.calc_hp(stat_mod, char_level, hit_dice)

            create_stats()

            input_weapon = input("Enter your weapon: ").capitalize()
            create_weapon()

            input_armor = input("Enter your armor: ").capitalize()
            create_armor()

        print("")
        print("")

    elif menu_input == "D":
        first_name = input("Enter the first name of your character: ").capitalize()

        display_char()

        print("")
        print("")

    elif menu_input == "M":
        first_name = input("What Character would you like to modify: ").capitalize()
        while mod_menu_input != "R":
            mod_menu_input = input('''What would you like to change:
            [C]hange Stat
            Modify [W]eapon
            Modify [A]rmor
            Modify [I]nventory Item
            [R]eturn to Previous Menu
            ''').capitalize()

            if mod_menu_input == "C":
                stat_select = input("What stat would you like to modify?: ").capitalize()
                mod_stat = int(input("What is the new stat value: "))
                modify_stats()

            elif mod_menu_input == "W":
                change_input_weapon = input("Do you want to [A]dd a weapon,[D]elete a weapon, or [L]ist available "
                                            "weapons?").capitalize()
                if change_input_weapon == "A":
                    input_weapon = input("Please enter the weapon you would like to add: ").capitalize()
                    create_weapon()

                elif change_input_weapon == "D":
                    input_weapon = input("Please enter the weapon you would like to delete: ").capitalize()
                    delete_weapon()

                elif change_input_weapon == "L":
                    list_weapons()

                else:
                    print("Invalid Selection. Please choose again.")

            elif mod_menu_input == "A":
                change_input_armor = input(
                    "Do you want to [A]dd an armor,[D]elete an armor, or [L]ist available armor?").capitalize()
                if change_input_armor == "A":
                    input_weapon = input("Please enter the armor you would like to add: ").capitalize()
                    create_armor()

                elif change_input_armor == "D":
                    input_weapon = input("Please enter the armor you would like to delete: ").capitalize()
                    delete_armor()

                elif change_input_armor == "L":
                    list_armor()
                else:
                    print("Invalid selection. Please make a different selection")

            elif mod_menu_input == "I":
                change_input_item = input("Do you want to [A]dd an item or [D]elete an item?")
                if change_input_item == "A":
                    input_item = input("Please enter the item you would like to add: ")
                    create_inventory()
                elif change_input_item == "D":
                    input_item = input("Please enter the item you would like to delete: ")
                else:
                    print("Invalid selection. Please make a different selection")
            else:
                print("Invalid selection. Please make a different selection: ")

    elif menu_input == "Q":
        print("Exiting...")
        break

    else:
        print("")
        print("Please enter a different selection ")
        print("")
