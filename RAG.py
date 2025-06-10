import chromadb
import requests

OLLAMA_BASE_URL = "http://localhost:3304"

def get_embedding(text, model="mxbai-embed-large"):
    res = requests.post(
        f"{OLLAMA_BASE_URL}/api/embeddings",
        json={"model": model, "prompt": text}
    )
    res.raise_for_status()
    return res.json()["embedding"]

def generate_with_llm(prompt, model="llama3.1"):
    res = requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json={"model": model, "prompt": prompt, "stream":False}
    )
    res.raise_for_status()
    return res.json()["response"]

chroma_client = chromadb.PersistentClient(path="/app/chroma_db_RAG")
collection = chroma_client.get_or_create_collection(name="my_collection")

documents = [
    "Lookout MKB Voor MKB: Stel uw medewerkers in staat om overal veilig te werken, ook vanaf hun smartphone of tablet",
    "Microsoft Intune Endpoint Manager Mobile Device Management, Application Management, Modern PC Management",
    "Werkplek bezetting Meet bezetting van werkplekken/ bureaus",
    "Slimme gebouwbeveiliging Deze cloudgebaseerde software verbindt producten en geeft gebruikers de mogelijkheid om fysieke beveiliging moeiteloos te beheren.",
    "TrendMicro Geavanceerde cyberbeveiliging voor PC, mail en cloud",
    "NCE Office 365 Enterprise(Apps for Enterprise) Kantoor waar en wanneer je het nodig hebt",
    "Bezetting en benutting van kantoren Plan je dag. Coördineer je mensen.",
    "Lookout Advanced Stel uw medewerkers in staat om overal veilig te werken, ook vanaf hun smartphone of tablet",
    "Vulnerability Assessment Opsporen van ontbrekende patches, afwijkingen van configuratierichtlijnen, best-practices of compliancenormen voor uw infrastructuur",
    "Penetration testing Een grondige handmatige testoefening die een echte aanval simuleert door de weg van de minste weerstand te volgen.",
    "Phishing Awareness service Een mensgerichte beoordeling waarbij werknemers worden getest met een simulatie van een phishing aanval via e-mailberichten",
    "Cyber Exposure Diagnostics service Een uitgebreid verslag over de cyberblootstelling en de weerbaarheid van de omgeving kan cyberinbreuken stoppen",
    "Ivanti Neurons for MDM Manage endpoints, beheer al je endpoints, waaronder iOS, iPadOS, macOS, Android, Windows, Zebra, Oculus-apparaten en wearables, en ondersteun zowel modern als clientbeheer."
]
ids = [f"id{i+1}" for i in range(len(documents))]

embeddings = [get_embedding(doc) for doc in documents]
collection.add(documents=documents, ids=ids, embeddings=embeddings)

query = "Wat is een goede service voor mij als ik werkplekken wil beheren"
query_embedding = get_embedding(query)
results = collection.query(query_embeddings=[query_embedding], n_results=2)

context = "\n".join(results['documents'][0])
rag_prompt = f"""Gebruik alleen de volgende context om de vraag te beantwoorden:

{context}

Vraag: {query}
Antwoord:"""

answer = generate_with_llm(rag_prompt)
print(">>> Antwoord van RAG LLM:\n", answer)