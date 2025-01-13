from Enemy import *
import random

class Zombie(Enemy):
    def __init__(self, health_points, attack_demage):
        super().__init__(
            type_of_enemy='Zombie',
            health_points=health_points,
            attack_demage=attack_demage,
        )
    
    def talk(self):
        print("Braaains!")

    def spread_disease(self):
        return "You are now infected with the zombie virus!"
    
    def special_attack(self):
        did_special_attack_work = random.random() < 0.50
        if did_special_attack_work:
            self.health_points += 2
            print('Zombie regenerate 2HP')
    