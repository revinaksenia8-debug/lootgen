#!/usr/bin/env python3
"""
LootGen - Генератор игрового лута
"""

import random
import os
import sys
import time
from typing import List
from dataclasses import dataclass
from enum import Enum

# ======================== ЦВЕТА ДЛЯ КОНСОЛИ ========================

class Colors:
    """Цвета для красивого вывода"""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    PURPLE = "\033[95m"

# ======================== КЛАССЫ ДАННЫХ ========================

class Rarity(Enum):
    """Редкость предметов"""
    COMMON = ("Обычный", 1, Colors.GREEN)
    RARE = ("Редкий", 2, Colors.BLUE)
    EPIC = ("Эпический", 3, Colors.YELLOW)
    LEGENDARY = ("Легендарный", 5, Colors.RED)

    def __init__(self, name, multiplier, color):
        self.ru_name = name
        self.multiplier = multiplier
        self.color = color

@dataclass
class LootItem:
    """Предмет лута"""
    name: str
    rarity: Rarity
    gold: int
    power: int
    
    def get_colored_name(self) -> str:
        """Цветное имя"""
        return f"{self.rarity.color}{self.name}{Colors.RESET}"

# ======================== ГЕНЕРАТОР ========================

class LootGenerator:
    """Генератор лута"""
    
    def __init__(self):
        self.inventory: List[LootItem] = []
        self.total_gold = 0
        self.chests_opened = 0
        random.seed(int(time.time()))
    
    def clear_screen(self):
        """Очистка экрана"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_title(self):
        """Показывает заголовок"""
        title = f"""
{Colors.PURPLE}╔══════════════════════════════════════════════════╗
║{Colors.RESET}{Colors.BOLD}{Colors.YELLOW}              L O O T   G E N                      {Colors.PURPLE}║
╚══════════════════════════════════════════════════╝{Colors.RESET}
{Colors.CYAN}         Генератор лута для настоящих героев        {Colors.RESET}
        """
        print(title)
    
    def generate_item(self) -> LootItem:
        """Генерирует случайный предмет"""
        # Шансы: 50% обычный, 30% редкий, 15% эпический, 5% легендарный
        roll = random.random()
        if roll < 0.5:
            rarity = Rarity.COMMON
        elif roll < 0.8:
            rarity = Rarity.RARE
        elif roll < 0.95:
            rarity = Rarity.EPIC
        else:
            rarity = Rarity.LEGENDARY
        
        # Имена предметов
        prefixes = ["Древний", "Зачарованный", "Пылающий", "Ледяной", "Темный"]
        suffixes = ["меч", "щит", "шлем", "кольцо", "амулет", "посох", "лук"]
        
        name = f"{random.choice(prefixes)} {random.choice(suffixes)}"
        gold = random.randint(50, 200) * rarity.multiplier
        power = random.randint(10, 50) * rarity.multiplier
        
        return LootItem(name, rarity, gold, power)
    
    def open_chest(self, count: int = 1) -> List[LootItem]:
        """Открывает сундуки"""
        print(f"\n{Colors.CYAN}🎁 Открываем {count} сундук(ов)...{Colors.RESET}")
        
        new_items = []
        for i in range(count):
            print(f"  Сундук {i+1}/{count}... ", end="", flush=True)
            time.sleep(0.2)
            item = self.generate_item()
            new_items.append(item)
            self.inventory.append(item)
            self.total_gold += item.gold
            print(f"{Colors.GREEN}✓{Colors.RESET} {item.get_colored_name()}")
        
        self.chests_opened += count
        return new_items
    
    def show_inventory(self):
        """Показывает инвентарь"""
        self.clear_screen()
        self.show_title()
        
        if not self.inventory:
            print(f"\n{Colors.YELLOW}📭 Инвентарь пуст! Откройте сундуки!{Colors.RESET}")
            return
        
        print(f"\n{Colors.BOLD}{Colors.PURPLE}═══════════════════════════════════════════{Colors.RESET}")
        print(f"{Colors.BOLD}              ИНВЕНТАРЬ                {Colors.RESET}")
        print(f"{Colors.PURPLE}═══════════════════════════════════════════{Colors.RESET}")
        print(f"{'№':<3} {'ПРЕДМЕТ':<20} {'РЕДКОСТЬ':<12} {'ЗОЛОТО':<8} {'СИЛА':<5}")
        print(f"{Colors.PURPLE}───────────────────────────────────────────{Colors.RESET}")
        
        for i, item in enumerate(self.inventory[-20:], 1):
            print(f"{i:<3} {item.name:<20} {item.rarity.color}{item.rarity.ru_name:<12}{Colors.RESET} {item.gold:<8} {item.power:<5}")
        
        print(f"{Colors.PURPLE}═══════════════════════════════════════════{Colors.RESET}")
        print(f"{Colors.BOLD}Всего предметов: {len(self.inventory)} | Золото: {self.total_gold}{Colors.RESET}")
    
    def show_stats(self):
        """Показывает статистику"""
        self.clear_screen()
        self.show_title()
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}📊 СТАТИСТИКА{Colors.RESET}")
        print(f"{Colors.CYAN}────────────────────────{Colors.RESET}")
        print(f"Открыто сундуков: {self.chests_opened}")
        print(f"Найдено предметов: {len(self.inventory)}")
        print(f"Всего золота: {self.total_gold}")
        
        if self.inventory:
            legendary = sum(1 for i in self.inventory if i.rarity == Rarity.LEGENDARY)
            epic = sum(1 for i in self.inventory if i.rarity == Rarity.EPIC)
            rare = sum(1 for i in self.inventory if i.rarity == Rarity.RARE)
            common = sum(1 for i in self.inventory if i.rarity == Rarity.COMMON)
            
            print(f"\n{Colors.BOLD}По редкости:{Colors.RESET}")
            print(f"{Colors.GREEN}Обычных: {common}{Colors.RESET}")
            print(f"{Colors.BLUE}Редких: {rare}{Colors.RESET}")
            print(f"{Colors.YELLOW}Эпических: {epic}{Colors.RESET}")
            print(f"{Colors.RED}Легендарных: {legendary}{Colors.RESET}")

# ======================== ГЛАВНАЯ ФУНКЦИЯ ========================

def main():
    """Точка входа"""
    generator = LootGenerator()
    
    while True:
        generator.clear_screen()
        generator.show_title()
        
        print(f"\n{Colors.BOLD}МЕНЮ:{Colors.RESET}")
        print(f"{Colors.GREEN}[1]{Colors.RESET} 🎁 Открыть 1 сундук")
        print(f"{Colors.GREEN}[2]{Colors.RESET} 📦 Открыть 5 сундуков")
        print(f"{Colors.GREEN}[3]{Colors.RESET} 🎰 Открыть 10 сундуков")
        print(f"{Colors.BLUE}[4]{Colors.RESET} 🎒 Инвентарь")
        print(f"{Colors.BLUE}[5]{Colors.RESET} 📊 Статистика")
        print(f"{Colors.RED}[0]{Colors.RESET} 🚪 Выход")
        
        choice = input(f"\n{Colors.BOLD}👉 Выберите действие: {Colors.RESET}").strip()
        
        if choice == "1":
            generator.open_chest(1)
            input(f"\n{Colors.GREEN}Нажмите Enter...{Colors.RESET}")
        elif choice == "2":
            generator.open_chest(5)
            input(f"\n{Colors.GREEN}Нажмите Enter...{Colors.RESET}")
        elif choice == "3":
            generator.open_chest(10)
            input(f"\n{Colors.GREEN}Нажмите Enter...{Colors.RESET}")
        elif choice == "4":
            generator.show_inventory()
            input(f"\n{Colors.GREEN}Нажмите Enter...{Colors.RESET}")
        elif choice == "5":
            generator.show_stats()
            input(f"\n{Colors.GREEN}Нажмите Enter...{Colors.RESET}")
        elif choice == "0":
            print(f"\n{Colors.PURPLE}Спасибо за игру! До свидания!{Colors.RESET}")
            break
        else:
            print(f"\n{Colors.RED}Неверный выбор!{Colors.RESET}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Пока!{Colors.RESET}")
        sys.exit(0)
