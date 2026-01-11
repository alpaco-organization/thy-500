import asyncio
import os
import sys
from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient

_APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _APP_ROOT not in sys.path:
    sys.path.insert(0, _APP_ROOT)

from app.utils.normalize import normalize_name


def _mongo_db_name_from_uri(uri: str) -> str:
    # Prefer explicit DB name if present in URI path, else fall back.
    # Example: mongodb://mongo:27017/thy500
    try:
        path = uri.split("?", 1)[0].split("//", 1)[1].split("/", 1)[1]
    except Exception:
        path = ""
    db = (path or "").strip("/")
    return db or os.getenv("MONGO_DB", "thy500")


async def main() -> None:
    mongo_uri = os.getenv("MONGO_URI", "mongodb://mongo:27017/thy500")
    db_name = _mongo_db_name_from_uri(mongo_uri)

    client = AsyncIOMotorClient(mongo_uri)
    db = client[db_name]
    persons = db["persons"]

    # Ensure the unique index exists (matches app startup behavior)
    await persons.create_index("personId", unique=True)

    sample: list[dict[str, Any]] = [
       {
        "personId": "00069094",
        "name": "NURSİBEL AYDIN",
        "grid_filename": "grid_1.png",
        "row": 0,
        "column": 9,
        "x": 738,
        "y": 0
    },
    {
        "personId": "00050400",
        "name": "AYŞEGÜL KARPUZOĞLU",
        "grid_filename": "grid_1.png",
        "row": 0,
        "column": 11,
        "x": 902,
        "y": 0
    },
    {
        "personId": "00050498",
        "name": "AKIN ÇARKÇI",
        "grid_filename": "grid_1.png",
        "row": 1,
        "column": 6,
        "x": 492,
        "y": 106
    },
    {
        "personId": "00070363",
        "name": "FEYYAZ ENES AKBEN",
        "grid_filename": "grid_1.png",
        "row": 1,
        "column": 9,
        "x": 738,
        "y": 106
    },
    {
        "personId": "00070352",
        "name": "YASİN BEKAROĞLU",
        "grid_filename": "grid_1.png",
        "row": 1,
        "column": 11,
        "x": 902,
        "y": 106
    },
    {
        "personId": "00079581",
        "name": "ÜLKER ŞULE AKSOY",
        "grid_filename": "grid_1.png",
        "row": 2,
        "column": 0,
        "x": 0,
        "y": 212
    },
    {
        "personId": "00062260",
        "name": "İNANÇ EMRE ALBAYRAK",
        "grid_filename": "grid_1.png",
        "row": 3,
        "column": 3,
        "x": 246,
        "y": 318
    },
    {
        "personId": "00051103",
        "name": "MEHMET İLKER BAŞARAN",
        "grid_filename": "grid_1.png",
        "row": 4,
        "column": 5,
        "x": 410,
        "y": 424
    },
    {
        "personId": "00053419",
        "name": "EMRE ÇELİK",
        "grid_filename": "grid_1.png",
        "row": 4,
        "column": 8,
        "x": 656,
        "y": 424
    },
    {
        "personId": "00069336",
        "name": "NİHAL AÇIKEL",
        "grid_filename": "grid_1.png",
        "row": 5,
        "column": 3,
        "x": 246,
        "y": 530
    },
    {
        "personId": "00058832",
        "name": "ŞAFAK BAŞARAN",
        "grid_filename": "grid_1.png",
        "row": 5,
        "column": 5,
        "x": 410,
        "y": 530
    },
    {
        "personId": "00061470",
        "name": "SÜLEYMAN SERDAR YAĞCI",
        "grid_filename": "grid_1.png",
        "row": 5,
        "column": 12,
        "x": 984,
        "y": 530
    },
    {
        "personId": "00063000",
        "name": "İBRAHİM SARIKAYA",
        "grid_filename": "grid_1.png",
        "row": 6,
        "column": 10,
        "x": 820,
        "y": 636
    },
    {
        "personId": "00068246",
        "name": "MEHMET CAN TAŞCI",
        "grid_filename": "grid_1.png",
        "row": 7,
        "column": 4,
        "x": 328,
        "y": 742
    },
    {
        "personId": "00046043",
        "name": "ŞULE YILMAZ",
        "grid_filename": "grid_1.png",
        "row": 10,
        "column": 0,
        "x": 0,
        "y": 1060
    },
    {
        "personId": "00069768",
        "name": "KORAY ÖZÖNER",
        "grid_filename": "grid_1.png",
        "row": 10,
        "column": 1,
        "x": 82,
        "y": 1060
    },
    {
        "personId": "00064656",
        "name": "ÖZER GÜLER",
        "grid_filename": "grid_1.png",
        "row": 10,
        "column": 8,
        "x": 656,
        "y": 1060
    },
    {
        "personId": "00075047",
        "name": "MEHMET BURAK ÇAKIR",
        "grid_filename": "grid_2.png",
        "row": 0,
        "column": 2,
        "x": 164,
        "y": 0
    },
    {
        "personId": "00061975",
        "name": "ELİF DEĞİRMENCİ",
        "grid_filename": "grid_2.png",
        "row": 2,
        "column": 2,
        "x": 164,
        "y": 212
    },
    {
        "personId": "00069386",
        "name": "HİLMİ HAKAN KAHRAMAN",
        "grid_filename": "grid_2.png",
        "row": 2,
        "column": 11,
        "x": 902,
        "y": 212
    },
    {
        "personId": "00081640",
        "name": "HATİCE ÜRKAN",
        "grid_filename": "grid_2.png",
        "row": 2,
        "column": 12,
        "x": 984,
        "y": 212
    },
    {
        "personId": "00072966",
        "name": "EBUZER TANHAN",
        "grid_filename": "grid_2.png",
        "row": 3,
        "column": 3,
        "x": 246,
        "y": 318
    },
    {
        "personId": "00053200",
        "name": "ALİ İHSAN DİKBAŞ",
        "grid_filename": "grid_2.png",
        "row": 3,
        "column": 11,
        "x": 902,
        "y": 318
    },
    {
        "personId": "00073646",
        "name": "CİHANGİR GÜN",
        "grid_filename": "grid_2.png",
        "row": 5,
        "column": 2,
        "x": 164,
        "y": 530
    },
    {
        "personId": "00063968",
        "name": "AHMET BURAK OKTAY",
        "grid_filename": "grid_2.png",
        "row": 5,
        "column": 7,
        "x": 574,
        "y": 530
    },
    {
        "personId": "00068250",
        "name": "ERHAN ŞENEL",
        "grid_filename": "grid_2.png",
        "row": 6,
        "column": 9,
        "x": 738,
        "y": 636
    },
    {
        "personId": "00042581",
        "name": "BÜLENT ÜNALAN",
        "grid_filename": "grid_2.png",
        "row": 7,
        "column": 1,
        "x": 82,
        "y": 742
    },
    {
        "personId": "00068047",
        "name": "MERVE ORUÇ",
        "grid_filename": "grid_2.png",
        "row": 8,
        "column": 1,
        "x": 82,
        "y": 848
    },
    {
        "personId": "00048323",
        "name": "CEM TANBURACI",
        "grid_filename": "grid_2.png",
        "row": 8,
        "column": 4,
        "x": 328,
        "y": 848
    },
    {
        "personId": "00085337",
        "name": "NECMEDDİN ESAT BELEN",
        "grid_filename": "grid_2.png",
        "row": 8,
        "column": 8,
        "x": 656,
        "y": 848
    },
    {
        "personId": "00063147",
        "name": "FATİH GÜVER",
        "grid_filename": "grid_2.png",
        "row": 9,
        "column": 10,
        "x": 820,
        "y": 954
    },
    {
        "personId": "00063761",
        "name": "ABDULLAH KOSİF",
        "grid_filename": "grid_2.png",
        "row": 9,
        "column": 13,
        "x": 1066,
        "y": 954
    },
    {
        "personId": "00068346",
        "name": "HALİT TUNCER",
        "grid_filename": "grid_2.png",
        "row": 10,
        "column": 7,
        "x": 574,
        "y": 1060
    },
    {
        "personId": "00067458",
        "name": "BARBAROS KURTUL",
        "grid_filename": "grid_2.png",
        "row": 10,
        "column": 13,
        "x": 1066,
        "y": 1060
    },
    {
        "personId": "00057988",
        "name": "HAKAN LOKMAN YÜKSEL",
        "grid_filename": "grid_3.png",
        "row": 1,
        "column": 2,
        "x": 164,
        "y": 106
    },
    {
        "personId": "00061125",
        "name": "HİLMİ BURCU",
        "grid_filename": "grid_3.png",
        "row": 1,
        "column": 13,
        "x": 1066,
        "y": 106
    },
    {
        "personId": "00054196",
        "name": "FEDAİ SAİT EŞ",
        "grid_filename": "grid_3.png",
        "row": 2,
        "column": 0,
        "x": 0,
        "y": 212
    },
    {
        "personId": "00067757",
        "name": "OZAN BELGE",
        "grid_filename": "grid_3.png",
        "row": 2,
        "column": 1,
        "x": 82,
        "y": 212
    },
    {
        "personId": "00051245",
        "name": "MEHMET GÜRHAN ARSLAN",
        "grid_filename": "grid_3.png",
        "row": 3,
        "column": 6,
        "x": 492,
        "y": 318
    },
    {
        "personId": "00074597",
        "name": "VELİ İBRAHİM UĞUR",
        "grid_filename": "grid_3.png",
        "row": 3,
        "column": 7,
        "x": 574,
        "y": 318
    },
    {
        "personId": "00046835",
        "name": "FERİDE SİBEL ALKAN",
        "grid_filename": "grid_3.png",
        "row": 3,
        "column": 10,
        "x": 820,
        "y": 318
    },
    {
        "personId": "00083039",
        "name": "OSMAN YURTTADUR",
        "grid_filename": "grid_3.png",
        "row": 3,
        "column": 12,
        "x": 984,
        "y": 318
    },
    {
        "personId": "00069988",
        "name": "SİNAN DİLEK",
        "grid_filename": "grid_3.png",
        "row": 5,
        "column": 3,
        "x": 246,
        "y": 530
    },
    {
        "personId": "00057538",
        "name": "KADİR BURÇİN YILMAZ",
        "grid_filename": "grid_3.png",
        "row": 5,
        "column": 6,
        "x": 492,
        "y": 530
    },
    {
        "personId": "00062830",
        "name": "MUHAMMED İKBAL ABAY",
        "grid_filename": "grid_3.png",
        "row": 7,
        "column": 0,
        "x": 0,
        "y": 742
    },
    {
        "personId": "00055043",
        "name": "ÜMİT EĞİN",
        "grid_filename": "grid_3.png",
        "row": 7,
        "column": 1,
        "x": 82,
        "y": 742
    },
    {
        "personId": "00073370",
        "name": "HÜSEYİN AVNİ GÜMRÜKÇÜOĞLU",
        "grid_filename": "grid_3.png",
        "row": 7,
        "column": 3,
        "x": 246,
        "y": 742
    },
    {
        "personId": "00100480",
        "name": "FATİH ŞİRİN",
        "grid_filename": "grid_3.png",
        "row": 7,
        "column": 12,
        "x": 984,
        "y": 742
    },
    {
        "personId": "00069818",
        "name": "OSMAN KERİM AVANAŞ",
        "grid_filename": "grid_3.png",
        "row": 8,
        "column": 0,
        "x": 0,
        "y": 848
    },
    {
        "personId": "00063185",
        "name": "RAMAZAN BİNGÜL",
        "grid_filename": "grid_3.png",
        "row": 9,
        "column": 0,
        "x": 0,
        "y": 954
    },
    {
        "personId": "00070061",
        "name": "MELEK BİLİCİ",
        "grid_filename": "grid_3.png",
        "row": 9,
        "column": 2,
        "x": 164,
        "y": 954
    },
    {
        "personId": "00083573",
        "name": "ABDULLAH ARİF UYSAL",
        "grid_filename": "grid_4.png",
        "row": 0,
        "column": 2,
        "x": 164,
        "y": 0
    },
    {
        "personId": "00080837",
        "name": "ÖMER MESUT ÖZEN",
        "grid_filename": "grid_4.png",
        "row": 1,
        "column": 11,
        "x": 902,
        "y": 106
    },
    {
        "personId": "00062762",
        "name": "YUSUF YILMAZ",
        "grid_filename": "grid_4.png",
        "row": 2,
        "column": 5,
        "x": 410,
        "y": 212
    },
    {
        "personId": "00063143",
        "name": "ÖMER ÜNSAL OKÇU",
        "grid_filename": "grid_4.png",
        "row": 2,
        "column": 13,
        "x": 1066,
        "y": 212
    },
    {
        "personId": "00067036",
        "name": "ABDULLAH AKAT",
        "grid_filename": "grid_4.png",
        "row": 3,
        "column": 13,
        "x": 1066,
        "y": 318
    },
    {
        "personId": "00068792",
        "name": "HUZEYFE BİRKAN",
        "grid_filename": "grid_4.png",
        "row": 4,
        "column": 6,
        "x": 492,
        "y": 424
    },
    {
        "personId": "00061687",
        "name": "OĞUZCAN YERLİ",
        "grid_filename": "grid_4.png",
        "row": 5,
        "column": 0,
        "x": 0,
        "y": 530
    },
    {
        "personId": "00069354",
        "name": "YAVUZ ULUSOY",
        "grid_filename": "grid_4.png",
        "row": 5,
        "column": 1,
        "x": 82,
        "y": 530
    },
    {
        "personId": "00069927",
        "name": "KENAN İNCE",
        "grid_filename": "grid_4.png",
        "row": 5,
        "column": 8,
        "x": 656,
        "y": 530
    },
    {
        "personId": "00060615",
        "name": "ABDULLAH BAHADIR BÜYÜKKAYMAZ",
        "grid_filename": "grid_4.png",
        "row": 5,
        "column": 12,
        "x": 984,
        "y": 530
    },
    {
        "personId": "00068347",
        "name": "MURAT YALÇIN KIRCA",
        "grid_filename": "grid_4.png",
        "row": 7,
        "column": 4,
        "x": 328,
        "y": 742
    },
    {
        "personId": "00054926",
        "name": "EROL ŞENOL",
        "grid_filename": "grid_4.png",
        "row": 8,
        "column": 0,
        "x": 0,
        "y": 848
    },
    {
        "personId": "00070864",
        "name": "HUZEYFE AKHAN",
        "grid_filename": "grid_4.png",
        "row": 8,
        "column": 2,
        "x": 164,
        "y": 848
    },
    {
        "personId": "00053412",
        "name": "YUSUF GÜRDAL YILMAZ",
        "grid_filename": "grid_4.png",
        "row": 8,
        "column": 13,
        "x": 1066,
        "y": 848
    },
    {
        "personId": "00102882",
        "name": "İBRAHİM HALİL TUNÇ",
        "grid_filename": "grid_4.png",
        "row": 9,
        "column": 12,
        "x": 984,
        "y": 954
    },
    {
        "personId": "00067755",
        "name": "MEHMET KIZILTAN",
        "grid_filename": "grid_4.png",
        "row": 10,
        "column": 2,
        "x": 164,
        "y": 1060
    },
    {
        "personId": "00075011",
        "name": "ABDULLAH YILMAZ",
        "grid_filename": "grid_4.png",
        "row": 10,
        "column": 3,
        "x": 246,
        "y": 1060
    },
    {
        "personId": "00073377",
        "name": "FEYZA İMAL",
        "grid_filename": "grid_4.png",
        "row": 10,
        "column": 4,
        "x": 328,
        "y": 1060
    },
    {
        "personId": "00053229",
        "name": "MEHMET AKİF KONAR",
        "grid_filename": "grid_5.png",
        "row": 0,
        "column": 2,
        "x": 164,
        "y": 0
    },
    {
        "personId": "00049410",
        "name": "SİNAN KÜNTAY",
        "grid_filename": "grid_5.png",
        "row": 0,
        "column": 8,
        "x": 656,
        "y": 0
    },
    {
        "personId": "00080784",
        "name": "ŞÜKÜR ERKUT",
        "grid_filename": "grid_5.png",
        "row": 1,
        "column": 7,
        "x": 574,
        "y": 106
    },
    {
        "personId": "00054148",
        "name": "MURAT BAŞ",
        "grid_filename": "grid_5.png",
        "row": 2,
        "column": 4,
        "x": 328,
        "y": 212
    },
    {
        "personId": "00060200",
        "name": "MEHMET EMİN İŞBİLEN",
        "grid_filename": "grid_5.png",
        "row": 3,
        "column": 9,
        "x": 738,
        "y": 318
    },
    {
        "personId": "00056441",
        "name": "ARİF AYAZ",
        "grid_filename": "grid_5.png",
        "row": 5,
        "column": 0,
        "x": 0,
        "y": 530
    },
    {
        "personId": "00057452",
        "name": "AHMET ACAR",
        "grid_filename": "grid_5.png",
        "row": 5,
        "column": 8,
        "x": 656,
        "y": 530
    },
    {
        "personId": "00074202",
        "name": "SELÇUK İBRAHİMOĞLU",
        "grid_filename": "grid_5.png",
        "row": 7,
        "column": 13,
        "x": 1066,
        "y": 742
    },
    {
        "personId": "00089801",
        "name": "AYDOĞAN CAN",
        "grid_filename": "grid_5.png",
        "row": 9,
        "column": 0,
        "x": 0,
        "y": 954
    },
    {
        "personId": "00080374",
        "name": "MELİH ÖZTÜRK",
        "grid_filename": "grid_5.png",
        "row": 9,
        "column": 5,
        "x": 410,
        "y": 954
    },
    {
        "personId": "00077469",
        "name": "MUSTAFA ÇALIŞKAN",
        "grid_filename": "grid_5.png",
        "row": 9,
        "column": 7,
        "x": 574,
        "y": 954
    },
    {
        "personId": "00055927",
        "name": "MESUT ALAN",
        "grid_filename": "grid_5.png",
        "row": 9,
        "column": 11,
        "x": 902,
        "y": 954
    },
    {
        "personId": "00060961",
        "name": "YAHYA ZAHİD ŞENSOY",
        "grid_filename": "grid_5.png",
        "row": 10,
        "column": 3,
        "x": 246,
        "y": 1060
    },
    {
        "personId": "00089802",
        "name": "ÖMER YUSUF KARAOĞLU",
        "grid_filename": "grid_5.png",
        "row": 10,
        "column": 10,
        "x": 820,
        "y": 1060
    },
    {
        "personId": "00044357",
        "name": "ŞEVKİ ERKAN ERDOĞAN",
        "grid_filename": "grid_6.png",
        "row": 0,
        "column": 0,
        "x": 0,
        "y": 0
    },
    {
        "personId": "00067991",
        "name": "SEDA LEBLEBİCİ",
        "grid_filename": "grid_6.png",
        "row": 2,
        "column": 10,
        "x": 820,
        "y": 212
    },
    {
        "personId": "00067014",
        "name": "FATİH TUNEL",
        "grid_filename": "grid_6.png",
        "row": 2,
        "column": 13,
        "x": 1066,
        "y": 212
    },
    {
        "personId": "00075176",
        "name": "HALİM YILMAZ",
        "grid_filename": "grid_6.png",
        "row": 3,
        "column": 5,
        "x": 410,
        "y": 318
    },
    {
        "personId": "00085900",
        "name": "MURAT ŞEKER",
        "grid_filename": "grid_6.png",
        "row": 3,
        "column": 6,
        "x": 492,
        "y": 318
    },
    {
        "personId": "00051183",
        "name": "TANER ERİM",
        "grid_filename": "grid_6.png",
        "row": 4,
        "column": 2,
        "x": 164,
        "y": 424
    },
    {
        "personId": "00066593",
        "name": "MUHAMMED NURULLAH HEPER",
        "grid_filename": "grid_6.png",
        "row": 5,
        "column": 11,
        "x": 902,
        "y": 530
    },
    {
        "personId": "00064810",
        "name": "RAFET FATİH ÖZGÜR",
        "grid_filename": "grid_6.png",
        "row": 6,
        "column": 7,
        "x": 574,
        "y": 636
    },
    {
        "personId": "00095286",
        "name": "KADİR BOZKURT",
        "grid_filename": "grid_6.png",
        "row": 6,
        "column": 10,
        "x": 820,
        "y": 636
    },
    {
        "personId": "00068052",
        "name": "CEMİL ÇİLOĞLU",
        "grid_filename": "grid_6.png",
        "row": 7,
        "column": 2,
        "x": 164,
        "y": 742
    },
    {
        "personId": "00074662",
        "name": "AYBİKE BAŞÇİVİ",
        "grid_filename": "grid_6.png",
        "row": 7,
        "column": 6,
        "x": 492,
        "y": 742
    },
    {
        "personId": "00063015",
        "name": "TARIK PARLAK",
        "grid_filename": "grid_6.png",
        "row": 7,
        "column": 11,
        "x": 902,
        "y": 742
    },
    {
        "personId": "00073957",
        "name": "MUSTAFA OĞULCAN BİLGİN",
        "grid_filename": "grid_6.png",
        "row": 8,
        "column": 6,
        "x": 492,
        "y": 848
    },
    {
        "personId": "00088095",
        "name": "SELİM YUMURTACI",
        "grid_filename": "grid_6.png",
        "row": 9,
        "column": 13,
        "x": 1066,
        "y": 954
    },
    {
        "personId": "00080793",
        "name": "GÖKHAN TAŞAR",
        "grid_filename": "grid_6.png",
        "row": 10,
        "column": 2,
        "x": 164,
        "y": 1060
    },
    {
        "personId": "00090410",
        "name": "EMRE MEMİŞ",
        "grid_filename": "grid_6.png",
        "row": 10,
        "column": 4,
        "x": 328,
        "y": 1060
    },
    {
        "personId": "00053206",
        "name": "ENİS ÖZDEMİRLİ",
        "grid_filename": "grid_6.png",
        "row": 10,
        "column": 11,
        "x": 902,
        "y": 1060
    },
    {
        "personId": "00051609",
        "name": "IBRAHIM SEDQI",
        "grid_filename": "grid_6.png",
        "row": 10,
        "column": 13,
        "x": 1066,
        "y": 1060
    },
    {
        "personId": "00051253",
        "name": "MUHAMMED MUSTAFA KUMSEL",
        "grid_filename": "grid_7.png",
        "row": 0,
        "column": 8,
        "x": 656,
        "y": 0
    },
    {
        "personId": "00072676",
        "name": "AHMET EMRE TÜRKOĞLU",
        "grid_filename": "grid_7.png",
        "row": 1,
        "column": 12,
        "x": 984,
        "y": 106
    },
    {
        "personId": "00047026",
        "name": "SERKAN MURAT AKHARMAN",
        "grid_filename": "grid_7.png",
        "row": 2,
        "column": 0,
        "x": 0,
        "y": 212
    },
    {
        "personId": "00062292",
        "name": "ÖMER FARUK YILMAZ",
        "grid_filename": "grid_7.png",
        "row": 2,
        "column": 6,
        "x": 492,
        "y": 212
    },
    {
        "personId": "00054925",
        "name": "SELİM KAHRAMAN",
        "grid_filename": "grid_7.png",
        "row": 3,
        "column": 0,
        "x": 0,
        "y": 318
    },
    {
        "personId": "00072981",
        "name": "ZEYNEP ÖZDEMİR",
        "grid_filename": "grid_7.png",
        "row": 3,
        "column": 1,
        "x": 82,
        "y": 318
    },
    {
        "personId": "00051669",
        "name": "MUZAFFER RİFAİOĞLU",
        "grid_filename": "grid_7.png",
        "row": 3,
        "column": 9,
        "x": 738,
        "y": 318
    },
    {
        "personId": "00069802",
        "name": "AHMET FARUK ŞAHİNER",
        "grid_filename": "grid_7.png",
        "row": 7,
        "column": 2,
        "x": 164,
        "y": 742
    },
    {
        "personId": "00054023",
        "name": "ERSEN KUZU",
        "grid_filename": "grid_7.png",
        "row": 7,
        "column": 4,
        "x": 328,
        "y": 742
    },
    {
        "personId": "00046557",
        "name": "VEDAT ÖZSABUNCU",
        "grid_filename": "grid_7.png",
        "row": 8,
        "column": 11,
        "x": 902,
        "y": 848
    },
    {
        "personId": "00073644",
        "name": "BAYRAM ERYILMAZ",
        "grid_filename": "grid_7.png",
        "row": 9,
        "column": 13,
        "x": 1066,
        "y": 954
    },
    {
        "personId": "00073302",
        "name": "TUĞBA KOÇ",
        "grid_filename": "grid_7.png",
        "row": 10,
        "column": 2,
        "x": 164,
        "y": 1060
    },
    {
        "personId": "00075289",
        "name": "MÜBAREK BAYRAM",
        "grid_filename": "grid_8.png",
        "row": 0,
        "column": 10,
        "x": 820,
        "y": 0
    },
    {
        "personId": "00073938",
        "name": "ALİ BATTAL",
        "grid_filename": "grid_8.png",
        "row": 1,
        "column": 1,
        "x": 82,
        "y": 106
    },
    {
        "personId": "00051436",
        "name": "TOLGAHAN AKBAŞ",
        "grid_filename": "grid_8.png",
        "row": 2,
        "column": 8,
        "x": 656,
        "y": 212
    },
    {
        "personId": "00085909",
        "name": "TÜLİN YILMAZ",
        "grid_filename": "grid_8.png",
        "row": 2,
        "column": 9,
        "x": 738,
        "y": 212
    },
    {
        "personId": "00066840",
        "name": "ÖMER FARUK SÖNMEZ",
        "grid_filename": "grid_8.png",
        "row": 2,
        "column": 11,
        "x": 902,
        "y": 212
    },
    {
        "personId": "00080786",
        "name": "BUĞRAHAN KARADEMİR",
        "grid_filename": "grid_8.png",
        "row": 2,
        "column": 12,
        "x": 984,
        "y": 212
    },
    {
        "personId": "00069450",
        "name": "FATİH BOZKURT",
        "grid_filename": "grid_8.png",
        "row": 3,
        "column": 6,
        "x": 492,
        "y": 318
    },
    {
        "personId": "00058385",
        "name": "HÜSEYİN YÜKSEK",
        "grid_filename": "grid_8.png",
        "row": 4,
        "column": 3,
        "x": 246,
        "y": 424
    },
    {
        "personId": "00074856",
        "name": "MİTHAT SAMED YAZICI",
        "grid_filename": "grid_8.png",
        "row": 5,
        "column": 11,
        "x": 902,
        "y": 530
    },
    {
        "personId": "00072998",
        "name": "MUSTAFA KEMAL ÖZAHİ",
        "grid_filename": "grid_8.png",
        "row": 6,
        "column": 2,
        "x": 164,
        "y": 636
    },
    {
        "personId": "00083057",
        "name": "SELÇUK İNCE",
        "grid_filename": "grid_8.png",
        "row": 7,
        "column": 0,
        "x": 0,
        "y": 742
    },
    {
        "personId": "00068755",
        "name": "SABRİ KARAKAŞ",
        "grid_filename": "grid_8.png",
        "row": 8,
        "column": 9,
        "x": 738,
        "y": 848
    },
    {
        "personId": "00064886",
        "name": "ALİ TİPİ",
        "grid_filename": "grid_8.png",
        "row": 10,
        "column": 1,
        "x": 82,
        "y": 1060
    },
    {
        "personId": "00020112",
        "name": "MECİT EŞ",
        "grid_filename": "grid_8.png",
        "row": 10,
        "column": 3,
        "x": 246,
        "y": 1060
    },
    {
        "personId": "00048736",
        "name": "ÜMİT DEVELİ",
        "grid_filename": "grid_8.png",
        "row": 10,
        "column": 11,
        "x": 902,
        "y": 1060
    },
    {
        "personId": "00063649",
        "name": "DURMUŞ TARIK KARADAĞ",
        "grid_filename": "grid_9.png",
        "row": 0,
        "column": 0,
        "x": 0,
        "y": 0
    },
    {
        "personId": "00052022",
        "name": "İLKER ÖZAYDIN",
        "grid_filename": "grid_9.png",
        "row": 0,
        "column": 1,
        "x": 82,
        "y": 0
    },
    {
        "personId": "00055187",
        "name": "MEHMET FATİH AYGÜNER",
        "grid_filename": "grid_9.png",
        "row": 1,
        "column": 2,
        "x": 164,
        "y": 106
    },
    {
        "personId": "00053104",
        "name": "BİLAL EKŞİ",
        "grid_filename": "grid_9.png",
        "row": 1,
        "column": 4,
        "x": 328,
        "y": 106
    },
    {
        "personId": "00117545",
        "name": "ÖZCAN BAŞOĞLU",
        "grid_filename": "grid_9.png",
        "row": 2,
        "column": 8,
        "x": 656,
        "y": 212
    },
    {
        "personId": "00063011",
        "name": "TARIK KURU",
        "grid_filename": "grid_9.png",
        "row": 4,
        "column": 9,
        "x": 738,
        "y": 424
    },
    {
        "personId": "00051906",
        "name": "MEHMET YILDIRIM",
        "grid_filename": "grid_9.png",
        "row": 5,
        "column": 7,
        "x": 574,
        "y": 530
    },
    {
        "personId": "00051483",
        "name": "CENGİZ TUNCEL",
        "grid_filename": "grid_9.png",
        "row": 6,
        "column": 0,
        "x": 0,
        "y": 636
    },
    {
        "personId": "00067658",
        "name": "NİHAT ÇEVİK",
        "grid_filename": "grid_9.png",
        "row": 6,
        "column": 11,
        "x": 902,
        "y": 636
    },
    {
        "personId": "00073477",
        "name": "ERSEL ÇAĞATAY SAVCI",
        "grid_filename": "grid_9.png",
        "row": 7,
        "column": 7,
        "x": 574,
        "y": 742
    },
    {
        "personId": "00070365",
        "name": "ŞERAFETTİN EKİCİ",
        "grid_filename": "grid_9.png",
        "row": 9,
        "column": 13,
        "x": 1066,
        "y": 954
    },
    {
        "personId": "00074199",
        "name": "HAMZA ALTUNDAĞ",
        "grid_filename": "grid_10.png",
        "row": 0,
        "column": 4,
        "x": 328,
        "y": 0
    },
    {
        "personId": "00061123",
        "name": "MUHAMMET BURAK ÖZTÜRK",
        "grid_filename": "grid_10.png",
        "row": 1,
        "column": 2,
        "x": 164,
        "y": 106
    },
    {
        "personId": "00063044",
        "name": "DİNÇER EROĞLU",
        "grid_filename": "grid_10.png",
        "row": 1,
        "column": 11,
        "x": 902,
        "y": 106
    },
    {
        "personId": "00074993",
        "name": "İBRAHİM BULUT",
        "grid_filename": "grid_10.png",
        "row": 2,
        "column": 7,
        "x": 574,
        "y": 212
    },
    {
        "personId": "00054306",
        "name": "ABDULLAH YORMAZ",
        "grid_filename": "grid_10.png",
        "row": 2,
        "column": 8,
        "x": 656,
        "y": 212
    },
    {
        "personId": "00066599",
        "name": "EMİNE AHMETOĞLU HAKBİLEN",
        "grid_filename": "grid_10.png",
        "row": 2,
        "column": 11,
        "x": 902,
        "y": 212
    },
    {
        "personId": "00065802",
        "name": "ÖMER FARUK ALİER",
        "grid_filename": "grid_10.png",
        "row": 4,
        "column": 0,
        "x": 0,
        "y": 424
    },
    {
        "personId": "00073273",
        "name": "HAMİD ELDELEKLİOĞLU",
        "grid_filename": "grid_10.png",
        "row": 5,
        "column": 2,
        "x": 164,
        "y": 530
    },
    {
        "personId": "00046198",
        "name": "FATİH ATACAN TEMEL",
        "grid_filename": "grid_10.png",
        "row": 6,
        "column": 10,
        "x": 820,
        "y": 636
    },
    {
        "personId": "00090381",
        "name": "GÜLÇİN GÜLKILIK",
        "grid_filename": "grid_10.png",
        "row": 7,
        "column": 2,
        "x": 164,
        "y": 742
    },
    {
        "personId": "00083609",
        "name": "ALPASLAN CEBE",
        "grid_filename": "grid_10.png",
        "row": 7,
        "column": 11,
        "x": 902,
        "y": 742
    },
    {
        "personId": "00063320",
        "name": "ÖMER ASLAN",
        "grid_filename": "grid_10.png",
        "row": 9,
        "column": 7,
        "x": 574,
        "y": 954
    },
    {
        "personId": "00047091",
        "name": "FİLİZ TUĞÇAY",
        "grid_filename": "grid_11.png",
        "row": 0,
        "column": 0,
        "x": 0,
        "y": 0
    },
    {
        "personId": "00058890",
        "name": "İSMET MİNDAŞ",
        "grid_filename": "grid_11.png",
        "row": 1,
        "column": 1,
        "x": 82,
        "y": 106
    },
    {
        "personId": "00069246",
        "name": "MUTTALİP İLHAN",
        "grid_filename": "grid_11.png",
        "row": 1,
        "column": 8,
        "x": 656,
        "y": 106
    },
    {
        "personId": "00072638",
        "name": "ABDULLAH AHMET TUĞCU",
        "grid_filename": "grid_11.png",
        "row": 2,
        "column": 11,
        "x": 902,
        "y": 212
    },
    {
        "personId": "00063507",
        "name": "BETÜL ÇOLAK",
        "grid_filename": "grid_11.png",
        "row": 3,
        "column": 11,
        "x": 902,
        "y": 318
    },
    {
        "personId": "00053159",
        "name": "LEVENT KONUKCU",
        "grid_filename": "grid_11.png",
        "row": 4,
        "column": 4,
        "x": 328,
        "y": 424
    },
    {
        "personId": "00085400",
        "name": "NECMİ BİRİNCİ",
        "grid_filename": "grid_11.png",
        "row": 4,
        "column": 13,
        "x": 1066,
        "y": 424
    },
    {
        "personId": "00045416",
        "name": "EMEL BİRYILMAZ",
        "grid_filename": "grid_11.png",
        "row": 6,
        "column": 8,
        "x": 656,
        "y": 636
    },
    {
        "personId": "00088127",
        "name": "MUSTAFA CİHANGİR OĞUZ",
        "grid_filename": "grid_11.png",
        "row": 7,
        "column": 4,
        "x": 328,
        "y": 742
    },
    {
        "personId": "00020256",
        "name": "GÜLDEN NACAR",
        "grid_filename": "grid_11.png",
        "row": 7,
        "column": 11,
        "x": 902,
        "y": 742
    },
    {
        "personId": "00093864",
        "name": "KÜBRA FİLİKCİ",
        "grid_filename": "grid_11.png",
        "row": 9,
        "column": 11,
        "x": 902,
        "y": 954
    },
    {
        "personId": "00020117",
        "name": "BİLAL EKŞİ",
        "grid_filename": "grid_11.png",
        "row": 10,
        "column": 3,
        "x": 246,
        "y": 1060
    },
    {
        "personId": "00065617",
        "name": "MUHAMMET ENSAR KARABULUT",
        "grid_filename": "grid_11.png",
        "row": 10,
        "column": 6,
        "x": 492,
        "y": 1060
    },
    {
        "personId": "00052413",
        "name": "İPEK GÜRBÜZ TOKLİCAN",
        "grid_filename": "grid_11.png",
        "row": 10,
        "column": 9,
        "x": 738,
        "y": 1060
    },
    {
        "personId": "00062774",
        "name": "EMRAH TEKİNDEMİR",
        "grid_filename": "grid_12.png",
        "row": 0,
        "column": 1,
        "x": 82,
        "y": 0
    },
    {
        "personId": "00063338",
        "name": "GÖKHAN ÇETİN",
        "grid_filename": "grid_12.png",
        "row": 0,
        "column": 7,
        "x": 574,
        "y": 0
    },
    {
        "personId": "00078680",
        "name": "İBRAHİM DÜNDARAN",
        "grid_filename": "grid_12.png",
        "row": 1,
        "column": 3,
        "x": 246,
        "y": 106
    },
    {
        "personId": "00047213",
        "name": "ERSEN ENGİN",
        "grid_filename": "grid_12.png",
        "row": 2,
        "column": 6,
        "x": 492,
        "y": 212
    },
    {
        "personId": "00049945",
        "name": "ERCAN LAÇİN",
        "grid_filename": "grid_12.png",
        "row": 3,
        "column": 8,
        "x": 656,
        "y": 318
    },
    {
        "personId": "00052500",
        "name": "HASAN DEMİR",
        "grid_filename": "grid_12.png",
        "row": 3,
        "column": 12,
        "x": 984,
        "y": 318
    },
    {
        "personId": "00075457",
        "name": "AYŞE TUBA BERK",
        "grid_filename": "grid_12.png",
        "row": 4,
        "column": 9,
        "x": 738,
        "y": 424
    },
    {
        "personId": "00068340",
        "name": "NEŞE AY",
        "grid_filename": "grid_12.png",
        "row": 5,
        "column": 13,
        "x": 1066,
        "y": 530
    },
    {
        "personId": "00063245",
        "name": "ALİ ENSAR KILIÇOĞLU",
        "grid_filename": "grid_12.png",
        "row": 7,
        "column": 6,
        "x": 492,
        "y": 742
    },
    {
        "personId": "00064874",
        "name": "SAMİ AYDOGAN",
        "grid_filename": "grid_12.png",
        "row": 7,
        "column": 7,
        "x": 574,
        "y": 742
    },
    {
        "personId": "00064346",
        "name": "FİGEN BAYER",
        "grid_filename": "grid_12.png",
        "row": 8,
        "column": 5,
        "x": 410,
        "y": 848
    },
    {
        "personId": "00054573",
        "name": "VURAL URSAVAŞ",
        "grid_filename": "grid_12.png",
        "row": 8,
        "column": 10,
        "x": 820,
        "y": 848
    },
    {
        "personId": "00072805",
        "name": "SÜLEYMAN YASİR VERİMLİ",
        "grid_filename": "grid_12.png",
        "row": 10,
        "column": 11,
        "x": 902,
        "y": 1060
    },
    {
        "personId": "00069771",
        "name": "BETÜL AKDOĞAN",
        "grid_filename": "grid_13.png",
        "row": 1,
        "column": 10,
        "x": 820,
        "y": 106
    },
    {
        "personId": "00062791",
        "name": "MEHMET SAMİ İKİNCİ",
        "grid_filename": "grid_13.png",
        "row": 2,
        "column": 4,
        "x": 328,
        "y": 212
    },
    {
        "personId": "00048556",
        "name": "HAKAN KOÇ",
        "grid_filename": "grid_13.png",
        "row": 2,
        "column": 11,
        "x": 902,
        "y": 212
    },
    {
        "personId": "00069380",
        "name": "MUSTAFA ERDOĞAN",
        "grid_filename": "grid_13.png",
        "row": 5,
        "column": 0,
        "x": 0,
        "y": 530
    },
    {
        "personId": "00060617",
        "name": "HATİCE GİRGİN",
        "grid_filename": "grid_13.png",
        "row": 5,
        "column": 10,
        "x": 820,
        "y": 530
    },
    {
        "personId": "00068245",
        "name": "GÜLAY ERKAL",
        "grid_filename": "grid_13.png",
        "row": 5,
        "column": 11,
        "x": 902,
        "y": 530
    },
    {
        "personId": "00043963",
        "name": "BÜLENT ECVET DENİZ",
        "grid_filename": "grid_13.png",
        "row": 7,
        "column": 4,
        "x": 328,
        "y": 742
    },
    {
        "personId": "00072085",
        "name": "SEYFULLAH İLYAS",
        "grid_filename": "grid_13.png",
        "row": 7,
        "column": 8,
        "x": 656,
        "y": 742
    },
    {
        "personId": "00059111",
        "name": "OSMAN DİNÇER SAYICI",
        "grid_filename": "grid_13.png",
        "row": 8,
        "column": 4,
        "x": 328,
        "y": 848
    },
    {
        "personId": "00089878",
        "name": "LAÇİN REYYAN GÜNDEN",
        "grid_filename": "grid_13.png",
        "row": 9,
        "column": 4,
        "x": 328,
        "y": 954
    },
    {
        "personId": "00083565",
        "name": "BANUHAN BERBEROĞLU TAŞAR",
        "grid_filename": "grid_13.png",
        "row": 9,
        "column": 7,
        "x": 574,
        "y": 954
    },
    {
        "personId": "00051606",
        "name": "AHMET SERHAT SARI",
        "grid_filename": "grid_13.png",
        "row": 10,
        "column": 8,
        "x": 656,
        "y": 1060
    },
    {
        "personId": "00063318",
        "name": "NEVZAT ERDEMİR",
        "grid_filename": "grid_13.png",
        "row": 10,
        "column": 12,
        "x": 984,
        "y": 1060
    },
    {
        "personId": "00074311",
        "name": "İREM KUYAN",
        "grid_filename": "grid_14.png",
        "row": 0,
        "column": 2,
        "x": 164,
        "y": 0
    },
    {
        "personId": "00054299",
        "name": "MAHMUT YAYLA",
        "grid_filename": "grid_14.png",
        "row": 0,
        "column": 13,
        "x": 1066,
        "y": 0
    },
    {
        "personId": "00061175",
        "name": "BORA AKSOYLU",
        "grid_filename": "grid_14.png",
        "row": 1,
        "column": 4,
        "x": 328,
        "y": 106
    },
    {
        "personId": "00053712",
        "name": "GÖKHAN ÇİFCİ",
        "grid_filename": "grid_14.png",
        "row": 1,
        "column": 9,
        "x": 738,
        "y": 106
    },
    {
        "personId": "00063738",
        "name": "ÖMER ÖNDER HABERDAR",
        "grid_filename": "grid_14.png",
        "row": 1,
        "column": 10,
        "x": 820,
        "y": 106
    },
    {
        "personId": "00079587",
        "name": "MELİK TAHA KİRAZ",
        "grid_filename": "grid_14.png",
        "row": 2,
        "column": 7,
        "x": 574,
        "y": 212
    },
    {
        "personId": "00052883",
        "name": "BANU KURT",
        "grid_filename": "grid_14.png",
        "row": 2,
        "column": 9,
        "x": 738,
        "y": 212
    },
    {
        "personId": "00065126",
        "name": "BİLAL ARPACI",
        "grid_filename": "grid_14.png",
        "row": 4,
        "column": 1,
        "x": 82,
        "y": 424
    },
    {
        "personId": "00061468",
        "name": "ÖZGE ŞAHİN",
        "grid_filename": "grid_14.png",
        "row": 4,
        "column": 9,
        "x": 738,
        "y": 424
    },
    {
        "personId": "00067411",
        "name": "YUNUS ÖZLEYEN",
        "grid_filename": "grid_14.png",
        "row": 4,
        "column": 10,
        "x": 820,
        "y": 424
    },
    {
        "personId": "00068051",
        "name": "İZZET EMRE GÖL",
        "grid_filename": "grid_14.png",
        "row": 4,
        "column": 12,
        "x": 984,
        "y": 424
    },
    {
        "personId": "00043858",
        "name": "ERKAN İNCE",
        "grid_filename": "grid_14.png",
        "row": 5,
        "column": 0,
        "x": 0,
        "y": 530
    },
    {
        "personId": "00074921",
        "name": "MESUT AYBAKAN",
        "grid_filename": "grid_14.png",
        "row": 5,
        "column": 13,
        "x": 1066,
        "y": 530
    },
    {
        "personId": "00060935",
        "name": "HANDE SÖYLER",
        "grid_filename": "grid_14.png",
        "row": 6,
        "column": 13,
        "x": 1066,
        "y": 636
    },
    {
        "personId": "00054283",
        "name": "SELAMET TURNA",
        "grid_filename": "grid_14.png",
        "row": 8,
        "column": 12,
        "x": 984,
        "y": 848
    },
    {
        "personId": "00052789",
        "name": "REŞAT GÜNDÜZ",
        "grid_filename": "grid_14.png",
        "row": 8,
        "column": 13,
        "x": 1066,
        "y": 848
    },
    {
        "personId": "00054203",
        "name": "NESİH GÜMÜŞ",
        "grid_filename": "grid_14.png",
        "row": 9,
        "column": 0,
        "x": 0,
        "y": 954
    },
    {
        "personId": "00077418",
        "name": "FATİH ONUL",
        "grid_filename": "grid_14.png",
        "row": 9,
        "column": 2,
        "x": 164,
        "y": 954
    },
    {
        "personId": "00067690",
        "name": "MAHMUD ÜSAME GÜNGÖR",
        "grid_filename": "grid_14.png",
        "row": 10,
        "column": 9,
        "x": 738,
        "y": 1060
    },
    {
        "personId": "00069103",
        "name": "AYDIN AKGÜL",
        "grid_filename": "grid_15.png",
        "row": 0,
        "column": 1,
        "x": 82,
        "y": 0
    },
    {
        "personId": "00051563",
        "name": "KAMİL ENGİN KARAMAN",
        "grid_filename": "grid_15.png",
        "row": 1,
        "column": 3,
        "x": 246,
        "y": 106
    },
    {
        "personId": "00070169",
        "name": "MEHMET NURETTİN KAYGISIZ",
        "grid_filename": "grid_15.png",
        "row": 1,
        "column": 8,
        "x": 656,
        "y": 106
    },
    {
        "personId": "00063740",
        "name": "UBEYDULLAH CAN",
        "grid_filename": "grid_15.png",
        "row": 1,
        "column": 9,
        "x": 738,
        "y": 106
    },
    {
        "personId": "00054246",
        "name": "ELİF ÖZSOY",
        "grid_filename": "grid_15.png",
        "row": 4,
        "column": 5,
        "x": 410,
        "y": 424
    },
    {
        "personId": "00054245",
        "name": "SERDAR ÖZKAN",
        "grid_filename": "grid_15.png",
        "row": 5,
        "column": 2,
        "x": 164,
        "y": 530
    },
    {
        "personId": "00069439",
        "name": "ERHAN BALABAN",
        "grid_filename": "grid_15.png",
        "row": 5,
        "column": 3,
        "x": 246,
        "y": 530
    },
    {
        "personId": "00069339",
        "name": "MUHAMMET TAHA ÖZKAN",
        "grid_filename": "grid_15.png",
        "row": 5,
        "column": 12,
        "x": 984,
        "y": 530
    },
    {
        "personId": "00051092",
        "name": "YÜCEL BAŞYİĞİT",
        "grid_filename": "grid_15.png",
        "row": 5,
        "column": 13,
        "x": 1066,
        "y": 530
    },
    {
        "personId": "00063586",
        "name": "KADİR YILDIZ",
        "grid_filename": "grid_15.png",
        "row": 6,
        "column": 9,
        "x": 738,
        "y": 636
    },
    {
        "personId": "00066788",
        "name": "ENES DEMİRÖZ",
        "grid_filename": "grid_15.png",
        "row": 6,
        "column": 11,
        "x": 902,
        "y": 636
    },
    {
        "personId": "00058255",
        "name": "SEDAT EŞGİ",
        "grid_filename": "grid_15.png",
        "row": 10,
        "column": 5,
        "x": 410,
        "y": 1060
    },
    {
        "personId": "00049778",
        "name": "GÜREL TÜMER",
        "grid_filename": "grid_15.png",
        "row": 10,
        "column": 13,
        "x": 1066,
        "y": 1060
    },
    {
        "personId": "00073673",
        "name": "EREN SÜRÜCÜ",
        "grid_filename": "grid_16.png",
        "row": 0,
        "column": 9,
        "x": 738,
        "y": 0
    },
    {
        "personId": "00080196",
        "name": "AYŞE SALCAN ARSLAN",
        "grid_filename": "grid_16.png",
        "row": 0,
        "column": 13,
        "x": 1066,
        "y": 0
    },
    {
        "personId": "00047034",
        "name": "ÜMİT ALBAYRAK",
        "grid_filename": "grid_16.png",
        "row": 1,
        "column": 0,
        "x": 0,
        "y": 106
    },
    {
        "personId": "00067010",
        "name": "DİLEK YALÇIN",
        "grid_filename": "grid_16.png",
        "row": 1,
        "column": 6,
        "x": 492,
        "y": 106
    },
    {
        "personId": "00067797",
        "name": "MEHMET ZAHİD ÖZEL",
        "grid_filename": "grid_16.png",
        "row": 2,
        "column": 3,
        "x": 246,
        "y": 212
    },
    {
        "personId": "00075459",
        "name": "ÖMER KEREM BEKTEŞ",
        "grid_filename": "grid_16.png",
        "row": 4,
        "column": 12,
        "x": 984,
        "y": 424
    },
    {
        "personId": "00093388",
        "name": "BİLAL OKUR",
        "grid_filename": "grid_16.png",
        "row": 5,
        "column": 0,
        "x": 0,
        "y": 530
    },
    {
        "personId": "00054361",
        "name": "GÖKAY KOCA",
        "grid_filename": "grid_16.png",
        "row": 5,
        "column": 1,
        "x": 82,
        "y": 530
    },
    {
        "personId": "00069898",
        "name": "BERKANT KOLCU",
        "grid_filename": "grid_16.png",
        "row": 5,
        "column": 6,
        "x": 492,
        "y": 530
    },
    {
        "personId": "00068486",
        "name": "BERK YILDIZ",
        "grid_filename": "grid_16.png",
        "row": 5,
        "column": 10,
        "x": 820,
        "y": 530
    },
    {
        "personId": "00079334",
        "name": "ÜMMET ŞENOCAK",
        "grid_filename": "grid_16.png",
        "row": 5,
        "column": 11,
        "x": 902,
        "y": 530
    },
    {
        "personId": "00013397",
        "name": "RAMAZAN SARI",
        "grid_filename": "grid_16.png",
        "row": 5,
        "column": 12,
        "x": 984,
        "y": 530
    },
    {
        "personId": "00067259",
        "name": "MUSTAFA DEMİRCİ",
        "grid_filename": "grid_16.png",
        "row": 6,
        "column": 13,
        "x": 1066,
        "y": 636
    },
    {
        "personId": "00075370",
        "name": "ESRA FINDIK",
        "grid_filename": "grid_16.png",
        "row": 7,
        "column": 8,
        "x": 656,
        "y": 742
    },
    {
        "personId": "00051672",
        "name": "FIRAT KİRİŞ",
        "grid_filename": "grid_16.png",
        "row": 7,
        "column": 10,
        "x": 820,
        "y": 742
    },
    {
        "personId": "00077578",
        "name": "HİLYE BANU DEĞERLİ",
        "grid_filename": "grid_16.png",
        "row": 9,
        "column": 6,
        "x": 492,
        "y": 954
    },
    {
        "personId": "00047828",
        "name": "YELİZ DUYURAN",
        "grid_filename": "grid_16.png",
        "row": 10,
        "column": 6,
        "x": 492,
        "y": 1060
    },
    {
        "personId": "00049854",
        "name": "ARİF EKEN",
        "grid_filename": "grid_16.png",
        "row": 10,
        "column": 11,
        "x": 902,
        "y": 1060
    },
    {
        "personId": "00047173",
        "name": "PINAR AYVAZ ARIKAN",
        "grid_filename": "grid_17.png",
        "row": 1,
        "column": 0,
        "x": 0,
        "y": 106
    },
    {
        "personId": "00085088",
        "name": "ÖZKAN ELBAN",
        "grid_filename": "grid_17.png",
        "row": 1,
        "column": 3,
        "x": 246,
        "y": 106
    },
    {
        "personId": "00088400",
        "name": "HABİBE ESRA ER",
        "grid_filename": "grid_17.png",
        "row": 3,
        "column": 3,
        "x": 246,
        "y": 318
    },
    {
        "personId": "00100616",
        "name": "OKAN AKTAŞ",
        "grid_filename": "grid_17.png",
        "row": 3,
        "column": 4,
        "x": 328,
        "y": 318
    },
    {
        "personId": "00063566",
        "name": "MUHARREM REÇBER",
        "grid_filename": "grid_17.png",
        "row": 4,
        "column": 3,
        "x": 246,
        "y": 424
    },
    {
        "personId": "00055408",
        "name": "AHMET ULUDAĞ",
        "grid_filename": "grid_17.png",
        "row": 5,
        "column": 0,
        "x": 0,
        "y": 530
    },
    {
        "personId": "00051933",
        "name": "OSMAN HACIMAHMUTOĞLU",
        "grid_filename": "grid_17.png",
        "row": 5,
        "column": 2,
        "x": 164,
        "y": 530
    },
    {
        "personId": "00060616",
        "name": "OKAN ÖKSÜZ",
        "grid_filename": "grid_17.png",
        "row": 6,
        "column": 7,
        "x": 574,
        "y": 636
    },
    {
        "personId": "00053407",
        "name": "RAFET ŞİŞMAN",
        "grid_filename": "grid_17.png",
        "row": 7,
        "column": 2,
        "x": 164,
        "y": 742
    },
    {
        "personId": "00057996",
        "name": "MUSTAFA PEHLİVAN",
        "grid_filename": "grid_17.png",
        "row": 7,
        "column": 13,
        "x": 1066,
        "y": 742
    },
    {
        "personId": "00053408",
        "name": "FERDİ ÖZBÜYÜKYÖRÜK",
        "grid_filename": "grid_17.png",
        "row": 8,
        "column": 4,
        "x": 328,
        "y": 848
    },
    {
        "personId": "00087332",
        "name": "MEHMET SADIK KARAKUŞ",
        "grid_filename": "grid_17.png",
        "row": 8,
        "column": 10,
        "x": 820,
        "y": 848
    },
    {
        "personId": "00060497",
        "name": "CENKER EVREN TEZEL",
        "grid_filename": "grid_17.png",
        "row": 9,
        "column": 2,
        "x": 164,
        "y": 954
    },
    {
        "personId": "00074400",
        "name": "ABDULKADİR KARAMAN",
        "grid_filename": "grid_17.png",
        "row": 10,
        "column": 0,
        "x": 0,
        "y": 1060
    },
    {
        "personId": "00064387",
        "name": "MUSTAFA ASIM SUBAŞI",
        "grid_filename": "grid_18.png",
        "row": 0,
        "column": 7,
        "x": 574,
        "y": 0
    },
    {
        "personId": "00058132",
        "name": "ALİ ÖZDEMİR",
        "grid_filename": "grid_18.png",
        "row": 1,
        "column": 3,
        "x": 246,
        "y": 106
    },
    {
        "personId": "00086779",
        "name": "MUSTAFA TUNCER",
        "grid_filename": "grid_18.png",
        "row": 3,
        "column": 0,
        "x": 0,
        "y": 318
    },
    {
        "personId": "00065124",
        "name": "MEHMED ZİNGAL",
        "grid_filename": "grid_18.png",
        "row": 3,
        "column": 4,
        "x": 328,
        "y": 318
    },
    {
        "personId": "00057801",
        "name": "FAİK DENİZ",
        "grid_filename": "grid_18.png",
        "row": 5,
        "column": 4,
        "x": 328,
        "y": 530
    },
    {
        "personId": "00051364",
        "name": "EMRE ŞEN",
        "grid_filename": "grid_18.png",
        "row": 6,
        "column": 1,
        "x": 82,
        "y": 636
    },
    {
        "personId": "00058926",
        "name": "MUSTAFA ABACI",
        "grid_filename": "grid_18.png",
        "row": 6,
        "column": 2,
        "x": 164,
        "y": 636
    },
    {
        "personId": "00085211",
        "name": "ÖMER SEVBAN CEYLAN",
        "grid_filename": "grid_18.png",
        "row": 6,
        "column": 3,
        "x": 246,
        "y": 636
    },
    {
        "personId": "00112215",
        "name": "HAMZA DİNÇ",
        "grid_filename": "grid_18.png",
        "row": 7,
        "column": 1,
        "x": 82,
        "y": 742
    },
    {
        "personId": "00042726",
        "name": "ABDULLAH TUNCER KEÇECİ",
        "grid_filename": "grid_18.png",
        "row": 7,
        "column": 3,
        "x": 246,
        "y": 742
    },
    {
        "personId": "00049446",
        "name": "FATİH ÇELİK",
        "grid_filename": "grid_18.png",
        "row": 7,
        "column": 4,
        "x": 328,
        "y": 742
    },
    {
        "personId": "00065250",
        "name": "ÖMER ÖZDERYA",
        "grid_filename": "grid_18.png",
        "row": 7,
        "column": 8,
        "x": 656,
        "y": 742
    },
    {
        "personId": "00046743",
        "name": "ALPER ATALAY",
        "grid_filename": "grid_18.png",
        "row": 8,
        "column": 5,
        "x": 410,
        "y": 848
    },
    {
        "personId": "00063916",
        "name": "HASAN ÖZGÜL",
        "grid_filename": "grid_18.png",
        "row": 8,
        "column": 8,
        "x": 656,
        "y": 848
    },
    {
        "personId": "00063985",
        "name": "ÖMER FARUK ULU",
        "grid_filename": "grid_18.png",
        "row": 8,
        "column": 9,
        "x": 738,
        "y": 848
    },
    {
        "personId": "00043328",
        "name": "AYŞE ÖZLEM AKOVA",
        "grid_filename": "grid_18.png",
        "row": 8,
        "column": 10,
        "x": 820,
        "y": 848
    },
    {
        "personId": "00060464",
        "name": "MURAT GEZERAVCI",
        "grid_filename": "grid_18.png",
        "row": 8,
        "column": 11,
        "x": 902,
        "y": 848
    },
    {
        "personId": "00053157",
        "name": "HALİD KOCA",
        "grid_filename": "grid_18.png",
        "row": 9,
        "column": 9,
        "x": 738,
        "y": 954
    },
    {
        "personId": "00053817",
        "name": "SELİM KAHRIMAN",
        "grid_filename": "grid_19.png",
        "row": 0,
        "column": 7,
        "x": 574,
        "y": 0
    },
    {
        "personId": "00047077",
        "name": "MUSTAFA KARAKAŞ",
        "grid_filename": "grid_19.png",
        "row": 1,
        "column": 7,
        "x": 574,
        "y": 106
    },
    {
        "personId": "00067657",
        "name": "ABDURRAHİM DÜZCAN",
        "grid_filename": "grid_19.png",
        "row": 2,
        "column": 4,
        "x": 328,
        "y": 212
    },
    {
        "personId": "00064254",
        "name": "AYNUR AŞKIN",
        "grid_filename": "grid_19.png",
        "row": 3,
        "column": 2,
        "x": 164,
        "y": 318
    },
    {
        "personId": "00062192",
        "name": "AHMET YILDIZ",
        "grid_filename": "grid_19.png",
        "row": 3,
        "column": 5,
        "x": 410,
        "y": 318
    },
    {
        "personId": "00070343",
        "name": "MUSTAFA İSMAİL MÜCAHİTOĞLU",
        "grid_filename": "grid_19.png",
        "row": 4,
        "column": 4,
        "x": 328,
        "y": 424
    },
    {
        "personId": "00088092",
        "name": "ENSAR AKDAĞ",
        "grid_filename": "grid_19.png",
        "row": 4,
        "column": 6,
        "x": 492,
        "y": 424
    },
    {
        "personId": "00058406",
        "name": "NİGAR YILMAZ",
        "grid_filename": "grid_19.png",
        "row": 4,
        "column": 8,
        "x": 656,
        "y": 424
    },
    {
        "personId": "00081431",
        "name": "BÜŞRA YILDIZ KORKMAZ",
        "grid_filename": "grid_19.png",
        "row": 6,
        "column": 6,
        "x": 492,
        "y": 636
    },
    {
        "personId": "00063013",
        "name": "SELÇUK GENÇASLAN",
        "grid_filename": "grid_19.png",
        "row": 6,
        "column": 7,
        "x": 574,
        "y": 636
    },
    {
        "personId": "00058221",
        "name": "ÖMER FARUK KILIÇ",
        "grid_filename": "grid_19.png",
        "row": 6,
        "column": 13,
        "x": 1066,
        "y": 636
    },
    {
        "personId": "00062214",
        "name": "KADİR COŞKUN",
        "grid_filename": "grid_19.png",
        "row": 7,
        "column": 9,
        "x": 738,
        "y": 742
    },
    {
        "personId": "00045303",
        "name": "GÜRHAN SÖZEN",
        "grid_filename": "grid_19.png",
        "row": 8,
        "column": 0,
        "x": 0,
        "y": 848
    },
    {
        "personId": "00058565",
        "name": "AHMET KAYA",
        "grid_filename": "grid_19.png",
        "row": 9,
        "column": 2,
        "x": 164,
        "y": 954
    },
    {
        "personId": "00047927",
        "name": "ÖMER DERE",
        "grid_filename": "grid_19.png",
        "row": 10,
        "column": 6,
        "x": 492,
        "y": 1060
    },
    {
        "personId": "00063969",
        "name": "AKIN ÖMERCİKOĞLU",
        "grid_filename": "grid_20.png",
        "row": 1,
        "column": 6,
        "x": 492,
        "y": 106
    },
    {
        "personId": "00083474",
        "name": "MEHMET YANMAZ",
        "grid_filename": "grid_20.png",
        "row": 2,
        "column": 5,
        "x": 410,
        "y": 212
    },
    {
        "personId": "00060754",
        "name": "MEHMET DENİZ AYBEY",
        "grid_filename": "grid_20.png",
        "row": 3,
        "column": 2,
        "x": 164,
        "y": 318
    },
    {
        "personId": "00074864",
        "name": "RAMAZAN YAŞA",
        "grid_filename": "grid_20.png",
        "row": 4,
        "column": 11,
        "x": 902,
        "y": 424
    },
    {
        "personId": "00062899",
        "name": "EMRE İSMAİLOĞLU",
        "grid_filename": "grid_20.png",
        "row": 5,
        "column": 0,
        "x": 0,
        "y": 530
    },
    {
        "personId": "00076885",
        "name": "ERTAN TENGİZ",
        "grid_filename": "grid_20.png",
        "row": 6,
        "column": 2,
        "x": 164,
        "y": 636
    },
    {
        "personId": "00048232",
        "name": "ADNAN SÖKER",
        "grid_filename": "grid_20.png",
        "row": 6,
        "column": 3,
        "x": 246,
        "y": 636
    },
    {
        "personId": "00117237",
        "name": "HASAN DOĞAN",
        "grid_filename": "grid_20.png",
        "row": 7,
        "column": 0,
        "x": 0,
        "y": 742
    },
    {
        "personId": "00063570",
        "name": "NASRULLAH ERULUSOY",
        "grid_filename": "grid_20.png",
        "row": 7,
        "column": 9,
        "x": 738,
        "y": 742
    },
    {
        "personId": "00098829",
        "name": "HÜSEYİN KÜÇÜK",
        "grid_filename": "grid_20.png",
        "row": 8,
        "column": 5,
        "x": 410,
        "y": 848
    },
    {
        "personId": "00054136",
        "name": "MUHAMMED SONER AYDIN",
        "grid_filename": "grid_20.png",
        "row": 8,
        "column": 7,
        "x": 574,
        "y": 848
    },
    {
        "personId": "00067375",
        "name": "DENİZ DAŞTAN",
        "grid_filename": "grid_20.png",
        "row": 8,
        "column": 11,
        "x": 902,
        "y": 848
    },
    {
        "personId": "00075918",
        "name": "GÜLDEHAN ERDOĞAN",
        "grid_filename": "grid_20.png",
        "row": 8,
        "column": 12,
        "x": 984,
        "y": 848
    },
    {
        "personId": "00060936",
        "name": "ŞUAYB ÖZHAN",
        "grid_filename": "grid_20.png",
        "row": 8,
        "column": 13,
        "x": 1066,
        "y": 848
    },
    {
        "personId": "00020136",
        "name": "AHMET BOLAT",
        "grid_filename": "grid_20.png",
        "row": 9,
        "column": 1,
        "x": 82,
        "y": 954
    },
    {
        "personId": "00062761",
        "name": "FATİH AYDIN",
        "grid_filename": "grid_20.png",
        "row": 9,
        "column": 2,
        "x": 164,
        "y": 954
    },
    {
        "personId": "00070175",
        "name": "ÇAĞKAN TORUNLAR",
        "grid_filename": "grid_20.png",
        "row": 10,
        "column": 0,
        "x": 0,
        "y": 1060
    },
    {
        "personId": "00063193",
        "name": "BİLAL ÇELİK",
        "grid_filename": "grid_20.png",
        "row": 10,
        "column": 7,
        "x": 574,
        "y": 1060
    },
    {
        "personId": "00045398",
        "name": "KAĞAN TARANCI",
        "grid_filename": "grid_21.png",
        "row": 1,
        "column": 5,
        "x": 410,
        "y": 106
    },
    {
        "personId": "00069819",
        "name": "İBRAHİM HAKKI GÜNTAY",
        "grid_filename": "grid_21.png",
        "row": 2,
        "column": 12,
        "x": 984,
        "y": 212
    },
    {
        "personId": "00049600",
        "name": "BERRAK DAMLA YILDIRIM",
        "grid_filename": "grid_21.png",
        "row": 3,
        "column": 4,
        "x": 328,
        "y": 318
    },
    {
        "personId": "00047215",
        "name": "SÜLEYMAN ONUR YILMAZ",
        "grid_filename": "grid_21.png",
        "row": 3,
        "column": 5,
        "x": 410,
        "y": 318
    },
    {
        "personId": "00061465",
        "name": "MEHMET FARUK GURULKAN",
        "grid_filename": "grid_21.png",
        "row": 4,
        "column": 3,
        "x": 246,
        "y": 424
    },
    {
        "personId": "00083144",
        "name": "SERASER GİZEM BAŞAK",
        "grid_filename": "grid_21.png",
        "row": 4,
        "column": 5,
        "x": 410,
        "y": 424
    },
    {
        "personId": "00057482",
        "name": "BİLAL DEMİÇ",
        "grid_filename": "grid_21.png",
        "row": 5,
        "column": 2,
        "x": 164,
        "y": 530
    },
    {
        "personId": "00066043",
        "name": "SİBEL EMRE",
        "grid_filename": "grid_21.png",
        "row": 9,
        "column": 1,
        "x": 82,
        "y": 954
    },
    {
        "personId": "00058831",
        "name": "ŞEVKİ BAŞ",
        "grid_filename": "grid_21.png",
        "row": 9,
        "column": 8,
        "x": 656,
        "y": 954
    },
    {
        "personId": "00073663",
        "name": "OSMANNURİ USTABAŞ",
        "grid_filename": "grid_21.png",
        "row": 9,
        "column": 9,
        "x": 738,
        "y": 954
    },
    {
        "personId": "00063501",
        "name": "İBRAHİM HÜNKAR HAN ÇELİKHATİBOĞLU",
        "grid_filename": "grid_21.png",
        "row": 10,
        "column": 10,
        "x": 820,
        "y": 1060
    },
    {
        "personId": "00113038",
        "name": "HAYRİ CAN DUYGUN",
        "grid_filename": "grid_21.png",
        "row": 10,
        "column": 11,
        "x": 902,
        "y": 1060
    },
    {
        "personId": "00073329",
        "name": "MEHMED EKREM ERGİN",
        "grid_filename": "grid_22.png",
        "row": 2,
        "column": 3,
        "x": 246,
        "y": 212
    },
    {
        "personId": "00020257",
        "name": "ÖZGÜL ÖZKAN YAVUZ",
        "grid_filename": "grid_22.png",
        "row": 3,
        "column": 0,
        "x": 0,
        "y": 318
    },
    {
        "personId": "00062347",
        "name": "MUSTAFA SANDIKÇI",
        "grid_filename": "grid_22.png",
        "row": 3,
        "column": 9,
        "x": 738,
        "y": 318
    },
    {
        "personId": "00068383",
        "name": "ZEKERİYA KURUÇAM",
        "grid_filename": "grid_22.png",
        "row": 4,
        "column": 2,
        "x": 164,
        "y": 424
    },
    {
        "personId": "00066749",
        "name": "MUHAMMED EMRECAN İNANÇER",
        "grid_filename": "grid_22.png",
        "row": 4,
        "column": 7,
        "x": 574,
        "y": 424
    },
    {
        "personId": "00069084",
        "name": "OĞUZHAN CERRAH",
        "grid_filename": "grid_22.png",
        "row": 5,
        "column": 7,
        "x": 574,
        "y": 530
    },
    {
        "personId": "00063750",
        "name": "EMRAH ÇAĞLAR DELEN",
        "grid_filename": "grid_22.png",
        "row": 6,
        "column": 4,
        "x": 328,
        "y": 636
    },
    {
        "personId": "00057595",
        "name": "SAİT ARSLAN",
        "grid_filename": "grid_22.png",
        "row": 6,
        "column": 9,
        "x": 738,
        "y": 636
    },
    {
        "personId": "00051125",
        "name": "YAVUZ AKKAYNAK",
        "grid_filename": "grid_22.png",
        "row": 6,
        "column": 11,
        "x": 902,
        "y": 636
    },
    {
        "personId": "00051089",
        "name": "HAYRULLAH TÜRHAN",
        "grid_filename": "grid_22.png",
        "row": 7,
        "column": 1,
        "x": 82,
        "y": 742
    },
    {
        "personId": "00077571",
        "name": "SILA ADİLOĞLU YETİK",
        "grid_filename": "grid_22.png",
        "row": 8,
        "column": 6,
        "x": 492,
        "y": 848
    },
    {
        "personId": "00052348",
        "name": "AHMET OLMUŞTUR",
        "grid_filename": "grid_22.png",
        "row": 8,
        "column": 13,
        "x": 1066,
        "y": 848
    },
    {
        "personId": "00068745",
        "name": "ÇAĞATAY CAN",
        "grid_filename": "grid_22.png",
        "row": 9,
        "column": 3,
        "x": 246,
        "y": 954
    },
    {
        "personId": "00051215",
        "name": "HAKAN KÜÇÜK",
        "grid_filename": "grid_22.png",
        "row": 9,
        "column": 6,
        "x": 492,
        "y": 954
    },
    {
        "personId": "00051680",
        "name": "İRFAN KELER",
        "grid_filename": "grid_22.png",
        "row": 9,
        "column": 11,
        "x": 902,
        "y": 954
    },
    {
        "personId": "00073501",
        "name": "SALİH AHZEM TOPAL",
        "grid_filename": "grid_22.png",
        "row": 10,
        "column": 2,
        "x": 164,
        "y": 1060
    },
    {
        "personId": "00060558",
        "name": "İSMAİL VOLKAN ÖZAYDINLI",
        "grid_filename": "grid_22.png",
        "row": 10,
        "column": 8,
        "x": 656,
        "y": 1060
    },
    {
        "personId": "00054202",
        "name": "AHMET İSMAİL GÜLLE",
        "grid_filename": "grid_22.png",
        "row": 10,
        "column": 9,
        "x": 738,
        "y": 1060
    },
    {
        "personId": "00054149",
        "name": "OKAN BAŞ",
        "grid_filename": "grid_23.png",
        "row": 0,
        "column": 8,
        "x": 656,
        "y": 0
    },
    {
        "personId": "00058563",
        "name": "KAMİL GÖKAL",
        "grid_filename": "grid_23.png",
        "row": 0,
        "column": 11,
        "x": 902,
        "y": 0
    },
    {
        "personId": "00098299",
        "name": "BABÜR KAAN ŞENER",
        "grid_filename": "grid_23.png",
        "row": 1,
        "column": 13,
        "x": 1066,
        "y": 106
    },
    {
        "personId": "00050148",
        "name": "UFUK ÜNAL",
        "grid_filename": "grid_23.png",
        "row": 3,
        "column": 2,
        "x": 164,
        "y": 318
    },
    {
        "personId": "00099793",
        "name": "KAYA KARAYEL",
        "grid_filename": "grid_23.png",
        "row": 3,
        "column": 5,
        "x": 410,
        "y": 318
    },
    {
        "personId": "00054287",
        "name": "HİKMET MESUT TÜRKSEVEN",
        "grid_filename": "grid_23.png",
        "row": 5,
        "column": 1,
        "x": 82,
        "y": 530
    },
    {
        "personId": "00061467",
        "name": "MUSTAFA DÖKMETAŞ",
        "grid_filename": "grid_23.png",
        "row": 5,
        "column": 3,
        "x": 246,
        "y": 530
    },
    {
        "personId": "00062870",
        "name": "DOĞAN CEBECİ",
        "grid_filename": "grid_23.png",
        "row": 5,
        "column": 12,
        "x": 984,
        "y": 530
    },
    {
        "personId": "00069037",
        "name": "EYÜP KARS",
        "grid_filename": "grid_23.png",
        "row": 9,
        "column": 13,
        "x": 1066,
        "y": 954
    },
    {
        "personId": "00081737",
        "name": "ADEM KILIÇ",
        "grid_filename": "grid_23.png",
        "row": 10,
        "column": 2,
        "x": 164,
        "y": 1060
    },
    {
        "personId": "00060083",
        "name": "FATİH HARAS",
        "grid_filename": "grid_24.png",
        "row": 1,
        "column": 12,
        "x": 984,
        "y": 106
    },
    {
        "personId": "00073571",
        "name": "AHMET HALİD KUTLUOĞLU",
        "grid_filename": "grid_24.png",
        "row": 2,
        "column": 11,
        "x": 902,
        "y": 212
    },
    {
        "personId": "00071314",
        "name": "OSMAN TÜZER",
        "grid_filename": "grid_24.png",
        "row": 4,
        "column": 0,
        "x": 0,
        "y": 424
    },
    {
        "personId": "00069763",
        "name": "KENAN TURGUT",
        "grid_filename": "grid_24.png",
        "row": 4,
        "column": 11,
        "x": 902,
        "y": 424
    },
    {
        "personId": "00042015",
        "name": "ABDULAZIZ SALIM ABDULLAH BA MOHAMMED",
        "grid_filename": "grid_24.png",
        "row": 6,
        "column": 1,
        "x": 82,
        "y": 636
    },
    {
        "personId": "00020249",
        "name": "AHMET BOLAT",
        "grid_filename": "grid_24.png",
        "row": 8,
        "column": 0,
        "x": 0,
        "y": 848
    },
    {
        "personId": "00066098",
        "name": "AHMET KÖSE",
        "grid_filename": "grid_24.png",
        "row": 8,
        "column": 12,
        "x": 984,
        "y": 848
    },
    {
        "personId": "00048419",
        "name": "BURAK ŞOLTAN",
        "grid_filename": "grid_24.png",
        "row": 9,
        "column": 2,
        "x": 164,
        "y": 954
    },
    {
        "personId": "00067464",
        "name": "BİLAL SEMİH ÖNEL",
        "grid_filename": "grid_24.png",
        "row": 9,
        "column": 5,
        "x": 410,
        "y": 954
    },
    {
        "personId": "00061887",
        "name": "MUHAMMED HAMZA ARSLAN",
        "grid_filename": "grid_24.png",
        "row": 9,
        "column": 12,
        "x": 984,
        "y": 954
    },
    {
        "personId": "00069089",
        "name": "ABDULLAH ÖMER ÇELİK",
        "grid_filename": "grid_25.png",
        "row": 0,
        "column": 4,
        "x": 328,
        "y": 0
    },
    {
        "personId": "00049610",
        "name": "SERKAN SÖNMEZ",
        "grid_filename": "grid_25.png",
        "row": 0,
        "column": 11,
        "x": 902,
        "y": 0
    },
    {
        "personId": "00075466",
        "name": "TUBA NUR YAZICI",
        "grid_filename": "grid_25.png",
        "row": 1,
        "column": 5,
        "x": 410,
        "y": 106
    },
    {
        "personId": "00064253",
        "name": "ORHAN DOĞAN",
        "grid_filename": "grid_25.png",
        "row": 1,
        "column": 11,
        "x": 902,
        "y": 106
    },
    {
        "personId": "00069138",
        "name": "ALİ FUAT CİCAVOĞLU",
        "grid_filename": "grid_25.png",
        "row": 4,
        "column": 8,
        "x": 656,
        "y": 424
    },
    {
        "personId": "00071061",
        "name": "FADEN ÖZTÜRK",
        "grid_filename": "grid_25.png",
        "row": 5,
        "column": 1,
        "x": 82,
        "y": 530
    },
    {
        "personId": "00068235",
        "name": "ADNAN KARAİSMAİLOĞLU",
        "grid_filename": "grid_25.png",
        "row": 5,
        "column": 8,
        "x": 656,
        "y": 530
    },
    {
        "personId": "00098768",
        "name": "MUSTAFA SÖZEN",
        "grid_filename": "grid_25.png",
        "row": 5,
        "column": 9,
        "x": 738,
        "y": 530
    },
    {
        "personId": "00053225",
        "name": "CENGİZ İNCEOSMAN",
        "grid_filename": "grid_25.png",
        "row": 5,
        "column": 12,
        "x": 984,
        "y": 530
    },
    {
        "personId": "00063463",
        "name": "SALİH KAMİL SALİHOĞLU",
        "grid_filename": "grid_25.png",
        "row": 6,
        "column": 2,
        "x": 164,
        "y": 636
    },
    {
        "personId": "00083341",
        "name": "YUNUS DOĞAN",
        "grid_filename": "grid_25.png",
        "row": 8,
        "column": 0,
        "x": 0,
        "y": 848
    },
    {
        "personId": "00049186",
        "name": "HASAN SAVAŞ ERDEN",
        "grid_filename": "grid_25.png",
        "row": 8,
        "column": 9,
        "x": 738,
        "y": 848
    },
    {
        "personId": "00064993",
        "name": "MUHAMMET BAYRAM TOPCU",
        "grid_filename": "grid_25.png",
        "row": 9,
        "column": 13,
        "x": 1066,
        "y": 954
    },
    {
        "personId": "00046053",
        "name": "ATİLLA COŞKUN",
        "grid_filename": "grid_26.png",
        "row": 1,
        "column": 0,
        "x": 0,
        "y": 106
    },
    {
        "personId": "00081708",
        "name": "MUHAMMET SELMAN ŞENKAL",
        "grid_filename": "grid_26.png",
        "row": 2,
        "column": 11,
        "x": 902,
        "y": 212
    },
    {
        "personId": "00086500",
        "name": "TUBA DEMİRTAŞ",
        "grid_filename": "grid_26.png",
        "row": 4,
        "column": 0,
        "x": 0,
        "y": 424
    },
    {
        "personId": "00072760",
        "name": "ECE BAŞ",
        "grid_filename": "grid_26.png",
        "row": 5,
        "column": 3,
        "x": 246,
        "y": 530
    },
    {
        "personId": "00067900",
        "name": "YASİN EROL",
        "grid_filename": "grid_26.png",
        "row": 6,
        "column": 1,
        "x": 82,
        "y": 636
    },
    {
        "personId": "00068037",
        "name": "TUĞBA YAŞAROĞLU YAVUZ",
        "grid_filename": "grid_26.png",
        "row": 6,
        "column": 5,
        "x": 410,
        "y": 636
    },
    {
        "personId": "00072747",
        "name": "MEHMET FATİH KORKMAZ",
        "grid_filename": "grid_26.png",
        "row": 6,
        "column": 7,
        "x": 574,
        "y": 636
    },
    {
        "personId": "00073326",
        "name": "AHMET KÜRŞAT BALTACI",
        "grid_filename": "grid_26.png",
        "row": 9,
        "column": 4,
        "x": 328,
        "y": 954
    },
    {
        "personId": "00083143",
        "name": "GÖKHAN DÖRTKOL",
        "grid_filename": "grid_26.png",
        "row": 10,
        "column": 2,
        "x": 164,
        "y": 1060
    },
    {
        "personId": "00089119",
        "name": "CİHAD MUHAMMED YILDIZ",
        "grid_filename": "grid_26.png",
        "row": 10,
        "column": 4,
        "x": 328,
        "y": 1060
    },
    {
        "personId": "00060069",
        "name": "MELİH TORLAK",
        "grid_filename": "grid_27.png",
        "row": 0,
        "column": 5,
        "x": 410,
        "y": 0
    },
    {
        "personId": "00068515",
        "name": "ŞEFİKA ARSLAN BOZ",
        "grid_filename": "grid_27.png",
        "row": 1,
        "column": 9,
        "x": 738,
        "y": 106
    },
    {
        "personId": "00068398",
        "name": "AYŞE BETÜL KABADAYI",
        "grid_filename": "grid_27.png",
        "row": 3,
        "column": 0,
        "x": 0,
        "y": 318
    },
    {
        "personId": "00089852",
        "name": "MURAT ATEŞ",
        "grid_filename": "grid_27.png",
        "row": 3,
        "column": 9,
        "x": 738,
        "y": 318
    },
    {
        "personId": "00058984",
        "name": "AHMET TİKVEŞ",
        "grid_filename": "grid_27.png",
        "row": 4,
        "column": 5,
        "x": 410,
        "y": 424
    },
    {
        "personId": "00080270",
        "name": "GİZEM ERCAN",
        "grid_filename": "grid_27.png",
        "row": 5,
        "column": 7,
        "x": 574,
        "y": 530
    },
    {
        "personId": "00098944",
        "name": "AHMET EMRE KAVAK",
        "grid_filename": "grid_27.png",
        "row": 6,
        "column": 2,
        "x": 164,
        "y": 636
    },
    {
        "personId": "00049834",
        "name": "EROL FAKİ",
        "grid_filename": "grid_27.png",
        "row": 7,
        "column": 2,
        "x": 164,
        "y": 742
    },
    {
        "personId": "00054158",
        "name": "UĞUR CANTİMUR",
        "grid_filename": "grid_27.png",
        "row": 8,
        "column": 7,
        "x": 574,
        "y": 848
    },
    {
        "personId": "00052294",
        "name": "SERHAT GÖK",
        "grid_filename": "grid_27.png",
        "row": 10,
        "column": 3,
        "x": 246,
        "y": 1060
    },
    {
        "personId": "00065363",
        "name": "OSMAN ŞAFAK KÜÇÜKÇOLAK",
        "grid_filename": "grid_27.png",
        "row": 10,
        "column": 4,
        "x": 328,
        "y": 1060
    },
    {
        "personId": "00075360",
        "name": "İREM DÜLGER",
        "grid_filename": "grid_28.png",
        "row": 1,
        "column": 5,
        "x": 410,
        "y": 106
    },
    {
        "personId": "00053044",
        "name": "BEKİR ALPER YILDIRIM",
        "grid_filename": "grid_28.png",
        "row": 1,
        "column": 7,
        "x": 574,
        "y": 106
    },
    {
        "personId": "00079316",
        "name": "MUSTAFA DEMİRAK",
        "grid_filename": "grid_28.png",
        "row": 1,
        "column": 11,
        "x": 902,
        "y": 106
    },
    {
        "personId": "00091365",
        "name": "GÖKHAN TELLİ",
        "grid_filename": "grid_28.png",
        "row": 2,
        "column": 5,
        "x": 410,
        "y": 212
    },
    {
        "personId": "00069934",
        "name": "HÜSEYİN ÖZBEK",
        "grid_filename": "grid_28.png",
        "row": 3,
        "column": 6,
        "x": 492,
        "y": 318
    },
    {
        "personId": "00061462",
        "name": "EMİR ALİ GÖZE",
        "grid_filename": "grid_28.png",
        "row": 4,
        "column": 4,
        "x": 328,
        "y": 424
    },
    {
        "personId": "00059310",
        "name": "TURGUT KENDİRCİ",
        "grid_filename": "grid_28.png",
        "row": 6,
        "column": 6,
        "x": 492,
        "y": 636
    },
    {
        "personId": "00074315",
        "name": "FATİH İNAN",
        "grid_filename": "grid_28.png",
        "row": 6,
        "column": 9,
        "x": 738,
        "y": 636
    },
    {
        "personId": "00049302",
        "name": "TURGUT KARADEDE",
        "grid_filename": "grid_28.png",
        "row": 6,
        "column": 10,
        "x": 820,
        "y": 636
    },
    {
        "personId": "00068205",
        "name": "AYŞE TOPÇU",
        "grid_filename": "grid_28.png",
        "row": 8,
        "column": 2,
        "x": 164,
        "y": 848
    },
    {
        "personId": "00069822",
        "name": "ABDULLAH SEYMEN",
        "grid_filename": "grid_28.png",
        "row": 8,
        "column": 4,
        "x": 328,
        "y": 848
    },
    {
        "personId": "00044074",
        "name": "MARAL ÖZODABAŞYAN",
        "grid_filename": "grid_28.png",
        "row": 8,
        "column": 8,
        "x": 656,
        "y": 848
    },
    {
        "personId": "00064470",
        "name": "MELTEM KARAN",
        "grid_filename": "grid_28.png",
        "row": 8,
        "column": 12,
        "x": 984,
        "y": 848
    },
    {
        "personId": "00020138",
        "name": "ŞEKİB AVDAGİÇ",
        "grid_filename": "grid_28.png",
        "row": 10,
        "column": 5,
        "x": 410,
        "y": 1060
    },
    {
        "personId": "00073496",
        "name": "ALİ DEMİRCAN",
        "grid_filename": "grid_28.png",
        "row": 10,
        "column": 13,
        "x": 1066,
        "y": 1060
    },
    {
        "personId": "00046537",
        "name": "İBRAHİM DEMİRDÖĞEN",
        "grid_filename": "grid_29.png",
        "row": 0,
        "column": 9,
        "x": 738,
        "y": 0
    },
    {
        "personId": "00044442",
        "name": "SERKAN ÖZBÜYÜKYÖRÜK",
        "grid_filename": "grid_29.png",
        "row": 1,
        "column": 0,
        "x": 0,
        "y": 106
    },
    {
        "personId": "00087268",
        "name": "ANIL MERCAN",
        "grid_filename": "grid_29.png",
        "row": 2,
        "column": 4,
        "x": 328,
        "y": 212
    },
    {
        "personId": "00052435",
        "name": "SERHAT TÜMER",
        "grid_filename": "grid_29.png",
        "row": 4,
        "column": 9,
        "x": 738,
        "y": 424
    },
    {
        "personId": "00053421",
        "name": "ÖMER UZUN",
        "grid_filename": "grid_29.png",
        "row": 4,
        "column": 11,
        "x": 902,
        "y": 424
    },
    {
        "personId": "00064972",
        "name": "AHMET NUMAN CEBECİ",
        "grid_filename": "grid_29.png",
        "row": 6,
        "column": 1,
        "x": 82,
        "y": 636
    },
    {
        "personId": "00057605",
        "name": "ABDULLAH BİNBİR",
        "grid_filename": "grid_29.png",
        "row": 9,
        "column": 3,
        "x": 246,
        "y": 954
    },
    {
        "personId": "00087164",
        "name": "SAMET ELİTOK",
        "grid_filename": "grid_29.png",
        "row": 10,
        "column": 1,
        "x": 82,
        "y": 1060
    },
    {
        "personId": "00049971",
        "name": "YAKUP GÜL",
        "grid_filename": "grid_29.png",
        "row": 10,
        "column": 2,
        "x": 164,
        "y": 1060
    },
    {
        "personId": "00121428",
        "name": "ÖZLEM İNANÇ",
        "grid_filename": "grid_29.png",
        "row": 10,
        "column": 4,
        "x": 328,
        "y": 1060
    },
    {
        "personId": "00063983",
        "name": "NECMİ BARIŞ ÜLGAY",
        "grid_filename": "grid_29.png",
        "row": 10,
        "column": 5,
        "x": 410,
        "y": 1060
    },
    {
        "personId": "00076961",
        "name": "SİNAN YEŞİLLER",
        "grid_filename": "grid_30.png",
        "row": 0,
        "column": 6,
        "x": 492,
        "y": 0
    },
    {
        "personId": "00045705",
        "name": "SERKAN CEVDET TANSU",
        "grid_filename": "grid_30.png",
        "row": 0,
        "column": 9,
        "x": 738,
        "y": 0
    },
    {
        "personId": "00063735",
        "name": "VEYSEL UZUN",
        "grid_filename": "grid_30.png",
        "row": 1,
        "column": 10,
        "x": 820,
        "y": 106
    },
    {
        "personId": "00093317",
        "name": "MUHAMMED FURKAN BULUT",
        "grid_filename": "grid_30.png",
        "row": 3,
        "column": 6,
        "x": 492,
        "y": 318
    },
    {
        "personId": "00054209",
        "name": "ORHAN GÜVEN",
        "grid_filename": "grid_30.png",
        "row": 3,
        "column": 7,
        "x": 574,
        "y": 318
    },
    {
        "personId": "00065352",
        "name": "MUSA DENİZ PERÇİNKAYA",
        "grid_filename": "grid_30.png",
        "row": 4,
        "column": 2,
        "x": 164,
        "y": 424
    },
    {
        "personId": "00072940",
        "name": "MEHMET ERTUĞRUL AKTAN",
        "grid_filename": "grid_30.png",
        "row": 7,
        "column": 2,
        "x": 164,
        "y": 742
    },
    {
        "personId": "00062357",
        "name": "ALPER KAŞIKÇI",
        "grid_filename": "grid_30.png",
        "row": 8,
        "column": 13,
        "x": 1066,
        "y": 848
    },
    {
        "personId": "00089609",
        "name": "YÜCEL DEMİRCİ",
        "grid_filename": "grid_30.png",
        "row": 9,
        "column": 1,
        "x": 82,
        "y": 954
    },
    {
        "personId": "00082713",
        "name": "YAHYA ÜSTÜN",
        "grid_filename": "grid_30.png",
        "row": 9,
        "column": 4,
        "x": 328,
        "y": 954
    },
    {
        "personId": "00090619",
        "name": "EYYÜP ÖZKAYMAK",
        "grid_filename": "grid_30.png",
        "row": 10,
        "column": 1,
        "x": 82,
        "y": 1060
    },
    {
        "personId": "00059940",
        "name": "BURAK YILDIZ",
        "grid_filename": "grid_31.png",
        "row": 1,
        "column": 2,
        "x": 164,
        "y": 106
    },
    {
        "personId": "00075003",
        "name": "ALİ FUAT KAZANCI",
        "grid_filename": "grid_31.png",
        "row": 1,
        "column": 3,
        "x": 246,
        "y": 106
    },
    {
        "personId": "00094478",
        "name": "MEHMET ALİ SÖYLET",
        "grid_filename": "grid_31.png",
        "row": 1,
        "column": 7,
        "x": 574,
        "y": 106
    },
    {
        "personId": "00087734",
        "name": "HAYRULLAH CİHAT TUTCUOĞLU",
        "grid_filename": "grid_31.png",
        "row": 1,
        "column": 9,
        "x": 738,
        "y": 106
    },
    {
        "personId": "00061823",
        "name": "MEHMET KEREM KIZILTUNÇ",
        "grid_filename": "grid_31.png",
        "row": 3,
        "column": 5,
        "x": 410,
        "y": 318
    },
    {
        "personId": "00068041",
        "name": "YASİN KAPANCI",
        "grid_filename": "grid_31.png",
        "row": 4,
        "column": 2,
        "x": 164,
        "y": 424
    },
    {
        "personId": "00071214",
        "name": "MEHMET EMİN TUFAN",
        "grid_filename": "grid_31.png",
        "row": 4,
        "column": 6,
        "x": 492,
        "y": 424
    },
    {
        "personId": "00068460",
        "name": "AHMET MİTHAT ÇELEBİ",
        "grid_filename": "grid_31.png",
        "row": 5,
        "column": 9,
        "x": 738,
        "y": 530
    },
    {
        "personId": "00062769",
        "name": "ÖZNUR AKSU",
        "grid_filename": "grid_31.png",
        "row": 6,
        "column": 1,
        "x": 82,
        "y": 636
    },
    {
        "personId": "00056457",
        "name": "ÖZLEM ÇERİ",
        "grid_filename": "grid_31.png",
        "row": 6,
        "column": 10,
        "x": 820,
        "y": 636
    },
    {
        "personId": "00055279",
        "name": "FATİH MATUK",
        "grid_filename": "grid_31.png",
        "row": 8,
        "column": 1,
        "x": 82,
        "y": 848
    },
    {
        "personId": "00065587",
        "name": "AYŞEGÜL AYDINLIK",
        "grid_filename": "grid_31.png",
        "row": 8,
        "column": 6,
        "x": 492,
        "y": 848
    },
    {
        "personId": "00079896",
        "name": "ABDULKERİM ÇAY",
        "grid_filename": "grid_31.png",
        "row": 9,
        "column": 0,
        "x": 0,
        "y": 954
    },
    {
        "personId": "00098585",
        "name": "SİNAN UĞUR",
        "grid_filename": "grid_31.png",
        "row": 9,
        "column": 5,
        "x": 410,
        "y": 954
    },
    {
        "personId": "00062098",
        "name": "BİRSEL DÖRTELMA",
        "grid_filename": "grid_31.png",
        "row": 10,
        "column": 9,
        "x": 738,
        "y": 1060
    },
    {
        "personId": "00064649",
        "name": "ENES SAİM ÖZYÜREK",
        "grid_filename": "grid_32.png",
        "row": 0,
        "column": 7,
        "x": 574,
        "y": 0
    },
    {
        "personId": "00057437",
        "name": "HASAN MALİK AYDINER",
        "grid_filename": "grid_32.png",
        "row": 1,
        "column": 3,
        "x": 246,
        "y": 106
    },
    {
        "personId": "00054126",
        "name": "BERNA SALİHOĞLU",
        "grid_filename": "grid_32.png",
        "row": 1,
        "column": 8,
        "x": 656,
        "y": 106
    },
    {
        "personId": "00062298",
        "name": "AHMET HARUN BAŞTÜRK",
        "grid_filename": "grid_32.png",
        "row": 1,
        "column": 11,
        "x": 902,
        "y": 106
    },
    {
        "personId": "00068981",
        "name": "ALİ ÇOLAK",
        "grid_filename": "grid_32.png",
        "row": 2,
        "column": 9,
        "x": 738,
        "y": 212
    },
    {
        "personId": "00061901",
        "name": "LEVENT KESKİNGÖZ",
        "grid_filename": "grid_32.png",
        "row": 2,
        "column": 13,
        "x": 1066,
        "y": 212
    },
    {
        "personId": "00058062",
        "name": "FATİH KARAMAN",
        "grid_filename": "grid_32.png",
        "row": 6,
        "column": 0,
        "x": 0,
        "y": 636
    },
    {
        "personId": "00069778",
        "name": "FATİH KARAKOÇ",
        "grid_filename": "grid_32.png",
        "row": 6,
        "column": 2,
        "x": 164,
        "y": 636
    },
    {
        "personId": "00059725",
        "name": "HALİT ANLATAN",
        "grid_filename": "grid_32.png",
        "row": 6,
        "column": 10,
        "x": 820,
        "y": 636
    },
    {
        "personId": "00068527",
        "name": "NEŞE ÇALIŞIR",
        "grid_filename": "grid_32.png",
        "row": 7,
        "column": 1,
        "x": 82,
        "y": 742
    },
    {
        "personId": "00072609",
        "name": "HÜSEYİN GÜZEL",
        "grid_filename": "grid_32.png",
        "row": 7,
        "column": 9,
        "x": 738,
        "y": 742
    },
    {
        "personId": "00049773",
        "name": "ÖZLEM ÖZYÖN",
        "grid_filename": "grid_32.png",
        "row": 9,
        "column": 4,
        "x": 328,
        "y": 954
    },
    {
        "personId": "00098302",
        "name": "CABİR KARANFİL",
        "grid_filename": "grid_32.png",
        "row": 9,
        "column": 10,
        "x": 820,
        "y": 954
    },
    {
        "personId": "00063345",
        "name": "MUHAMMED ZİYA ÖZTÜRK",
        "grid_filename": "grid_32.png",
        "row": 10,
        "column": 13,
        "x": 1066,
        "y": 1060
    },
    {
        "personId": "00066531",
        "name": "AYŞE ALTAN",
        "grid_filename": "grid_33.png",
        "row": 0,
        "column": 6,
        "x": 492,
        "y": 0
    },
    {
        "personId": "00045975",
        "name": "ALİ BULUT",
        "grid_filename": "grid_33.png",
        "row": 1,
        "column": 3,
        "x": 246,
        "y": 106
    },
    {
        "personId": "00050317",
        "name": "MUAMMER SANCAKLI",
        "grid_filename": "grid_33.png",
        "row": 4,
        "column": 6,
        "x": 492,
        "y": 424
    },
    {
        "personId": "00058824",
        "name": "BİLAL ACAR",
        "grid_filename": "grid_33.png",
        "row": 5,
        "column": 4,
        "x": 328,
        "y": 530
    },
    {
        "personId": "00073080",
        "name": "NURAN ERDAĞ HABERDAR",
        "grid_filename": "grid_33.png",
        "row": 7,
        "column": 10,
        "x": 820,
        "y": 742
    },
    {
        "personId": "00051205",
        "name": "YILMAZ GÜN",
        "grid_filename": "grid_33.png",
        "row": 8,
        "column": 6,
        "x": 492,
        "y": 848
    },
    {
        "personId": "00067771",
        "name": "ALİ TÜRK",
        "grid_filename": "grid_33.png",
        "row": 8,
        "column": 10,
        "x": 820,
        "y": 848
    },
    {
        "personId": "00055075",
        "name": "KADİR KÖK",
        "grid_filename": "grid_33.png",
        "row": 9,
        "column": 7,
        "x": 574,
        "y": 954
    },
    {
        "personId": "00068412",
        "name": "SALİH DÖĞENCİ",
        "grid_filename": "grid_33.png",
        "row": 9,
        "column": 13,
        "x": 1066,
        "y": 954
    },
    {
        "personId": "00053723",
        "name": "İSMAİL USTAOĞLU",
        "grid_filename": "grid_33.png",
        "row": 10,
        "column": 2,
        "x": 164,
        "y": 1060
    },
    {
        "personId": "00063052",
        "name": "MUHAMMED FATİH DURMAZ",
        "grid_filename": "grid_33.png",
        "row": 10,
        "column": 7,
        "x": 574,
        "y": 1060
    },
    {
        "personId": "00075124",
        "name": "MEHMET AŞIK",
        "grid_filename": "grid_33.png",
        "row": 10,
        "column": 9,
        "x": 738,
        "y": 1060
    },
    {
        "personId": "00053382",
        "name": "KAMİL ÖNDER NERGİZ",
        "grid_filename": "grid_34.png",
        "row": 0,
        "column": 4,
        "x": 328,
        "y": 0
    },
    {
        "personId": "00065390",
        "name": "MUTLU DÖNMEZ",
        "grid_filename": "grid_34.png",
        "row": 1,
        "column": 10,
        "x": 820,
        "y": 106
    },
    {
        "personId": "00075614",
        "name": "SEMİH KARTALOĞLU",
        "grid_filename": "grid_34.png",
        "row": 1,
        "column": 11,
        "x": 902,
        "y": 106
    },
    {
        "personId": "00048765",
        "name": "RASİM KUZGUNLU",
        "grid_filename": "grid_34.png",
        "row": 2,
        "column": 6,
        "x": 492,
        "y": 212
    },
    {
        "personId": "00074152",
        "name": "İSLAM GÜRE",
        "grid_filename": "grid_34.png",
        "row": 3,
        "column": 4,
        "x": 328,
        "y": 318
    },
    {
        "personId": "00054634",
        "name": "AYHAN TAN",
        "grid_filename": "grid_34.png",
        "row": 3,
        "column": 11,
        "x": 902,
        "y": 318
    },
    {
        "personId": "00067693",
        "name": "VEYSEL SERDAR",
        "grid_filename": "grid_34.png",
        "row": 4,
        "column": 0,
        "x": 0,
        "y": 424
    },
    {
        "personId": "00074037",
        "name": "ALPER ÖZYILMAZ",
        "grid_filename": "grid_34.png",
        "row": 4,
        "column": 7,
        "x": 574,
        "y": 424
    },
    {
        "personId": "00073699",
        "name": "HAKAN ANKARA",
        "grid_filename": "grid_34.png",
        "row": 5,
        "column": 4,
        "x": 328,
        "y": 530
    },
    {
        "personId": "00068652",
        "name": "YUSUF ZİYA İSKENDER",
        "grid_filename": "grid_34.png",
        "row": 5,
        "column": 9,
        "x": 738,
        "y": 530
    },
    {
        "personId": "00052186",
        "name": "AHMET METİN ÖLMEZ",
        "grid_filename": "grid_34.png",
        "row": 10,
        "column": 1,
        "x": 82,
        "y": 1060
    },
    {
        "personId": "00054533",
        "name": "FARUK BİLİR",
        "grid_filename": "grid_34.png",
        "row": 10,
        "column": 9,
        "x": 738,
        "y": 1060
    },
    {
        "personId": "00075131",
        "name": "BAYRAM BURAK KARALİ",
        "grid_filename": "grid_35.png",
        "row": 0,
        "column": 8,
        "x": 656,
        "y": 0
    },
    {
        "personId": "00064974",
        "name": "KEMAL AKIN ÖZYAKA",
        "grid_filename": "grid_35.png",
        "row": 1,
        "column": 3,
        "x": 246,
        "y": 106
    },
    {
        "personId": "00059707",
        "name": "DENİZ DEMİROĞLU",
        "grid_filename": "grid_35.png",
        "row": 3,
        "column": 2,
        "x": 164,
        "y": 318
    },
    {
        "personId": "00053722",
        "name": "YAVUZ BARBAROS ULUSOY",
        "grid_filename": "grid_35.png",
        "row": 3,
        "column": 5,
        "x": 410,
        "y": 318
    },
    {
        "personId": "00065127",
        "name": "ALİ VAHAP NANE",
        "grid_filename": "grid_35.png",
        "row": 3,
        "column": 10,
        "x": 820,
        "y": 318
    },
    {
        "personId": "00071887",
        "name": "MEHMET YELTEKİN",
        "grid_filename": "grid_35.png",
        "row": 5,
        "column": 5,
        "x": 410,
        "y": 530
    },
    {
        "personId": "00061134",
        "name": "SERAP OKÇU",
        "grid_filename": "grid_35.png",
        "row": 8,
        "column": 4,
        "x": 328,
        "y": 848
    },
    {
        "personId": "00058137",
        "name": "DEMET TÜRKEL",
        "grid_filename": "grid_35.png",
        "row": 8,
        "column": 8,
        "x": 656,
        "y": 848
    },
    {
        "personId": "00072677",
        "name": "YUSUF GÖKSU",
        "grid_filename": "grid_35.png",
        "row": 8,
        "column": 9,
        "x": 738,
        "y": 848
    },
    {
        "personId": "00054223",
        "name": "HALİS CUMHUR KILINÇ",
        "grid_filename": "grid_35.png",
        "row": 10,
        "column": 3,
        "x": 246,
        "y": 1060
    },
    {
        "personId": "00051126",
        "name": "AHMET KULA",
        "grid_filename": "grid_36.png",
        "row": 0,
        "column": 10,
        "x": 820,
        "y": 0
    },
    {
        "personId": "00080829",
        "name": "MEHMET ARİF TATOĞLU",
        "grid_filename": "grid_36.png",
        "row": 0,
        "column": 12,
        "x": 984,
        "y": 0
    },
    {
        "personId": "00051880",
        "name": "ERTAN ALPAY",
        "grid_filename": "grid_36.png",
        "row": 2,
        "column": 10,
        "x": 820,
        "y": 212
    },
    {
        "personId": "00069462",
        "name": "ABDULLAH YILDIZ",
        "grid_filename": "grid_36.png",
        "row": 2,
        "column": 13,
        "x": 1066,
        "y": 212
    },
    {
        "personId": "00083959",
        "name": "SAMİ ARVAS",
        "grid_filename": "grid_36.png",
        "row": 4,
        "column": 6,
        "x": 492,
        "y": 424
    },
    {
        "personId": "00087324",
        "name": "METİN GÜLŞEN",
        "grid_filename": "grid_36.png",
        "row": 6,
        "column": 2,
        "x": 164,
        "y": 636
    },
    {
        "personId": "00069289",
        "name": "YAVUZ AYMELEK",
        "grid_filename": "grid_36.png",
        "row": 6,
        "column": 4,
        "x": 328,
        "y": 636
    },
    {
        "personId": "00053214",
        "name": "MEHMET EKŞİ",
        "grid_filename": "grid_36.png",
        "row": 6,
        "column": 6,
        "x": 492,
        "y": 636
    },
    {
        "personId": "00053385",
        "name": "AŞKIN CANTİMUR",
        "grid_filename": "grid_36.png",
        "row": 7,
        "column": 13,
        "x": 1066,
        "y": 742
    },
    {
        "personId": "00085234",
        "name": "MEHMET ÇİÇEK",
        "grid_filename": "grid_36.png",
        "row": 8,
        "column": 4,
        "x": 328,
        "y": 848
    },
    {
        "personId": "00079845",
        "name": "GÖKHAN ÖZBEY",
        "grid_filename": "grid_37.png",
        "row": 0,
        "column": 6,
        "x": 492,
        "y": 0
    },
    {
        "personId": "00063161",
        "name": "ADEM EKMEKCİ",
        "grid_filename": "grid_37.png",
        "row": 1,
        "column": 7,
        "x": 574,
        "y": 106
    },
    {
        "personId": "00057456",
        "name": "AHMET MENNAN MÜFTÜOĞLU",
        "grid_filename": "grid_37.png",
        "row": 3,
        "column": 4,
        "x": 328,
        "y": 318
    },
    {
        "personId": "00082725",
        "name": "MÜNİR BEYAZAL",
        "grid_filename": "grid_37.png",
        "row": 4,
        "column": 10,
        "x": 820,
        "y": 424
    },
    {
        "personId": "00123820",
        "name": "HAMDİ CEM KARADAŞ",
        "grid_filename": "grid_37.png",
        "row": 6,
        "column": 11,
        "x": 902,
        "y": 636
    },
    {
        "personId": "00069377",
        "name": "ARİF ŞENGÖR",
        "grid_filename": "grid_37.png",
        "row": 7,
        "column": 1,
        "x": 82,
        "y": 742
    },
    {
        "personId": "00057757",
        "name": "MEHMET CÜNEYD DOĞRUER",
        "grid_filename": "grid_37.png",
        "row": 7,
        "column": 12,
        "x": 984,
        "y": 742
    },
    {
        "personId": "00074946",
        "name": "İBRAHİM ORHANLI",
        "grid_filename": "grid_37.png",
        "row": 8,
        "column": 10,
        "x": 820,
        "y": 848
    },
    {
        "personId": "00054267",
        "name": "ABDULLAH SAİT ŞENLER",
        "grid_filename": "grid_37.png",
        "row": 9,
        "column": 5,
        "x": 410,
        "y": 954
    },
    {
        "personId": "00068077",
        "name": "MUHAMMED İBRAHİM KAVRANOĞLU",
        "grid_filename": "grid_38.png",
        "row": 2,
        "column": 0,
        "x": 0,
        "y": 212
    },
    {
        "personId": "00057501",
        "name": "ZEYNEP TARTAN GÜÇEL",
        "grid_filename": "grid_38.png",
        "row": 3,
        "column": 7,
        "x": 574,
        "y": 318
    },
    {
        "personId": "00085084",
        "name": "İLKER HOLOĞLU",
        "grid_filename": "grid_38.png",
        "row": 4,
        "column": 12,
        "x": 984,
        "y": 424
    },
    {
        "personId": "00058381",
        "name": "MEHMET ALAGÖZ",
        "grid_filename": "grid_38.png",
        "row": 5,
        "column": 2,
        "x": 164,
        "y": 530
    },
    {
        "personId": "00062178",
        "name": "ALİ ALTINOK",
        "grid_filename": "grid_38.png",
        "row": 5,
        "column": 5,
        "x": 410,
        "y": 530
    },
    {
        "personId": "00068973",
        "name": "FUAT FIRAT",
        "grid_filename": "grid_38.png",
        "row": 5,
        "column": 10,
        "x": 820,
        "y": 530
    },
    {
        "personId": "00070062",
        "name": "MUHAMMET YAZICI",
        "grid_filename": "grid_38.png",
        "row": 6,
        "column": 10,
        "x": 820,
        "y": 636
    },
    {
        "personId": "00049794",
        "name": "MEHMET AKAY",
        "grid_filename": "grid_38.png",
        "row": 6,
        "column": 12,
        "x": 984,
        "y": 636
    },
    {
        "personId": "00066473",
        "name": "HASAN BEYAZÖRTÜ",
        "grid_filename": "grid_38.png",
        "row": 8,
        "column": 7,
        "x": 574,
        "y": 848
    },
    {
        "personId": "00057088",
        "name": "ERTUĞRUL SEVİMLİ",
        "grid_filename": "grid_38.png",
        "row": 10,
        "column": 7,
        "x": 574,
        "y": 1060
    },
    {
        "personId": "00054224",
        "name": "MUSTAFA KEMAL KIZILAY",
        "grid_filename": "grid_38.png",
        "row": 10,
        "column": 8,
        "x": 656,
        "y": 1060
    },
    {
        "personId": "00066282",
        "name": "SERTAN YÜCE",
        "grid_filename": "grid_39.png",
        "row": 0,
        "column": 9,
        "x": 738,
        "y": 0
    },
    {
        "personId": "00066157",
        "name": "ESRA KARAYAKA",
        "grid_filename": "grid_39.png",
        "row": 0,
        "column": 10,
        "x": 820,
        "y": 0
    },
    {
        "personId": "00074014",
        "name": "EMRE ARPA",
        "grid_filename": "grid_39.png",
        "row": 1,
        "column": 2,
        "x": 164,
        "y": 106
    },
    {
        "personId": "00051344",
        "name": "SELÇUK ÇAPUK",
        "grid_filename": "grid_39.png",
        "row": 1,
        "column": 3,
        "x": 246,
        "y": 106
    },
    {
        "personId": "00020159",
        "name": "RAMAZAN SARI",
        "grid_filename": "grid_39.png",
        "row": 3,
        "column": 3,
        "x": 246,
        "y": 318
    },
    {
        "personId": "00065998",
        "name": "ESER KARAMAN",
        "grid_filename": "grid_39.png",
        "row": 3,
        "column": 8,
        "x": 656,
        "y": 318
    },
    {
        "personId": "00064261",
        "name": "ÖMER SAKA",
        "grid_filename": "grid_39.png",
        "row": 4,
        "column": 2,
        "x": 164,
        "y": 424
    },
    {
        "personId": "00045552",
        "name": "SERKAN BAŞAR",
        "grid_filename": "grid_39.png",
        "row": 5,
        "column": 2,
        "x": 164,
        "y": 530
    },
    {
        "personId": "00075591",
        "name": "AGAH SELİM ALUÇ",
        "grid_filename": "grid_39.png",
        "row": 5,
        "column": 8,
        "x": 656,
        "y": 530
    },
    {
        "personId": "00063194",
        "name": "SEDAT ORMAN",
        "grid_filename": "grid_39.png",
        "row": 5,
        "column": 10,
        "x": 820,
        "y": 530
    },
    {
        "personId": "00079643",
        "name": "AHMET ENES ADALI",
        "grid_filename": "grid_39.png",
        "row": 7,
        "column": 1,
        "x": 82,
        "y": 742
    },
    {
        "personId": "00080075",
        "name": "MÜMİN ALADAĞ",
        "grid_filename": "grid_39.png",
        "row": 7,
        "column": 4,
        "x": 328,
        "y": 742
    },
    {
        "personId": "00059982",
        "name": "SELAHATTİN EYÜP ÖZBAY",
        "grid_filename": "grid_39.png",
        "row": 8,
        "column": 7,
        "x": 574,
        "y": 848
    },
    {
        "personId": "00020128",
        "name": "MELİH ŞÜKRÜ ECERTAŞ",
        "grid_filename": "grid_39.png",
        "row": 8,
        "column": 10,
        "x": 820,
        "y": 848
    },
    {
        "personId": "00053411",
        "name": "İSMAİL HAKKI KILIÇ",
        "grid_filename": "grid_39.png",
        "row": 9,
        "column": 4,
        "x": 328,
        "y": 954
    },
    {
        "personId": "00092099",
        "name": "ERSİN DENİZ",
        "grid_filename": "grid_39.png",
        "row": 9,
        "column": 10,
        "x": 820,
        "y": 954
    },
    {
        "personId": "00054307",
        "name": "MURAT SAMİ YÜZBAŞI",
        "grid_filename": "grid_39.png",
        "row": 10,
        "column": 8,
        "x": 656,
        "y": 1060
    },
    {
        "personId": "00071951",
        "name": "MURAT ŞAHİN",
        "grid_filename": "grid_40.png",
        "row": 0,
        "column": 5,
        "x": 410,
        "y": 0
    },
    {
        "personId": "00081788",
        "name": "KÜBRA AĞAÇ",
        "grid_filename": "grid_40.png",
        "row": 2,
        "column": 2,
        "x": 164,
        "y": 212
    },
    {
        "personId": "00070047",
        "name": "EMRAH KARACA",
        "grid_filename": "grid_40.png",
        "row": 2,
        "column": 5,
        "x": 410,
        "y": 212
    },
    {
        "personId": "00050290",
        "name": "SERKAN YÜRÜMEZ",
        "grid_filename": "grid_40.png",
        "row": 3,
        "column": 2,
        "x": 164,
        "y": 318
    },
    {
        "personId": "00080838",
        "name": "AYTEKİN SERBEST",
        "grid_filename": "grid_40.png",
        "row": 5,
        "column": 2,
        "x": 164,
        "y": 530
    },
    {
        "personId": "00049109",
        "name": "ESRA KAV",
        "grid_filename": "grid_40.png",
        "row": 7,
        "column": 4,
        "x": 328,
        "y": 742
    },
    {
        "personId": "00048017",
        "name": "UTKU YAZAN",
        "grid_filename": "grid_40.png",
        "row": 7,
        "column": 7,
        "x": 574,
        "y": 742
    },
    {
        "personId": "00074509",
        "name": "ABDULSAMET SAFA DİLMAÇ",
        "grid_filename": "grid_40.png",
        "row": 8,
        "column": 1,
        "x": 82,
        "y": 848
    },
    {
        "personId": "00076851",
        "name": "MUHARREM BİLAL GURBETCİ",
        "grid_filename": "grid_40.png",
        "row": 9,
        "column": 4,
        "x": 328,
        "y": 954
    },
    {
        "personId": "00057224",
        "name": "DİLEK DANIŞMAN",
        "grid_filename": "grid_40.png",
        "row": 10,
        "column": 10,
        "x": 820,
        "y": 1060
    },
    {
        "personId": "00051577",
        "name": "VOLKAN SOLMAZ",
        "grid_filename": "grid_41.png",
        "row": 2,
        "column": 7,
        "x": 574,
        "y": 212
    },
    {
        "personId": "00067695",
        "name": "MUHAMMED OSMAN BAYRAK",
        "grid_filename": "grid_41.png",
        "row": 2,
        "column": 8,
        "x": 656,
        "y": 212
    },
    {
        "personId": "00104825",
        "name": "ÖZEN ÖZER",
        "grid_filename": "grid_41.png",
        "row": 4,
        "column": 10,
        "x": 820,
        "y": 424
    },
    {
        "personId": "00051478",
        "name": "ÖZGÜR KOCABAY",
        "grid_filename": "grid_41.png",
        "row": 5,
        "column": 4,
        "x": 328,
        "y": 530
    },
    {
        "personId": "00059350",
        "name": "SERKAN KANDEMİR",
        "grid_filename": "grid_41.png",
        "row": 5,
        "column": 7,
        "x": 574,
        "y": 530
    },
    {
        "personId": "00053707",
        "name": "FATİH RÜŞTÜ ALTUNOK",
        "grid_filename": "grid_41.png",
        "row": 5,
        "column": 10,
        "x": 820,
        "y": 530
    },
    {
        "personId": "00054309",
        "name": "ÖMER ÇAPOĞLU",
        "grid_filename": "grid_41.png",
        "row": 5,
        "column": 13,
        "x": 1066,
        "y": 530
    },
    {
        "personId": "00088447",
        "name": "BURHAN GÜNGÖR",
        "grid_filename": "grid_41.png",
        "row": 6,
        "column": 12,
        "x": 984,
        "y": 636
    },
    {
        "personId": "00050451",
        "name": "AKIN ERÇETİN",
        "grid_filename": "grid_41.png",
        "row": 6,
        "column": 13,
        "x": 1066,
        "y": 636
    },
    {
        "personId": "00085927",
        "name": "AYŞEGÜL DENLİ",
        "grid_filename": "grid_41.png",
        "row": 7,
        "column": 5,
        "x": 410,
        "y": 742
    },
    {
        "personId": "00076889",
        "name": "ALİ ARTUN TELLİ",
        "grid_filename": "grid_41.png",
        "row": 7,
        "column": 7,
        "x": 574,
        "y": 742
    },
    {
        "personId": "00049716",
        "name": "ÖNER CAN GÜNAYAR",
        "grid_filename": "grid_41.png",
        "row": 7,
        "column": 9,
        "x": 738,
        "y": 742
    },
    {
        "personId": "00086841",
        "name": "OSMAN ŞAFAK",
        "grid_filename": "grid_41.png",
        "row": 8,
        "column": 5,
        "x": 410,
        "y": 848
    },
    {
        "personId": "00067264",
        "name": "ORHAN ÖNAL",
        "grid_filename": "grid_41.png",
        "row": 8,
        "column": 6,
        "x": 492,
        "y": 848
    },
    {
        "personId": "00065598",
        "name": "MUHAMMED BİLAL DÖNER",
        "grid_filename": "grid_41.png",
        "row": 8,
        "column": 11,
        "x": 902,
        "y": 848
    },
    {
        "personId": "00069337",
        "name": "FIRAT ÖZBAY",
        "grid_filename": "grid_41.png",
        "row": 9,
        "column": 5,
        "x": 410,
        "y": 954
    },
    {
        "personId": "00058167",
        "name": "GÖKHAN ÇERİ",
        "grid_filename": "grid_41.png",
        "row": 9,
        "column": 8,
        "x": 656,
        "y": 954
    },
    {
        "personId": "00074319",
        "name": "YÜCEL ÇINAR",
        "grid_filename": "grid_41.png",
        "row": 10,
        "column": 1,
        "x": 82,
        "y": 1060
    },
    {
        "personId": "00051524",
        "name": "ÖZLEM ÖNCEL",
        "grid_filename": "grid_42.png",
        "row": 0,
        "column": 0,
        "x": 0,
        "y": 0
    },
    {
        "personId": "00061461",
        "name": "İSMAİL SELİM ECİRLİ",
        "grid_filename": "grid_42.png",
        "row": 1,
        "column": 1,
        "x": 82,
        "y": 106
    },
    {
        "personId": "00060945",
        "name": "HASAN SERKAN BİNYAR",
        "grid_filename": "grid_42.png",
        "row": 1,
        "column": 5,
        "x": 410,
        "y": 106
    },
    {
        "personId": "00064809",
        "name": "İSMAİL ÖZTÜRK",
        "grid_filename": "grid_42.png",
        "row": 1,
        "column": 7,
        "x": 574,
        "y": 106
    },
    {
        "personId": "00052196",
        "name": "SÜLEYMAN ERSİN ÖZTOPAL",
        "grid_filename": "grid_42.png",
        "row": 2,
        "column": 7,
        "x": 574,
        "y": 212
    },
    {
        "personId": "00081647",
        "name": "MUHAMMED MASUM AYDIN",
        "grid_filename": "grid_42.png",
        "row": 5,
        "column": 2,
        "x": 164,
        "y": 530
    },
    {
        "personId": "00054140",
        "name": "NERMİN AZEM KIRAN",
        "grid_filename": "grid_42.png",
        "row": 6,
        "column": 2,
        "x": 164,
        "y": 636
    },
    {
        "personId": "00080216",
        "name": "MUHAMMED ALİ YAPAR",
        "grid_filename": "grid_42.png",
        "row": 7,
        "column": 13,
        "x": 1066,
        "y": 742
    },
    {
        "personId": "00068521",
        "name": "RESUL ÇAKMAK",
        "grid_filename": "grid_42.png",
        "row": 8,
        "column": 6,
        "x": 492,
        "y": 848
    },
    {
        "personId": "00069823",
        "name": "FATİH MEHMET KURŞUN",
        "grid_filename": "grid_42.png",
        "row": 9,
        "column": 0,
        "x": 0,
        "y": 954
    },
    {
        "personId": "00057427",
        "name": "CELAL BAYKAL",
        "grid_filename": "grid_42.png",
        "row": 9,
        "column": 3,
        "x": 246,
        "y": 954
    },
    {
        "personId": "00020134",
        "name": "MURAT ŞEKER",
        "grid_filename": "grid_42.png",
        "row": 9,
        "column": 7,
        "x": 574,
        "y": 954
    },
    {
        "personId": "00082453",
        "name": "SEFA KARAKELLE",
        "grid_filename": "grid_42.png",
        "row": 9,
        "column": 10,
        "x": 820,
        "y": 954
    },
    {
        "personId": "00051365",
        "name": "ERSİN DEMİR",
        "grid_filename": "grid_42.png",
        "row": 10,
        "column": 13,
        "x": 1066,
        "y": 1060
    },
    {
        "personId": "00065731",
        "name": "NUMAN ÇİZMECİOĞLU",
        "grid_filename": "grid_43.png",
        "row": 0,
        "column": 7,
        "x": 574,
        "y": 0
    },
    {
        "personId": "00104636",
        "name": "FİLİZ SEMERCİ",
        "grid_filename": "grid_43.png",
        "row": 0,
        "column": 8,
        "x": 656,
        "y": 0
    },
    {
        "personId": "00074999",
        "name": "TUĞBA CERRAH",
        "grid_filename": "grid_43.png",
        "row": 1,
        "column": 2,
        "x": 164,
        "y": 106
    },
    {
        "personId": "00048529",
        "name": "BURÇAK KAYACAN",
        "grid_filename": "grid_43.png",
        "row": 1,
        "column": 5,
        "x": 410,
        "y": 106
    },
    {
        "personId": "00059382",
        "name": "MURAT GÜR",
        "grid_filename": "grid_43.png",
        "row": 2,
        "column": 6,
        "x": 492,
        "y": 212
    },
    {
        "personId": "00089904",
        "name": "FATİH TAYYAR",
        "grid_filename": "grid_43.png",
        "row": 2,
        "column": 13,
        "x": 1066,
        "y": 212
    },
    {
        "personId": "00059981",
        "name": "EBUBEKİR AKGÜL",
        "grid_filename": "grid_43.png",
        "row": 3,
        "column": 1,
        "x": 82,
        "y": 318
    },
    {
        "personId": "00090420",
        "name": "GÖZDE ŞEN",
        "grid_filename": "grid_43.png",
        "row": 4,
        "column": 1,
        "x": 82,
        "y": 424
    },
    {
        "personId": "00069803",
        "name": "İBRAHİM BAHADIR KORKMAZ",
        "grid_filename": "grid_43.png",
        "row": 5,
        "column": 8,
        "x": 656,
        "y": 530
    },
    {
        "personId": "00061279",
        "name": "AHMET TURSUN",
        "grid_filename": "grid_43.png",
        "row": 6,
        "column": 3,
        "x": 246,
        "y": 636
    },
    {
        "personId": "00085966",
        "name": "GÖKTUĞ DERVİŞOĞLU",
        "grid_filename": "grid_43.png",
        "row": 10,
        "column": 10,
        "x": 820,
        "y": 1060
    },
    {
        "personId": "00048801",
        "name": "ALPASLAN AĞDAŞ",
        "grid_filename": "grid_43.png",
        "row": 10,
        "column": 13,
        "x": 1066,
        "y": 1060
    },
    {
        "personId": "00072774",
        "name": "MUKADDES SERT",
        "grid_filename": "grid_44.png",
        "row": 0,
        "column": 4,
        "x": 328,
        "y": 0
    },
    {
        "personId": "00074868",
        "name": "EKREM RODOPLU",
        "grid_filename": "grid_44.png",
        "row": 0,
        "column": 6,
        "x": 492,
        "y": 0
    },
    {
        "personId": "00068337",
        "name": "HASAN YILDIZ",
        "grid_filename": "grid_44.png",
        "row": 1,
        "column": 1,
        "x": 82,
        "y": 106
    },
    {
        "personId": "00051342",
        "name": "ONUR ALPAN",
        "grid_filename": "grid_44.png",
        "row": 1,
        "column": 10,
        "x": 820,
        "y": 106
    },
    {
        "personId": "00051940",
        "name": "EDA OCAK",
        "grid_filename": "grid_44.png",
        "row": 2,
        "column": 2,
        "x": 164,
        "y": 212
    },
    {
        "personId": "00086839",
        "name": "İBRAHİM TUNÇ",
        "grid_filename": "grid_44.png",
        "row": 3,
        "column": 9,
        "x": 738,
        "y": 318
    },
    {
        "personId": "00081435",
        "name": "GONCA GÜL EREN PINAR",
        "grid_filename": "grid_44.png",
        "row": 6,
        "column": 1,
        "x": 82,
        "y": 636
    },
    {
        "personId": "00066867",
        "name": "TARIK ZİYA GÜRLER",
        "grid_filename": "grid_44.png",
        "row": 8,
        "column": 2,
        "x": 164,
        "y": 848
    },
    {
        "personId": "00051458",
        "name": "YİĞİT NELİK",
        "grid_filename": "grid_44.png",
        "row": 8,
        "column": 6,
        "x": 492,
        "y": 848
    },
    {
        "personId": "00054116",
        "name": "ENGİN AKBAŞ",
        "grid_filename": "grid_44.png",
        "row": 10,
        "column": 8,
        "x": 656,
        "y": 1060
    },
    {
        "personId": "00073678",
        "name": "AHMET FARUK TUNA",
        "grid_filename": "grid_44.png",
        "row": 10,
        "column": 10,
        "x": 820,
        "y": 1060
    },
    {
        "personId": "00098698",
        "name": "GÖKHAN KARAHAN",
        "grid_filename": "grid_45.png",
        "row": 1,
        "column": 2,
        "x": 164,
        "y": 106
    },
    {
        "personId": "00074223",
        "name": "AHMET EREN",
        "grid_filename": "grid_45.png",
        "row": 1,
        "column": 4,
        "x": 328,
        "y": 106
    },
    {
        "personId": "00054291",
        "name": "MUSTAFA EMRE UZUNHÜSEYİNOĞLU",
        "grid_filename": "grid_45.png",
        "row": 6,
        "column": 2,
        "x": 164,
        "y": 636
    },
    {
        "personId": "00063163",
        "name": "UMUT GÜRŞEN",
        "grid_filename": "grid_45.png",
        "row": 6,
        "column": 4,
        "x": 328,
        "y": 636
    },
    {
        "personId": "00062358",
        "name": "ENGİN DURMAZ",
        "grid_filename": "grid_45.png",
        "row": 7,
        "column": 8,
        "x": 656,
        "y": 742
    },
    {
        "personId": "00050012",
        "name": "ÖMER UĞUR",
        "grid_filename": "grid_45.png",
        "row": 7,
        "column": 11,
        "x": 902,
        "y": 742
    },
    {
        "personId": "00063316",
        "name": "YUSUF DİLBEROĞLU",
        "grid_filename": "grid_45.png",
        "row": 9,
        "column": 3,
        "x": 246,
        "y": 954
    },
    {
        "personId": "00069759",
        "name": "GAMZE UÇAR",
        "grid_filename": "grid_45.png",
        "row": 10,
        "column": 1,
        "x": 82,
        "y": 1060
    },
    {
        "personId": "00070369",
        "name": "AHMET AKBULUT",
        "grid_filename": "grid_45.png",
        "row": 10,
        "column": 3,
        "x": 246,
        "y": 1060
    },
    {
        "personId": "00057076",
        "name": "MEHMET KADAİFÇİLER",
        "grid_filename": "grid_45.png",
        "row": 10,
        "column": 13,
        "x": 1066,
        "y": 1060
    },
    {
        "personId": "00054150",
        "name": "RESUL BAŞ",
        "grid_filename": "grid_46.png",
        "row": 0,
        "column": 1,
        "x": 82,
        "y": 0
    },
    {
        "personId": "00054115",
        "name": "MEHMET AKALIN",
        "grid_filename": "grid_46.png",
        "row": 0,
        "column": 9,
        "x": 738,
        "y": 0
    },
    {
        "personId": "00052426",
        "name": "LATİF CEMRE OKTAR",
        "grid_filename": "grid_46.png",
        "row": 1,
        "column": 10,
        "x": 820,
        "y": 106
    },
    {
        "personId": "00053784",
        "name": "GÖKHAN EMİR",
        "grid_filename": "grid_46.png",
        "row": 1,
        "column": 12,
        "x": 984,
        "y": 106
    },
    {
        "personId": "00073583",
        "name": "LOKMAN BALKAN",
        "grid_filename": "grid_46.png",
        "row": 6,
        "column": 5,
        "x": 410,
        "y": 636
    },
    {
        "personId": "00054161",
        "name": "FATİH CIĞAL",
        "grid_filename": "grid_46.png",
        "row": 7,
        "column": 0,
        "x": 0,
        "y": 742
    },
    {
        "personId": "00075396",
        "name": "YUSUF İSLAM EGİCİ",
        "grid_filename": "grid_46.png",
        "row": 7,
        "column": 1,
        "x": 82,
        "y": 742
    },
    {
        "personId": "00055013",
        "name": "RAİF ASANA",
        "grid_filename": "grid_46.png",
        "row": 8,
        "column": 5,
        "x": 410,
        "y": 848
    },
    {
        "personId": "00072617",
        "name": "İBRAHİM KÜÇÜK",
        "grid_filename": "grid_46.png",
        "row": 8,
        "column": 10,
        "x": 820,
        "y": 848
    }
    ]

    upserts = 0
    for doc in sample:
        if "name" in doc:
            doc["name_normalized"] = normalize_name(str(doc["name"]))
        res = await persons.update_one(
            {"personId": doc["personId"]},
            {"$set": doc},
            upsert=True,
        )
        if res.upserted_id is not None:
            upserts += 1

    total = await persons.count_documents({})
    print(f"Seed complete. Upserted {upserts} docs. persons total={total}. DB={db_name}")

    client.close()


if __name__ == "__main__":
    asyncio.run(main())
