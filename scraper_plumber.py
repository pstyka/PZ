import csv

# Ścieżki do plików wejściowego i wyjściowego
input_file = 'substituents.csv'
output_file = 'substituents1.csv'

# Otwieranie pliku wejściowego i wyjściowego
with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
    # Czytanie danych z pliku wejściowego z użyciem średnika jako separatora
    reader = csv.reader(infile, delimiter=';')

    # Tworzenie obiektu zapisującego dane do pliku wyjściowego z użyciem przecinka jako separatora
    writer = csv.writer(outfile, delimiter=',')

    # Przepisywanie wierszy z pliku wejściowego do wyjściowego
    for row in reader:
        writer.writerow(row)

print(f"Plik został zapisany jako {output_file} z przecinkami jako separatorami.")
