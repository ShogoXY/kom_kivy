import re
import pandas as pd
import sqlite3 as db
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable


con = db.connect("glowna.db")
con2 = db.connect("komplementarna.db")

# path_excel = "glowna.xlsx"
# path_excel_kom = "kom.xlsx"
# df = pd.read_excel(path_excel)
# df_kom = pd.read_excel(path_excel_kom)

# path_excel = "glowna.csv"
# path_excel_kom = "kom.csv"
# df = pd.read_csv(path_excel)
df = pd.read_sql_query("SELECT * FROM glowna", con)
df_kom = pd.read_sql_query("SELECT * FROM kom", con2)
# df_kom = pd.read_csv(path_excel_kom)
df = pd.DataFrame(df)
df_kom = pd.DataFrame(df_kom)
df_glowna = df["NAZWA"]
df_glowna = pd.DataFrame(df_glowna)
df_nauka_g = df

df_komplementarna = df_kom["NAZWA"]
df_komplementarna = pd.DataFrame(df_komplementarna)


def wybrana_lista(szukaj):
    show = P()

    szukaj2 = szukaj.split()
    if szukaj == "":
        sm.current = "glowna"
    global df_glowna
    df_glowna = df

    for i in range(len(szukaj2)):

        df_glowna = df_glowna[df_glowna["NAZWA"].str.contains(szukaj2[i], flags=re.IGNORECASE, regex=True)]
        df_glowna = df_glowna["NAZWA"].drop_duplicates()

        df_glowna = pd.DataFrame(df_glowna)


        if df_glowna.empty:
            df_glowna = df["NAZWA"].drop_duplicates()

            df_glowna = pd.DataFrame(df_glowna)
            Popup(size_hint=(None, None), size=(400, 400), title="BŁĄD", auto_dismiss=True, content=show).open()
            sm.current = "glowna"

def cala_lista(szukaj):
    show = P()

    szukaj2 = szukaj.split()
    # if szukaj == "":
    #     sm.current = "nauka1"
    global df_nauka_g
    df_nauka_g = df

    for i in range(len(szukaj2)):

        df_nauka_g = df_nauka_g[df_nauka_g["NAZWA"].str.contains(szukaj2[i], flags=re.IGNORECASE, regex=True)]

        if df_nauka_g.empty:
            df_nauka_g = df
            df_nauka_g = pd.DataFrame(df_nauka_g)
            Popup(size_hint=(None, None), size=(400, 400), title="BŁĄD", auto_dismiss=True, content=show).open()
            sm.current = "nauka1"
def wybrana_lista_2(szukaj):

    szukaj2 = szukaj.split()


    df_glowna_2 = df
    for i in range(len(szukaj2)):

        df_glowna_2 = df_glowna_2[df_glowna_2["NAZWA"].str.contains(szukaj2[i], flags=re.IGNORECASE, regex=False)]

    df_glowna_2 = df_glowna_2["KATEGORIA"].unique()
    df_glowna_2 = pd.DataFrame(df_glowna_2)
    # df_glowna_2 = df_glowna_2.to_string(index=False, header=False)
    return (df_glowna_2)



def wynik_komplemanatrny(szukaj_kom):
    show = P()
    global df_komplementarna
    df_komplementarna = df_kom
    szukaj_kom2 = szukaj_kom.split()
    if szukaj_kom == "":
        sm.current = "komplementarna"

    for i in range(len(szukaj_kom2)):

        # df_kom2 = df_kom2[df_kom2["KATEGORIA"].str.contains(str(kat_g), flags=re.IGNORECASE, regex=True)]
        df_komplementarna = df_komplementarna[df_komplementarna["NAZWA"].str.contains(szukaj_kom2[i], flags=re.IGNORECASE, regex=True)]
        df_komplementarna = df_komplementarna["NAZWA"].drop_duplicates()

        df_komplementarna = pd.DataFrame(df_komplementarna)

    if df_komplementarna.empty:
        df_komplementarna = df_kom["NAZWA"].drop_duplicates()

        df_komplementarna = pd.DataFrame(df_komplementarna)
        Popup(size_hint=(None, None), size=(400, 400), title="BŁĄD", auto_dismiss=True, content=show).open()
        sm.current = "komplementarna"

def nauka_komp(szukaj_kom):
    show = P()
    global df_nauka_k

    szukaj_kom2 = szukaj_kom.split()


    for i in range(len(szukaj_kom2)):

        df_nauka_k = df_nauka_k[df_nauka_k["NAZWA"].str.contains(szukaj_kom2[i], flags=re.IGNORECASE, regex=True)]

        # df_nauka_k = pd.DataFrame(df_nauka_k)

    if df_nauka_k.empty:
        df_nauka_k = df_kom
        df_nauka_k = df_nauka_k[df_nauka_k["KATEGORIA"].str.contains(nauka_kat, flags=re.IGNORECASE, regex=True)]


        Popup(size_hint=(None, None), size=(400, 400), title="BŁĄD", auto_dismiss=True, content=show).open()
        sm.current = "nauka2"

