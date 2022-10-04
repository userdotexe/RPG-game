from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random

glitter = Spell("Glitter", 28, 390, "black")
grapple = Spell("grapple", 30, 430, "black")
fire = Spell("Fire", 25, 700, "black")
thunder = Spell("Thunder", 25, 700, "black")
blizzard = Spell("Blizzard", 25, 700, "black")
meteor = Spell("Meteor", 40, 1300, "black")
quake = Spell("Quake", 14, 140, "black")

heal = Spell("Heal", 25, 800, "white")
morebetterheal = Spell("More better heal", 32, 1900, "white")
enemyheal = Spell("heal", 25, 470, "white")

potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super potion", "potion", "Heals 500 HP", 500)
elixer = Item("Elixer", "elixer", "Fully restore HP/MP of one party member", 9999)
hielixer = Item("Mega Elixer", "elixer", "Fully restores party's HP", 9999)

grenade = Item("Grenade", "attack", "Deals 750 damage", 750)

player_spells = [fire, thunder, blizzard, meteor, heal, morebetterheal]
enemy_spells = [grapple, glitter, enemyheal]
player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5}, {"item": elixer, "quantity": 5},
                {"item": hielixer, "quantity": 3}, {"item": grenade, "quantity": 5}]


player1 = Person("Elio:", 3260, 132, 367, 45, player_spells, player_items)
player2 = Person("ivan:", 4160, 188, 378, 45, player_spells, player_items)
player3 = Person("Enzo:", 3189, 174, 294, 45, player_spells, player_items)

enemy1 = Person("Imp  ", 1550, 130, 400, 325, enemy_spells, [])
enemy2 = Person("Demon", 11160, 701, 500, 25, enemy_spells, [])
enemy3 = Person("Imp  ", 1550, 130, 390, 325, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

defeated_enemies = 0
defeated_players = 0

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY IS ATTACKING!!" + bcolors.ENDC)

while running:
    print("===========================")

    print("\n\n")
    print("NAME                  HP                                       MP")
    for player in players:
        player.get_stats()

    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:

        player.choose_action()
        choice = input("    Choose an action: ")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)

            enemies[enemy].take_damage(dmg)
            print("You attacked " + enemies[enemy].name.replace(" ", "") + " for", dmg, "points of damage!")

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ", "") + " got died")
                del enemies[enemy]
                defeated_enemies += 1

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("    Choose magic: ")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nYou're too tired to use magic\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + spell.name + " heals" + "for", str(magic_dmg), "HP" + bcolors.ENDC)
            elif spell.type == "black":

                enemy = player.choose_target(enemies)

                enemies[enemy].take_damage(magic_dmg)

                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg),
                      "points of damage to  " + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " got died")
                    del enemies[enemy]
                    defeated_enemies += 1

        elif index == 2:
            player.choose_item()
            item_choice = int(input("    Choose item: ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "you better get more stuff..." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP" + bcolors.ENDC)
            elif item.type == "elixer":

                if item.name == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP\MP" + bcolors.ENDC)
            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)

                print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop), "points of damage to" + enemies[enemy].name + bcolors.ENDC)
                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died.")
                    del enemies[enemy]
                    defeated_enemies += 1

            # Check is player has won
        if defeated_enemies == 3:
            print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
            running = False
            break

        print("\n")
        # Enemy attack phase
        for enemy in enemies:
            enemy_choice = random.randrange(0, 2)

            if enemy_choice == 0:
                target = random.randrange(0, len(players))
                enemy_dmg = enemy.generate_damage()

                players[target].take_damage(enemy_dmg)
                print(bcolors.FAIL + bcolors.BOLD + enemy.name.replace(" ", "").replace(":", "") + " attacks " +
                      players[target].name.replace(" ", "").replace(":", "") + " for", enemy_dmg, bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(bcolors.FAIL + bcolors.BOLD + players[target].name.replace(" ", "").replace(":", "") +
                          " has died!" + bcolors.ENDC)
                    del players[target]
                    defeated_players += 1

            elif enemy_choice == 1:
                spell, magic_dmg = enemy.choose_enemy_spell()
                # magic_dmg = spell.generate_damage()
                enemy.reduce_mp(spell.cost)

                if spell.type == "white":
                    enemy.heal(magic_dmg)
                    print(bcolors.FAIL + spell.name + " heals " + enemy.name.replace(" ", "").replace(":", "") +
                          " for", str(magic_dmg), "HP." + bcolors.ENDC)
                elif spell.type == "black":
                    target = random.randrange(0, len(players))
                    players[target].take_damage(magic_dmg)
                    print(bcolors.FAIL + bcolors.BOLD + enemy.name.replace(" ", "").replace(":",
                                                                                              "") + "'s " + spell.name +
                          " deals", str(magic_dmg), "points of damage to " +
                          players[target].name.replace(" ", "").replace(":", "") + bcolors.ENDC)

                    if players[target].get_hp() == 0:
                        print(bcolors.FAIL + bcolors.BOLD + players[target].name.replace(" ", "").replace(":", "") +
                              " has died!" + bcolors.ENDC)
                        del players[target]
                        defeated_players += 1

        # Check if Enemy won
        if defeated_players == 3:
            print(bcolors.FAIL + "Your enemies have defeated you!" + bcolors.ENDC)
            running = False
            break







