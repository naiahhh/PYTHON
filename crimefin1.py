# create a crimanal information system
# CRUD functions: insert, update, delete, search, save, fetch/view all, clear, get_cur, add_to_main, upload_img
# GUI: tkinter, ttk, Combobox, messagebox, askstring, font, Image, ImageTk, filedialog
# Database: pymysql
# Table: db name = dbcrime, table name = tblcrime
# verification: criminal ID must be a number, at least 6 digits, unique
#               name, location, crime type must be alphabetic
#               must upload an image before adding
# Sorting: by criminal ID in ascending order

from tkinter import *
from tkinter import ttk
from tkinter.ttk import Combobox
from tkinter import messagebox
import pymysql
from tkinter.simpledialog import askstring
from tkinter import font
from PIL import Image, ImageTk
from tkinter import filedialog

# Define a class for Criminal Information System
class Criminal:
    
    # CRUD functions
    
     # Function to insert criminal information
    def insert_criminal(self):
        self.wn.withdraw()  # Hide the main window
        
        # Function to upload image
        def upload_img():
            filename = filedialog.askopenfilename(initialdir='/img', title='Select Image', filetypes=(('jpeg files', '*.jpg'), ('all files', '*.*')))
            if filename:
                img = Image.open(filename)
                img = img.resize((170, 170), Image.LANCZOS)
                img = ImageTk.PhotoImage(img)
                img_square.config(image=img)
                img_square.image = img   
                   
        # Function to add criminal information to the main database
        def add_to_main():
            
            if entry_criminal_id.get() == '':
                messagebox.showerror('Error', 'Criminal ID is required')
            elif not img_square.cget('image'):
                messagebox.showerror('Error', 'Please upload an image')
            else:
                try:
                    conn = pymysql.connect(host='localhost', user='root', password='', db='dbcrime')
                    cur = conn.cursor()
                    cur.connection.ping()
                    if not entry_criminal_id.get().isdigit():
                        messagebox.showerror('Error', 'Criminal ID must be a number')
                        return
                    if len(entry_criminal_id.get()) < 6:
                        messagebox.showerror('Error', 'Criminal ID must be at least 6 digits')
                        return
                    if not entry_name.get().isalpha():
                        messagebox.showerror('Error', 'Name must be alphabetic')
                        return
                    if not entry_location.get().isalpha():
                        messagebox.showerror('Error', 'Location must be alphabetic')
                        return
                    if not entry_crime_type.get().isalpha():
                        messagebox.showerror('Error', 'Crime Type must be alphabetic')
                        return
                    
                    # Check if criminal ID already exists
                    cur.execute('SELECT * FROM tblcrime WHERE `CRIMINAL ID`=%s', (entry_criminal_id.get(),))
                    exist = cur.fetchone()
                    if exist:
                        conn.close()
                        messagebox.showerror('Error', 'Criminal ID already exists. Please use another ID.')
                        return
                    
                    # Insert criminal information into the database
                    cur.execute('INSERT INTO tblcrime VALUES(%s,%s,%s,%s,%s,%s)',
                                (entry_criminal_id.get().upper(),
                                entry_name.get().upper(),
                                cb_entry_gender.get().upper(),
                                entry_location.get().upper(),
                                entry_crime_type.get().upper(),
                                cb_entry_status.get().upper()))
                    conn.commit()
                    self.fetch_criminal()
                    self.clear()
                    conn.close()
                    messagebox.showinfo('Success', 'Criminal Information Added Successfully')
                    add_window.destroy()  # Close the add_window after adding
                    self.wn.deiconify()  # Show the main window again
                except Exception as e:
                    messagebox.showerror('Error', f'Error due to: {str(e)}')
                    
        # Create a new window for adding criminal information
        add_window = Toplevel()  # Create a new window
        add_window.title('Add Criminal')
        add_window.geometry('680x490')
        add_window.configure(bg='white')
        add_window.resizable(False, False)
        
        # Header Label
        lbl_header = Label(add_window, text='WINX CLUB DISTRICT', font=('Arial', 20, 'bold'), height='2', width='100',
                        bg='black', fg='white', relief=RIDGE)
        lbl_header.pack(pady=10)
        
        # Left Frame for Image and Upload Button
        left_frame = Frame(add_window, bd=2, relief=RIDGE, bg='black')
        left_frame.place(x=0, y=80, width=280, height=420)

        img_square = Label(left_frame, bg='white', relief=RIDGE)
        img_square.place(x=60, y=50, width=170, height=170)
        upload_btn = Button(left_frame, text='UPLOAD IMAGE', font=self.wn_font, bg='black', fg='white', relief=RIDGE, command=upload_img)
        upload_btn.place(x=70, y=240, width=150, height=50)
        
        # Add and Clear Buttons
        add_btn = Button(add_window, text='ADD', font=('Arial', 10, 'bold'), bg='black', fg='white', relief=RIDGE,
                        command=add_to_main)  
        clear_btn = Button(add_window, text='CLEAR', font=('Arial', 10, 'bold'), bg='black', fg='white', relief=RIDGE,
                        command=self.clear)
        add_btn.place(x=460, y=435, width=100, height=40)
        clear_btn.place(x=570, y=435, width=100, height=40)

        # Upper Frame for entering criminal information
        upper_frame = LabelFrame(add_window, text='Add Criminal Information', bd=2, relief=RIDGE, bg='white', fg='black')
        upper_frame.place(x=290, y=90, width=380, height=200)

        lbl_criminal_id = Label(upper_frame, text='CRIMINAL ID', font=self.wn_font, bg='white', fg='black')
        lbl_name = Label(upper_frame, text='NAME', font=self.wn_font, bg='white', fg='black')
        lbl_gender = Label(upper_frame, text='GENDER', font=self.wn_font, bg='white', fg='black')
        lbl_location = Label(upper_frame, text='LOCATION', font=self.wn_font, bg='white', fg='black')
        lbl_criminal_id.place(x=10, y=20)
        lbl_name.place(x=10, y=60)
        lbl_gender.place(x=10, y=100)
        lbl_location.place(x=10, y=140)

        entry_criminal_id = Entry(upper_frame, font=('Arial', 10), bd=2, relief=RIDGE)
        entry_name = Entry(upper_frame, font=('Arial', 10), bd=2, relief=RIDGE)
        cb_entry_gender = Combobox(upper_frame, values=('MALE', 'FEMALE'), font=('Arial', 10))
        entry_location = Entry(upper_frame, font=('Arial', 10), bd=2, relief=RIDGE)

        entry_criminal_id.place(x=150, y=20, width=200)
        entry_name.place(x=150, y=60, width=200)
        cb_entry_gender.place(x=150, y=100, width=200)
        entry_location.place(x=150, y=140, width=200)

        # Lower Frame for Crime Record
        lower_frame = LabelFrame(add_window, text='Add Crime Record', bd=2, relief=RIDGE, bg='white', fg='black')
        lower_frame.place(x=290, y=300, width=380, height=120)

        lbl_crime_type = Label(lower_frame, text='CRIME TYPE', font=self.wn_font, bg='white', fg='black')
        lbl_status = Label(lower_frame, text='STATUS', font=self.wn_font, bg='white', fg='black')
        lbl_crime_type.place(x=10, y=20)
        lbl_status.place(x=10, y=60)

        entry_crime_type = Entry(lower_frame, font=('Arial', 10), bd=2, relief=RIDGE)
        cb_entry_status = Combobox(lower_frame, values=('WANTED', 'CHARGED', 'CONVICTED', 'ACQUITTED'), font=('Arial', 10))
        entry_crime_type.place(x=150, y=20, width=200)
        cb_entry_status.place(x=150, y=60, width=200)
        
    # Function to search for criminal information  
    def search_criminal(self):
        search_field = self.cb_search.get()
        search_value = self.entry_value.get()

        if search_field:
            try:
                conn = pymysql.connect(host='localhost', user='root', password='', db='dbcrime')
                cur = conn.cursor()
                if search_field == "id":  # If searching by ID
                    search_value = int(search_value)  # Convert search_value to integer for exact match
                    cur.execute("SELECT * FROM tblcrime WHERE `id` = %s", (search_value,))
                elif search_field == "gender":  # If searching by gender
                    cur.execute("SELECT * FROM tblcrime WHERE `gender` = %s", (search_value,))
                else:  # For other fields, use exact match without wildcards
                    cur.execute(f"SELECT * FROM tblcrime WHERE `{search_field}` = %s", (search_value,))

                data = cur.fetchall()
                if len(data) != 0:
                    self.criminal_table.delete(*self.criminal_table.get_children())
                    for row in data:
                        self.criminal_table.insert('', END, values=row)
                    conn.commit()
                else:
                    messagebox.showinfo('Information', f'No criminal found with the specified {search_field}.')
                conn.close()
            except pymysql.Error as e:
                messagebox.showerror('Error', f'Error connecting to database: {str(e)}')
            except Exception as e:
                messagebox.showerror('Error', f'Error: {str(e)}')
        else:
            messagebox.showerror('Error', 'Please select a search field from the dropdown.')
            
    # Function to save criminal information to a new table          
    def save_criminal(self):
        try:
            table_name = askstring("Enter Table Name", "Enter the name for the new table:")
            if not table_name:
                messagebox.showerror('Error', 'Table name cannot be empty')
                return

            conn = pymysql.connect(host='localhost', user='root', password='', db='dbcrime')
            cur = conn.cursor()

            create_table_query = f"""CREATE TABLE IF NOT EXISTS {table_name} (
                                Criminal_ID VARCHAR(255),
                                Name VARCHAR(255),
                                Gender VARCHAR(255),
                                Location VARCHAR(255),
                                Crime_Type VARCHAR(255),
                                Status VARCHAR(255)
                            )"""
            cur.execute(create_table_query)


            for record in self.criminal_table.get_children():
                values = self.criminal_table.item(record, 'values')
                cur.execute(f"INSERT INTO {table_name} (Criminal_ID, Name, Gender, Location, Crime_Type, Status) VALUES (%s, %s, %s, %s, %s, %s)",
                            (values[0], values[1], values[2], values[3], values[4], values[5]))

            conn.commit()
            conn.close()
            messagebox.showinfo('Success', f'Criminal Information Saved Successfully to table: {table_name}')

        except pymysql.Error as e:
            messagebox.showerror('Error', f'Error connecting to database: {str(e)}')
        except Exception as e:
            messagebox.showerror('Error', f'Error: {str(e)}')
  
    # Function to delete criminal information
    def delete_criminal(self):
        if self.criminal_id.get() == '':
            messagebox.showerror('Error', 'Criminal ID is required')
        else:
            try:
                dlt = messagebox.askyesno('Delete', 'Do you want to delete this record?')
                if dlt:
                    conn = pymysql.connect(host='localhost', user='root', password='', db='dbcrime')
                    cur = conn.cursor()
                    cur.connection.ping()
                    sql='DELETE FROM tblcrime WHERE `CRIMINAL ID`=%s'
                    value=(self.criminal_id.get(),)
                    cur.execute(sql, value)
                else:
                    if not dlt:
                        return
                conn.commit()
                self.fetch_criminal()
                self.clear()
                conn.close()
                messagebox.showinfo('Success', 'Criminal Information Deleted Successfully')
            except Exception as e:
                messagebox.showerror('Error', f'Error due to: {str(e)}')
            
    # Function to update criminal information
    def update_criminal(self):
        if self.criminal_id.get() == '':
            messagebox.showerror('Error', 'Please select a record to update.')
        else:
            try:
                conn = pymysql.connect(host='localhost', user='root', password='', db='dbcrime')
                cur = conn.cursor()
                cur.execute('UPDATE tblcrime SET NAME=%s, GENDER=%s, LOCATION=%s, `CRIME TYPE`=%s, STATUS=%s WHERE `CRIMINAL ID`=%s',
                        (
                        self.name.get(),
                        self.gender.get(),
                        self.location.get(),
                        self.crime_type.get(),
                        self.status.get(),
                        self.criminal_id.get()))
                conn.commit()
                self.fetch_criminal()  
                conn.close()
                messagebox.showinfo('Success', 'Criminal Information Updated Successfully')
                
            except Exception as e:
                messagebox.showerror('Error', f'Error due to: {str(e)}')                            
    
    # Function to clear criminal information
    def clear(self):
        self.criminal_id.set('')
        self.name.set('')
        self.gender.set('')
        self.location.set('')
        self.crime_type.set('')
        self.status.set('')
       
    # Function to fetch criminal information         
    def fetch_criminal(self):
        conn = pymysql.connect(host = 'localhost', user = 'root',password = '',db = 'dbcrime' )
        cur = conn.cursor()
        cur.connection.ping()
        cur.execute('SELECT * FROM tblcrime ORDER BY `CRIMINAL ID` ASC')
        data = cur.fetchall()
        if len(data) != 0:
            self.criminal_table.delete(*self.criminal_table.get_children())
            for row in data:
                self.criminal_table.insert('', END, values=row)
            conn.commit()
        conn.close()
        
    # Function to get current data when clicked
    def get_cur(self, event=''):
        cursor_row = self.criminal_table.focus()
        content = self.criminal_table.item(cursor_row)
        row = content['values']
        self.criminal_id.set(row[0])
        self.name.set(row[1])
        self.gender.set(row[2])
        self.location.set(row[3])
        self.crime_type.set(row[4])
        self.status.set(row[5])
        
    # Initialize the Criminal Information System
    def __init__ (self,wn):
        self.wn = wn
        self.wn.title('Criminal Information System')
        self.wn.geometry('900x540+100+100')
        self.wn.configure(bg='white')
        self.wn.resizable(False, False)
        self.wn_font = wn_font = ('Arial', 11, 'bold')

        # Variables to hold data
        self.criminal_id = StringVar()
        self.name = StringVar()
        self.gender = StringVar()
        self.location = StringVar()
        self.crime_type = StringVar()
        self.status = StringVar()
        self.cb_search = ''
        self.entry_value = ''
        
        # Header
        lbl_header = Label(wn, text='CRIMINAL INFORMATION SYSTEM', font=('Arial', 20, 'bold'), height='2',width= '100', bg='black', fg='white')
        lbl_header.pack(pady=10)

        # Left frame for information
        left_frame = Frame(wn, bd=2,relief=RIDGE, bg='black')
        left_frame.place(x=0, y=80, width=320, height=520)
        info_title = Label(wn, text='WINX CLUB DISTRICT', font=('Arial', 19, 'bold'), bg='black', fg='gray')
        info_title.place(x=25, y=105)
        info_title = Label(wn, text='CRIMINAL ID', font=wn_font, bg='black', fg='gray')
        info_title.place(x=20, y=170)
        info_title = Label(wn, text='NAME', font=wn_font,  bg='black',fg='gray')
        info_title.place(x=20, y=220)
        info_title = Label(wn, text='GENDER', font=wn_font, bg='black', fg='gray')
        info_title.place(x=20, y=270)
        info_title = Label(wn, text='LOCATION', font=wn_font, bg='black', fg='gray')
        info_title.place(x=20, y=325)
        info_title = Label(wn, text='CRIME TYPE', font=wn_font, bg='black', fg='gray')
        info_title.place(x=20, y=375)
        info_title = Label(wn, text='STATUS', font=wn_font,  bg='black', fg='gray')
        info_title.place(x=20, y=425)

        # Entry fields for criminal information
        entry_id = Entry(wn, font=('Arial', 10), textvariable=self.criminal_id, bd=2,relief=RIDGE,width=22)
        entry_id.place(x=140, y=165, height=30)
        entry_name = Entry(wn, font=('Arial', 10),textvariable=self.name, bd=2,relief=RIDGE, width=22)
        entry_name.place(x=140, y=215, height=30)
        cb_gender = Combobox(wn, values=('FEMALE', 'MALE'), textvariable=self.gender, font=('Arial', 10), width=20)
        cb_gender.place(x=140, y=266, height=30)
        entry_location = Entry(wn, font=('Arial', 10), textvariable=self.location, bd=2,relief=RIDGE, width=22)
        entry_location.place(x=140, y=319, height=30)
        entry_crime_type = Entry(wn, font=('Arial', 10), textvariable=self.crime_type, bd=2,relief=RIDGE, width=22)
        entry_crime_type.place(x=140, y=372, height=30)
        cb_status = Combobox(wn, values=('WANTED', 'CHARGED','CONVICTED', 'ACQUITTED'), font=('Arial', 10), textvariable=self.status, width=20)
        cb_status.place(x=140, y=425, height=30)

        # Search and View
        self.cb_search = Combobox(wn, value=('CRIMINAL ID', 'NAME', 'GENDER', 'LOCATION', 'CRIME TYPE', 'STATUS'), font=('Arial', 10), width=25)
        self.cb_search.place(x=328, y=105, width=180, height=30)
        self.entry_value = Entry(wn, font=('Arial', 10), bd=2, relief=RIDGE, width=15)
        self.entry_value.place(x=525, y=105, width=130, height=30)
        self.search_btn = Button(wn, text='SEARCH', font=self.wn_font, bg='black', fg='white', bd=2, relief=RIDGE, width=10, command=self.search_criminal)
        self.search_btn.place(x=670, y=100, width=100, height=38)
        view_btn = Button(wn, text='VIEW ALL', font=self.wn_font, bg='black', fg='white', bd=2, relief=RIDGE, width=10, command=self.fetch_criminal)
        view_btn.place(x=785, y=100, width=100, height=38)
        
        # Main frame for displaying criminal records
        main_frame = Frame(wn, bd=3,relief=RIDGE, bg='white')
        main_frame.place(x=325, y=160, width=565, height=300)

        scroll_x = ttk.Scrollbar(main_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(main_frame, orient=VERTICAL)
        self.criminal_table = ttk.Treeview(main_frame, column=('1', '2', '3', '4', '5', '6'), 
                                        xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.criminal_table.xview)
        scroll_y.config(command=self.criminal_table.yview)
        
        self.criminal_table.heading('1', text='CRIMINAL ID')
        self.criminal_table.heading('2', text='NAME')
        self.criminal_table.heading('3', text='GENDER')
        self.criminal_table.heading('4', text='LOCATION')
        self.criminal_table.heading('5', text='CRIME TYPE')
        self.criminal_table.heading('6', text='STATUS') 
        
        self.criminal_table['show'] = 'headings'
        self.criminal_table.column('1', width=150)
        self.criminal_table.column('2', width=150)
        self.criminal_table.column('3', width=150)
        self.criminal_table.column('4', width=150)
        self.criminal_table.column('5', width=150)
        self.criminal_table.column('6', width=150)
        self.criminal_table.pack(fill=BOTH, expand=1)
        
        # Get current data when clicked
        self.criminal_table.bind('<ButtonRelease-1>', self.get_cur)
        self.fetch_criminal()
        
        # CRUD buttons
        clear_btn = Button(wn, text='CLEAR', font=wn_font, bg='black', fg='white', bd=2,relief=RIDGE, width=8, command=self.clear)   
        clear_btn.place(x=202, y=480, width=100, height=40)
        update_btn = Button(wn, text='UPDATE', font=wn_font, bg='black', fg='white', bd=2,relief=RIDGE, width=10, command=self.update_criminal)
        update_btn.place(x=555, y=480, width=100, height=40)
        delete_btn = Button(wn, text='DELETE', font=wn_font, bg='black', fg='white', bd=2,relief=RIDGE, width=10, command=self.delete_criminal)
        delete_btn.place(x=670, y=480, width=100, height=40)
        save_btn = Button(wn, text='SAVE', font=wn_font, bg='black', fg='white', bd=2,relief=RIDGE, width=10, command=self.save_criminal)
        save_btn.place(x=785, y=480, width=100, height=40 )
        insert_btn = Button(wn, text='INSERT', font=wn_font, bg='black', fg='white', bd=2,relief=RIDGE, width=10, command=self.insert_criminal)
        insert_btn.place(x=440, y=480, width=100, height=40)
        
# Main
if __name__ == '__main__':
    wn = Tk()
    obj = Criminal(wn) # object of the class
    wn.mainloop()






