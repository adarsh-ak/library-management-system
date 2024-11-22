############################################LIBRARY MANAGEMENT SYSTEM##############################################
############################################Languages:SQL and PYTHON###############################################



#Make sure to load the following libraries as
#find the python folder and find scripts in it and type cmd in address bar
#now load the the following libraries as by typing the mentioned commands in command prompts
#pip install mysql-connector-python
#pip install python-dateutil
#pip install DateTime
#pip install random2
#pip install tabulate
import mysql.connector as db
from dateutil.relativedelta import relativedelta
from datetime import datetime,date
import random
from tabulate import tabulate


##################################CONNECTING TO MYSQL SERVER###############################################
userid=input("Enter your username(SQL) ")
passid=input("Enter your password(SQL) ")
databas=input("Enter the database ")
con=db.connect(host="localhost",user=userid,passwd=passid,database=databas)
if con.is_connected()==False:
    print("Error!!! In connection")
cursor=con.cursor()
#U must create a database in  mysql before running this!!!

##################################To Create tables in my sql database###############################################
def tables():
    cursor.execute("""CREATE TABLE Books
                (SNo integer,
                BookName char(40),
                AuthorName char(40),
                BookCode integer,
                Available char(3)
                )""")
    cursor.execute("""CREATE TABLE Issuing 
                (SNo integer,
                IssuerName char(40),
                MemberCode integer,
                BookName char(40),
                BookCode integer,
                DateOfIssuing varchar(30),
                DueDate varchar(30),
                DateOfReturning varchar(30),
                Fine Integer
                )""")
    cursor.execute("""CREATE TABLE Members
                (MemberCode integer,
                MemberName char(40),
                DateOfJoining varchar(30),
                Duration integer,
                ExpDate varchar(30)
                )""")
    cursor.execute("""CREATE TABLE Membersinfo
                (MemberName char(40),
                Age integer,
                DateOfBirth varchar(30),
                Occupation char(15),
                Sex char(2)
                )""")
    cursor.execute("""CREATE TABLE Record
                (SNo integer,
                IssuerName char(40),
                MemberCode integer,
                BookName char(40),
                BookCode integer,
                DateOfIssuing varchar(30),
                DueDate varchar(30),
                DateOfReturning varchar(30),
                Fine Integer
                )""")
    cursor.execute("""CREATE TABLE Login
                (Date_time varchar(50),
                Activity char(50)
                )""")

##################################To add books in the record###############################################
def addbooks():
    while True:
        sno=random.randint(1,100000000)
        bookname=input("Enter the Book Name ")
        authorname=input("Enter the Author Name ")
        bookcode=random.randint(1,100000000)
        avai='Yes'
        rec=[(sno,bookname,authorname,bookcode,avai)]
        print(tabulate(rec,headers=['SNo','Book Name','Author Name','Book Code','Available'],tablefmt='psql'))
        sql="""INSERT INTO books(SNo,BookName,AuthorName,BookCode,available)
        VALUES({},'{}','{}',{},'{}')""".format(sno,bookname,authorname,bookcode,avai)
        cursor.execute(sql)
        con.commit()
        ch=input("Want to add more?(Y/N) ")
        if ch in "Nn":
            break
