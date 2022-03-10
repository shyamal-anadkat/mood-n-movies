from sentence_transformers import SentenceTransformer

modelPath = "../models/multi-qa-MiniLM-L6-cos-v1"

model = SentenceTransformer("sentence-transformers/multi-qa-MiniLM-L6-cos-v1")
model.save(modelPath)
model = SentenceTransformer(modelPath)
