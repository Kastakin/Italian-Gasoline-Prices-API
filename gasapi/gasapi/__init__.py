from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

query_tags = [
    {
        "name": "Places",
        "description": "Search gasoline vendors.",
    },
    {
        "name": "Prices",
        "description": "Search for prices.",
    },
    {
        "name": "Misc",
        "description": "Other data.",
    }
]

app = FastAPI(    
    title="Italian Gasoline Prices API",
    description="Get the prices of gasoline in Italy, daily updated.",
    version="0.0.1",
    openapi_tags=query_tags,
    redoc_url=None
)


app.mount('/static', StaticFiles(directory='./gasapi/static'), name='static')
templates = Jinja2Templates(directory='./gasapi/templates')


from gasapi.views import main
from gasapi import query