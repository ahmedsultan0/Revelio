import os
import sqlite3
import unittest
import io
import sys
import itertools
import shutil
from magic.scan.index import index
from magic.inventory import db_connection
from magic.config import IMAGE_EXTENSIONS
from PIL import Image
from pathlib import Path

MOCK_SIZES = [(100, 100), (200, 150), (300, 300), (400, 250), (500, 500), (700, 1200), (1500, 2500)] 

class TestScanning(unittest.TestCase):

    test_db = "revelio_test.db"

    def setUp(self):
        """Runs before every test"""

        test_conn = sqlite3.connect(self.test_db)
        test_cursor = test_conn.cursor()
        test_cursor.execute(db_connection.FILE_DB_SQL_COMMAND)
        test_conn.commit()

        # Replace module-level connection and cursor
        db_connection.connection = test_conn
        db_connection.cursor = test_cursor

        self.test_dir = self.create_fake_files()
        if not self.test_dir: 
            raise Exception("Could not mock the images to test.")

    def doCleanups(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        os.remove(self.test_db)

    def create_fake_files(self):

        data_dir = Path(__file__).parent / "data"
        data_dir.mkdir(exist_ok=True)

        try:
            for i in range(10):
                (data_dir / f"file_{i}.txt").write_text(f"This is dummy file {i}")
            
            for i, (size, fmt) in enumerate(itertools.product(MOCK_SIZES, IMAGE_EXTENSIONS)):
                img = Image.new("RGB", size, color=(i*40 % 255, i*80 % 255, i*120 % 255))
                img_path = data_dir / f"image_{i}{fmt.lower()}"
                img.save(img_path)

        except (Exception, AttributeError):
            return False

        return data_dir
    
    def test_db_connection(self):
        assert os.path.exists(self.test_db) 
        assert(db_connection.connection != None)

    def test_run_scanner(self):
        test_input = "."
        expected_number_of_images_processed = len(IMAGE_EXTENSIONS) * len(MOCK_SIZES)

        sys.stdin = io.StringIO(test_input)
        number_of_images_processed, number_of_images_already_processed = index() 

        self.assertEqual(number_of_images_already_processed, 0, f"Expected the number of images re-processed to be 0 got {number_of_images_already_processed}")
        self.assertEqual(number_of_images_processed, expected_number_of_images_processed, f"Expected the number of images processed to be {expected_number_of_images_processed} got {number_of_images_processed}")
