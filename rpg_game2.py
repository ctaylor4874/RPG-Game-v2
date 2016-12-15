import random
import time
from random import randint


class Character(object):
    def __init__(self):
        self.name = '<undefined>'
        self.health = 10
        self.power = 5

    def alive(self):
        return self.health > 0

    def attack(self, enemy):
        if not self.alive():
            hero.coins += self.bounty
            print "Hero receives %d bounty coins for killing %s." % (self.bounty, self.name)
            return
        print "%s attacks %s" % (self.name, enemy.name)
        enemy.receive_damage(self.power)
        time.sleep(1.5)

    def receive_damage(self, points):
        self.health -= points
        print "%s received %d damage." % (self.name, points)
        if self.health <= 0:
            print "%s is dead." % self.name

    def print_status(self):
        print "%s has %d health and %d power." % (self.name, self.health, self.power)


class Hero(Character):
    armor = 0
    evade = 0.0
    poison = False
    tcount = 0
    scount = 0
    useS = 0
    swapped = False

    def __init__(self):
        super(Hero, self).__init__()
        self.name = 'hero'
        self.health = 10
        self.power = 5
        self.coins = 20

    def restore(self):
        self.health = 10
        print "Hero's heath is restored to %d!" % self.health
        time.sleep(1)

    def attack(self, enemy):
        if self.poison:
            print "%s has poison on his blade, attack deals + 1 damage to %s" % (self.name, enemy.name)
            self.power += 1
        if self.tcount > 0:
            print("%s has %d tonics, would you like to use one?") % (self.name, self.tcount)
            useT = input("1 for yes, 2 for no: ")
            if useT == 1:
                self.health += 2
                print "%s's health increased to %d." % (self.name, self.health)
                self.tcount -= 1
        if self.scount > 0:
            print("%s has %d power swaps, would you like to use one?") % (self.name, self.scount)
            useS = input("1 for yes, 2 for no: ")
            if useS == 1:
                self.swapped = True
                self.power, enemy.power = enemy.power, self.power
                print "%s swapped powers with %s." % (self.name, enemy.name)
                print "%s's power is now %d, and %s's power is now %d" % (
                self.name, self.power, enemy.name, enemy.power)
        super(Hero, self).attack(enemy)
        if self.swapped:
            self.power, enemy.power = enemy.power, self.power
            self.scount -= 1
            useS = 0
            self.swapped = False
        if self.poison:
            self.power -= 1
            self.poison = False

    def receive_damage(self, points):
        evadeChance = float(self.evade / 20.0)
        evaded = random.random() < evadeChance
        if evaded:
            print "%s has evaded the attack!" % (self.name)
            points = 0
            return
        if self.armor:
            # healthArmor = self.health + armor
            self.health += self.armor
            print "%s has %d armor, health increased to %d" % (self.name, self.armor, (self.health))
        super(Hero, self).receive_damage(points)
        if self.armor:
            self.armor -= points
            if self.armor < 0:
                self.armor = 0

    def buy(self, item):
        self.coins -= item.cost
        item.apply(hero)


class Zombie(Character):
    def __init__(self):
        super(Zombie, self).__init__()
        self.name = 'Zombie'
        self.health = 5
        self.power = 2
        self.bounty = 2

    def receive_damage(self, points):
        dead = random.random() < 2
        if dead:
            self.health = 0
        else:
            self.health -= points
            print "%s received %d damage." % (self.name, points)
            if self.health <= 0:
                return


class Medic(Character):
    def __init__(self):
        super(Medic, self).__init__()
        self.name = "Medic"
        self.bounty = 4
        self.power = 3

    def receive_damage(self, points):
        super(Medic, self).receive_damage(points)
        plus2health = random.random() < 0.2
        if plus2health:
            self.health += 2
            print("Medic self healed +2 HP!")


class Knight(Character):
    def __init__(self):
        super(Knight, self).__init__()
        self.name = "Knight"
        self.health = 7
        self.power = 7
        self.bounty = 8


class Shadow(Character):
    def __init__(self):
        super(Shadow, self).__init__()
        self.name = 'Shadow'
        self.health = 1
        self.bounty = 8
        self.power = 1

    def receive_damage(self, points):
        recDamage = random.random() > 0.1
        if recDamage:
            print("Shadow evaded attack!!")
            points = 0
        super(Shadow, self).receive_damage(points)


class Mage(Character):
    def __init__(self):
        super(Mage, self).__init__()
        self.name = "Mage"
        self.health = 6
        self.power = 3
        self.bounty = 8

    def receive_damage(self, points):
        boostHP = random.random() < 0.2
        if boostHP:
            print("%s boosted health by 3 for this turn!") % (self.name)
            self.health += 3
        super(Mage, self).receive_damage(points)

    def attack(self, enemy):
        boostPWR = random.random() < 0.2
        if boostPWR:
            print("%s boosted power by 5 for this turn!") % (self.name)
            self.power += 3
        super(Mage, self).attack(enemy)


