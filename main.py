# main.py
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

# OpenTelemetry Imports
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Initialize Tracer
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

app = FastAPI(title="iris classifier API")

# Instrument FastAPI app
FastAPIInstrumentor.instrument_app(app)

# Load your trained model
model = joblib.load("iris_model.joblib")

class IrisInput(BaseModel):
    sepal_length: float
    sepal_width:  float
    petal_length: float
    petal_width: float

@app.get("/")
def read_root():
    return {"message": "Welcome to iris classifier API"}

@app.post("/predict/")
def predict_species(payload: IrisInput):
    # Build a single-row DataFrame from the JSON body
    input_df = pd.DataFrame([payload.dict()])
    
    # Custom Span for model prediction
    with tracer.start_as_current_span("model_prediction_span") as span:
        prediction = model.predict(input_df)[0]
        span.set_attribute("prediction.class", prediction) # Optional: add attributes
    
    return {"prediction_class": prediction}
