from dataclasses import dataclass
from skills import Skill, FuryPunch, HardShot


@dataclass
class UnitClass:
    name: str
    max_health: float
    max_stamina: float
    attack: float
    stamina: float
    armor: float
    skill: Skill


WarriorClass = UnitClass() # TODO Инициализируем экземпляр класса UnitClass и присваиваем ему необходимые значения аттрибуотов

ThiefClass = UnitClass() # TODO действуем так же как и с войном

unit_classes = {
    ThiefClass.name: ThiefClass,
    WarriorClass.name: WarriorClass
}
