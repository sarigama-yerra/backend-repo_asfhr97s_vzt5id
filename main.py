import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Client, Employee, Project, Task, Invoice

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Utility to convert Mongo _id to str recursively

def serialize_doc(doc: dict):
    if not doc:
        return doc
    doc = dict(doc)
    if "_id" in doc:
        doc["id"] = str(doc.pop("_id"))
    # Convert nested ObjectIds if any
    for k, v in list(doc.items()):
        if isinstance(v, ObjectId):
            doc[k] = str(v)
    return doc

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI Backend!"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    import os as _os
    response["database_url"] = "✅ Set" if _os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if _os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response

# --------------------------- Admin/Dashboard APIs ---------------------------

# Clients
@app.post("/api/clients")
def create_client(payload: Client):
    cid = create_document("client", payload)
    return {"id": cid}

@app.get("/api/clients")
def list_clients():
    docs = get_documents("client")
    return [serialize_doc(d) for d in docs]

# Employees
@app.post("/api/employees")
def create_employee(payload: Employee):
    eid = create_document("employee", payload)
    return {"id": eid}

@app.get("/api/employees")
def list_employees():
    docs = get_documents("employee")
    return [serialize_doc(d) for d in docs]

# Projects
@app.post("/api/projects")
def create_project(payload: Project):
    pid = create_document("project", payload)
    return {"id": pid}

@app.get("/api/projects")
def list_projects():
    docs = get_documents("project")
    return [serialize_doc(d) for d in docs]

# Tasks
@app.post("/api/tasks")
def create_task(payload: Task):
    tid = create_document("task", payload)
    return {"id": tid}

@app.get("/api/tasks")
def list_tasks(project_id: Optional[str] = None):
    filt = {"project_id": project_id} if project_id else {}
    docs = get_documents("task", filt)
    return [serialize_doc(d) for d in docs]

# Invoices
@app.post("/api/invoices")
def create_invoice(payload: Invoice):
    iid = create_document("invoice", payload)
    return {"id": iid}

@app.get("/api/invoices")
def list_invoices(client_id: Optional[str] = None, project_id: Optional[str] = None):
    filt = {}
    if client_id:
        filt["client_id"] = client_id
    if project_id:
        filt["project_id"] = project_id
    docs = get_documents("invoice", filt)
    return [serialize_doc(d) for d in docs]

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