def wynik_komplemanatrny_2(szukaj_kom):

    df_komplementarna_2 = df_kom
    szukaj_kom2 = szukaj_kom

    for i in range(len(szukaj_kom2)):

        df_komplementarna_2 = df_komplementarna_2[df_komplementarna_2["NAZWA"].str.contains(szukaj_kom2[i], flags=re.IGNORECASE, regex=False)]

    df_komplementarna_2 = df_komplementarna_2["KATEGORIA"].unique()
    df_komplementarna_2 = pd.DataFrame(df_komplementarna_2)
    # df_komplementarna_2 = df_komplementarna_2.to_string(index=False, header=False)
    return (df_komplementarna_2)




def get_data_table(dataframe):
    column_data = list(dataframe.columns)
    row_data = dataframe.to_records(index=False)
    return column_data, row_data

class odp(FloatLayout):
    pass
class P(FloatLayout):
    pass
class MenuScreen(Screen):
    pass


class GlownaScreen(Screen):

    def tabelka(self):
        layout = AnchorLayout()

        column_data, row_data = get_data_table(df_glowna)
        column_data = [(x, dp(60)) for x in column_data]

        self.table = MDDataTable(

            pos_hint={'center_y': 0.5, 'center_x': 0.5},
            size_hint=(0.9, 0.6),
            # check=True,
            column_data=column_data,
            row_data=row_data,
            use_pagination=True,
            rows_num=100
        )

        self.table.bind(on_check_press=self.checked)
        self.table.bind(on_row_press=self.row_checked)

        self.add_widget(self.table)

        return layout

    def on_enter(self):
        self.tabelka()

    def checked(self, instance_table, current_row):

        self.manager.get_screen("komplementarna").ids.label_kom.text = str(current_row[0])
        self.manager.get_screen("wynik").ids.label_wynik_1.text = str(current_row[0])


    def row_checked(self, instance_table, instance_row):
        # print(instance_table, instance_row)

        if instance_row.ids.check.state == 'normal':
            instance_row.ids.check.state = 'down'
            sm.current = "komplementarna"  # przejście na nowy ekran

        else:
            instance_row.ids.check.state = 'normal'

    def popup(self):
        show = P()

        if self.manager.get_screen("glowna").ids.glowny_input_text.text == "":
            Popup(size_hint=(None, None), size=(400, 400), title="BŁĄD", auto_dismiss=True, content=show).open()  # wyświetlenie komunikatu o błędzie
        else:
            wybrana_lista(self.manager.get_screen("glowna").ids.glowny_input_text.text)
            self.clear_widgets(self.children[:1])  # usuwanie tabelki (self.tabelka())
            self.tabelka()
        self.manager.get_screen("glowna").ids.glowny_input_text.text = ""



class KomplementarnaScreen(Screen):
    def tabelka(self):
        layout = AnchorLayout()

        column_data, row_data = get_data_table(df_komplementarna)
        column_data = [(x, dp(60)) for x in column_data]

        self.table = MDDataTable(
            pos_hint={'center_y': 0.5, 'center_x': 0.5},
            size_hint=(0.9, 0.6),
            # check=True,
            column_data=column_data,
            row_data=row_data,
            use_pagination=True,
            rows_num=100
        )
        self.table.bind(on_check_press=self.checked)
        self.table.bind(on_row_press=self.row_checked)

        self.add_widget(self.table)

        return layout

    def on_enter(self):
        self.tabelka()

    def checked(self, instance_table, current_row):


        self.manager.get_screen("wynik").ids.label_wynik_2.text = str(current_row[0])


    def row_checked(self, instance_table, instance_row):


        if instance_row.ids.check.state == 'normal':
            instance_row.ids.check.state = 'down'
            sm.current = "wynik"  # przejście na nowy ekran

        else:
            instance_row.ids.check.state = 'normal'

    def popup(self):
        show = P()

        if self.manager.get_screen("komplementarna").ids.kom_input_text.text == "":
            Popup(size_hint=(None, None), size=(400, 400), title="BŁĄD", auto_dismiss=True, content=show).open()  # wyświetlenie komunikatu o błędzie
        else:
            wynik_komplemanatrny(self.manager.get_screen("komplementarna").ids.kom_input_text.text)
            self.clear_widgets(self.children[:1])  # usuwanie tabelki (self.tabelka())
            self.tabelka()

        self.manager.get_screen("komplementarna").ids.kom_input_text.text = ""


