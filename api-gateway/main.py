
from fastapi import FastAPI, Request, HTTPException, Body, Depends
from fastapi.responses import Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx

app = FastAPI(title="Student Management - API Gateway")
security = HTTPBearer()

AUTH_SERVICE = "http://127.0.0.1:8001"
STUDENT_SERVICE = "http://127.0.0.1:8002"
COURSE_SERVICE = "http://127.0.0.1:8003"


@app.get("/")
def home():
    return {
        "message": "Student Management API Gateway is running",
        "services": ["Auth", "Student", "Course"]
    }


async def forward_request(request: Request, service_url: str, path: str, protected: bool = False, authorization: str = None):
    headers = dict(request.headers)
    headers.pop("host", None)
    headers.pop("content-length", None)

    if protected:
        if not authorization:
            raise HTTPException(status_code=401, detail="Authorization token required")
        headers["authorization"] = authorization

    async with httpx.AsyncClient(timeout=30.0) as client:
        if protected:
            auth_response = await client.get(
                f"{AUTH_SERVICE}/auth/me",
                headers={"Authorization": authorization}
            )
            if auth_response.status_code != 200:
                raise HTTPException(status_code=401, detail="Invalid or expired token")

        response = await client.request(
            method=request.method,
            url=f"{service_url}/{path}",
            params=request.query_params,
            content=await request.body(),
            headers=headers
        )

    excluded_headers = {"content-encoding", "content-length", "transfer-encoding", "connection"}
    response_headers = {
        key: value for key, value in response.headers.items()
        if key.lower() not in excluded_headers
    }

    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=response_headers
    )


@app.post("/auth/login")
async def gateway_login(payload: dict = Body(...)):
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(f"{AUTH_SERVICE}/auth/login", json=payload)

    return Response(
        content=response.content,
        status_code=response.status_code,
        media_type="application/json"
    )


@app.api_route("/auth/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def auth_gateway(path: str, request: Request):
    return await forward_request(request, AUTH_SERVICE, f"auth/{path}")


@app.api_route("/students", methods=["GET", "POST"])
async def students_gateway(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    return await forward_request(
        request, STUDENT_SERVICE, "students",
        protected=True, authorization=f"Bearer {credentials.credentials}"
    )


@app.api_route("/students/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def student_detail_gateway(
    path: str,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    return await forward_request(
        request, STUDENT_SERVICE, f"students/{path}",
        protected=True, authorization=f"Bearer {credentials.credentials}"
    )


@app.api_route("/courses", methods=["GET", "POST"])
async def courses_gateway(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    return await forward_request(
        request, COURSE_SERVICE, "courses",
        protected=True, authorization=f"Bearer {credentials.credentials}"
    )


@app.api_route("/courses/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def course_detail_gateway(
    path: str,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    return await forward_request(
        request, COURSE_SERVICE, f"courses/{path}",
        protected=True, authorization=f"Bearer {credentials.credentials}"
    )
