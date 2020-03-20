import unittest
from unittest.mock import patch
import app

class TestApp(unittest.TestCase):
    
    def setUp(self):
        self.documents = app.documents
        self.directories = app.directories
        self.test_doc = {'type': 'test_type', 'number': 'test_number', 'name': 'test_name'}
        self.test_shelf = ['4', 'y', '4', '4']
        self.test_error_shelf = ['-1', '0', '1.5', 'test','1']
    
    def test_isint(self):
        self.assertTrue(app.is_positive_int(2))
        self.assertFalse(app.is_positive_int(0))
        self.assertFalse(app.is_positive_int(-1))
        self.assertFalse(app.is_positive_int('test'))
    
    def test_request_number(self):
        with patch('app.input', return_value ='2128506'):
            self.assertEqual(app.request_number(), '2128506')
    
    def test_request_shelf(self):
        with patch('app.input',  side_effect = self.test_error_shelf):
            self.assertEqual(app.request_shelf(), '1')
            
    def test_find_doc(self):
        self.assertEqual(app.find_doc('11-2'), self.documents[1])
        self.assertEqual(app.find_doc('11-3'), None)
        
    def test_find_shelf(self):
        self.assertEqual(app.find_shelf('10006'), ('2', ['10006', '5400 028765', '5455 002299']))
        self.assertEqual(app.find_shelf('11-3'), None)
        
    def test_request_attr(self):
        with patch('app.input', return_value ='passport'):
            self.assertEqual(app.request_attr('type'), 'passport')
            
    def test_add_docs(self):
        before_len_doc = len(self.documents)
        before_len_dir = len(self.directories)
        with patch('app.input', side_effect = ['test_type', 'test_number', 'test_name'] + self.test_shelf):
            app.add_docs()
        self.assertGreater(len(self.documents), before_len_doc)
        self.assertEqual(self.documents[4], self.test_doc)
        self.assertEqual(self.directories['4'][0], 'test_number')
        
    def test_add_doc_shelf(self):
        before_len_dir = len(self.directories)
        with patch('app.input', side_effect = self.test_shelf):
            app.add_doc_shelf(self.test_doc)
        self.assertGreater(len(self.directories), before_len_dir)
        self.assertEqual(self.directories['4'][0], self.test_doc['number'])
        
    def test_del_doc_shelf(self):
        before_len_dir = len(self.directories['1'])
        app.del_doc_shelf('11-2')
        self.assertLess(len(self.directories['1']), before_len_dir)

    def test_move_doc_shelf(self):
        before_len_dir = len(self.directories['1'])
        with patch('app.input', side_effect = self.test_shelf):
            app.move_doc_shelf('2207 876234')
        self.assertLess(len(self.directories['1']), before_len_dir)
        self.assertGreater(len(self.directories['4']), 0)
        
    def test_add_shelf(self):
        before_len_dir = len(self.directories)
        with patch('app.input', side_effect = self.test_error_shelf + ['2', '3', '4']):
            app.add_shelf()
        self.assertGreater(len(self.directories), before_len_dir)
    
    def test_cleaner_dict(self):
        before_len_doc = len(self.documents[3])
        app.cleaner_dict()
        self.assertLess(len(self.documents[3]), before_len_doc)
            
    def test_inspection_doc(self):
        before_len_doc = len(self.documents)
        with patch('app.input', side_effect = ['y', 'test_type1', 'test_name1', 'test_type2', 'test_name2', 'test_type3', 'test_name3']):
            app.inspection_doc()
        self.assertEqual(len(self.documents), before_len_doc + 3)
        self.assertEqual(self.documents[-1]['name'], 'test_name3')
            
        



