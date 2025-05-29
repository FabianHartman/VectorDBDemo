import chromadb

chroma_client = chromadb.Client()

collection = chroma_client.create_collection(name="my_collection")

collection.add(
    documents=[
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
    ],
    ids=[
        "id1", "id2", "id3", "id4", "id5", "id6", "id7", "id8", "id9", "id10", "id11", "id12",
        "id13"
    ],
)

results = collection.query(
    query_texts=["inzicht in bureau gebruik"],
    n_results=4
)

for document in results['documents'][0]:
    print(document)
