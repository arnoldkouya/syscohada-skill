"""Tests du script syscohada.py. Lancer : python3 -m unittest discover -s tests -v"""

import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "skills" / "syscohada" / "scripts" / "syscohada.py"
PLAN = ROOT / "skills" / "syscohada" / "references" / "plan-comptable.csv"

spec = importlib.util.spec_from_file_location("syscohada", SCRIPT)
syscohada = importlib.util.module_from_spec(spec)
spec.loader.exec_module(syscohada)


def run(*argv):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = syscohada.main(["--plan", str(PLAN), *argv])
    return code, out.getvalue()


def balance_file(content: str) -> str:
    handle = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8")
    handle.write(content)
    handle.close()
    return handle.name


class PlanTests(unittest.TestCase):
    def setUp(self):
        self.plan = syscohada.load_plan(PLAN)

    def test_plan_size_and_integrity(self):
        self.assertEqual(len(self.plan), 878)
        for code, row in self.plan.items():
            self.assertEqual(row["niveau"], len(code))
            self.assertEqual(str(row["classe"]), code[0])
            if row["niveau"] > 2:
                self.assertTrue(row["parent"] in self.plan, f"parent absent pour {code}")
            else:
                self.assertEqual(row["parent"], code[0])

    def test_find_and_chain(self):
        code, out = run("find", "6011")
        self.assertEqual(code, 0)
        self.assertIn("60 > 601 > 6011", out)

    def test_find_unknown_returns_error(self):
        code, out = run("find", "9999")
        self.assertEqual(code, 1)
        self.assertIn("introuvable", out)

    def test_search_ignores_accents_and_case(self):
        _, out = run("search", "MATIERES premieres")
        self.assertIn("602", out)

    def test_validate_groups(self):
        code, out = run("validate", "6011", "9999", "ABCD", "40110000", "--json")
        data = json.loads(out)
        self.assertEqual(data["valides"], ["6011"])
        self.assertEqual(data["invalides"], ["9999"])
        self.assertEqual(data["format_incorrect"], ["ABCD"])
        self.assertEqual(data["auxiliaires"], [["40110000", "4011"]])
        self.assertEqual(code, 1)

    def test_tree_depth(self):
        _, out = run("tree", "60", "--depth", "1")
        self.assertIn("601", out)
        self.assertNotIn("6011 ", out)


class BalanceTests(unittest.TestCase):
    def test_example_balance(self):
        code, out = run("balance", str(ROOT / "examples" / "balance-exemple.csv"), "--json")
        data = json.loads(out)
        self.assertEqual(code, 0)
        self.assertTrue(data["equilibree"])
        self.assertEqual(data["resultat"], 600000.0)
        self.assertEqual(data["contre_sens"], [])

    def test_unbalanced_balance_fails(self):
        path = balance_file("compte,debit,credit\n4111,1000,0\n7011,0,900\n")
        code, out = run("balance", path)
        self.assertEqual(code, 1)
        self.assertIn("ÉCART", out)

    def test_anomalies_detected(self):
        path = balance_file(
            "compte;debit;credit\n"
            "4111;0;500,50\n"      # client créditeur
            "4011;300;0\n"         # fournisseur débiteur
            "471;200;0\n"          # compte d'attente non soldé
            "9999;0;0,01\n"        # code inconnu
            "52100001;0;0\n"       # auxiliaire rattaché
            "7011;0;0\n"
            "TOTAL;500;500,51\n"   # ligne de total ignorée
        )
        code, out = run("balance", path, "--json")
        data = json.loads(out)
        flagged = {item["compte"] for item in data["contre_sens"]}
        self.assertEqual(flagged, {"4111", "4011"})
        self.assertIn("9999", data["codes_inconnus"])
        self.assertEqual(data["auxiliaires_rattaches"], [["52100001", "521"]])
        self.assertEqual(data["comptes_attente_non_soldes"][0]["compte"], "471")
        self.assertEqual(data["lignes_ignorees"], ["TOTAL"])

    def test_number_formats(self):
        parse = syscohada.parse_number
        self.assertEqual(parse("1 234 567,89"), 1234567.89)
        self.assertEqual(parse("1,234,567.89"), 1234567.89)
        self.assertEqual(parse("1.234.567,89"), 1234567.89)
        self.assertEqual(parse("1234,5"), 1234.5)
        self.assertEqual(parse("(250)"), -250.0)
        self.assertEqual(parse(""), 0.0)

    def test_signed_solde_column(self):
        path = balance_file("compte,solde\n4111,1000\n7011,-1000\n")
        code, out = run("balance", path, "--json")
        data = json.loads(out)
        self.assertTrue(data["equilibree"])
        self.assertEqual(data["resultat"], 1000.0)


if __name__ == "__main__":
    unittest.main()
