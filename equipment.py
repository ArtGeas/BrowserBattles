from dataclasses import dataclass
from typing import List
from random import uniform
import marshmallow_dataclass
import marshmallow
import json


@dataclass
class Armor:
    id: int
    name: str
    defence: float
    stamina_per_turn: float


@dataclass
class Weapon:

    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    @property
    def damage(self):
        return uniform(self.min_damage, self.max_damage)


@dataclass
class EquipmentData:
    # TODO содержит 2 списка - с оружием и с броней
    weapons: list[Weapon]
    armors: list[Armor]


class Equipment:

    def __init__(self):
        self.equipment = self._get_equipment_data()

    def get_weapon(self, weapon_name) -> Weapon:
        # TODO возвращает объект оружия по имени
        try:
            weapon_index = self.equipment.weapons.index(weapon_name)
            weapon: dict = self.equipment.weapons[weapon_index]
            return Weapon(id=weapon['id'],
                          name=weapon['name'],
                          min_damage=weapon['min_damage'],
                          max_damage=weapon['max_damage'],
                          stamina_per_hit=weapon['stamina_per_hit'])
        except ValueError:
            print('ValueError')

    def get_armor(self, armor_name) -> Armor:
        # TODO возвращает объект брони по имени
        try:
            armor_index = self.equipment.armors.index(armor_name)
            armor: dict = self.equipment.armors[armor_index]
            return Armor(id=armor['id'],
                          name=armor['name'],
                          defence=armor['defence'],
                          stamina_per_turn=armor['stamina_per_turn'])
        except ValueError:
            print('ValueError')

    def get_weapons_names(self) -> list:
        # TODO возвращаем список с оружием
        try:
            weapon_list: list = []
            for weapon in self.equipment.weapons:
                weapon_list.append(weapon.name)
            return weapon_list
        except ValueError:
            print('ValueError')

    def get_armors_names(self) -> list:
        # TODO возвращаем список с броней
        try:
            armor_list: list = []
            for armor in self.equipment.armors:
                armor_list.append(armor.name)
            return armor_list
        except ValueError:
            print('ValueError')

    @staticmethod
    def _get_equipment_data() -> EquipmentData:
        # TODO этот метод загружает json в переменную EquipmentData
        with open("./data/equipment.json") as equipment_file:
            data = json.load(equipment_file)

        equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
        try:
            return equipment_schema().load(data)
        except marshmallow.exceptions.ValidationError:
            raise ValueError