class Goblin(Character):
    def __init__(self):
        super(Goblin, self).__init__()
        self.name = 'goblin'
        self.health = 6
        self.power = 2
        self.bounty = 2


class Wizard(Character):
    def __init__(self):
        super(Wizard, self).__init__()
        self.name = 'wizard'
        self.health = 7
        self.power = 3
        self.bounty = 6

    def attack(self, enemy):
        swap_power = random.random() > 0.5
        if swap_power:
            print "%s swaps power with %s during attack" % (self.name, enemy.name)
            self.power, enemy.power = enemy.power, self.power
        super(Wizard, self).attack(enemy)
        if swap_power:
            self.power, enemy.power = enemy.power, self.power


class Battle(object):
    def do_battle(self, hero, enemy):
        print "====================="
        print "Hero faces the %s" % enemy.name
        print "====================="
        while hero.alive() and enemy.alive():
            hero.print_status()
            enemy.print_status()
            time.sleep(1.5)
            print "-----------------------"
            print "What do you want to do?"
            print "1. fight %s" % enemy.name
            print "2. do nothing"
            print "3. flee"
            print "> ",
            input = int(raw_input())
            if input == 1:
                hero.attack(enemy)
            elif input == 2:
                pass
            elif input == 3:
                print "Goodbye."
                exit(0)
            else:
                print "Invalid input %r" % input
                continue
            enemy.attack(hero)
        if hero.alive():
            print "You defeated the %s" % enemy.name
            return True
        else:
            return False


hero = Hero()


class Tonic(object):
    cost = 5
    name = 'tonic'

    def apply(self, character):
        hero.tcount += 1
        print("%s has %d tonics, would you like to use one?") % (hero.name, hero.tcount)
        useTnow = input("1 for yes, 2 for no: ")
        if useTnow == 1:
            hero.health += 2
            print "%s's health increased to %d." % (hero.name, hero.health)
            hero.tcount -= 1


class Sword(object):
    cost = 10
    name = 'sword'

    def apply(self, hero):
        hero.power += 2
        print "%s's power increased to %d." % (hero.name, hero.power)


class SuperTonic(object):
    cost = 10
    name = 'super tonic'

    def apply(self, character):
        character.health = 10
        print "%s's health increased to %d." % (character.name, character.health)


class Armor(object):
    cost = 10
    name = 'armor'

    def apply(self, hero):
        hero.armor += 2
        print "%s's armor increased to %d." % (hero.name, hero.armor)


class Evade(object):
    if Hero.evade < 100:
        cost = 5
        name = 'evade'

        def apply(self, hero):
            hero.evade += 2
            print "%s's evade increased to %d." % (hero.name, hero.evade)
    else:
        print("You cannot purchase any more Evade, you are maxed out...")


class Poison(object):
    cost = 1
    name = 'Poison'

    def apply(self, hero):
        hero.poison = True
        print ("%s's power increased by 1 for one attack.") % (hero.name)


class SuperArmor(object):
    cost = 15
    name = 'superarmor'

    def apply(self, hero):
        hero.armor += 5
        print "%s's armor increased to %d." % (hero.name, hero.armor)


class Swap(object):
    cost = 10
    name = 'swap'

    def apply(self, character):
        hero.scount += 1


class Store(object):
    # If you define a variable in the scope of a class:
    # This is a class variable and you can access it like
    # Store.items => [Tonic, Sword]

    items = [Tonic, Sword, SuperTonic, Armor, Evade, Poison, SuperArmor, Swap]

    def do_shopping(self, hero):
        while True:
            print "====================="
            print "Welcome to the store!"
            print "====================="
            print "You have %d coins." % hero.coins
            if hero.coins <= 0:
                print "You don't have any coins."
            print "What do you want to do?"
            for i in xrange(len(Store.items)):
                item = Store.items[i]
                print "%d. buy %s (%d)" % (i + 1, item.name, item.cost)
            print "10. leave"
            input = int(raw_input("> "))
            if input == 10:
                break
            else:
                ItemToBuy = Store.items[input - 1]
                item = ItemToBuy()
                if item.cost > hero.coins:
                    print "You don't have enough coins for %s.. Select another item." % (item.name)
                else:
                    hero.buy(item)


enemies = [Goblin(), Wizard(), Mage(), Shadow(), Knight(), Medic(), Zombie()]
battle_engine = Battle()
shopping_engine = Store()

for enemy in enemies:
    hero_won = battle_engine.do_battle(hero, enemy)
    if not hero_won:
        print "YOU LOSE!"
        exit(0)
    shopping_engine.do_shopping(hero)

print "YOU WIN!"
