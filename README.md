---
title: Vibe-Math
emoji: 🧮
colorFrom: green
colorTo: blue
sdk: docker
pinned: false
---

# Vibe-Math – 2-second math solver

Snap any handwritten equation and get the answer + explanation instantly.

## Endpoints

| Path | Method | Description |
|---|---|---|
| `/solve` | `POST` | Upload an image (`multipart/form-data`) → JSON `{answer}` |
| `/health` | `GET` | Health check |
| `/docs` | `GET` | Swagger UI |

## Example usage

```bash
curl -X POST https://d4ydy-vibe-math.hf.space/solve \
  -F "file=@equation.png"