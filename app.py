from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi import UploadFile, File
import shutil
import json
import os
from datetime import datetime

# Ensure these files/modules exist in your local workspace directory
from ppt_scanner import scan_ppt
from publisher import publish
from transformation_registry import TransformationRegistry

app = FastAPI()

# ==================================================
# DASHBOARD
# ==================================================

@app.get("/", response_class=HTMLResponse)
def dashboard():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>FMS Dashboard</title>
        <style>
            body {
                font-family: Arial;
                padding: 30px;
                background-color: #f8f9fa;
            }
            .btn {
                display: inline-block;
                padding: 10px 20px;
                margin: 10px 5px;
                background: #007BFF;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
            }
            .btn:hover {
                background: #0056b3;
            }
            button {
                padding: 10px 20px;
                margin-top: 10px;
                background: #28a745;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-weight: bold;
            }
            button:hover {
                background: #218838;
            }
            form {
                margin-bottom: 25px;
                background: white;
                padding: 20px;
                border-radius: 5px;
                border: 1px solid #dee2e6;
            }
        </style>
    </head>
    <body>

        <h1>FMS Publishing project</h1>

        <h2>Upload Excel</h2>
        <!-- Fixed: HTML Form Wrapper Added with Multipart Enforcement -->
        <form action="/upload_excel" method="post" enctype="multipart/form-data">
            <input type="file" name="file" accept=".xlsx" required>
            <br><br>
          
        </form>

        <hr>

        <h2>Upload PPT Template</h2>
        <!-- Fixed: HTML Form Wrapper Added with Multipart Enforcement -->
        <form action="/upload_ppt" method="post" enctype="multipart/form-data">
            <input type="file" name="file" accept=".pptx" required>
            <br><br>
           
        </form>

        <hr>

        <a href="/scan" class="btn">Scan Template</a>
        <a href="/mapping" class="btn">Mapping</a>
        <a href="/transformations" class="btn">Transformations</a>
        <a href="/generate" class="btn">Generate PPT</a>

    </body>
    </html>
    """

# ==================================================
# UPLOAD EXCEL
# ==================================================

@app.post("/upload_excel")
async def upload_excel(file: UploadFile = File(...)):
    with open("input_files/HoldingData.xlsx", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return RedirectResponse("/", status_code=303)

# ==================================================
# UPLOAD PPT
# ==================================================

@app.post("/upload_ppt")
async def upload_ppt(file: UploadFile = File(...)):
    with open("templates/TestCase1.pptx", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return RedirectResponse("/", status_code=303)

# ==================================================
# SCAN
# ==================================================

@app.get("/scan", response_class=HTMLResponse)
def scan():
    inventory = scan_ppt("templates/TestCase1.pptx")

    html = """
    <html>
    <head>
        <title>Template Inventory</title>
        <style>
            body { font-family: Arial; padding: 30px; }
            table { border-collapse: collapse; width: 100%; margin-bottom: 20px;}
            th, td { border: 1px solid #ccc; padding: 10px; }
            th { background: #3949AB; color: white; }
            .btn {
                display: inline-block;
                padding: 10px 20px;
                background: #6c757d;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
    <h1>Template Inventory</h1>
    <table>
        <tr>
            <th>Slide</th>
            <th>Object Name</th>
            <th>Object Type</th>
        </tr>
    """

    for item in inventory:
        html += f"""
        <tr>
            <td>{item['slide']}</td>
            <td>{item['object_name']}</td>
            <td>{item['object_type']}</td>
        </tr>
        """

    # Fixed: Restored Back Button
    html += """
    </table>
    <a href="/" class="btn">Back to Dashboard</a>
    </body>
    </html>
    """
    return HTMLResponse(content=html)

# ==================================================
# MAPPING
# ==================================================

@app.get("/mapping", response_class=HTMLResponse)
def mapping():
    with open("configuration_files/mapping.json", "r", encoding="utf-8") as f:
        mapping_data = json.load(f)

    transformations = [
        item for item in dir(TransformationRegistry) if not item.startswith("_")
    ]

    html = """
    <html>
    <head>
        <title>Mapping Configuration</title>
        <style>
            body { font-family: Arial; padding: 30px; }
            table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
            th, td { border: 1px solid #ccc; padding: 10px; }
            th { background: #343a40; color: white; }
            .btn {
                display: inline-block;
                padding: 10px 20px;
                background: #6c757d;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
            }
            button {
                padding: 10px 20px;
                background: #28a745;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
    <h1>Mapping Configuration</h1>
    
    <!-- Fixed: Form Tag Action Definition Added -->
    <form action="/save_mapping" method="post">
    <table>
        <tr>
            <th>Slide</th>
            <th>Object Name</th>
            <th>Object Type</th>
            <th>Transformation</th>
        </tr>
    """

    for idx, obj in enumerate(mapping_data["objects"]):
        html += f"""
        <tr>
            <td>{obj['slide']}</td>
            <td>{obj['object_name']}</td>
            <td>{obj['object_type']}</td>
            <td>
                <select name="transformation_{idx}">
        """
        for transformation in transformations:
            selected = "selected" if transformation == obj["transformation"] else ""
            html += f"""
                <option value="{transformation}" {selected}>
                    {transformation}
                </option>
            """
        html += """
                </select>
            </td>
        </tr>
        """

    # Fixed: Restored Back Button and closed tags properly
    html += """
    </table>
    <button type="submit">Save Mapping</button>
    </form>
    <br>
    <a href="/" class="btn">Back to Dashboard</a>
    </body>
    </html>
    """
    return HTMLResponse(content=html)

# ==================================================
# SAVE MAPPING
# ==================================================

@app.post("/save_mapping")
async def save_mapping(request: Request):
    form = await request.form()

    with open("configuration_files/mapping.json", "r", encoding="utf-8") as f:
        mapping_data = json.load(f)

    for idx, obj in enumerate(mapping_data["objects"]):
        obj["transformation"] = form[f"transformation_{idx}"]

    with open("configuration_files/mapping.json", "w", encoding="utf-8") as f:
        json.dump(mapping_data, f, indent=4)

    return RedirectResponse("/mapping", status_code=303)

# ==================================================
# TRANSFORMATIONS
# ==================================================

@app.get("/transformations", response_class=HTMLResponse)
def transformations():
    transformation_list = [
        item for item in dir(TransformationRegistry) if not item.startswith("_")
    ]

    html = """
    <html>
    <head>
        <title>Available Transformations</title>
        <style>
            body { font-family: Arial; padding: 30px; }
            table { border-collapse: collapse; width: 50%; margin-bottom: 20px; }
            th, td { border: 1px solid #ccc; padding: 10px; text-align: left; }
            th { background: #17a2b8; color: white; }
            .btn {
                display: inline-block;
                padding: 10px 20px;
                background: #6c757d;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
    <h1>Available Transformations</h1>
    <table>
        <tr>
            <th>Transformation Name</th>
        </tr>
    """

    for item in transformation_list:
        html += f"""
        <tr>
            <td>{item}</td>
        </tr>
        """

    # Fixed: Closed template string correctly and added Dashboard link
    html += """
    </table>
    <br>
    <a href="/" class="btn">Back to Dashboard</a>
    </body>
    </html>
    """
    return HTMLResponse(content=html)
# ==================================================
# DOWNLOAD PPT (Placeholder route added for stability)
# ==================================================
@app.get("/download")
def download():

    return FileResponse(
        path="output_files/output.pptx",
        filename="output.pptx"
    )
# ==================================================
# GENERATE PPT (Placeholder route added for stability)
# ==================================================
@app.get("/generate", response_class=HTMLResponse)
def generate():

    try:

        publish()

        html = """
        <html>

        <body style="font-family:Arial;padding:30px;">

        <h1>Publishing Status</h1>

        <p>✅ Excel Loaded</p>

        <p>✅ PowerPoint Template Loaded</p>

        <p>✅ Mapping Configuration Loaded</p>

        <p>✅ Text Objects Updated</p>

        <p>✅ Table Objects Updated</p>

        <p>✅ Chart Objects Updated</p>

        <p>✅ PPT Generated Successfully</p>

         <br>
            <!-- Ensure these EXACT lines are used in your python string -->
            <a href="/download" class="btn">Download PPT</a>
            <a href="/" class="btn btn-secondary">Back to Dashboard</a>

        </body>
        </html>
        """
        return HTMLResponse(content=html)

    except Exception as e:

        return {
            "error": str(e)
        }
 
