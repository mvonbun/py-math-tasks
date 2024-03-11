'''Math Task PDF Generator'''
import random
import argparse

from math import floor, log10

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, KeepTogether, Paragraph, Frame
from reportlab.platypus.flowables import BalancedColumns


# define functions
#
def get_numbers(digits_min: int = 4, digits_max: int = 6) -> tuple:
  """
  Generates two random integers with fixed amount of digits.

  Returns:
      tuple: A tuple containing two random integers.
  """
  # set value ranges based on the number of digits requested
  #
  int_max = 10**digits_max-1
  int_min = 10**(digits_min-1)

  # get two random numbers
  #
  first_int = random.randint(int_min, int_max)
  second_int = random.randint(int_min, int_max)
  return first_int, second_int


class AddSubFormal:
    """Formal Addition and Subtraction."""
    def __init__(self, digits_min: int, digits_max: int,
                 rows_above: int = 1, rows_below: int = 1,
                 cols_before: int = 1 , cols_after: int = 1) -> None:
        # set task properties
        #
        self.digits = [digits_min, digits_max]
        self.int_min = 10**(digits_min-1)
        self.int_max = 10**digits_max-1

        # set task layout
        #
        self.rows_above = rows_above
        self.rows_below = rows_below
        self.cols_before = cols_before
        self.cols_after = cols_after
        self.rows = 4 + rows_above + rows_below
        self.cols = digits_max + 1 + cols_before + cols_after

        # set task rendering style
        #
        self.table_style = TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'),
                                       ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                                       ('FONTSIZE', (cols_before+1,-2-rows_below), (-1-cols_after,-2-rows_below), 8),
                                       ('LINEABOVE', (cols_before,-1-rows_below), (-1-cols_after,-1-rows_below), 2, colors.black),
                                       ('INNERGRID', (0,0), (-1,-1), 0.25, colors.grey),
                                       ('BOX', (0,0), (-1,-1), 0.5, colors.black),
                                       ])
        self.table_cell_size = 12
        self.table_sep = 16
    
    def initTableData(self) -> list:
        """Initializes a rows-by-cols table data list."""
        return [ [ '' for i in range(self.cols) ] for j in range(self.rows) ]
    
    def intToList(self, a: int) -> list:
        """Splits the digits of an integer into a list."""
        return [int(char) for char in str(a)]
    
    def getRandomInteger(self) -> int:
        """Get a random integer from the specified range."""
        return random.randint(self.int_min, self.int_max)
    
    def sign(self, a: int, b: int) -> str:
        """Return operator + or - based on which value is bigger."""
        if a > b:
            return '-'
        else:
            return '+'
        
    def result(self, a: int, b: int) -> int:
        """Return result of addition or substraction."""
        if a > b:
            return a - b
        else:
            return a + b
        
    def carry(self, a: list, b: list, addNotSub: bool) -> list:
        """Return list of carries."""
        numel = max(len(a), len(b))
        carries = [0 for i in range(numel)]
        for k in range(0, numel-1):
            if (k < len(a)) and (k < len(b)):
                if addNotSub:
                    if k == 0:
                        if (a[-1] + b[-1]) > 9:
                            carries[-2] = 1
                    else:
                        if (a[-1-k] + b[-1-k] + carries[-1-k]) > 9:
                            carries[-2-k] = 1
                else:
                    if k == 0:
                        if (a[-1] < b[-1]):
                            carries[-2] = 1
                    else:
                        if (a[-1-k] - b[-1-k] - carries[-1-k]) < 0:
                            carries[-2-k] = 1
        return [str(c) if c == 1 else '' for c in carries]
        
    def fillRowLeft(self, table_data: list, row: int, row_data: list) -> None:
        """Fills a row of a table with some row data from the left."""
        for k in range(0, len(row_data)):
            table_data[row][self.cols_before + k] = row_data[k]
    
    def fillRowRight(self, table_data: list, row: int, row_data: list) -> None:
        """Fills a row of a table with some row data from the right."""
        for k in range(0, len(row_data)):
            table_data[row][-1 -self.cols_after -k] = row_data[-1-k]
        
    def getTask(self) -> dict:
        """Get a task."""
        # get two random integers
        #
        a = self.getRandomInteger()
        b = self.getRandomInteger()

        # and turn them into character lists
        #
        a_list = self.intToList(a)
        b_list = self.intToList(b)

        # loop to create taks and solution
        #
        for k in range(2):
            # init table data
            #
            table_data = self.initTableData()

            # write first number line
            #
            self.fillRowRight(table_data, self.rows_above+0, a_list)

            # write second number line
            #
            self.fillRowRight(table_data, self.rows_above+1, b_list)

            # write operator in carry line
            #
            self.fillRowLeft(table_data, self.rows_above+2, [self.sign(a,b)])

            # write solution (results and carries)
            #
            if k == 1:
                self.fillRowRight(table_data, self.rows_above+2, self.carry(a_list, b_list, a<b))
                self.fillRowRight(table_data, self.rows_above+3, self.intToList(self.result(a,b)))

            # write to table
            #
            table = Table(table_data,
                        colWidths=self.table_cell_size,
                        rowHeights=self.table_cell_size,
                        spaceAfter=self.table_sep)
            table.setStyle(self.table_style)

            # store table
            #
            if k == 0:
                task = table
            else:
                solution = table
        return {'task': task, 'solution': solution}


