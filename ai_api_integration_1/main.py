from fastapi import FastAPI , Response,HTTPException,Request,Security
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List , Dict , Optional , Any
from enum import Enum
from html import escape
from dotenv import load_dotenv
import httpx
from fastapi import Depends, security,status
import os
from fastapi.security import APIKeyHeader
import json

load_dotenv() # This Loads environment variables from .env file

class outFormat(str , Enum):
    html="html"
    markdown="markdown"
#--------------The set of rules that validates  client's request for the route(@app.post('/ZahraTable')) ----------
class tableRequest(BaseModel):
    format:outFormat=outFormat.html
    columns:Optional[list[str]]=None
    data:list[dict[str,Any]]

#-------------The set of rules that validates  client's request for the route(@app.post("/smart_columns"))--
class SmartColumnsRequest(BaseModel):
    sample:List[Dict[str,Any]]


app=FastAPI(title="ZahraTableMaker")
app.add_middleware(CORSMiddleware, allow_origins=["*"],allow_methods=["*"],allow_headers=["*"],)

@app.get('/health')
def health():
    return {"ok":True}

#----------------Security(api key )----------------
API_KEY=os.getenv("zahraTableMaker_API_Key","zahra-key") #the API_KEY can be created by myself as well or can be fetch from database or anywhere else.
api_key_header=APIKeyHeader(name="z_api_key", auto_error=False) # here api_key_header holds the object of APIKeyHeader that searches for z_api_key, and auto_error=False means that do not raise an error automatically so that we can manage it by our own logic.
def require_api_key(z_api_key:str=Security(api_key_header)):# here the security dependency extracts the value of z_api_key that is in header of client request
    if z_api_key !=API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    

# ------------------ Error handlers ------------------
@app.exception_handler(RequestValidationError)# whenever a RequestValidationError occurs this route or function will be called.
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # 422 when JSON syntax is valid but shape/semantics don't match the model
    return JSONResponse(
        status_code=422,
        content={
            "error": "Unprocessable Content",
            "message": "Expected JSON body: { format, columns?, data: array of objects }.",
            "details": exc.errors(),
        },
    )
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

#---------------End Point for the url(smartColumns) that integrates the openai api for fetching the fixed column names through sending client request data.

class SmartColumnsRequest(BaseModel):
    sample: List[Dict[str, Any]]

@app.post("/smart-columns")
async def smart_columns(req:SmartColumnsRequest, _=Depends(require_api_key)):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(400, detail="Set OPENAI_API_KEY in your environment")

    
    from openai import OpenAI
    client = OpenAI(api_key=api_key)

    prompt = (
            "Given these JSON objects, propose a friendly column order (just keys). "
            "Reply ONLY with a JSON array of strings.\n"
            f"Sample:\n{req.sample[:3]}"   # small slice to keep tokens cheap
        )

    resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
    text = resp.choices[0].message.content.strip()
    try:
        cols = json.loads(text)  # Expecting a JSON array from the model

        if not isinstance(cols, list) or not all(isinstance(x, str) for x in cols):
                raise ValueError("Model did not return a JSON string array")
    except Exception :
        # default to union of keys
        cols = arrange_columns(req.sample, None)


    return {"columns": cols}

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
def make_table(req:tableRequest ,_=Depends(require_api_key)):
    try:
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
    
    except Exception as e:
        # Pass through 429 (quota) as a 502 with cause included
        raise HTTPException(status_code=502, detail=f"AI call failed: {e}")


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



    
    

            
         
    

