'''Tests for formulas API'''

from api import API, APIFormulas, APIPlugin
import helpers_test as ht
import table_evaluator as te
import numpy as np
from util.trinary import Trinary
import unittest

COLUMN1 = "Col_1"
COLUMN2 = "Col_2"
TRUTH_COLUMNS = ['A', 'B']
COLUMN1_VALUES = range(10)

#############################
# Tests
#############################
# pylint: disable=W0212,C0111,R0904
class TestAPI(unittest.TestCase):

  def setUp(self):
    self.api = API()
    self.api._table = ht.createTable("test", column_name=COLUMN1)
    self.column1 = self.api._table.columnFromName(COLUMN1)
    self.column1.addCells(COLUMN1_VALUES, replace=True)

  def testGetColumnValues(self):
    values = self.api.getColumnValues(COLUMN1)
    self.assertTrue(all(values == COLUMN1_VALUES))

  def testSetColumnValues(self):
    new_column1_values = list(COLUMN1_VALUES)
    new_column1_values.extend(range(5))
    self.api.setColumnValues(COLUMN1, new_column1_values)
    values = self.api.getColumnValues(COLUMN1)
    self.assertTrue(all(values == np.array(new_column1_values)))
    

# pylint: disable=W0212,C0111,R0904
class TestAPIFormulas(unittest.TestCase):

  def setUp(self):
    table = ht.createTable("test", column_name=COLUMN1)
    self.api = APIFormulas(table)

  def testGetValidatedColumn(self):
    column = self.api._getColumn(COLUMN1)
    self.assertEqual(column.getName(), COLUMN1)

  def _createColumn(self):
    self.api.createColumn(COLUMN2)
    return self.api._getColumn(COLUMN2)

  def testCreateColumn(self):
    column = self._createColumn()
    self.assertEqual(column.getName(), COLUMN2)

  def testDeleteColumn(self):
    _ = self._createColumn()
    self.api.deleteColumn(COLUMN2)
    is_absent = all([c.getName() != COLUMN2  \
        for c in self.api._table.getColumns()])
    self.assertTrue(is_absent)
    _ = self._createColumn()
    self.api.deleteColumn(2)
    is_absent = all([c.getName() != COLUMN2  \
        for c in self.api._table.getColumns()])
    self.assertTrue(is_absent)

  def testParam(self):
    p1 = self.api.param(COLUMN1)
    self.assertEqual(p1, 0)
    p2 = self.api.param(COLUMN1, row_num=2)
    self.assertEqual(p2, 1)

  def _createTruthTable(self):
    return
    self.api.deleteColumn(COLUMN1)
    self.api.createTruthTable(TRUTH_COLUMNS, only_boolean = True)

  def testCreateTruthTable(self):
    return
    self._createTruthTable()
    for n in range(len(TRUTH_COLUMNS)):
      self.assertTrue(any([c.getName() == TRUTH_COLUMNS[n]
          for c in self.api._table.getColumns()]))

  def testCreateTrinary(self):
    return
    self._createTruthTable()
    for n in range(len(TRUTH_COLUMNS)):
      column = self.api._table.columnFromName(TRUTH_COLUMNS[n])
      trinary = self.api.createTrinary(column.getCells())
      new_trinary = -trinary
      self.assertTrue(isinstance(new_trinary, Trinary))
    

# pylint: disable=W0212,C0111,R0904
class TestAPIPlugin(unittest.TestCase):

  def setUp(self):
    table = ht.createTable("test", column_name=COLUMN1)
    self.api = APIPlugin(table.getFilepath())
    self.api.initialize()


if __name__ == '__main__':
  unittest.main()