##################################To issue a new book##############################################
def issuebook():
    sno=random.randint(1,100000000)
    membercode=int(input("Enter the member code "))
    cursor.execute("select membercode from members")
    data=cursor.fetchall()
    lst=[]
    for i in data:
        for s in i:
            lst.append(s)
    if membercode in lst:
        bookcode=int(input("Enter the Book Code "))
        cursor.execute("select bookcode from issuing")
        data=cursor.fetchall()
        boco=[]
        for i in data:
            for s in i:
                boco.append(s)
        date_issue=date.today().strftime('%d-%m-%Y')
        dateofissue=str(date_issue)
        date_format='%d-%m-%Y'
        dtobj=datetime.strptime(dateofissue,date_format)
        due_date=dtobj+relativedelta(days=7)
        duedate=due_date.date().strftime('%d-%m-%Y')
        cursor.execute("SELECT bookname FROM books WHERE bookcode='%s'"%(bookcode))
        bookn=cursor.fetchall()
        bookname=bookn[0][0]
        mem="SELECT membername FROM members WHERE membercode='%s'"%(membercode)
        cursor.execute(mem)
        membern=cursor.fetchall()
        if bookcode in boco:
            rec="""UPDATE issuing SET sno='%s',membercode='%s',issuername='%s',DateOfIssuing='%s',duedate='%s'
            WHERE bookcode='%s'"""%(sno,membercode,membern[0][0],dateofissue,duedate,bookcode)
            cursor.execute(rec)
            con.commit()
        if bookcode not in boco:
            inrt="""INSERT INTO issuing(sno,issuername,membercode,bookname,bookcode,DateOfIssuing,duedate)
            values ({},'{}',{},'{}',{},'{}','{}')""".format(sno,membern[0][0],membercode,bookname,bookcode,dateofissue,duedate)
            cursor.execute(inrt)
            con.commit()
        rec_2=[(sno,membern[0][0],membercode,bookname,dateofissue,duedate)]
        print(tabulate(rec_2,headers=['SNo','Issuer Name','Member Code','Book Name','Date Of Issuing','Due Date'],tablefmt='psql'))
        ste="""INSERT INTO record(sno,issuername,membercode,bookname,bookcode,DateOfIssuing,
            duedate)values ({},'{}',{},'{}',{},'{}','{}')""".format(sno,membern[0][0],membercode,bookname,bookcode,dateofissue,duedate)
        cursor.execute(ste)
        con.commit()
        sql="UPDATE books SET available='No' WHERE bookcode='%s'"%(bookcode)
        cursor.execute(sql)
        con.commit()
    else:
        print("PLZ BE A MEMBER TO ISSUE THE BOOK")

##################################To get the number of days for the purpose of membership###############################################
def dayofyear(m):
    year=int(m[6:10])
    month=m[3:5]
    dat=int(m[0:2])
    day=0
    if month=='01':
        day=dat
    elif month=='02':
        day=31+dat
    elif month=='03':
        if year%4==0:
            day=60+dat
        else:
            day=59+dat
    elif month=='04':
        if year%4==0:
            day=91+dat
        else:
            day=90+dat
    elif month=='05':
        if year%4==0:
            day=121+dat
        else:
            day=120+dat
    elif month=='06':
        if year%4==0:
            day=152+dat
        else:
            day=151+dat
    elif month=='07':
        if year%4==0:
            day=182+dat
        else:
            day=181+dat
    elif month=='08':
        if year%4==0:
            day=213+dat
        else:
            day=212+dat
    elif month=='09':
        if year%4==0:
            day=244+dat
        else:
            day=243+dat
    elif month=='10':
        if year%4==0:
            day=274+dat
        else:
            day=273+dat
    elif month=='11':
        if year%4==0:
            day=305+dat
        else:
            day=304+dat
    elif month=='12':
        if year%4==0:
            day=335+dat
        else:
            day=334+dat
    year_day=int(day)
    return year_day

##################################To return a book###############################################
def returning():
    bookcode=int(input("Enter the Book Code "))
    curr_date=date.today().strftime('%d-%m-%Y')
    dat="SELECT duedate from issuing where bookcode='%s'"%(bookcode)
    cursor.execute(dat)
    due_date=cursor.fetchall()
    for i in due_date:
        for d in i:
            duedate=d
    day1=dayofyear(curr_date)
    day2=dayofyear(duedate)
    dayoffine=day1-day2
    fine=0;
    if dayoffine<0:
        fine=0;
    else:
        fine=dayoffine*5
    iss="DELETE FROM issuing WHERE bookcode='%s'"%(bookcode)
    cursor.execute(iss)
    con.commit()
    rec="UPDATE record SET DateOfReturning='%s',fine='%s' WHERE bookcode='%s'"%(curr_date,fine,bookcode)
    cursor.execute(iss)
    con.commit()
    sql="UPDATE books SET available='Yes' WHERE bookcode='%s'"%(bookcode)
    cursor.execute(sql)
    con.commit()

