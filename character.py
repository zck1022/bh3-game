class HP:
    def __init__(self, base):
        self.base = base
        self.offset = 0

        self.round_begin_hp = base

    def current(self):
        return self.base + self.offset

    def round_begin(self):
        self.round_begin_hp = self.current()


class ATK:
    def __init__(self, base):
        self.base = base
        self.offset = 0

    def current(self):
        return self.base + self.offset


class DEF:
    def __init__(self, base):
        self.base = base
        self.offset = 0

    def current(self):
        return self.base + self.offset

    def __int__(self):
        return self.current()

    def __str__(self):
        return str(self.current())


class Speed:
    def __init__(self, base):
        self.base = base
        self.offset = 0

    def current(self):
        return self.base + self.offset


class Status:
    def __init__(self):
        self.dizzy = False
        self.chaos = False
        self.cont_effect = []

    def __str__(self):
        status = []
        if self.dizzy is True:
            status.append("眩晕")
        if self.chaos is True:
            status.append("混乱")
        for effect in self.cont_effect:
            status.append(effect.name)
        return status.__str__()


class Character:
    def __init__(self, name, hp, attack, defend, speed, active, passive):
        self.name = name

        self.HP = HP(hp)
        self.ATK = ATK(attack)
        self.DEF = DEF(defend)
        self.speed = Speed(speed)

        self.active = active
        self.passive = passive

        self.status = Status()

    def __str__(self):
        return "{0}\n" \
               "生命 {1:<5d} 攻击 {2:<5d}\n" \
               "防御 {3:<5d} 速度 {4:<5d}\n" \
               "状态 {5}".format(self.name,
                                 self.HP.current(), self.ATK.current(), self.DEF.current(), self.speed.current(),
                                 self.status.__str__())
