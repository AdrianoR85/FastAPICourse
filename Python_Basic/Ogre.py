from Enemy import *
import random

class Ogre(Enemy):
    def __init__(self, health_points, attack_demage):
        super().__init__(
            type_of_enemy='Ogre',
            health_points=health_points,
            attack_demage=attack_demage,
        )
    
    def talk(self):
        print('Ogre is slamming hands all around')

    def throw_stone(self):
        return 'Ogre throws a stone at you'

    def special_attack(self):
        did_special_attack_work = random.random() < 0.20
        if did_special_attack_work:
            self.attack_damage += 4
            print('Ogre gets angry and increases attack by 4')
    