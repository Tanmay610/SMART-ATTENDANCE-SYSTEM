
from pymongo import MongoClient
import pandas as pd

class database:
    def __init__(self):
        self.client=MongoClient()
        self.db=self.client.students

    def update(self,name,lecture):
        if(lecture=='1'):
            self.db.Hindi.update_one({"Name":name},{"$inc":{"Attendance":1}})
        else:
            self.db.English.update_one({"Name":name},{"$inc":{"Attendance":1}})

    def export_csv(self,lecture):
        df=pd.DataFrame(columns=["Roll Number","Name","Attendance"])

        if(lecture=='1'):
            records=self.db.Hindi.find()
            Temp_name="Hindi"
            path="Hindi_attendance/"
        else:
            records=self.db.English.find()
            Temp_name="English"
            path="English_attendance/"


        rows = []
        for i in records:
            rows.append({
                "Roll Number": i.get("Roll_number", ""),
                "Name": i.get("Name", ""),
                "Attendance": i.get("Attendance", 0)
            })
        if rows:
            df = pd.DataFrame(rows)
        CSV_Name=path+Temp_name+"_Attendance.csv"
        df.to_csv(CSV_Name,index=True)
   
