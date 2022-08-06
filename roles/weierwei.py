import random

from battle import Effect
from character import Character
from skill import Active, Passive


class CharacterActive(Active):
    def __init__(self):
        super(CharacterActive, self).__init__("创（造）力", 3)

    def skill(self, my: Character, enemy: Character) -> tuple[Effect, Effect]:
        my_effect = Effect(self.name)
        enemy_effect = Effect(self.name)
        print("触发主动技能: [{}]".format(self.name))
        if my.status.chaos:
            print("自己打自己")
            my_effect.changed = True
            my_effect.normal.append(my.ATK.current())
            my_effect.chaos = True
        else:
            enemy_effect.changed = True
            enemy_effect.normal.append(my.ATK.current())
            enemy_effect.chaos = True

        return my_effect, enemy_effect


class CharacterPassive(Passive):
    def __init__(self):
        super(CharacterPassive, self).__init__("大变活人")
        self.has_up_atk = False

    def before_round(self, my: Character, enemy: Character) -> tuple[Effect, Effect]:
        my_effect = Effect(self.name)
        enemy_effect = Effect(self.name)
        if my.HP.round_begin_hp < 31 and not self.has_up_atk:
            self.has_up_atk = True
            my_effect.changed = True
            enemy_effect.changed = True
            print("触发被动技能: [{}]".format(self.name))
            my_effect.up_hp = random.randint(10, 20)
            enemy_effect.up_hp = random.randint(10, 20)
            print("自己回血[{}], 对手回血[{}]".format(my_effect.up_hp, enemy_effect.up_hp))

            my_effect.up_atk = random.randint(2, 15)
            print("自己加攻击力[{}]".format(my_effect.up_atk))
        return my_effect, enemy_effect


class Weierwei(Character):
    def __init__(self):
        super(Weierwei, self).__init__("维尔薇", 100, 20, 12, 25, CharacterActive(), CharacterPassive())


if __name__ == '__main__':
    char = Weierwei()
    print(char)
    char.active.hit(None, None)
    char.active.hit(None, None)
    char.active.hit(None, None)
    char.active.hit(None, None)
