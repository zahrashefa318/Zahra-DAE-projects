from fastapi import FastAPI , Response,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List , Dict , Optional , Any
from enum import Enum
from html import escape
import httpx

class outFormat(str , Enum):
    html="html"
    markdown="markdown"
#--------------the format of client's request body----------
class tableRequest(BaseModel):
    format:outFormat=outFormat.html
    columns:Optional[list[str]]=None
    data:list[dict[str,Any]]

app=FastAPI(title="ZahraTableMaker")
app.add_middleware(CORSMiddleware, allow_origins=["*"],allow_methods=["*"],allow_headers=["*"],)

@app.get('/health')
def health():
    return {"ok":True}

#----Function for returning Columns by extracting keys from data list of dictionaries-----
def arrange_columns(rows:List[Dict[str,Any]], columns:Optional[List[str]]=None)->List[str]:
    if columns:
        return columns
    cols:List[str]=[]
    for r in rows:
        for k in r.keys():
            if k not in cols:
                cols.append(k)
    return cols

#------Function for Formatting data as html table for giving response or out put for the client that has requested---------------
def to_html(rows:List[Dict[str,Any]], columns:List[str])->str:
    # CSS + wrapper so the header sticks and borders look clean
    css = """
    <style>
      .tm-wrap { max-height: 420px; overflow: auto;
                 border: 1px solid #e5e7eb; border-radius: 10px; }
      .tm      { width: 100%; border-collapse: collapse;
                 font: 14px/1.5 system-ui,-apple-system,Segoe UI,Roboto,"Helvetica Neue",Arial,sans-serif; }
      .tm th, .tm td { border: 1px solid #e5e7eb; padding: 10px 12px; text-align: left; vertical-align: top; }
      .tm thead th { position: sticky; top: 0; z-index: 1; background: #f8fafc; box-shadow: 0 1px 0 rgba(0,0,0,0.05) inset; }
      .tm tbody tr:nth-child(even) td { background: #fafafa; }
      .tm tbody tr:hover td { background: #f1f5f9; }
    </style>
    """
    #---------Table header from keys in dictionary--------------------
    tableHeader="<thead><tr>"+ "". join(f"<th>{escape(str(c))}</th>" for c in columns)+"</tr></thead>"
    trs=[]
    for r in rows:
        tds=[]
        for c in columns:
            v=r.get(c , "")
            tds.append(f"<td>{'' if v is None else escape(str(v))}</td>")
        trs.append(f"<tr>{ "".join(tds)}</tr>")

    tableBody="<tbody>"+"".join(trs)+"</tbody>"
    return f"""{css}<div class="tm-wrap"><table class="tm">{tableHeader}{tableBody}</table></div>"""

#--------Function for Formatting data as markdown table for giving response to the client that has requested my api---------------
def to_markdown(rows:List[Dict[str,Any]], columns:List[str])->str:
    def myMarkEscape(s:str)->str:
        return s.replace("|","\\|")
    header="| "+" | ".join(myMarkEscape(c) for c in columns)+" |"
    sep="| "+" | ".join("---" for c in columns)+" | "
    lines=[header,sep]
    for r in rows:
        tds=[]
        for c in columns:
            value=r.get(c,"")
            value="" if value is None else str(value)
            tds.append(myMarkEscape(value))
        lines.append("| "+" | ".join(tds)+" |")
    return "\n".join(lines)

#-------------End Point the url that client uses to make request and get response for making tabular display of his data-------------------------------
@app.post('/ZahraTable')
def make_table(req:tableRequest):
    rows=req.data
    if not isinstance(rows,list) or not all (isinstance(x,dict)for x in rows):
        raise HTTPException(status_code=400, detail="Data should be list of objects !")
    if len(rows)>1000:
        raise HTTPException(status_code=413 , detail="Too many data to demo ! (max=1000 rows)")
    columns=arrange_columns(rows, req.columns)

    if req.format==outFormat.html:
        html=to_html(rows,columns)
        return Response(content=html, media_type="text/html")
    else:
        md=to_markdown(rows, columns)
        return Response(content=md , media_type="text/plain")
    
#---Integrated with a public fake API(https://jsonplaceholder.typicode.com/users) in order to make a get request for fake data fetch.-
@app.get("/demo/jsonplaceholder")
async def demo_jsonplaceholder():
    url="https://jsonplaceholder.typicode.com/users"
    async with httpx.AsyncClient(timeout=5.0)as client: #--------creates a http client session-----(httpx is a python http client library and AsyncClient is a class from that library)
        r= await client.get(url)
        r.raise_for_status()
        users=r.json()
    rows=[{"name":u.get("name"), "email":u.get("email"), "company":(u.get("company")) or {}.get("name")} for u in users]
    columns=["name", "email", "company"]
    return Response(content=to_html(rows,columns), media_type="text/html")



    
    

            
         
    

