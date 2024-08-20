import smtplib
import tkinter as tk
from Customwidgets import Drag_and_Drop_Listbox
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import formatdate
from email import encoders  
import base64
import os

class MailSetup:
    def __init__(self,smtp_domain=None,smtp_port=None,sender_email=None,password=None,receive_email=None):
        self.smtp_domain = smtp_domain
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.receive_email = receive_email
        self.password = password
        pass
    

    def get_domain(self):
        return self.smtp_domain

    def get_port(self):
        return self.smtp_port

    def get_sender_email(self):
        return self.sender_email

    def get_receive_email(self):
        return self.receive_email
    
    def get_password(self):
        return self.password
    
    def set_domain(self,smtp_domain):
        self.smtp_domain = smtp_domain

    def set_port(self,smtp_port):
        self.smtp_port = smtp_port

    def set_sender_email(self,sender_email):
        self.sender_email = sender_email

    def set_receive_email(self,receive_email):
        self.receive_email = receive_email

    def set_password(self,password):
        self.password = password

    def domain_setup(self,sender_email,password,receive_email):

        if "@gmail.com" in sender_email:
            self.smtp_domain = "smtp.gmail.com"
            self.smtp_port = 587

        elif "@outlook.com" in sender_email:
            self.smtp_domain = "smtp.office365.com"
            self.smtp_port = 587

        elif "@yahoo.com" in sender_email:
            self.smtp_domain = "smtp.mail.yahoo.com"
            self.smtp_port = 587

        elif "@aol.com" in sender_email:
            self.smtp_domain = "smtp.aol.com"
            self.smtp_port = 587

        elif "@icloud.com" in sender_email:
            self.smtp_domain = "smtp.mail.me.com"
            self.smtp_port = 587

        self.sender_email = sender_email
        self.password = password
        self.receive_email = receive_email

        encoded_password = base64.b64encode(self.get_password().encode('utf-8'))
        with open("usersetup.txt","wb") as f:
            f.write(self.get_sender_email().encode('utf-8')+b'\n')
            f.write(encoded_password+b"\n")
            f.write(self.smtp_domain.encode('utf-8')+b'\n')
            f.write(str(self.smtp_port).encode('utf-8')+b'\n')
            f.write(self.receive_email.encode('utf-8')+b'\n')

