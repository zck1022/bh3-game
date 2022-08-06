import random

from character import Character
from skill import Active, Passive
from battle import Effect, ContEffect


class CharacterActive(Active):
    def __init__(self):
        super(CharacterActive, self).__init__("邪渊之钩", 2)

    def skill(self, my: Character, enemy: Character) -> tuple[Effect, Effect]:
        my_effect = Effect(self.name)
        enemy_effect = Effect(self.name)
        print("触发主动技能: [{}]".format(self.name))

        enemy_effect.changed = True
        enemy_effect.normal = [random.randint(11, 22) for _ in range(4)]

        for effect in enemy.status.cont_effect:
            if "撕裂" in effect.name:
                enemy_effect.element = [3, 3, 3, 3]
                break

        return my_effect, enemy_effect


class CharacterPassive(Passive):
    def __init__(self):
        super(CharacterPassive, self).__init__("不归之爪")

    def after_atk(self, my: Character, enemy: Character) -> tuple[Effect, Effect]:
        my_effect = Effect(self.name)
        enemy_effect = Effect(self.name)
        if random.random() < 0.15:
            print("触发被动技能: [{}]".format(self.name))
            if my.status.chaos:
                my_effect.changed = True
                my_effect.cont_effect.append(ContEffect(name="{}->撕裂".format(self.name),
                                                        times=3, hard=4, refresh=True))
                print("自身处于[混乱]状态, 自身陷入[撕裂]状态")
            else:
                enemy_effect.changed = True
                enemy_effect.cont_effect.append(ContEffect(name="{}->撕裂".format(self.name),
                                                           times=3, hard=4, refresh=True))
                print("对敌人施加[撕裂]状态")
        return my_effect, enemy_effect


class Kesimo(Character):
    def __init__(self):
        super(Kesimo, self).__init__("科斯魔", 100, 19, 11, 19, CharacterActive(), CharacterPassive())
