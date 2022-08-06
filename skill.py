from battle import Effect
from character import Character


class Active:
    def __init__(self, name, times):
        self.name = name
        self.times = times
        self.leave_times = self.times

    def hit(self, my: Character, enemy: Character) -> tuple[Effect, Effect]:
        self.leave_times -= 1
        if self.leave_times == 0:
            print("[{}]发动主动技能: [{}]".format(my.name, self.name))
            self.leave_times = self.times
            return self.skill(my, enemy)
        else:
            print("[{}]发动普通攻击".format(my.name))
            return self.common(my)

    def common(self, my: Character) -> tuple[Effect, Effect]:
        my_effect = Effect("普通攻击")
        enemy_effect = Effect("普通攻击")
        if my.status.chaos:
            my_effect.changed = True
            my_effect.normal.append(my.ATK.current())
            my.status.chaos = False
        else:
            enemy_effect.changed = True
            enemy_effect.normal.append(my.ATK.current())
        return my_effect, enemy_effect

    def skill(self, my: Character, enemy: Character) -> tuple[Effect, Effect]:
        pass

    def sleep(self):
        self.leave_times -= 1
        if self.leave_times == 0:
            self.leave_times = self.times
            print("哈哈，被晕了，放不出技能")


class Passive:
    def __init__(self, name):
        self.name = name

    def before_round(self, my: Character, enemy: Character) -> tuple[Effect, Effect]:
        """
        回合开始时的被动效果
        :param my: 自己的实例
        :param emeny: 敌人的实例
        :return: (对自己造成的效果, 对敌人造成的效果)
        """
        pass

    def before_atk(self, my: Character, enemy: Character) -> tuple[Effect, Effect]:
        pass

    def on_atk(self, my: Character, enemy: Character) -> tuple[Effect, Effect]:
        pass

    def after_atk(self, my: Character, enemy: Character) -> tuple[Effect, Effect]:
        pass

    def after_round(self, my: Character, enemy: Character) -> tuple[Effect, Effect]:
        pass