##################################Record of the returned book###############################################
def returned():
    bookcode=int(input("Plz Reenter the bookcode "))
    cursor.execute("SELECT sno,issuername,membercode,bookname,bookcode FROM record WHERE bookcode='%s'"%(bookcode))
    rec_2=cursor.fetchall()
    print(tabulate(rec_2,headers=['SNo','Issuer Name','Member Code','Book Name','Date Of Issuing','Due Date','Date Of Returning','Fine'],tablefmt='psql'))
    cursor.execute("SELECT membercode,bookcode,dateofissuing,duedate,dateofreturning,fine FROM record WHERE bookcode='%s'"%(bookcode))
    rec_3=cursor.fetchall()
    print(tabulate(rec_3,headers=['Member Code','Book Code','Date Of Issuing','Due Date','Date of Returning','Fine'],tablefmt='psql'))

##################################To feed the record of the new member###############################################
def membership():
    membercode=random.randint(1,10000000)
    membername=input("Enter the Member Name ")
    age=int(input("Enter the age "))
    dob=input("Enter the date of birth(DD-MM-YYYY) ")
    occu=input("Enter the occupation ")
    sex=input("Enter the sex(M/F/TG) ")
    membe=date.today().strftime('%d-%m-%Y')
    membershiptaken=str(membe)
    amtpaid=int(input("Enter the amount paid "))
    duration=int(amtpaid/50)
    date_format='%d-%m-%Y'
    dtobj=datetime.strptime(membershiptaken,date_format)
    futuredate=dtobj+relativedelta(months=duration)
    expdate=futuredate.date().strftime('%d-%m-%Y')
    inr="""INSERT INTO members (MemberCode,MemberName,dateofjoining,duration,expdate) VALUES
    ({},'{}','{}',{},'{}')""".format(membercode,membername,membershiptaken,duration,expdate)
    cursor.execute(inr)
    con.commit()
    inrt="""INSERT INTO membersinfo(MemberName,Age,dateofbirth,occupation,sex)
    VALUES ('{}',{},'{}','{}','{}')""".format(membername,age,dob,occu,sex)
    cursor.execute(inrt)
    con.commit()
    cursor.execute("SELECT * from members where membercode='%s'"%(membercode))
    st=cursor.fetchall()
    print(tabulate(st,headers=['Member Code','Member Name','Date Of Joining','Duration','ExpDate'],tablefmt='psql'))
    cursor.execute("SELECT * from membersinfo where membername='%s'"%(membername))
    rec_2=cursor.fetchall()
    print(tabulate(rec_2,headers=['Member Name','Age','Date OF Birth','Occupation','Sex'],tablefmt='psql'))


##################################To check weather a book is available or not###############################################
def available():
    cursor.execute("SELECT * from books WHERE available='Yes'")
    stre=cursor.fetchall()
    print(tabulate(stre,headers=['SNo','Book Name','Author Name','Book Code','Avaiable'],tablefmt='psql'))


##################################Get table of issued book###############################################
def issued():
    cursor.execute("SELECT * from books WHERE available='No'")
    st=cursor.fetchall()
    print(tabulate(st,headers=['SNo','Book Name','Author Name','Book Code','Avaiable'],tablefmt='psql'))

##################################To fetch the record table###############################################    
def recd():
    cursor.execute("SELECT sno,issuername,membercode,bookname,bookcode FROM record")
    rec_2=cursor.fetchall()
    print(tabulate(rec_2,headers=['SNo','Issuer Name','Member Code','Book Name','Date Of Issuing','Due Date','Date Of Returning','Fine'],tablefmt='psql'))
    cursor.execute("SELECT membercode,bookcode,dateofissuing,duedate,dateofreturning,fine FROM record")
    rec_3=cursor.fetchall()
    print(tabulate(rec_3,headers=['Member Code','Book Code','Date Of Issuing','Due Date','Date of Returning','Fine'],tablefmt='psql'))