class WynikScreen(Screen):

    def sprawdzenie(self):
        kategora_wynik = wybrana_lista_2(self.manager.get_screen("wynik").ids.label_wynik_1.text)
        kategora_wynik_kom = wynik_komplemanatrny_2(self.manager.get_screen("wynik").ids.label_wynik_2.text)

        wynik_loop=[]
        for i in range(len(kategora_wynik)):
            val_1=(kategora_wynik.iloc[i, 0])
            # print (val_1)
            if val_1 not in kategora_wynik_kom.values:
                x=(f"nie zaliczone dla {val_1}")
                wynik_loop.append(x)
            else:
                x=(f"zaliczone dla  {val_1}")
                wynik_loop.append(x)




        # self.manager.get_screen("wynik").ids.label_wynik_3.text = str(wynik_loop)
        self.manager.get_screen("wynik").ids.label_wynik_4.text = ('\n'.join(str(e) for e in wynik_loop))




    def on_enter(self):
        self.sprawdzenie()

class NaukaScreen1(Screen):
    def tabelka(self):
        layout = AnchorLayout()

        column_data, row_data = get_data_table(df_nauka_g)
        column_data = [(x, dp(60)) for x in column_data]

        self.table = MDDataTable(
            pos_hint={'center_y': 0.5, 'center_x': 0.5},
            size_hint=(0.9, 0.6),
            # check=True,
            column_data=column_data,
            row_data=row_data,
            use_pagination=True,
            rows_num=100
        )

        self.table.bind(on_check_press=self.checked)
        self.table.bind(on_row_press=self.row_checked)

        self.add_widget(self.table)

        return layout

    def on_enter(self):
        self.tabelka()

    def checked(self, instance_table, current_row):
        self.manager.get_screen("nauka2").ids.label_kom.text = str(current_row[0])
        global nauka_kat
        nauka_kat = (str(current_row[1]))
        global df_nauka_k
        df_nauka_k = df_kom
        df_nauka_k = df_nauka_k[df_nauka_k["KATEGORIA"].str.contains(nauka_kat, flags=re.IGNORECASE, regex=True)]

    def row_checked(self, instance_table, instance_row):
        # print(instance_table, instance_row)


        if instance_row.ids.check.state == 'normal':
            instance_row.ids.check.state = 'down'
            sm.current = "nauka2"  # przejście na nowy ekran

        else:
            instance_row.ids.check.state = 'normal'

    def popup(self):
        show = P()

        if self.manager.get_screen("nauka1").ids.glowny_input_text.text == "":
            Popup(size_hint=(None, None), size=(400, 400), title="BŁĄD", auto_dismiss=True,
                  content=show).open()  # wyświetlenie komunikatu o błędzie
        else:
            cala_lista(self.manager.get_screen("nauka1").ids.glowny_input_text.text)
            self.clear_widgets(self.children[:1])  # usuwanie tabelki (self.tabelka())
            self.tabelka()
        self.manager.get_screen("nauka1").ids.glowny_input_text.text = ""
class NaukaScreen2(Screen):
    def tabelka(self):
        layout = AnchorLayout()

        column_data, row_data = get_data_table(df_nauka_k)
        column_data = [(x, dp(60)) for x in column_data]

        self.table = MDDataTable(
            pos_hint={'center_y': 0.5, 'center_x': 0.5},
            size_hint=(0.9, 0.6),
            # check=True,
            column_data=column_data,
            row_data=row_data,
            use_pagination=True,
            rows_num=100
        )
        # self.table.bind(on_check_press=self.checked)
        # self.table.bind(on_row_press=self.row_checked)

        self.add_widget(self.table)

        return layout

    def on_enter(self):
        self.tabelka()

    # def checked(self, instance_table, current_row):
    #
    #     self.manager.get_screen("wynik").ids.label_wynik_2.text = str(current_row[0])
    #
    # def row_checked(self, instance_table, instance_row):
    #
    #     if instance_row.ids.check.state == 'normal':
    #         instance_row.ids.check.state = 'down'
    #         sm.current = "wynik"  # przejście na nowy ekran
    #
    #     else:
    #         instance_row.ids.check.state = 'normal'

    def popup(self):
        show = P()

        if self.manager.get_screen("nauka2").ids.kom_input_text.text == "":
            Popup(size_hint=(None, None), size=(400, 400), title="BŁĄD", auto_dismiss=True,
                  content=show).open()  # wyświetlenie komunikatu o błędzie
        else:
            nauka_komp(self.manager.get_screen("nauka2").ids.kom_input_text.text)
            self.clear_widgets(self.children[:1])  # usuwanie tabelki (self.tabelka())
            self.tabelka()

        self.manager.get_screen("nauka2").ids.kom_input_text.text = ""

sm = ScreenManager()


class DemoApp(MDApp):

    def build(self):

        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(GlownaScreen(name='glowna'))
        sm.add_widget(KomplementarnaScreen(name='komplementarna'))
        sm.add_widget(WynikScreen(name='wynik'))
        sm.add_widget(NaukaScreen1(name='nauka1'))
        sm.add_widget(NaukaScreen2(name='nauka2'))

        return sm


if __name__ == '__main__':
    DemoApp().run()
