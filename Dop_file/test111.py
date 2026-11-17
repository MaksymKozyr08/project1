import time
import keyboard

INTERVAL_SECONDS = 25

def wait_for_space_or_timeout(timeout: int) -> bool:
    """
    Чекає натискання пробілу протягом заданого часу (timeout).
    Повертає True, якщо пробіл натиснуто, або False після вичерпання часу.
    """
    start_time = time.time()
    
    # Очищаємо залишковий стан клавіші перед початком очікування
    while keyboard.is_pressed("space"):
        time.sleep(0.01)

    while time.time() - start_time < timeout:
        if keyboard.is_pressed("space"):
            # Очікуємо відпускання, щоб не ловити подвійне натискання
            while keyboard.is_pressed("space"):
                time.sleep(0.01)
            return True
        time.sleep(0.05)  # Зниження навантаження на процесор
        
    return False

def main():
    print(f"Скрипт запущено. Цикли очікування по {INTERVAL_SECONDS} секунд.")
    print("Натисніть Ctrl+C у терміналі для виходу.\n")
    
    round_number = 1
    try:
        while True:
            print(f"[Раунд {round_number}] Очікування пробілу протягом {INTERVAL_SECONDS} с...")
            pressed = wait_for_space_or_timeout(INTERVAL_SECONDS)
            
            if pressed:
                print(f" -> Пробіл натиснуто вчасно!\n")
            else:
                print(f" -> Час вичерпано (пробіл не натиснуто).\n")
                
            round_number += 1
            
    except KeyboardInterrupt:
        print("\nРоботу скрипта зупинено користувачем.")

if __name__ == "__main__":
    main()