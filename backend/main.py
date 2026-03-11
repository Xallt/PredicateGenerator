from pathlib import Path

import asyncio
import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse

from FormulaClasses import Lang
from PredicateTools import math_evolution
from ToTexTransformer import TeX_Transformer, clear_brackets

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BACKEND_DIR = Path(__file__).parent


@app.get("/api/generate")
async def api_generate(size: int | None = None, lang: str = "MathLexs"):
    lang_path = BACKEND_DIR / "Languages" / f"{lang}.txt"

    async def event_generator():
        for pred in math_evolution(Lang.open(str(lang_path)), size):
            tex = TeX_Transformer.transform_sent(clear_brackets(pred))
            yield {"data": json.dumps({"expression": tex, "raw": pred})}
            await asyncio.sleep(0)

    return EventSourceResponse(event_generator())
