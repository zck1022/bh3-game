import sys

from character import Character
import random


class Effect:
    def __init__(self, name=None, normal=0, element=0, hard=0,
                 up_hp=0, up_atk=0,
                 dizzy=False, chaos=False, first_hand=False, vulnerability=0):
        self.name = name
        self.changed = False

        self.normal = []  # 普攻伤害
        self.element = []  # 元素伤害
        # self.hard = []  # 硬伤害

        self.up_hp = up_hp
        self.up_atk = up_atk

        self.dizzy = dizzy
        self.chaos = chaos
        self.first_hand = first_hand
        self.vulnerability = vulnerability

        self.cont_effect: list[ContEffect] = []


class ContEffect:
    def __init__(self, name=None, times=0, normal=0, element=0, hard=0,
                 refresh=False):
        self.name = name
        self.times = times
        self.normal = normal
        self.element = element
        self.hard = hard
        self.refresh = refresh


class Battle:
    def __init__(self, character1: Character, character2: Character):
        self.character1: Character = character1
        self.character2: Character = character2
        self.first_hand = None
        self.round_num = 0

    def run(self):
        while True:
            self.one_round()

    def judge_first(self) -> tuple[Character, Character]:
        """
        判断先后手
        :return: (先手, 后手)
        """
        first = self.first_hand
        self.first_hand = None
        if first is None:
            if self.character1.speed.current() > self.character2.speed.current():
                return self.character1, self.character2
            elif self.character1.speed.current() < self.character2.speed.current():
                return self.character2, self.character1
        if first is None or first == "roll":
            if random.randint(0, 1) == 0:
                return self.character1, self.character2
            else:
                return self.character2, self.character1
        second = self.character1
        if first == self.character1:
            second = self.character2
        return first, second

    def one_round(self):
        self.round_num += 1
        print("=======当前回合： [{}]=============".format(self.round_num))

        first, second = self.judge_first()
        print("先手: [{}], 后手：[{}]".format(first.name, second.name))

        # 回合开始
        first.HP.round_begin()
        second.HP.round_begin()
        # 进行跨回合增益伤害结算
        self.cont_effect_handle(first)
        self.cont_effect_handle(second)
        # 触发回合开始被动
        self.effect_handle(first.passive.before_round(first, second), first, second)
        self.effect_handle(second.passive.before_round(second, first), second, first)

        self.effect_handle(first.passive.before_atk(first, second), first, second)

        self.effect_handle(first.active.hit(first, second), first, second)

        self.effect_handle(first.passive.after_atk(first, second), first, second)
        # second.passive.on_atk()

        self.effect_handle(second.passive.before_atk(second, first), second, first)
        self.effect_handle(second.active.hit(second, first), second, first)

        self.effect_handle(second.passive.after_atk(second, first), second, first)

    # def one_hit(self, attacker: Character, defender: Character):
    #     res = attacker.active.hit(attacker)

    def cont_effect_handle(self, character: Character):
        if len(character.status.cont_effect) == 0:
            return
        for current_cont_effect in character.status.cont_effect:
            current_cont_effect.times -= 1
            character.HP.base -= current_cont_effect.hard
            print("[{}]状态导致[{}]减少[{}]血量".format(current_cont_effect.name, character.name,
                                                        current_cont_effect.hard))
            if character.HP.current() <= 0:
                print("[{}]太逊了,输了".format(character.name))
                sys.exit(0)

        character.status.cont_effect = [current_cont_effect for current_cont_effect in character.status.cont_effect
                                        if current_cont_effect.times != 0]

    def effect_handle(self, effects, attacker, defender):
        if effects is not None:
            self.character_with_effect(attacker, effects[0])
            self.character_with_effect(defender, effects[1])

    def character_with_effect(self, character: Character, effect: Effect):
        if not effect.changed:
            return
        print("[{}]对[{}]造成效果".format(effect.name, character.name))
        if len(effect.normal) != 0:
            effect_sum = sum(map(lambda val: val - character.DEF.current() if val - character.DEF.current() > 0 else 0,
                                 effect.normal))
            character.HP.base -= effect_sum
            print("普通攻击伤害 [{}]".format(effect_sum))
        if len(effect.element) != 0:
            effect_sum = sum(effect.element)
            character.HP.base -= effect_sum
            print("元素攻击伤害 [{}]".format(effect_sum))
        if effect.up_hp != 0:
            character.HP.base += effect.up_hp
            print("回血 [{}]".format(effect.up_hp))
        if effect.up_atk != 0:
            character.ATK.base += effect.up_atk
            print("提升攻击力 [{}]".format(effect.up_atk))

        if effect.dizzy:
            character.status.dizzy = True
            print("眩晕")
        if effect.chaos:
            character.status.chaos = True
            print("混乱")
        if effect.first_hand:
            self.first_hand = character
            print("下回合先手")
        if len(effect.cont_effect) != 0:
            for new_cont_effect in effect.cont_effect:
                has_in = False
                for current_cont_effect in character.status.cont_effect:
                    if new_cont_effect.name == current_cont_effect.name:
                        has_in = True
                        if new_cont_effect.refresh:
                            current_cont_effect.times = new_cont_effect.times
                            print("更新效果[{}]".format(new_cont_effect.name))
                            break
                if not has_in:
                    character.status.cont_effect.append(new_cont_effect)
                    print("得到效果[{}]".format(new_cont_effect.name))

        if character.HP.current() <= 0:
            print("[{}]太逊了,输了".format(character.name))
            sys.exit(0)
        else:
            print("[{}]剩余血量[{}]".format(character.name, character.HP.current()))
