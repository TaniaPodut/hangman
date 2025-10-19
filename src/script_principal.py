#!/usr/bin/env python3
"""
Script principal pentru Rezolvatorul Spânzurătoare
"""
import csv
import argparse
import sys
from pathlib import Path
from rezolvator_spanzuratoare import incarca_dictionar, rezolva_joc_procedural

def citeste_csv_intrare(cale: str):
	"""Citește fișierul CSV de intrare"""
	jocuri = []
	with open(cale, 'r', encoding='utf-8') as f:
		for idx, linie in enumerate(f, 1):
			linie = linie.strip()
			if not linie or linie.startswith('game_id'):
				continue
			parti = linie.split(';')
			if len(parti) == 3:
				id_joc, tipar, tinta = parti
			elif len(parti) == 2:
				tipar, tinta = parti
				id_joc = str(idx)
			else:
				continue
			tipar = tipar.strip()
			tinta = tinta.strip()
			# Validare
			if len(tipar) != len(tinta):
				print(f"⚠️  Joc {id_joc}: lungimi diferite")
				continue
			jocuri.append({
				'game_id': id_joc,
				'pattern': tipar,
				'target': tinta
			})
	return jocuri

def scrie_csv_rezultate(rezultate: list, cale: str):
	"""Scrie rezultatele în CSV"""
	Path(cale).parent.mkdir(parents=True, exist_ok=True)
	with open(cale, 'w', encoding='utf-8', newline='') as f:
		writer = csv.DictWriter(
			f,
			fieldnames=['game_id', 'incercari', 'cuvant', 'status', 'secventa']
		)
		writer.writeheader()
		writer.writerows(rezultate)
	print(f"✅ Rezultate salvate: {cale}")

def main():
	parser = argparse.ArgumentParser(description='Rezolvator Spânzurătoare')
	parser.add_argument('--input', help='Fișier CSV de intrare')
	parser.add_argument('--output', default='results/output.csv', help='Fișier CSV de ieșire')
	parser.add_argument('--dict', default='data/resource.txt', help='Dicționar')
	parser.add_argument('--generate-dict', action='store_true', help='Generează dicționar')
	parser.add_argument('--verbose', action='store_true', help='Mod detaliat')

	args = parser.parse_args()

	# Generare dicționar
	if args.generate_dict:
		print("Funcția de generare dicționar nu mai este disponibilă. Folosiți un fișier existent.")
		return

	# Verificare parametri
	if not args.input:
		print("❌ Eroare: --input este obligatoriu")
		parser.print_help()
		sys.exit(1)

	# Încărcare dicționar
	print(f"📖 Încărcare dicționar: {args.dict}")
	dictionar = incarca_dictionar(args.dict)

	# Citire input
	print(f"📥 Citire fișier de intrare: {args.input}")
	jocuri = citeste_csv_intrare(args.input)
	print(f"   Total jocuri: {len(jocuri)}")

	# Rezolvare
	rezultate = []
	total_incercari = 0
	corecte = 0

	for i, joc in enumerate(jocuri, 1):
		if args.verbose:
			print(f"\n🎮 Joc {i}/{len(jocuri)} - ID: {joc['game_id']}")
			print(f"   Tipar: {joc['pattern']}")

		rezultat = rezolva_joc_procedural(dictionar, joc['pattern'], joc['target'])

		status = 'OK' if rezultat['succes'] else 'FAIL'
		if rezultat['succes']:
			corecte += 1

		total_incercari += rezultat['incercari']

		rezultate.append({
			'game_id': joc['game_id'],
			'incercari': rezultat['incercari'],
			'cuvant': rezultat['cuvant'],
			'status': status,
			'secventa': ' '.join(rezultat['secventa'])
		})

		# Printează cuvântul găsit și numărul de încercări pentru fiecare joc
		print(f"Joc {joc['game_id']}: cuvânt găsit = {rezultat['cuvant']} | încercări = {rezultat['incercari']} | status = {status}")

	# Scriere output
	scrie_csv_rezultate(rezultate, args.output)

	# Statistici
	print(f"\n📊 STATISTICI:")
	print(f"   Total jocuri: {len(jocuri)}")
	print(f"   Corecte: {corecte}/{len(jocuri)} ({100*corecte/len(jocuri):.1f}%)")
	print(f"   Total încercări: {total_incercari}")
	print(f"   Medie încercări: {total_incercari/len(jocuri):.1f}")

	if total_incercari < 1200:
		print(f"   ✅ PERFORMANȚĂ ATINSĂ (<1200)")
	else:
		print(f"   ❌ Peste țintă (≥1200)")

if __name__ == '__main__':
	main()
