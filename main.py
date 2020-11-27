from flask import Flask, render_template,request
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html"
    )
    
@app.route("/post",methods = ["POST","GET"])
def func():
    
    ##11連
    if "ren10" in request.form:
        result = Gacha(10)
        countData_list = CountData(10 + 1)
        rareCount_list = GetTxtData("rarecount")
        srpCount = GetTxtData("srpcount",mode = "str")
        message = SRpComplete()

    ##単発
    if "ren1" in request.form:
        result = Gacha(1)
        countData_list = CountData(1)
        rareCount_list = GetTxtData("rarecount")
        srpCount = GetTxtData("srpcount",mode = "str")
        message = SRpComplete()
    
    ##SR+を全種類揃えるまで    
    if "complete" in request.form:
        result = ""
        GachaComplete()
        countData_list = GetTxtData("count")
        rareCount_list = GetTxtData("rarecount")
        srpCount = GetTxtData("srpcount",mode = "str")
        message = SRpComplete()
    
    ##初期化    
    if "reset" in request.form:
        TextClear("count",4)
        TextClear("rarecount",6)
        TextClear("srpcount",1,str)
        result = ""
        countData_list = [0,0,0,0]
        rareCount_list = [0,0,0,0,0,0]
        srpCount = ""
        message = ""
        
    return render_template(
        "index.html",
        result = result,
        count = countData_list[0],
        money = countData_list[1],
        t_count = countData_list[2],
        ren_count = countData_list[3],
        N = rareCount_list[0],
        Np = rareCount_list[1],
        R = rareCount_list[2],
        Rp = rareCount_list[3],
        SR = rareCount_list[4],
        SRp = rareCount_list[5],
        srpcount = srpCount,
        message = message
        )
        
        
##関数

##ガチャを引く    
def Gacha(ren):
    result = []
    rare_list, rareWeight = RareSelect(ren)
    for i in range(ren):
        rare = random.choices(rare_list,rareWeight)
        result.append(ImageSelect(rare[0]))
        RareCountData(rare[0])
    if (ren == 10):
        result.append(ImageSelect("SR"))
        RareCountData("SR")
    return result
    

##SR+が全種類でるまでガチャを引く
def GachaComplete():
    while True:
        result = []
        rare_list, rareWeight = RareSelect(1)
        rare = random.choices(rare_list,rareWeight)
        result.append(ImageSelect(rare[0]))
        RareCountData(rare[0])
        CountData(1)
        temp = GetTxtData("srpcount",mode = "str")
        if (len(temp) == 10):
            break
        
    
##レアリティを設定    
def RareSelect(ren):
    if (ren == 1):
        rare_list = ["N","Np","R","Rp","SR","SRp"]
        rareWeight = [33, 25, 20, 15, 5, 2]
    if (ren == 10):
        rare_list = ["R","Rp","SR","SRp"]
        rareWeight = [57, 30, 10, 3]
    return rare_list, rareWeight
    
    
##画像を選択    
def ImageSelect(rare):
    rare_dic = {"N":42,"Np":42,"R":133,"Rp":98,"SR":24,"SRp":9}
    imageNum = random.randint(0,rare_dic[rare])
    imageName = "static/images/" + rare + "/" + rare + str(imageNum) + ".jpg"
    if (rare == "SRp"):
        SRpCount(imageName)
    return imageName
    
    
##金額とガチャ回数を保存
def CountData(num):
    list = GetTxtData("count")
    for i in range(num):
        list[0] += 1
        list[1] += 100
    if (num == 1):
        list[2] += 1
    else:
        list[1] -= 100
        list[3] += 1
    TextSave("count",3,list)
    return list


##レアリティごとの回数を保存
def RareCountData(rare):
    dic = {"N":0,"Np":1,"R":2,"Rp":3,"SR":4,"SRp":5}
    list = GetTxtData("rarecount")
    list[dic[rare]] += 1
    TextSave("rarecount",5,list)
    
 
##新しく引いたSR+を保存
def SRpCount(result):
    list = GetTxtData("srpcount",mode = "str")
    if (result in list):
        pass
    else:
        list.append(result)
    temp = "\n".join(list)
            
    with open("data/srpcount.txt", mode = "w") as f:
        f.write(temp)
    return list
    
    
##SR+が全種類揃ったらメッセージを返す
def SRpComplete():
    list = GetTxtData("srpcount",str)
    if (len(list) == 10):
        message = "SR+が全種類揃いました！"
    else:
        message = ""
    return message

    
##変数からパスを作成
def CreateDirectoryStr(fileName):
    return  "data/" + fileName + ".txt"


##テキストファイルの中身をリストに変形
def GetTxtData(fileName,mode = "int"):
    list = []
    directory = CreateDirectoryStr(fileName)
    with open(directory) as f:
        file_data = f.readlines()
        if (mode == "int"):
            for i in file_data:
                list.append(int(i.strip()))
        else:
            for i in file_data:
                list.append(i.strip())
    return list
    
    
##テキストファイルを初期化
def TextClear(fileName,num,mode = "int"):
    directory = CreateDirectoryStr(fileName)
    with open(directory, mode = "w") as f:
        for i in range(num - 1):
            f.write("0" + "\n")
        if (mode == "int"):
            f.write("0")
        else:
            f.write("")
            
            
##リストをテキストファイルに書き込む
def TextSave(fileName,num,list):
    directory = CreateDirectoryStr(fileName)
    with open(directory, mode = "w") as f:
        for i in range(num):
            f.write(str(list[i]) + "\n")
        f.write(str(list[num]))
        

app.run(host = "0.0.0.0", debug = True)
            
        

