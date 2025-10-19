"""
Modul pentru funcții hash și filtrare candidați
"""
import unicodedata
from typing import List, Set, Tuple
from collections import Counter

def normalizeaza_cuvant(cuvant: str) -> str:
	"""Normalizează cuvântul: Unicode NFKC + litere mici"""
	return unicodedata.normalize("NFKC", cuvant.strip()).casefold()

def calculeaza_hash(cuvant: str, tipar: str) -> Tuple:
	"""
	Calculează hash pentru cuvânt în raport cu tipar
	Returnează: tuplu (lungime, vector_potrivire) sau None
	"""
	if len(cuvant) != len(tipar):
		return None
	vector_potrivire = tuple(
		tipar[i] == '*' or tipar[i] == cuvant[i]
		for i in range(len(cuvant))
	)
	return (len(cuvant), vector_potrivire)

def potriveste_tipar(cuvant: str, tipar: str, litere_incercate: Set[str]) -> bool:
	"""Verifică dacă cuvântul se potrivește cu tiparul"""
	if len(cuvant) != len(tipar):
		return False
	# Verifică literele cunoscute
	for i, caracter in enumerate(tipar):
		if caracter != '*' and caracter != cuvant[i]:
			return False
	# Elimină cuvintele care conțin literele încercate pe alte poziții decât cele din tipar
	for i, litera in enumerate(cuvant):
		if tipar[i] == '*' and litera in litere_incercate:
			return False
	return True

def filtreaza_candidati(
	dictionar: List[str],
	tipar: str,
	litere_incercate: Set[str]
) -> List[str]:
	"""Filtrează candidații valizi"""
	return [
		cuvant for cuvant in dictionar
		if potriveste_tipar(cuvant, tipar, litere_incercate)
	]

def cea_mai_frecventa_litera(
	candidati: List[str],
	tipar: str,
	litere_incercate: Set[str],
	alfabet: str = "aăâbcdefghiîjklmnopqrsștțuvwxyz"
) -> str:
	"""Selectează litera cu frecvența maximă"""
	if not candidati:
		return None
	# Colectează litere din poziții necunoscute
	litere_necunoscute = []
	for cuvant in candidati:
		for i, caracter in enumerate(cuvant):
			if tipar[i] == '*' and caracter not in litere_incercate:
				litere_necunoscute.append(caracter)
	if not litere_necunoscute:
		return None
	# Calculează frecvențe
	frecventa = Counter(litere_necunoscute)
	# Prioritizează vocale
	vocale = set("aăâeiîou")
	cea_mai_buna = max(
		frecventa.items(),
		key=lambda x: (x[1], x[0] in vocale)
	)[0]
	return cea_mai_buna

def actualizeaza_tipar(tipar: str, litera: str, cuvant_tinta: str) -> str:
	"""Actualizează tiparul pe baza literei ghicite"""
	tipar_nou = list(tipar)
	for i, caracter in enumerate(cuvant_tinta):
		if caracter == litera:
			tipar_nou[i] = litera
	return ''.join(tipar_nou)
