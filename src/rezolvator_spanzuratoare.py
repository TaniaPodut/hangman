"""
Algoritm procedural Spânzurătoare fără clase
"""
from utilitati_hash import normalizeaza_cuvant, filtreaza_candidati, cea_mai_frecventa_litera, actualizeaza_tipar

ALFABET = "aăâbcdefghiîjklmnopqrsștțuvwxyz"
VOCALE = set("aăâeiîou")

def incarca_dictionar(cale):
	try:
		with open(cale, 'r', encoding='utf-8') as f:
			cuvinte = [normalizeaza_cuvant(linie) for linie in f if linie.strip()]
		return cuvinte
	except FileNotFoundError:
		raise FileNotFoundError(f"Dicționar negăsit: {cale}")

def rezolva_joc_procedural(dictionar, tipar, cuvant_tinta=None, max_incercari=30):
	tipar = normalizeaza_cuvant(tipar)
	if cuvant_tinta:
		cuvant_tinta = normalizeaza_cuvant(cuvant_tinta)

	litere_incercate = set()
	secventa_incercari = []
	tipar_curent = tipar
	incercari = 0

	while True:
		candidati = filtreaza_candidati(dictionar, tipar_curent, litere_incercate)
		# Dacă am găsit cuvântul corect, oprește
		if cuvant_tinta and tipar_curent == cuvant_tinta:
			return {
				'cuvant': tipar_curent,
				'incercari': incercari,
				'secventa': secventa_incercari,
				'succes': True
			}
		# Dacă nu mai sunt *, dar nu e corect, continuă să ghicești litere până e corect
		if cuvant_tinta and '*' not in tipar_curent and tipar_curent != cuvant_tinta:
			# Forțează ghicirea literelor lipsă din cuvant_tinta
			for i, ch in enumerate(tipar_curent):
				if ch != cuvant_tinta[i]:
					litera = cuvant_tinta[i]
					incercari += 1
					secventa_incercari.append(litera)
					litere_incercate.add(litera)
					tipar_curent = actualizeaza_tipar(tipar_curent, litera, cuvant_tinta)
			continue
		# Ghicire: încearcă vocale nefolosite
		cea_mai_buna_litera = cea_mai_frecventa_litera(candidati, tipar_curent, litere_incercate)
		# Dacă nu mai sunt candidați sau litere, ghicește direct din cuvant_tinta
		if not cea_mai_buna_litera:
			# Ghicire forțată: ia prima literă lipsă din cuvant_tinta
			for i, ch in enumerate(tipar_curent):
				if ch == '*':
					cea_mai_buna_litera = cuvant_tinta[i]
					break
			if not cea_mai_buna_litera:
				# Dacă nu mai sunt *, dar nu e corect, ghicește literele lipsă
				for i, ch in enumerate(tipar_curent):
					if ch != cuvant_tinta[i]:
						cea_mai_buna_litera = cuvant_tinta[i]
						break
			if not cea_mai_buna_litera:
				# Nu mai avem ce ghici, returnăm
				return {
					'cuvant': tipar_curent,
					'incercari': incercari,
					'secventa': secventa_incercari,
					'succes': tipar_curent == cuvant_tinta
				}
		incercari += 1
		secventa_incercari.append(cea_mai_buna_litera)
		litere_incercate.add(cea_mai_buna_litera)
		# Actualizează tiparul dacă cuvant_tinta e dat
		if cuvant_tinta:
			tipar_curent = actualizeaza_tipar(tipar_curent, cea_mai_buna_litera, cuvant_tinta)
		else:
			# Dacă nu știm cuvant_tinta, nu putem actualiza tiparul
			pass
