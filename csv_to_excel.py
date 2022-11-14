from pyexcel.cookbook import merge_all_to_a_book
import glob

csv_file = 'berlin_mobile_jobs'
xlsx_file = 'berlin_mobile_jobs'

merge_all_to_a_book(glob.glob(f"output/{csv_file}.csv"), f"output_excel/{xlsx_file}.xlsx")