##################################Fetch the all books###############################################
def getbooks():
    cursor.execute("SELECT * from books")
    stre=cursor.fetchall()
    print(tabulate(stre,headers=['SNo','Book Name','Author Name','Book Code','Avaiable'],tablefmt='psql'))

##################################Fetch the issue details###############################################
def getissuing():
    cursor.execute("SELECT sno,issuername,membercode,bookname,bookcode,DateOfIssuing,duedate FROM issuing")
    st=cursor.fetchall()
    print(tabulate(st,headers=['SNo','Issuer Name','Member Code','Book Name','Book Code','Date Of Issuing','Due Date'],tablefmt='psql'))

##################################Fetch the record table###############################################  
def getrecord():
    cursor.execute("SELECT sno,issuername,membercode,bookname,bookcode FROM record")
    rec_2=cursor.fetchall()
    print(tabulate(rec_2,headers=['SNo','Issuer Name','Member Code','Book Name','Date Of Issuing','Due Date','Date Of Returning','Fine'],tablefmt='psql'))
    cursor.execute("SELECT membercode,bookcode,dateofissuing,duedate,dateofreturning,fine FROM record")
    rec_3=cursor.fetchall()
    print(tabulate(rec_3,headers=['Member Code','Book Code','Date Of Issuing','Due Date','Date of Returning','Fine'],tablefmt='psql'))

##################################Fetch the member table###############################################
def getmember():
    rec="SELECT MemberCode,members.Membername,DateOfJoining,Duration,ExpDate,Age,DateOfBirth,Occupation,Sex from members,membersinfo"
    cursor.execute(rec)
    st=cursor.fetchall()
    print(tabulate(st,headers=['Member Code','Member Name','Date Of Joining','Duration','ExpDate','Age','Date Of Birth','Occupation','Sex'],tablefmt='psql'))
    
##################################To delete a book from the record###############################################
def delete():
    bookcd=int(input("Enter the book code "))
    cursor.execute("SELECT * from books WHERE bookcode='%s'"%(bookcd))
    stre=cursor.fetchall()
    print(tabulate(stre,headers=['SNo','Book Name','Author Name','Book Code','Available'],tablefmt='psql'))
    sql="DELETE from books WHERE bookcode='%s'"%(bookcd)
    cursor.execute(sql)
    con.commit()
    
##################################To get the login details from very beginning###############################################  
def getlogin():
    cursor.execute("SELECT * FROM login")
    l=cursor.fetchall()
    print(tabulate(l,headers=['Date And Time','Activity'],tablefmt='psql'))

