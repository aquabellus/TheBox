import telepot, time, os, json, getpass, re, math, random, pandas

tgl = time.strftime("%d %b", time.localtime())
bln = time.strftime("%b %Y", time.localtime())
thn = time.strftime("%Y", time.localtime())
jam = time.strftime("%H:%M", time.localtime())
full = time.strftime("%d %b %Y", time.localtime())
nama = getpass.getuser()

def cek():
    if os.path.exists("/home/{}/Documents/BoxDump.d".format(nama)) == False:
        os.makedirs("/home/{}/Documents/BoxDump.d/{}".format(nama,thn))
        with open("/home/{}/Documents/BoxDump.d/{}/{}.json".format(nama,thn,bln), "w") as outfile:
            outfile.write(json_object)
    else:
        if os.path.exists("/home/{}/Documents/BoxDump.d/{}".format(nama,thn)) == False:
            os.makedirs("/home/{}/Documents/BoxDump.d/{}".format(nama,thn))
            with open("/home/{}/Documents/BoxDump.d/{}/{}.json".format(nama,thn,bln), "w") as outfile:
                outfile.write(json_object)
        else:
            if os.path.exists("/home/{}/Documents/BoxDump.d/{}/{}.json".format(nama,thn,bln)) == False:
                with open("/home/{}/Documents/BoxDump.d/{}/{}.json".format(nama,thn,bln), "w") as outfile:
                    outfile.write(json_object)

tmprpt = {
    "{}".format(tgl) : [
        {
            "Status" : "Mulai",
            "Jam" : jam
        }
    ]
}

def write_json(data, filename=("/home/{}/Documents/BoxDump.d/{}/{}.json".format(nama,thn,bln))):
    with open(filename, 'w') as jswrt:
        json.dump(data, jswrt, indent = 4)

json_object = json.dumps(tmprpt, indent = 4)

