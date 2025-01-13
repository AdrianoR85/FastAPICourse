class Enemy:
    def __init__(self, type_of_enemy, health_points, attack_demage):
        self.__type_of_enemy = type_of_enemy
        self.health_points = health_points
        self.attack_damage = attack_demage

    def get_type_of_enemy(self):
        return self.__type_of_enemy

    def set_type_of_enemy(self, new_type: str):
        self.__type_of_enemy = new_type

    def talk(self):
        print(f"I'm a {self.__type_of_enemy}. Be prepared to fight!")

    def walk_forward(self):
        print(f"{self.__type_of_enemy} moves cleser to you")

    def attack(self):
        print(f"{self.__type_of_enemy} attacks for {self.attack_damage} damage!")
    
    def special_attack(self):
        print('Enemy has no special attack')
