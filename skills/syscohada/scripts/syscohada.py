#!/usr/bin/env python3
"""Outil en ligne de commande pour le plan comptable SYSCOHADA.

Bibliothèque standard uniquement (Python 3.8+).

Commandes : find, search, validate, tree, classe, export, stats, balance.
Le plan est lu dans references/plan-comptable.csv (chemin modifiable avec
--plan ou la variable d'environnement SYSCOHADA_PLAN).
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import os
import re
import sys
import unicodedata
from pathlib import Path

TOL = 0.005
COLUMNS = ["code", "libelle", "classe", "niveau", "parent", "nature", "sens"]


# --------------------------------------------------------------------------
# Chargement du plan
# --------------------------------------------------------------------------

def locate_plan(explicit: str | None) -> Path:
    here = Path(__file__).resolve().parent
    candidates = []
    if explicit:
        candidates.append(Path(explicit))
    if os.environ.get("SYSCOHADA_PLAN"):
        candidates.append(Path(os.environ["SYSCOHADA_PLAN"]))
    candidates += [
        here.parent / "references" / "plan-comptable.csv",
        here / "plan-comptable.csv",
        Path.cwd() / "plan-comptable.csv",
    ]
    for path in candidates:
        if path.is_file():
            return path
    sys.exit("Fichier plan-comptable.csv introuvable. Utiliser --plan CHEMIN.")


def load_plan(path: Path) -> dict[str, dict]:
    plan: dict[str, dict] = {}
    with open(path, encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            row["classe"] = int(row["classe"])
            row["niveau"] = int(row["niveau"])
            row["parent"] = row["parent"] or None
            plan[row["code"]] = row
    return plan


def norm(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text)
    stripped = "".join(c for c in decomposed if not unicodedata.combining(c))
    return stripped.lower().replace("’", "'")


def resolve(code: str, plan: dict[str, dict]):
    """Retourne (compte, exact). Cherche le plus long préfixe existant."""
    if code in plan:
        return plan[code], True
    for size in range(min(len(code), 4), 1, -1):
        if code[:size] in plan:
            return plan[code[:size]], False
    return None, False


def chain(code: str, plan: dict[str, dict]) -> list[dict]:
    out = []
    current = plan.get(code)
    while current:
        out.append(current)
        current = plan.get(current["parent"]) if current["parent"] else None
    return list(reversed(out))


def children(code: str, plan: dict[str, dict]) -> list[dict]:
    return [r for r in plan.values() if r["parent"] == code]


def descendants(code: str, plan: dict[str, dict]):
    for child in children(code, plan):
        yield child
        yield from descendants(child["code"], plan)


def suggestions(code: str, plan: dict[str, dict], limit: int = 6) -> list[dict]:
    """Comptes voisins : même préfixe le plus long."""
    for size in range(min(len(code), 3), 0, -1):
        prefix = code[:size]
        found = [r for c, r in plan.items() if c.startswith(prefix) and c != code]
        if found:
            return found[:limit]
    return []


def line(row: dict) -> str:
    return f"{row['code']:<5} {row['libelle']}  [{row['nature']}, {row['sens']}]"


# --------------------------------------------------------------------------
# Commandes sur le plan
# --------------------------------------------------------------------------

def cmd_find(args, plan):
    code = args.code.strip()
    row = plan.get(code)
    if not row:
        print(f"Compte {code} introuvable dans le plan.")
        near = suggestions(code, plan)
        if near:
            print("Comptes voisins :")
            for r in near:
                print("  " + line(r))
        return 1
    print(f"{row['code']} : {row['libelle']}")
    print(f"  Classe {row['classe']}, niveau {row['niveau']}, nature {row['nature']}, sens {row['sens']}")
    print("  Chemin : " + " > ".join(r["code"] for r in chain(code, plan)))
    kids = children(code, plan)
    if kids:
        print("  Enfants :")
        for r in kids:
            print("    " + line(r))
    return 0


def cmd_search(args, plan):
    words = norm(args.terme).split()
    hits = []
    for row in plan.values():
        if args.classe and row["classe"] != args.classe:
            continue
        haystack = row["code"] + " " + norm(row["libelle"])
        if all(w in haystack for w in words):
            hits.append(row)
    for row in hits[: args.limit]:
        print(line(row))
    if len(hits) > args.limit:
        print(f"... {len(hits) - args.limit} autres résultats (utiliser --limit).")
    if not hits:
        print("Aucun résultat.")
        return 1
    return 0


def cmd_validate(args, plan):
    codes = list(args.codes)
    if codes == ["-"]:
        codes = sys.stdin.read().split()
    result = {"valides": [], "invalides": [], "format_incorrect": [], "auxiliaires": []}
    for code in codes:
        if not re.fullmatch(r"\d+", code):
            result["format_incorrect"].append(code)
        elif len(code) > 4:
            parent, _ = resolve(code, plan)
            result["auxiliaires"].append((code, parent["code"] if parent else None))
        elif code in plan:
            result["valides"].append(code)
        else:
            result["invalides"].append(code)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Valides ({len(result['valides'])}) : {' '.join(result['valides']) or '-'}")
        print(f"Invalides ({len(result['invalides'])}) :")
        for code in result["invalides"]:
            near = ", ".join(r["code"] for r in suggestions(code, plan, 4)) or "aucun"
            print(f"  {code}  (voisins : {near})")
        print(f"Format incorrect ({len(result['format_incorrect'])}) : {' '.join(result['format_incorrect']) or '-'}")
        if result["auxiliaires"]:
            print("Auxiliaires de plus de 4 chiffres (rattachés au plan) :")
            for code, parent in result["auxiliaires"]:
                print(f"  {code} -> {parent or 'aucun préfixe connu'}")
    return 1 if result["invalides"] or result["format_incorrect"] else 0


def cmd_tree(args, plan):
    root = plan.get(args.code)
    if not root:
        print(f"Compte {args.code} introuvable.")
        return 1

    def walk(row, depth):
        print("  " * depth + line(row))
        if args.depth is None or depth < args.depth:
            for child in children(row["code"], plan):
                walk(child, depth + 1)

    walk(root, 0)
    return 0


def select(plan, classe=None, niveau=None, nature=None, sens=None):
    return [
        r for r in plan.values()
        if (classe is None or r["classe"] == classe)
        and (niveau is None or r["niveau"] == niveau)
        and (nature is None or r["nature"] == nature)
        and (sens is None or r["sens"] == sens)
    ]


def cmd_classe(args, plan):
    for row in select(plan, classe=args.numero, niveau=args.niveau):
        print(line(row))
    return 0


def cmd_export(args, plan):
    rows = select(plan, args.classe, args.niveau, args.nature, args.sens)
    if args.format == "json":
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    elif args.format == "md":
        print("| Code | Libellé | Nature | Sens |\n|---|---|---|---|")
        for r in rows:
            print(f"| {r['code']} | {r['libelle']} | {r['nature']} | {r['sens']} |")
    else:
        writer = csv.DictWriter(sys.stdout, fieldnames=COLUMNS, lineterminator="\n")
        writer.writeheader()
        for r in rows:
            writer.writerow({k: ("" if r[k] is None else r[k]) for k in COLUMNS})
    return 0


def cmd_stats(args, plan):
    print(f"Total : {len(plan)} comptes")
    for classe in range(1, 10):
        print(f"  Classe {classe} : {len(select(plan, classe=classe))}")
    return 0


# --------------------------------------------------------------------------
# Contrôle de balance
# --------------------------------------------------------------------------

def parse_number(text: str) -> float:
    value = (text or "").strip().replace(" ", "").replace(" ", "")
    if not value or value in {"-", "—"}:
        return 0.0
    negative = value.startswith("(") and value.endswith(")")
    value = value.strip("()")
    if "," in value and "." in value:
        decimal = "," if value.rfind(",") > value.rfind(".") else "."
        thousands = "." if decimal == "," else ","
        value = value.replace(thousands, "").replace(decimal, ".")
    elif "," in value:
        head, _, tail = value.rpartition(",")
        value = (head + "." + tail) if len(tail) in (1, 2) and "," not in head else value.replace(",", "")
    number = float(value)
    return -number if negative else number


def find_column(headers: list[str], *needles: str):
    for index, header in enumerate(headers):
        if any(n in header for n in needles):
            return index
    return None


def read_balance(path: Path):
    text = path.read_text(encoding="utf-8-sig")
    first = text.splitlines()[0] if text else ""
    delimiter = max([",", ";", "\t"], key=first.count)
    rows = list(csv.reader(io.StringIO(text), delimiter=delimiter))
    if len(rows) < 2:
        sys.exit("Balance vide ou sans en-tête.")
    headers = [norm(h) for h in rows[0]]
    i_code = find_column(headers, "compte", "code", "numero", "account")
    i_debit = find_column(headers, "debit")
    i_credit = find_column(headers, "credit")
    i_solde = find_column(headers, "solde")
    if i_code is None or (i_debit is None and i_credit is None and i_solde is None):
        sys.exit("Colonnes attendues : compte (ou code), debit, credit (ou solde).")
    entries, ignored = {}, []
    for raw in rows[1:]:
        if not any(cell.strip() for cell in raw):
            continue
        code = re.sub(r"\D", "", raw[i_code]) if i_code < len(raw) else ""
        if not code or not re.fullmatch(r"\d+", raw[i_code].strip().replace(" ", "")):
            ignored.append(raw[i_code].strip() if i_code < len(raw) else "?")
            continue
        get = lambda i: parse_number(raw[i]) if i is not None and i < len(raw) else 0.0
        debit, credit = get(i_debit), get(i_credit)
        if i_debit is None and i_credit is None:
            solde = get(i_solde)
            debit, credit = (solde, 0.0) if solde >= 0 else (0.0, -solde)
        slot = entries.setdefault(code, [0.0, 0.0])
        slot[0] += debit
        slot[1] += credit
    return entries, ignored


def money(value: float) -> str:
    return f"{value:,.2f}".replace(",", " ")


def cmd_balance(args, plan):
    entries, ignored = read_balance(Path(args.fichier))
    total_d = sum(d for d, _ in entries.values())
    total_c = sum(c for _, c in entries.values())
    gap = round(total_d - total_c, 2)

    unknown, auxiliaires, contre_sens, attente = [], [], [], []
    charges = produits = autres8 = 0.0
    for code, (debit, credit) in sorted(entries.items()):
        net = debit - credit
        account, exact = resolve(code, plan)
        if account is None:
            unknown.append(code)
        elif not exact and len(code) > 4:
            auxiliaires.append((code, account["code"]))
        elif not exact:
            unknown.append(code)
        if account and abs(net) > TOL:
            if (account["sens"] == "debit" and net < 0) or (account["sens"] == "credit" and net > 0):
                contre_sens.append((code, account["libelle"], net))
        if (code.startswith("471") or code.startswith("58")) and abs(net) > TOL:
            attente.append((code, net))
        if code[0] == "6":
            charges += net
        elif code[0] == "7":
            produits -= net
        elif code[0] == "8":
            autres8 -= net
    gestion = any(c[0] in "678" for c in entries)
    resultat = produits + autres8 - charges

    report = {
        "total_debit": round(total_d, 2),
        "total_credit": round(total_c, 2),
        "ecart": gap,
        "equilibree": abs(gap) <= TOL,
        "comptes": len(entries),
        "lignes_ignorees": ignored,
        "codes_inconnus": unknown,
        "auxiliaires_rattaches": auxiliaires,
        "contre_sens": [{"compte": c, "libelle": l, "solde": round(n, 2)} for c, l, n in contre_sens],
        "comptes_attente_non_soldes": [{"compte": c, "solde": round(n, 2)} for c, n in attente],
        "charges_classe6": round(charges, 2) if gestion else None,
        "produits_classe7": round(produits, 2) if gestion else None,
        "net_classe8": round(autres8, 2) if gestion else None,
        "resultat": round(resultat, 2) if gestion else None,
    }
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report["equilibree"] else 1

    print(f"Comptes lus : {len(entries)}")
    print(f"Total débit  : {money(total_d)}")
    print(f"Total crédit : {money(total_c)}")
    if report["equilibree"]:
        print("Équilibre : OK")
    else:
        print(f"Équilibre : ÉCART de {money(gap)} (débit moins crédit). S'arrêter et corriger avant la clôture.")
    if ignored:
        print(f"Lignes ignorées (non numériques, par exemple totaux) : {', '.join(ignored)}")
    if unknown:
        print("Codes absents du plan :")
        for code in unknown:
            near = ", ".join(r["code"] for r in suggestions(code, plan, 4)) or "aucun"
            print(f"  {code}  (voisins : {near})")
    if auxiliaires:
        print(f"Auxiliaires rattachés au plan : {len(auxiliaires)} (ex. {auxiliaires[0][0]} -> {auxiliaires[0][1]})")
    if contre_sens:
        print("Soldes à contre-sens (à examiner) :")
        for code, label, net in contre_sens:
            side = "débiteur" if net > 0 else "créditeur"
            print(f"  {code} {label} : solde {side} de {money(abs(net))}")
    if attente:
        print("Comptes d'attente ou de virement non soldés :")
        for code, net in attente:
            print(f"  {code} : {money(net)}")
    if gestion:
        print("Résultat provisoire (classes 6, 7, 8) :")
        print(f"  Charges (classe 6)   : {money(charges)}")
        print(f"  Produits (classe 7)  : {money(produits)}")
        print(f"  Classe 8 (net)       : {money(autres8)}")
        label = "bénéfice" if resultat >= 0 else "perte"
        print(f"  Résultat             : {money(resultat)} ({label})")
    else:
        print("Aucun compte de gestion (6, 7, 8) : résultat non calculable ou exercice déjà soldé.")
    return 0 if report["equilibree"] else 1


# --------------------------------------------------------------------------
# Programme principal
# --------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Plan comptable SYSCOHADA")
    parser.add_argument("--plan", help="Chemin de plan-comptable.csv")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("find", help="Fiche d'un compte")
    p.add_argument("code")
    p.set_defaults(func=cmd_find)

    p = sub.add_parser("search", help="Recherche sur le code ou le libellé")
    p.add_argument("terme")
    p.add_argument("--classe", type=int)
    p.add_argument("--limit", type=int, default=40)
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("validate", help="Valider des codes (ou - pour lire stdin)")
    p.add_argument("codes", nargs="+")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("tree", help="Descendants d'un compte")
    p.add_argument("code")
    p.add_argument("--depth", type=int)
    p.set_defaults(func=cmd_tree)

    p = sub.add_parser("classe", help="Comptes d'une classe")
    p.add_argument("numero", type=int)
    p.add_argument("--niveau", type=int)
    p.set_defaults(func=cmd_classe)

    p = sub.add_parser("export", help="Exporter le plan (csv, json, md)")
    p.add_argument("--format", choices=["csv", "json", "md"], default="csv")
    p.add_argument("--classe", type=int)
    p.add_argument("--niveau", type=int)
    p.add_argument("--nature", choices=["bilan", "gestion", "hors-bilan", "cage"])
    p.add_argument("--sens", choices=["debit", "credit", "mixte"])
    p.set_defaults(func=cmd_export)

    p = sub.add_parser("stats", help="Statistiques du plan")
    p.set_defaults(func=cmd_stats)

    p = sub.add_parser("balance", help="Contrôler une balance (CSV) et calculer le résultat")
    p.add_argument("fichier")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_balance)
    return parser


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    args = build_parser().parse_args(argv)
    plan = load_plan(locate_plan(args.plan))
    try:
        return args.func(args, plan)
    except BrokenPipeError:
        # Sortie tronquée par un tube (par exemple | head) : fin silencieuse.
        try:
            sys.stdout.close()
        except Exception:
            pass
        return 0


if __name__ == "__main__":
    sys.exit(main())
