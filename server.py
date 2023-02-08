from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.exceptions import RequestValidationError
import uvicorn
from keras.models import load_model

model = load_model('UniversityModel.h5')
async def notFound(a, b):
	return FileResponse('./html/wrongPage.html')

exception_handlers = {
	404 : notFound
}


app = FastAPI(exception_handlers=exception_handlers)

origins = [
    "*"
]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"]
)

@app.get('/')
async def a():
	return FileResponse('./html/ask.html')

@app.get('/predict/{gre}/{gpa}/{rank}')
async def predict(gre : str, gpa : str, rank : str):
	try:
		gre = int(gre)
		gpa = float(gpa)
		rank = float(rank)
		
		prediction = model.predict([
			[gre, gpa, rank]
		])
		prediction = int(float(prediction[0][0]) * 100)
		return RedirectResponse(f"http://localhost:1001/result/?percent={prediction}")
	except:
		return FileResponse('./html/checkPlease.html')

@app.get('/result/')
def predictionResult():
	return FileResponse('./html/predictResult.html')

if __name__ == "__main__":
	uvicorn.run("server:app", host="0.0.0.0", port=1001, reload=True)