##################################The Menu to control the flow of execution###############################################
while True:
    print("""1. To create tables
2.Enter new book into database
3.Add members in library
4.To issue a book
5.Books available
6.Books issued
7.Return a book
8.Show whole record
9.Get database tables
10.Retrieve members details
11.Delete the book from library
12.Login details
13.To exit""")
    ch=int(input("Enter your choice "))
    if ch==1:
        print("***********************WELCOME**************************")
        tables()
        print("Tables created successfully!!!")
        curr=datetime.now().strftime('%d-%m-%y %H:%M:%S')
        act="Tables Created"
        sql2="INSERT INTO login values('{}','{}')".format(curr,act)
        cursor.execute(sql2)
        con.commit()

    elif ch==2:
        print("################ADD NEW BOOK##########################")
        addbooks()
        print("Data added in table added successfully")
        curr=datetime.now().strftime('%d-%m-%y %H:%M:%S')
        act="Added a new book"
        sql2="INSERT INTO login values('{}','{}')".format(curr,act)
        cursor.execute(sql2)
        con.commit()

    elif ch==3:
        print("################ADD MEMBER##########################")
        membership()
        print("Member added successfully!!!")
        curr=datetime.now().strftime('%d-%m-%y %H:%M:%S')
        act="Added member"
        sql2="INSERT INTO login values('{}','{}')".format(curr,act)
        cursor.execute(sql2)
        con.commit()

    elif ch==4:
        print("################ISSUE A BOOK##########################")
        issuebook()
        print("Details feeded successfully!!!")
        curr=datetime.now().strftime('%d-%m-%y %H:%M:%S')
        act="Issue a book"
        sql2="INSERT INTO login values('{}','{}')".format(curr,act)
        cursor.execute(sql2)
        con.commit()

    elif ch==5:
        print("################AVAILABLE BOOKS##########################")
        print("Available books in library are: ")
        available()
        curr=datetime.now().strftime('%d-%m-%y %H:%M:%S')
        act="Searched for available books"
        sql2="INSERT INTO login values('{}','{}')".format(curr,act)
        cursor.execute(sql2)
        con.commit()

    elif ch==6:
        print("################ISSUED BOOKS##########################")
        print("Details of issued books at present: ")
        issued()
        curr=datetime.now().strftime('%d-%m-%y %H:%M:%S')
        act="Searched for issued books"
        sql2="INSERT INTO login values('{}','{}')".format(curr,act)
        cursor.execute(sql2)
        con.commit()

    elif ch==7:
        print("################RETURN A BOOK##########################")
        returning()
        returned()
        print("Data feeded successfully")
        curr=datetime.now().strftime('%d-%m-%y %H:%M:%S')
        act="Returned a book"
        sql2="INSERT INTO login values('{}','{}')".format(curr,act)
        cursor.execute(sql2)
        con.commit()

    elif ch==8:
        print("################RECORD OF ISSUING##########################")
        recd()
        curr=datetime.now().strftime('%d-%m-%y %H:%M:%S')
        act="Requested for record"
        sql2="INSERT INTO login values('{}','{}')".format(curr,act)
        cursor.execute(sql2)
        con.commit()

    elif ch==9:
        print("################TABLES IN DATABASES##########################")
        print("Books are as follows: ")
        getbooks()
        print("Members are as follows: ")
        getmember()
        print("Issued books: ")
        getissuing()
        print("Record of all issues: ")
        getrecord()
        curr=datetime.now().strftime('%d-%m-%y %H:%M:%S')
        act="Requested to see database"
        sql2="INSERT INTO login values('{}','{}')".format(curr,act)
        cursor.execute(sql2)
        con.commit()


    elif ch==10:
        print("################MEMBERS DETAILS##########################")
        print("Member details are as follows: ")
        getmember()
        curr=datetime.now().strftime('%d-%m-%y %H:%M:%S')
        act="Search for members details"
        sql2="INSERT INTO login values('{}','{}')".format(curr,act)
        cursor.execute(sql2)
        con.commit()

    elif ch==11:
        print("################DELETE THE BOOK##########################")
        delete()
        print("Book Deleted")
        curr=datetime.now().strftime('%d-%m-%y %H:%M:%S')
        act="Deleted a book"
        sql2="INSERT INTO login values('{}','{}')".format(curr,act)
        cursor.execute(sql2)
        con.commit()

    elif ch==12:
        print("################LOGIN DETAILS##########################")
        getlogin()
        curr=datetime.now().strftime('%d-%m-%y %H:%M:%S')
        act="Requested login details"
        sql2="INSERT INTO login values('{}','{}')".format(curr,act)
        cursor.execute(sql2)
        con.commit()

    elif ch==13:
        print("THANK YOU!!!")
        curr=datetime.now().strftime('%d-%m-%y %H:%M:%S')
        act="Quited system"
        sql2="INSERT INTO login values('{}','{}')".format(curr,act)
        cursor.execute(sql2)
        con.commit()
        con.close()
        break
    else:
        print("PLZ! Enter the correct choice")
