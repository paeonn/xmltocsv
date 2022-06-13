import xml.etree.ElementTree as ET
from pathlib import Path
import pandas as pd
import time

#Actual time of the day
timestr = time.strftime("%d-%m-%Y-%H%M%S")

for file in Path("xml/03/").iterdir():
    if file.suffix == '.xml':
      
        root = ET.parse(str(file)).getroot()
        
        ns0 = "http://www.portalfiscal.inf.br/nfe"
        ns1 = "http://www.w3.org/2000/09/xmldsig#"

        ET.register_namespace("f", "http://www.portalfiscal.inf.br/nfe")
        ET.register_namespace("el", "http://www.w3.org/2000/09/xmldsig#")

        ns = {
            "f": ns0,
            "el": ns1
        }
        
        a = root.iterfind(".//f:xProd", ns)
        b = root.iterfind(".//f:NCM", ns)
        c = root.iterfind(".//f:uCom", ns)
        d = root.iterfind(".//f:qCom", ns)
        e = root.iterfind(".//f:vUnCom", ns)
        f = root.iterfind(".//f:vProd", ns)
        
        #Static information
        yy = root.find(".//f:nNF", ns)
        zz = root.find(".//f:xNome", ns)
        xx = root.find(".//f:dhEmi", ns)
        
        #Columns of CSV
        cols = ["Nota Fiscal","Empresa", "Emissao", "Produto", "NCM", "Tipo",
                "Quantidade", "ValorUnidade", "ValorTotal"]
        
        #Row data
        rows = []

        #Loop through elements and iterate
        for a, b, c, d, e, f in zip(a, b, c, d, e, f):
          
            aa = a.text
            ab = b.text
            ac = c.text
            ad = float(d.text)
            ae = float(e.text)
            af = float(f.text)
            
            rows.append({
                "Produto": aa,
                "NCM": ab,
                "Tipo": ac,
                "Quantidade": ad,
                "ValorUnidade": ae,
                "ValorTotal": af})

            df = pd.DataFrame(rows, columns=cols)            
            df['Nota Fiscal'] = yy.text
            df['Empresa'] = zz.text
            df['Emissao'] = xx.text
            
            print(df)
            
    df.to_csv(""+timestr+".csv", encoding='utf-8', mode='a')