class App(tk.Tk):
    def __init__(self,useremail=None,password=None,smtp_domain=None,smtp_port=None,receiver_email=None):
        super().__init__()
        self.title("Send To")
        self.geometry("1080x720")
        self.resizable(False, False)
        self.colors = {"bg1":"#343A40","fg1":"white","bg2":"#DEE2E6","fg2":"black","white":"white","black":"#212529"}
        self.topframe = tk.Frame(self,bg=self.colors["bg1"])
        self.topframe.pack(side="top",fill="both",expand=True)
        self.topleftframe = tk.Frame(self.topframe,bg=self.colors["bg1"])
        self.topleftframe.pack(side="left",fill="both",expand=True,pady=(20,0))
        self.toprightframe = tk.Frame(self.topframe,bg=self.colors["bg1"])
        self.toprightframe.pack(side="right",fill="both",expand=True,ipadx=30)
        self.bottomframe = tk.Frame(self,bg=self.colors["black"])
        self.bottomframe.pack(side="bottom",fill="both",expand=True,ipady=50) 
        self.usersetup = MailSetup(smtp_domain,smtp_port,useremail,password,receiver_email) 


        
        #Log section

        self.logframe = tk.Frame(self.bottomframe,bg=self.colors["black"])
        self.logframe.pack(side="top",anchor="nw",padx=0,pady=0,fill="both",expand=True)
        self.logfield = tk.Text(self.logframe,bg=self.colors["black"],fg=self.colors["fg1"],highlightthickness=1,highlightbackground=self.colors["white"],width=100)
        self.logfield.pack(side="top",anchor="nw",padx=0,pady=0,fill="both",expand=True,ipady=20)

        
        def log(message):

            #check if bottom line is full and delete , else insert the text
            print(message)
            if int(self.logfield.index('end-1c').split('.')[0]) > 7:
                self.logfield.delete("1.0","2.0")
                self.logfield.insert("end", message+ '\n')

            else:
                self.logfield.insert("end",message + '\n')


        self.yourinfolbl = tk.Label(self.topleftframe,text="Your info: ",bg=self.colors["bg1"],fg=self.colors["fg1"],font=("Arial",20,"bold"))
        self.yourinfolbl.pack(side="top",anchor="nw",padx=0,pady=20)
        self.mailframe = tk.Frame(self.topleftframe,bg=self.colors["bg1"])
        self.mailframe.pack(side="top",anchor="nw",padx=(30,0),pady=10)
        self.maillabel = tk.Label(self.mailframe,text="Your Email: ",bg=self.colors["bg1"],fg=self.colors["fg1"])
        self.maillabel.pack(side="left")
        self.mailentry = tk.Entry(self.mailframe,bg=self.colors["bg1"],fg=self.colors["fg1"],highlightthickness=1,highlightbackground=self.colors["white"],width=28)
        self.mailentry.pack(side="left")
        self.mailentry.insert(0,self.usersetup.sender_email)
        


    
        self.passwordframe = tk.Frame(self.topleftframe,bg=self.colors["bg1"])
        self.passwordframe.pack(side="top",anchor="nw",padx=(30,0),pady=5)
        self.passwordlabel = tk.Label(self.passwordframe,text="Email password: ",bg=self.colors["bg1"],fg=self.colors["fg1"])
        self.passwordlabel.pack(side="left")
        self.passwordentry = tk.Entry(self.passwordframe,bg=self.colors["bg1"],fg=self.colors["fg1"],highlightthickness=1,highlightbackground=self.colors["white"],width=24)
        self.passwordentry.pack(side="left")
        self.passwordentry.insert(0,self.usersetup.password)
        




        def setuserinfo(self):
            log('Setting and storing user info to usersetup.txt...')
            password = self.passwordentry.get()
            senderemail = self.mailentry.get()
            
            self.usersetup.domain_setup(senderemail,password,self.receiverentry.get())
            log(f"Sender email:{self.usersetup.get_sender_email()} set successfully")
            log(f"Sender password:{self.usersetup.get_password()} set successfully")
            log(f"Receiver email:{self.usersetup.receive_eemail} set successfully")
            pass
            
        
        def showhelp(self):
            helpmessage = """Welcome to Sendto a gui interface to send files from one email to another.\n
            This was made with the intention of sending files to kindle devices \n but it can be used for any type of file. \n
            It requires an smtp server to send the emails. \n
            It requires an email and password to send the emails. \n
            It also requires an email to receive the files. \n
            Your email and password will be stored in usersetup.txt. \n
            **Important** If you use a gmail account, you will need to get an app password. \n
            You can get one for free at https://myaccount.google.com/apppasswords 
            Once you have an app password, enter it in the app password field. \n
            Afterwards set the information and it will be stored in usersetup.txt. \n
            
            App binds: \n
            Double click the queue to remove files from queue. \n
            """
            helpwindow = tk.Toplevel(self)
            helpwindow.title("Help")
            helpwindow.geometry("700x700")
            helpwindow.resizable(False, False)
            helpwindow.configure(bg=self.colors["bg1"])

            helpframe = tk.Frame(helpwindow,bg=self.colors["bg1"])
            helpframe.pack(side="top",anchor="nw",padx=0,pady=0,fill="both",expand=True)

            helptext = tk.Label(helpframe,bg=self.colors["bg1"],text=helpmessage,fg=self.colors["fg1"],highlightthickness=1,highlightbackground=self.colors["white"],width=100)
            helptext.pack(side="top",anchor="nw",padx=0,pady=0,fill="both",expand=True,ipady=20)



        self.setinfo = tk.Button(self.topleftframe,text="Set",bg=self.colors["bg1"],fg=self.colors["fg1"],width=35,command=lambda:setuserinfo(self))
        self.setinfo.pack(side="top",anchor="nw",padx=30,pady= (10,0))
        self.receiversectionlbl = tk.Label(self.topleftframe,text="Send to: ",bg=self.colors["bg1"],fg=self.colors["fg1"],font=("Arial",20,"bold"))
        self.receiversectionlbl.pack(side="top",anchor="nw",padx=0,pady=20)
        self.receiveremail = tk.Label(self.topleftframe,text="Receiver email: ",bg=self.colors["bg1"],fg=self.colors["fg1"])
        self.receiveremail.pack(side="left",anchor="nw",padx=0,pady=10)
        self.receiverentry = tk.Entry(self.topleftframe,bg=self.colors["bg1"],fg=self.colors["fg1"],highlightthickness=1,highlightbackground=self.colors["white"],width=28)
        self.receiverentry.insert(0,self.usersetup.receive_email)
        self.receiverentry.pack(side="top",anchor="nw",padx=0,pady=10)
        
        
        


        def sendmessage():
            log("Sending email")
            if type(self.usersetup.smtp_domain) == type(None)  or type(self.usersetup.smtp_port)== type(None):
                log("Configuring smtp-domain and sm-port")
                self.usersetup.domain_setup(self.usersetup.sender_email,self.usersetup.password,self.receiverentry.get())
            msg = MIMEMultipart()
            msg['From'] = self.usersetup.get_sender_email()
            msg['To'] = self.receiverentry.get()
            msg['Date'] = formatdate(localtime=True)
            msg['Subject'] = "Sendto: File sent"

            files = self.queue.get(0,'end')
            body = "Sendto: File sent from " + self.usersetup.get_sender_email()  

            msg.attach(MIMEText(body, 'plain'))
            log("Attaching files....")
            try:
                for file in files:
                    with open(file, "rb") as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())

                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename= {file}')
                    msg.attach(part)
            except:
                log("Failed to attach files")
            server = smtplib.SMTP(self.usersetup.smtp_domain, self.usersetup.smtp_port)
            log(f"Connecting to {self.usersetup.smtp_domain,self.usersetup.smtp_port}....")
            server.ehlo()
            server.starttls()
            server.ehlo()
            log(f"Logging in {self.usersetup.sender_email}:{self.usersetup.password}")
            server.login(self.usersetup.sender_email, self.usersetup.password)
            log("Login successful")
            log("Sending email....")
            server.sendmail(self.usersetup.sender_email, self.receiverentry.get(), msg.as_string())
            server.quit()
            log("Email sent successfully")
         

        self.sendbtn = tk.Button(self.topleftframe,text="Send",bg=self.colors["bg1"],fg=self.colors["fg1"],width=20,command=sendmessage)
        self.sendbtn.pack(side="left",anchor="nw",padx=0,pady=10)

           

        def select_file():
            filetypes = (
                ('epub files', '*.epub'),
                ('pdf files', '*.pdf'),
                ('mobi files', '*.mobi'),
                ('All files', '*.*')
            )

            filenames = fd.askopenfilenames(
                title='Open a file',
                initialdir='/',
                filetypes=filetypes)
            list_files = self.queue.get(0,'end')
            for file in filenames:
                if file not in list_files:
                    self.queue.insert('end',file)
            else:
                log("File already in queue")


        def addfile():
            if self.queuepathentry.get() == "":
                log("No file path provided")
            self.queue.insert('end',self.queuepathentry.get())
            self.queuepathentry.delete(0,'end')

        def removeValue(event):
            selection = self.queue.curselection()
 
            self.queue.delete(selection)

        self.queueframe = tk.Frame(self.toprightframe,bg=self.colors["bg1"])
        self.queueframe.pack(side="top",anchor="nw",padx=(30,0),pady=10,fill="both",expand=True)

        self.lblhelpframe = tk.Frame(self.queueframe,bg=self.colors["bg1"])
        self.lblhelpframe.pack(side="top",padx=0,pady=10,fill="both",expand=True)
        self.queuelbl = tk.Label(self.lblhelpframe,text="Queue: ",bg=self.colors["bg1"],fg=self.colors["fg1"],font=("Arial",20,"bold"))
        self.queuelbl.pack(side="left",anchor="nw",padx=0,pady=20)
        self.queuepathentry = tk.Entry(self.queueframe,bg=self.colors["bg1"],fg=self.colors["fg1"],highlightthickness=1,highlightbackground=self.colors["white"],width=38)
        self.addbtn = tk.Button(self.queueframe,text="Add",bg=self.colors["bg1"],fg=self.colors["fg1"],width=2,command=addfile)
        
        self.browsepath = tk.Button(self.queueframe,text="Browse",bg=self.colors["bg1"],fg=self.colors["fg1"],width=4,command=select_file)
        self.queuepathentry.pack(side="left",anchor="nw",padx=(0,10),pady=10)
        self.addbtn.pack(side="left",anchor="nw",padx=(0,5),pady=10)
        self.browsepath.pack(side="left",anchor="nw",padx=(0,5),pady=10)

        
        self.queue = Drag_and_Drop_Listbox(self.toprightframe,bg=self.colors["bg1"],fg=self.colors["fg1"],highlightthickness=1,highlightbackground=self.colors["white"],width=50,height=15)
        self.queue.pack(side="top",anchor="nw",padx=(20,0),pady=15,expand=True,ipadx=45,ipady=0)
        self.queue.bind("<Double-Button-1>" , removeValue)
        self.queue.bind("<Button-3>" , removeValue)

        self.clearqueuebtn = tk.Button(self.queueframe,text="Clear",bg=self.colors["bg1"],fg=self.colors["fg1"],width=3,command=lambda: self.queue.delete(0,'end'))
        self.clearqueuebtn.pack(side="left",anchor="nw",pady=10)

        self.helpbutton = tk.Button(self.lblhelpframe,text="Help",bg=self.colors["bg1"],fg=self.colors["fg1"],width=2,command=lambda:showhelp(self))
        self.helpbutton.pack(side="right",anchor="ne",pady=(20,0),padx=(0,35))
        

        self.mainloop()


if os.path.exists("usersetup.txt"):
    try:
        with open("usersetup.txt","rb") as f:

            lines = f.readlines()
            if len(lines) < 5:
                app = App("test@test.com",0,receiver_email="test@test.com")
            sender_email = lines[0].strip().decode('utf-8')
            decoded_b_password = base64.b64decode(lines[1].strip())
            decode_s_password = decoded_b_password.decode('utf-8')
            password = decode_s_password
            smtp_domain = lines[2].strip().decode('utf-8')
            smtp_port = int(lines[3].strip())
            receiver_email = lines[4].strip().decode('utf-8')
            #usersetup = MailSetup(smtp_domain,smtp_port,sender_email,password,'None')

            app = App(sender_email,password,receiver_email=receiver_email)
    except RuntimeError:
        print("Failed to read user setup file")
        app = App("test@test.com",0,receiver_email="test@test.com")
else:
    app = App('test',0,receiver_email='test@test.com')

