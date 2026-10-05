import csv
import re
import unittest
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('capacity_parser', ROOT / 'scripts/parse_capacity_1405_experimental.py')
parser = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parser)


class Capacity1405Regression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with (ROOT / 'data/capacity/normalized/1405/capacities-all.csv').open(encoding='utf-8-sig') as stream:
            cls.all_rows = list(csv.DictReader(stream))
            cls.rows = [row for row in cls.all_rows if parser.admission_group(row) == 'experimental']

    def test_refresh_preserves_other_groups_even_when_codes_overlap(self):
        math = {'code': '37807', 'source_id': '1405-math-booklet', 'major': 'مهندسی مکانیک', 'capacity': '7'}
        old_experimental = {'code': '37807', 'source_id': '1405-booklet', 'admission_category': 'شرایط خاص'}
        updated = dict(old_experimental, admission_category='تعهد خدمت')
        self.assertEqual(parser.preserve_other_groups([updated], [old_experimental, math]), [updated, math])

    def test_shared_export_preserves_math_raw_values(self):
        path = ROOT / 'data/capacity/normalized/1405/capacities-math.csv'
        if not path.exists():
            self.skipTest('No separate math export in this checkout')
        with path.open(encoding='utf-8-sig') as stream:
            original = list(csv.DictReader(stream))
        actual = [row for row in self.all_rows if parser.admission_group(row) == 'math']
        fields = list(original[0])
        self.assertEqual([{key: row[key] for key in fields} for row in actual], original)

    def test_37807_zahedan_physiotherapy_service_commitment(self):
        matches = [row for row in self.rows if '37807' in row['notes']]
        self.assertEqual(len(matches), 1)
        row = matches[0]
        self.assertEqual(row['major'], 'فیزیوتراپی')
        self.assertIn('زاهدان', row['university'])
        self.assertEqual(int(row['capacity']), 7)
        self.assertEqual(row['admission_category'], 'تعهد خدمت')
        self.assertIn('تعهد خدمت دو برابر', row['admission_conditions'])
        self.assertIn('بومی', row['admission_conditions'])
        self.assertIn('میرجاوه', row['native_scope'])
        self.assertEqual(row['program_type'], 'روزانه')

    def test_delayed_1406_intake_keeps_admission_year(self):
        row = next(row for row in self.rows if '33891' in row['notes'])
        self.assertEqual(int(row['year']), 1405)
        self.assertEqual(row.get('study_start_year'), '1406')

    def test_codes_and_semesters_have_independent_identity(self):
        identities = [(row.get('code') or re.search(r'\d{5}', row['notes']).group(), row['intake']) for row in self.rows]
        self.assertEqual(len(identities), len(set(identities)))
        codes = {code for code, _ in identities}
        self.assertTrue({'37811', '37812'}.issubset(codes))
        first = next(row for row in self.rows if row.get('code') == '37811')
        second = next(row for row in self.rows if row.get('code') == '37812')
        self.assertEqual(first['intake'], 'نیمسال اول')
        self.assertEqual(second['intake'], 'نیمسال دوم')
        self.assertEqual(first['capacity'], '5')
        self.assertEqual(second['capacity'], '5')

    def test_hostel_noncommitment_is_not_service_commitment(self):
        self.assertEqual(parser.classify_admission('عدم تعهد در واگذاری خوابگاه'), 'عادی')
        self.assertNotEqual(parser.classify_admission('عدم تعهد در واگذاری خوابگاه', special_table=True), 'تعهد خدمت')

    def test_explicit_commitment_survives_hostel_noncommitment(self):
        self.assertEqual(parser.classify_admission('داراي تعهد\nخدمت دو برابر طول مدت تحصيل - عدم تعهد در واگذاري خوابگاه'), 'تعهد خدمت')
        self.assertEqual(parser.classify_admission('عدم تعهد در واگذاری خوابگاه', 'سهمیه بومی دارای تعهد خدمت'), 'تعهد خدمت')
        self.assertNotEqual(parser.classify_admission('بدون تعهد خدمت'), 'تعهد خدمت')

    def test_real_pdf_row_extraction_and_service_context(self):
        raw = ROOT / 'data/raw/sanjesh/experimental/1405'
        inputs = [raw / f'Tajrobi_part_{part}.pdf' for part in (1, 2)]
        if not all(path.exists() for path in inputs):
            # The single original file is available in this Work workspace.
            inputs = [ROOT.parent / 'upload/Tajrobi(1).pdf']
        rows, candidates, skipped = parser.parse_booklet(inputs, pages=[206])
        self.assertEqual(skipped, [])
        self.assertEqual(len(rows), 14)
        row = next(row for row in rows if row['code'] == '37807')
        self.assertEqual(row['capacity'], 7)
        self.assertEqual(row['admission_category'], 'تعهد خدمت')
        self.assertIn('میرجاوه', row['native_scope'])
        self.assertEqual({row['admission_category'] for row in rows}, {'تعهد خدمت'})

    def test_38950_institution_does_not_leak_from_previous_row(self):
        row = next(row for row in self.rows if row.get('code') == '38950')
        self.assertIn('رفسنجان', row['university'])
        self.assertNotIn('هرمزگان', row['university'])


if __name__ == '__main__':
    unittest.main()
