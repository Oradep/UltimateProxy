import ipaddress
import os

input_file = 'blacklist.txt'
output_file = 'blacklist_mihomo.yaml'

def classify_and_format(line):
    # Убираем пробелы и символы переноса строки
    line = line.strip()
    
    # Пропускаем пустые строки и комментарии
    if not line or line.startswith('#'):
        return None
    
    try:
        # Проверяем, является ли строка IP-адресом или подсетью
        if '/' not in line:
            ip = ipaddress.ip_address(line)
            if isinstance(ip, ipaddress.IPv4Address):
                return f"  - 'IP-CIDR,{line}/32'"
            else:
                return f"  - 'IP-CIDR6,{line}/128'"
        else:
            net = ipaddress.ip_network(line, strict=False)
            if isinstance(net, ipaddress.IPv4Network):
                return f"  - 'IP-CIDR,{line}'"
            else:
                return f"  - 'IP-CIDR6,{line}'"
                
    except ValueError:
        # Если это не IP, значит это домен
        # Убираем лишние точки или *. в начале, если они там есть
        domain = line.lstrip('*.')
        return f"  - 'DOMAIN-SUFFIX,{domain}'"

def main():
    if not os.path.exists(input_file):
        print(f"❌ Ошибка: Файл {input_file} не найден в текущей папке!")
        return

    print("⏳ Начинаю обработку файла...")
    
    with open(input_file, 'r', encoding='utf-8') as f_in, \
         open(output_file, 'w', encoding='utf-8') as f_out:
        
        # Обязательный заголовок для Mihomo YAML
        f_out.write("payload:\n")
        
        count = 0
        for line in f_in:
            formatted_line = classify_and_format(line)
            if formatted_line:
                f_out.write(formatted_line + "\n")
                count += 1
                
    print(f"✅ Готово! Обработано записей: {count}")
    print(f"📁 Результат сохранен в файл: {output_file}")

if __name__ == '__main__':
    main()