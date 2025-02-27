from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

# Mock database for demonstration purposes
job_types = [
    {"id": 1, "name": "Type1", "minDuration": 10, "maxDuration": 30, "priority": "High", "active": True,
     "createdOn": "2023-01-01T00:00:00Z", "modifiedOn": "2023-01-01T00:00:00Z"},
    {"id": 2, "name": "Type2", "minDuration": 5, "maxDuration": 15, "priority": "Low", "active": True,
     "createdOn": "2023-01-02T00:00:00Z", "modifiedOn": "2023-01-02T00:00:00Z"},
]


class JobType(BaseModel):
    id: int
    name: str
    minDuration: int
    maxDuration: int
    priority: str
    active: bool
    createdOn: str
    modifiedOn: str


@app.get("/jpm/v2/tenant/{tenant}/job-types")
async def read_job_types(
        tenant: int,
        name: Optional[str] = None,
        minDuration: Optional[int] = None,
        maxDuration: Optional[int] = None,
        priority: Optional[str] = None,
        ids: Optional[str] = None,
        page: Optional[int] = None,
        pageSize: Optional[int] = 50,
        includeTotal: Optional[bool] = False,
        active: Optional[str] = "True",
        orderBy: Optional[str] = None,
        orderByDirection: Optional[str] = "asc",
        createdBefore: Optional[str] = None,
        createdOnOrAfter: Optional[str] = None,
        modifiedBefore: Optional[str] = None,
        modifiedOnOrAfter: Optional[str] = None,
        externalDataApplicationGuid: Optional[str] = None,
):
    filtered_job_types = job_types.copy()

    if name:
        filtered_job_types = [jt for jt in filtered_job_types if jt["name"] == name]
    if minDuration:
        filtered_job_types = [jt for jt in filtered_job_types if jt["minDuration"] >= minDuration]
    if maxDuration:
        filtered_job_types = [jt for jt in filtered_job_types if jt["maxDuration"] <= maxDuration]
    if priority:
        filtered_job_types = [jt for jt in filtered_job_types if jt["priority"] == priority]
    if ids:
        ids_list = [int(id) for id in ids.split(",")]
        filtered_job_types = [jt for jt in filtered_job_types if jt["id"] in ids_list]
    if active == "True":
        filtered_job_types = [jt for jt in filtered_job_types if jt["active"]]
    elif active == "False":
        filtered_job_types = [jt for jt in filtered_job_types if not jt["active"]]
    elif active == "Any":
        pass  # No filtering

    if createdBefore:
        created_before_date = datetime.strptime(createdBefore, "%Y-%m-%dT%H:%M:%SZ")
        filtered_job_types = [jt for jt in filtered_job_types if
                              datetime.strptime(jt["createdOn"], "%Y-%m-%dT%H:%M:%SZ") < created_before_date]
    if createdOnOrAfter:
        created_on_or_after_date = datetime.strptime(createdOnOrAfter, "%Y-%m-%dT%H:%M:%SZ")
        filtered_job_types = [jt for jt in filtered_job_types if
                              datetime.strptime(jt["createdOn"], "%Y-%m-%dT%H:%M:%SZ") >= created_on_or_after_date]
    if modifiedBefore:
        modified_before_date = datetime.strptime(modifiedBefore, "%Y-%m-%dT%H:%M:%SZ")
        filtered_job_types = [jt for jt in filtered_job_types if
                              datetime.strptime(jt["modifiedOn"], "%Y-%m-%dT%H:%M:%SZ") < modified_before_date]
    if modifiedOnOrAfter:
        modified_on_or_after_date = datetime.strptime(modifiedOnOrAfter, "%Y-%m-%dT%H:%M:%SZ")
        filtered_job_types = [jt for jt in filtered_job_types if
                              datetime.strptime(jt["modifiedOn"], "%Y-%m-%dT%H:%M:%SZ") >= modified_on_or_after_date]

    if orderBy:
        if orderBy == "id":
            key = "id"
        elif orderBy == "modifiedOn":
            key = "modifiedOn"
        elif orderBy == "createdOn":
            key = "createdOn"
        else:
            raise HTTPException(status_code=400, detail="Invalid orderBy parameter")

        if orderByDirection == "asc":
            filtered_job_types.sort(key=lambda x: x[key])
        elif orderByDirection == "desc":
            filtered_job_types.sort(key=lambda x: x[key], reverse=True)
        else:
            raise HTTPException(status_code=400, detail="Invalid orderByDirection parameter")

    # Pagination
    if page and pageSize:
        start_index = (page - 1) * pageSize
        end_index = start_index + pageSize
        filtered_job_types = filtered_job_types[start_index:end_index]

    response = {
        "jobTypes": filtered_job_types,
    }

    if includeTotal:
        response["total"] = len(job_types)

    return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
