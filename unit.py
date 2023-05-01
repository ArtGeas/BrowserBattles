from __future__ import annotations
from abc import ABC, abstractmethod
from equipment import Equipment, Weapon, Armor
from classes import UnitClass
from random import randint
from typing import Optional


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """
    def __init__(self, name: str, unit_class: UnitClass):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon = None
        self.armor = None
        self._is_skill_used = False

    @property
    def health_points(self):
        return round(self.hp, 1) # TODO возвращаем аттрибут hp в красивом виде

    @property
    def stamina_points(self):
        return round(self.stamina, 1)  # TODO возвращаем аттрибут hp в красивом виде

    def equip_weapon(self, weapon: Weapon):
        # TODO присваиваем нашему герою новое оружие
        self.weapon = weapon
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor):
        # TODO одеваем новую броню
        self.armor = armor
        return f"{self.name} экипирован броней {self.armor.name}"

    def _count_damage(self, target: BaseUnit) -> int:
        # TODO Эта функция должна содержать:
        #  логику расчета урона игрока
        #  логику расчета брони цели
        #  здесь же происходит уменьшение выносливости атакующего при ударе
        #  и уменьшение выносливости защищающегося при использовании брони
        #  если у защищающегося нехватает выносливости - его броня игнорируется
        #  после всех расчетов цель получает урон - target.get_damage(damage)
        #  и возвращаем предполагаемый урон для последующего вывода пользователю в текстовом виде

        attack_damage = self.weapon.damage * self.unit_class.attack

        if target.stamina >= target.armor.stamina_per_turn:
            target.stamina = target.stamina - target.armor.stamina_per_turn
            target_armor = target.armor.defence * target.unit_class.armor
        else:
            target_armor = 0

        self.stamina = self.stamina - self.weapon.stamina_per_hit
        damage = attack_damage - target_armor

        return damage

    def get_damage(self, damage: int) -> Optional[int]:
        # TODO получение урона целью
        #      присваиваем новое значение для аттрибута self.hp
        self.hp = self.hp - damage
        return damage

    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        """
        этот метод будет переопределен ниже
        """
        pass

    def use_skill(self, target: BaseUnit) -> str:
        """
        метод использования умения.
        если умение уже использовано возвращаем строку
        Навык использован
        Если же умение не использовано тогда выполняем функцию
        self.unit_class.skill.use(user=self, target=target)
        и уже эта функция вернет нам строку которая характеризует выполнение умения
        """
        if self._is_skill_used:
            return 'Навык использован.'
        else:
            result = self.unit_class.skill.use(user=self, target=target)
            self._is_skill_used = True
            return result


class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        функция удар игрока:
        здесь происходит проверка достаточно ли выносливости для нанесения удара.
        вызывается функция self._count_damage(target)
        а также возвращается результат в виде строки
        """

        # TODO результат функции должен возвращать следующие строки:

        if self.stamina >= self.weapon.stamina_per_hit:
            damage = self._count_damage(target)
            if damage > target.armor.defence * target.unit_class.armor:
                return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит {damage} урона."
            else:
                return f"{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} cоперника его останавливает."
        else:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."


class EnemyUnit(BaseUnit):

    def _hit_checkout(self, target: BaseUnit) -> str:

        if self.stamina >= self.weapon.stamina_per_hit:
            damage = self._count_damage(target)
            if damage > target.armor.defence * target.unit_class.armor:
                return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} и наносит Вам {damage} урона."
            else:
                return f"{self.name} используя {self.weapon.name} наносит удар, но Ваш(а) {target.armor.name} его останавливает."
        else:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

    def hit(self, target: BaseUnit) -> str:
        """
        функция удар соперника
        должна содержать логику применения соперником умения
        (он должен делать это автоматически и только 1 раз за бой).
        Например, для этих целей можно использовать функцию randint из библиотеки random.
        Если умение не применено, противник наносит простой удар, где также используется
        функция _count_damage(target)
        """
        # TODO результат функции должен возвращать результат функции skill.use или же следующие строки:

        using_skill = bool(randint(0, 1))
        if using_skill:
            if not self._is_skill_used:
                self._is_skill_used = True
                return self.unit_class.skill.use(user=self, target=target)
            else:
                return self._hit_checkout(target)
        else:
            return self._hit_checkout(target)