def task(digits_min: int, digits_max: int,
         row_above: int = 1, row_below: int = 1,
         col_before: int =1 , col_after: int = 1) -> Table:
    """
    Generates the actual tasks rendered in a table.
    """
    # get two random integers
    #
    a, b = get_numbers(digits_max=digits_max, digits_min=digits_min)
    print(f"First random integer: {a}")
    print(f"Second random integer: {b}")

    # turn into digit list
    #
    a_list = [char for char in str(a)]
    b_list = [char for char in str(b)]

    # configure cells
    #
    empty=' '
    if a > b:
        sign = '-'
    else:
        sign = '+'
    
    # make table data
    #
    n_rows = 4 + row_above + row_below
    n_cols = digits_max + 1 + col_before + col_after
    table_data = []
    for row in range(0, n_rows):
        row_data = []
        if row == row_above:
            # a-number line
            n_empty_col = col_before + 1 + (digits_max-len(a_list))
            for col in range(0, n_empty_col):
                row_data.append(empty)
            row_data.extend(a_list)
            n_empty_col = col_after
        elif row == (row_above + 1):
            # b-number line
            n_empty_col = col_before + 1 + (digits_max-len(b_list))
            for col in range(0, n_empty_col):
                row_data.append(empty)
            row_data.extend(b_list)
        elif row == (row_above + 2):
            # sign and carry line
            n_empty_col = col_before
            for col in range(0, n_empty_col):
                row_data.append(empty)
            row_data.append(sign)
            for col in range(0, digits_max):
                row_data.append(empty)

        else:
            for col in range(0, n_cols - col_after):
                row_data.append(empty)
        
        # add extra columns to end
        #
        for col in range(0, col_after):
            row_data.append(empty)

        table_data.append(row_data)

    # t = Table([first_int_list, second_int_list])
    t = Table(table_data, colWidths=12, rowHeights=12, spaceAfter=16)
    t.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LINEABOVE', (col_before,-1-row_below), (-1-col_after,-1-row_below), 2, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.grey),
        ('BOX', (0,0), (-1,-1), 0.5, colors.black),
        ]))
    
    return t


def create_parser() -> argparse.ArgumentParser:
    """
    Creates an ArgumentParser object for handling command line arguments.

    Returns:
    argparse.ArgumentParser: The initialized ArgumentParser object.
    """
    parser = argparse.ArgumentParser(description="Mathe Aufgaben Generator.")
    # Define your arguments here using parser.add_argument()
    # For example:
    parser.add_argument("dateiname", help="Aufgaben PDF Dateiname.")
    parser.add_argument("-a", "--aufgabe", type=list, default=['addsub'],
                        help="Liste von Aufgaben.")
    parser.add_argument("-n", "--num", type=int, default=1,
                        help="Anzahl an erstellten Aufgabenblättern.")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Verbosen modus aktivieren.")
    return parser

def main() -> None:
    """
    The main function of the script.

    This is where the script's core logic resides. It parses the arguments
    using the parser created by create_parser() and executes the desired 
    functionality.
    """
    parser = create_parser()
    args = parser.parse_args()

    # make task class
    #
    T = AddSubFormal(4,6)
    
    # Define PDF file name
    #
    filename = args.dateiname

    # set some styles for the document
    #
    styles = getSampleStyleSheet()

    # worksheet title
    #
    title_base = "Schriftliche Addition und Subtraktion"
    title = Paragraph(title_base, styles['Heading1'])
    title_sol = Paragraph(f"{title_base} - Lösung", styles['Heading1'])

    # week days for excersises
    #
    days = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']

    # define layout of tasks on page
    #
    tasks_per_day = 6
    tasks_per_row = 3

    # document generation loop
    #
    pagenum_digits = floor(log10(args.num))+1
    filename_base = args.dateiname.split('.')[0]
    for n in range(args.num):
        # document name
        #
        if args.num == 1:
            filename = f"{filename_base}.pdf"
            loesung = f"{filename_base}_loesung.pdf"
        else:
            filename = f"{filename_base}_{n:0{pagenum_digits}d}.pdf"
            loesung = f"{filename_base}_{n:0{pagenum_digits}d}_loesung.pdf"

        # create document
        #
        doc = SimpleDocTemplate(filename, pagesize=A4, showBoundary=0)
        doc_sol = SimpleDocTemplate(loesung, pagesize=A4, showBoundary=0)

        # init document content
        #
        story = []
        story_sol = []

        # add title
        #
        story.append(title)
        story_sol.append(title_sol)

        for d in days:
            story.append(Paragraph(d, styles['Heading2']))
            story_sol.append(Paragraph(d, styles['Heading2']))

            # create list of tasks (tables actually)
            #
            tasks_and_solutions = [T.getTask() for x in range(0, tasks_per_day)]

            # tasks
            #
            tasks = [t['task'] for t in tasks_and_solutions]

            # solutions
            #
            solutions = [t['solution'] for t in tasks_and_solutions]

            # add tasks to document preserving the defined layout
            #
            story.append(BalancedColumns(tasks, nCols=tasks_per_row))
            story_sol.append(BalancedColumns(solutions, nCols=tasks_per_row))

        # write file
        #
        doc.build(story)
        doc_sol.build(story_sol)

        if args.verbose:
            print(f"Neues Aufgabenblatt: {filename}")

  
if __name__ == "__main__":
  main()
