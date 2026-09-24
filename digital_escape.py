from typing import List, Dict

class Room:
    def __init__(self, name: str, description: str, item: str):
        self.name = name
        self.description = description
        self.item = item
        self.next_rooms: List[str] = []

class Player:
    def __init__(self, name: str):
        self.name = name
        self.lives: int = 3
        self.inventory: List[str] = []
        self.current_room: str = "комната управления"

class Game:
    def __init__(self):
        self.rooms: Dict[str, Room] = {}
        self.create_world()
        self.player = None

    def create_world(self):
        r1 = Room("комната управления", "На столе лежит КАРТА.", "карта")
        r2 = Room("серверная", "Загадка: сколько будет 15 + 27?", "ключ")
        r3 = Room("лаборатория", "Напиши слово 'выход' наоборот.", "код выхода")
        r1.next_rooms = ["серверная"]
        r2.next_rooms = ["лаборатория"]
        r3.next_rooms = ["главная дверь"]
        self.rooms = {
            r1.name: r1,
            r2.name: r2,
            r3.name: r3,
            "главная дверь": Room("главная дверь", "Финал!", "")
        }

    def start(self):
        name = input("Как тебя зовут? ")
        self.player = Player(name)
        print(f"Привет, {name}! Жизней: {self.player.lives}")
        while self.player.lives > 0:
            self.show_room()
            cmd = input("> ").lower()
            if cmd == "осмотреться":
                room = self.rooms[self.player.current_room]
                if room.item and room.item not in self.player.inventory:
                    self.player.inventory.append(room.item)
                    print(f"Нашел: {room.item}")
            elif cmd == "инвентарь":
                print(f"Инвентарь: {self.player.inventory}")
            elif cmd == "перейти":
                print(f"Можно в: {self.rooms[self.player.current_room].next_rooms}")
                where = input("Куда? ").lower()
                if where in self.rooms[self.player.current_room].next_rooms:
                    self.player.current_room = where
                    print(f"Перешел в {where}")
                    if where == "главная дверь":
                        print("🏆 ПОБЕДА!")
                        break
                else:
                    print("Туда нельзя!")
                    self.player.lives -= 1
            print(f"Жизней осталось: {self.player.lives}")

    def show_room(self):
        room = self.rooms[self.player.current_room]
        print(f"\n--- {room.name.upper()} ---")
        print(room.description)

if __name__ == "__main__":
    game = Game()
    game.start()
