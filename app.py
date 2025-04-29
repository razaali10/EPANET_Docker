from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import subprocess
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to EPANET Simulation API"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/simulate")
async def simulate(inp_file: UploadFile = File(...)):
    try:
        file_location = f"/tmp/{inp_file.filename}"
        with open(file_location, "wb") as f:
            content = await inp_file.read()
            f.write(content)

        print(f"[INFO] File saved at {file_location}, size: {len(content)} bytes")

        output_rpt = file_location.replace(".inp", ".rpt")
        output_bin = file_location.replace(".inp", ".bin")

        cmd = f"epanet2 {file_location} {output_rpt} {output_bin}"
        print(f"[INFO] Running command: {cmd}")
        subprocess.run(cmd.split(), check=True)

        with open(output_rpt, "r") as f:
            rpt_content = f.read()

        return {"report": rpt_content}

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] EPANET CLI error: {e}")
        return JSONResponse(status_code=500, content={"error": "EPANET simulation failed. Check .inp formatting or CLI."})
    except FileNotFoundError as e:
        print(f"[ERROR] CLI missing: {e}")
        return JSONResponse(status_code=500, content={"error": "EPANET CLI not installed or not found in container."})
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})
        

          
       


    
