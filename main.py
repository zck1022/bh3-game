from roles.kesimo import Kesimo
from roles.weierwei import Weierwei
from battle import Battle

if __name__ == '__main__':
    Battle(Kesimo(), Weierwei()).run()
