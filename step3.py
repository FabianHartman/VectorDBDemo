import chromadb
import requests

def get_ollama_embeddings(texts, model="mxbai-embed-large"):
    url = "http://localhost:3304/api/embeddings"
    embeddings = []
    for text in texts:
        response = requests.post(url, json={"model": model, "prompt": text})
        response.raise_for_status()
        embedding = response.json()["embedding"]
        embeddings.append(embedding)
    return embeddings

chroma_client = chromadb.PersistentClient(path="./chroma_db_step_3")
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

embeddings = get_ollama_embeddings(documents)
collection.add(documents=documents, ids=ids, embeddings=embeddings)

query = "inzicht in bureau gebruik"
query_embedding = get_ollama_embeddings([query])[0]

results = collection.query(query_embeddings=[query_embedding], n_results=4)

for doc in results['documents'][0]:
    print(doc)
