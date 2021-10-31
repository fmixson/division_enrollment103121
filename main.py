import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import lxml

class CourseName:
    def __init__(self, html_table):
        self.html_table = html_table

    def pull_course_name(self):
        # for i in range(len(self.html_table)):
        print('count', table_count)
        print(h2_source[table_count].text.strip())
        print('table count', table_count)
        course_name = h2_source[table_count].text.strip()
        # print(course_name)
        return course_name


class SessionName:
    row_count = 0

    def __init__(self, html_table):
        self.html_table = html_table
        # print(html_table)

    def pull_session(self):
        rows = self.html_table.find_all('tr')
        for row in rows:
            # print('row', row)
            cols = row.find_all('td')
            cols = [x.text.strip() for x in cols]
            if len(cols) == 2:
                for item in cols:
                    if 'Session' in item:
                        session = item
                        print(session)
                        return session


class TableWork:
    length = 0

    def __init__(self, html_table, course_name, session):
        self.html_table = html_table
        self.course_name = course_name
        self.session = session

    def extract_row(self):
        rows = self.html_table.find_all('tr')
        for row in rows:
            # print('row', row)
            cols = row.find_all('td')
            cols = [x.text.strip() for x in cols]
            if len(cols) == 17:
                cols.insert(0, self.course_name)
                cols.insert(1, self.session)
                enrollment_df.loc[TableWork.length] = cols
                TableWork.length += 1
                # print(cols)
        print(enrollment_df)

        # if len(cols) == 2:
        #     print('cols', cols[1])
        #     # enrollment_df.loc[SessionName.row_count, 'Session'] = cols[1]
        #     print('row count', SessionName.row_count)
        #     # enrollment_df.loc[table_count, 'Session'] = cols[1]
        #     SessionName.row_count += 1

driver = webdriver.Chrome(ChromeDriverManager().install())
# driver = webdriver.Chrome("C:/Users/family/PycharmProjects/chromedriver.exe")
driver.get('https://secure.cerritos.edu/schedule/')
check_fall_or_spring = driver.find_element(By.XPATH, '/html/body/form/p/b/b/label[2]/input').click()
check_fall_or_spring = driver.find_element(By.XPATH, '/html/body/form/p/b/b/label[1]/input').click()
# check_fall_or_spring = driver.find_element(By.XPATH, '/html/body/form/p/b/b/label[2]/input').click()
check_all = driver.find_element(By.XPATH, '/html/body/form/table/tbody/tr[1]/td[1]/label/input').click()
check_LA = driver.find_element(By.XPATH, '/html/body/form/b/b/table[4]/tbody/tr[5]/td[2]/label/input').click()
click_View = driver.find_element(By.XPATH, '/html/body/form/b/b/p[2]/input').click()
page_loading = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ASL110descs')))
headers = ['Course Name', 'Session', 'Class', 'Start', 'End', 'Days', 'Room', 'Size', 'Max', 'Wait', 'Cap', 'Seats',
           'WaitAv', 'Status', 'Instructor', 'Type', 'Hours', 'Books', 'Modality']
enrollment_df = pd.DataFrame(columns=headers)
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'lxml')
# div_table = soup.find_all('div', {'name': 'desc'}).decompose()
# print(div_table)
table_count = 0
h2_source = soup.find_all('h2')
session_source = soup.find_all('tr', {'class': 'sess1head', 'colspan': '14'})
tables = soup.find_all(['table', {'cellspacing': '0', 'class': 'class'}])

for table in tables:
    c = CourseName(html_table=h2_source)
    course_name = c.pull_course_name()
    s = SessionName(html_table=table)
    session = s.pull_session()
    t = TableWork(html_table=table, course_name=course_name, session=session)
    t.extract_row()
    table_count += 1
    # print(enrollment_df)
enrollment_df.to_excel('C:/Users/family/Desktop/Division_Enrollment.xlsx')

