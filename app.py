from fastapi import FastAPI, File, UploadFile
import os
import subprocess

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to EPANET Simulation API"}

@app.post("/simulate")
async def simulate(inp_file: UploadFile = File(...)):
    file_location = f"/tmp/{inp_file.filename}"
    
    with open(file_location, "wb") as f:
        f.write(await inp_file.read())

    output_rpt = file_location.replace(".inp", ".rpt")
    output_bin = file_location.replace(".inp", ".bin")

    cmd = f"epanet2 {file_location} {output_rpt} {output_bin}"
    try:
        subprocess.run(cmd.split(), check=True)
    except subprocess.CalledProcessError as e:
        return {"error": str(e)}

    with open(output_rpt, "r") as f:
        rpt_content = f.read()

    return {"report": rpt_content}