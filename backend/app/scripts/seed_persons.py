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
        "personId": "00054148",
        "name": "MURAT BAŞ",
        "grid_filename": "grid_1.png",
        "x": 2.382,
        "y": -1.763,
        "z": 4.269
    },
    {
        "personId": "00075591",
        "name": "AGAH SELİM ALUÇ",
        "grid_filename": "grid_1.png",
        "x": -2.161,
        "y": -0.09,
        "z": -18.391
    },
    {
        "personId": "00031313",
        "name": "HÜSEYİN BORAZAN",
        "grid_filename": "grid_1.png",
        "x": -1.902,
        "y": 3.365,
        "z": -20.208
    },
    {
        "personId": "00116537",
        "name": "SERHAT BÖR",
        "grid_filename": "grid_1.png",
        "x": 2.922,
        "y": 0.884,
        "z": -13.19
    },
    {
        "personId": "00065390",
        "name": "MUTLU DÖNMEZ",
        "grid_filename": "grid_1.png",
        "x": 2.192,
        "y": -1.809,
        "z": 4.416
    },
    {
        "personId": "00048419",
        "name": "BURAK ŞOLTAN",
        "grid_filename": "grid_1.png",
        "x": 3.014,
        "y": 1.163,
        "z": -7.74
    },
    {
        "personId": "00069336",
        "name": "NİHAL AÇIKEL",
        "grid_filename": "grid_1.png",
        "x": 2.052,
        "y": -0.15,
        "z": -18.804
    },
    {
        "personId": "00068346",
        "name": "HALİT TUNCER",
        "grid_filename": "grid_1.png",
        "x": 2.773,
        "y": 0.324,
        "z": -11.154
    },
    {
        "personId": "00102943",
        "name": "AHMET ZİYAEDDİN ÖZTÜRK",
        "grid_filename": "grid_1.png",
        "x": -1.582,
        "y": 3.65,
        "z": -20.352
    },
    {
        "personId": "00054149",
        "name": "OKAN BAŞ",
        "grid_filename": "grid_1.png",
        "x": -2.728,
        "y": -1.029,
        "z": -4.852
    },
    {
        "personId": "00059981",
        "name": "EBUBEKİR AKGÜL",
        "grid_filename": "grid_1.png",
        "x": 2.989,
        "y": 0.98,
        "z": -9.41
    },
    {
        "personId": "00067010",
        "name": "DİLEK YALÇIN",
        "grid_filename": "grid_1.png",
        "x": 2.818,
        "y": 0.511,
        "z": -15.532
    },
    {
        "personId": "00063052",
        "name": "MUHAMMED FATİH DURMAZ",
        "grid_filename": "grid_1.png",
        "x": 2.996,
        "y": 1.444,
        "z": -14.952
    },
    {
        "personId": "00074509",
        "name": "ABDULSAMET SAFA DİLMAÇ",
        "grid_filename": "grid_1.png",
        "x": 0.456,
        "y": 4.181,
        "z": -15.097
    },
    {
        "personId": "00054267",
        "name": "ABDULLAH SAİT ŞENLER",
        "grid_filename": "grid_1.png",
        "x": 2.238,
        "y": 3.219,
        "z": -9.702
    },
    {
        "personId": "00053421",
        "name": "ÖMER UZUN",
        "grid_filename": "grid_1.png",
        "x": 2.098,
        "y": -0.244,
        "z": -18.151
    },
    {
        "personId": "00089801",
        "name": "AYDOĞAN CAN",
        "grid_filename": "grid_1.png",
        "x": 2.776,
        "y": 0.325,
        "z": -14.864
    },
    {
        "personId": "00045303",
        "name": "GÜRHAN SÖZEN",
        "grid_filename": "grid_1.png",
        "x": 2.823,
        "y": 0.512,
        "z": -11.154
    },
    {
        "personId": "00046537",
        "name": "İBRAHİM DEMİRDÖĞEN",
        "grid_filename": "grid_1.png",
        "x": -0.216,
        "y": 4.18,
        "z": -18.459
    },
    {
        "personId": "00069462",
        "name": "ABDULLAH YILDIZ",
        "grid_filename": "grid_1.png",
        "x": 2.46,
        "y": 0.602,
        "z": -19.749
    },
    {
        "personId": "00060069",
        "name": "MELİH TORLAK",
        "grid_filename": "grid_1.png",
        "x": 2.903,
        "y": 0.881,
        "z": -15.603
    },
    {
        "personId": "00068337",
        "name": "HASAN YILDIZ",
        "grid_filename": "grid_1.png",
        "x": 2.696,
        "y": 0.046,
        "z": -10.501
    },
    {
        "personId": "00053430",
        "name": "OĞUZ DÖNMEZ",
        "grid_filename": "grid_1.png",
        "x": -3.08,
        "y": -0.467,
        "z": -5.943
    },
    {
        "personId": "00079334",
        "name": "ÜMMET ŞENOCAK",
        "grid_filename": "grid_1.png",
        "x": 1.765,
        "y": 3.687,
        "z": -7.594
    },
    {
        "personId": "00072676",
        "name": "AHMET EMRE TÜRKOĞLU",
        "grid_filename": "grid_1.png",
        "x": -2.626,
        "y": 2.715,
        "z": -11.395
    },
    {
        "personId": "00087164",
        "name": "SAMET ELİTOK",
        "grid_filename": "grid_1.png",
        "x": 2.82,
        "y": 0.512,
        "z": -10.283
    },
    {
        "personId": "00063463",
        "name": "SALİH KAMİL SALİHOĞLU",
        "grid_filename": "grid_1.png",
        "x": 2.924,
        "y": 0.699,
        "z": -9.555
    },
    {
        "personId": "00065250",
        "name": "ÖMER ÖZDERYA",
        "grid_filename": "grid_1.png",
        "x": -3.27,
        "y": -0.467,
        "z": -3.541
    },
    {
        "personId": "00060936",
        "name": "ŞUAYB ÖZHAN",
        "grid_filename": "grid_1.png",
        "x": -2.884,
        "y": 2.152,
        "z": -0.563
    },
    {
        "personId": "00060558",
        "name": "İSMAİL VOLKAN ÖZAYDINLI",
        "grid_filename": "grid_1.png",
        "x": -2.796,
        "y": 2.343,
        "z": -3.831
    },
    {
        "personId": "00053206",
        "name": "ENİS ÖZDEMİRLİ",
        "grid_filename": "grid_1.png",
        "x": 2.88,
        "y": 0.787,
        "z": -16.769
    },
    {
        "personId": "00062762",
        "name": "YUSUF YILMAZ",
        "grid_filename": "grid_1.png",
        "x": 3.013,
        "y": 1.168,
        "z": -10.355
    },
    {
        "personId": "00081431",
        "name": "BÜŞRA YILDIZ KORKMAZ",
        "grid_filename": "grid_1.png",
        "x": 2.484,
        "y": -0.051,
        "z": -15.532
    },
    {
        "personId": "00063011",
        "name": "TARIK KURU",
        "grid_filename": "grid_1.png",
        "x": 2.949,
        "y": 0.978,
        "z": -11.664
    },
    {
        "personId": "00074993",
        "name": "İBRAHİM BULUT",
        "grid_filename": "grid_1.png",
        "x": -2.792,
        "y": 2.337,
        "z": 3.284
    },
    {
        "personId": "00051577",
        "name": "VOLKAN SOLMAZ",
        "grid_filename": "grid_1.png",
        "x": 0.267,
        "y": 4.226,
        "z": -1.921
    },
    {
        "personId": "00069037",
        "name": "EYÜP KARS",
        "grid_filename": "grid_1.png",
        "x": -0.864,
        "y": 4.109,
        "z": -4.922
    },
    {
        "personId": "00072098",
        "name": "İSMAİL KIYAR",
        "grid_filename": "grid_1.png",
        "x": 3.012,
        "y": 1.35,
        "z": -8.247
    },
    {
        "personId": "00112268",
        "name": "ÖMER FURKANALTAY",
        "grid_filename": "grid_1.png",
        "x": 2.986,
        "y": 1.537,
        "z": -14.064
    },
    {
        "personId": "00051563",
        "name": "KAMİL ENGİN KARAMAN",
        "grid_filename": "grid_1.png",
        "x": 2.963,
        "y": 0.778,
        "z": -8.248
    },
    {
        "personId": "00020136",
        "name": "AHMET BOLAT",
        "grid_filename": "grid_1.png",
        "x": 2.689,
        "y": 0.127,
        "z": -14.062
    },
    {
        "personId": "00061192",
        "name": "ÖMER FARUK YAVUZ",
        "grid_filename": "grid_1.png",
        "x": 2.987,
        "y": 1.54,
        "z": -13.481
    },
    {
        "personId": "00073377",
        "name": "FEYZA İMAL",
        "grid_filename": "grid_1.png",
        "x": 1.857,
        "y": 3.596,
        "z": -8.319
    },
    {
        "personId": "00066098",
        "name": "AHMET KÖSE",
        "grid_filename": "grid_1.png",
        "x": 2.8,
        "y": 0.419,
        "z": -14.355
    },
    {
        "personId": "00067898",
        "name": "MUHAMMED CÜNEYT AYDAR",
        "grid_filename": "grid_1.png",
        "x": -2.963,
        "y": 1.314,
        "z": -16.426
    },
    {
        "personId": "00088127",
        "name": "MUSTAFA CİHANGİR OĞUZ",
        "grid_filename": "grid_1.png",
        "x": 2.1,
        "y": -1.842,
        "z": 4.27
    },
    {
        "personId": "00700000",
        "name": "GÜZİDE AKDOĞAN",
        "grid_filename": "grid_1.png",
        "x": 2.898,
        "y": 0.786,
        "z": -12.099
    },
    {
        "personId": "00052022",
        "name": "İLKER ÖZAYDIN",
        "grid_filename": "grid_1.png",
        "x": 2.919,
        "y": 0.975,
        "z": -16.332
    },
    {
        "personId": "00068527",
        "name": "NEŞE ÇALIŞIR",
        "grid_filename": "grid_1.png",
        "x": -2.921,
        "y": 1.961,
        "z": -6.969
    },
    {
        "personId": "00082713",
        "name": "YAHYA ÜSTÜN",
        "grid_filename": "grid_1.png",
        "x": 1.885,
        "y": -0.241,
        "z": -19.386
    },
    {
        "personId": "00063968",
        "name": "AHMET BURAK OKTAY",
        "grid_filename": "grid_1.png",
        "x": 2.849,
        "y": 0.603,
        "z": -13.481
    },
    {
        "personId": "00065982",
        "name": "ALPER RIZA ÖZDEMİR",
        "grid_filename": "grid_1.png",
        "x": 2.442,
        "y": 3.031,
        "z": -14.425
    },
    {
        "personId": "00087269",
        "name": "ERHAN YEŞİLKAYA",
        "grid_filename": "grid_1.png",
        "x": 2.678,
        "y": 0.044,
        "z": -13.118
    },
    {
        "personId": "00080196",
        "name": "AYŞE SALCANARSLAN",
        "grid_filename": "grid_1.png",
        "x": -2.835,
        "y": 1.774,
        "z": -18.317
    },
    {
        "personId": "00063013",
        "name": "SELÇUK GENÇASLAN",
        "grid_filename": "grid_1.png",
        "x": 2.715,
        "y": 0.788,
        "z": -18.954
    },
    {
        "personId": "00075360",
        "name": "İREM DÜLGER",
        "grid_filename": "grid_1.png",
        "x": 2.968,
        "y": 1.535,
        "z": -16.185
    },
    {
        "personId": "00054203",
        "name": "NESİH GÜMÜŞ",
        "grid_filename": "grid_1.png",
        "x": -3.018,
        "y": 1.209,
        "z": -7.978
    },
    {
        "personId": "00062260",
        "name": "İNANÇ EMRE ALBAYRAK",
        "grid_filename": "grid_1.png",
        "x": 1.679,
        "y": 3.774,
        "z": -8.322
    },
    {
        "personId": "00062298",
        "name": "AHMET HARUN BAŞTÜRK",
        "grid_filename": "grid_1.png",
        "x": -2.031,
        "y": 3.367,
        "z": -18.172
    },
    {
        "personId": "00085966",
        "name": "GÖKTUĞ DERVİŞOĞLU",
        "grid_filename": "grid_1.png",
        "x": 1.859,
        "y": 3.595,
        "z": -8.029
    },
    {
        "personId": "00047173",
        "name": "PINAR AYVAZ ARIKAN",
        "grid_filename": "grid_1.png",
        "x": 2.996,
        "y": 1.166,
        "z": -12.536
    },
    {
        "personId": "00050012",
        "name": "ÖMER UĞUR",
        "grid_filename": "grid_1.png",
        "x": 2.957,
        "y": 1.725,
        "z": -14.136
    },
    {
        "personId": "00054121",
        "name": "GÜRKANAKIN",
        "grid_filename": "grid_1.png",
        "x": -2.762,
        "y": 1.312,
        "z": -19.191
    },
    {
        "personId": "00075047",
        "name": "MEHMET BURAK ÇAKIR",
        "grid_filename": "grid_1.png",
        "x": 2.731,
        "y": 1.537,
        "z": -19.749
    },
    {
        "personId": "00065124",
        "name": "MEHMED ZİNGAL",
        "grid_filename": "grid_1.png",
        "x": 0.138,
        "y": -2.207,
        "z": 3.906
    },
    {
        "personId": "00053229",
        "name": "MEHMET AKİF KONAR",
        "grid_filename": "grid_1.png",
        "x": 2.505,
        "y": -0.141,
        "z": -14.136
    },
    {
        "personId": "00072981",
        "name": "ZEYNEP ÖZDEMİR",
        "grid_filename": "grid_1.png",
        "x": 2.972,
        "y": 1.634,
        "z": -10.283
    },
    {
        "personId": "00085927",
        "name": "AYŞEGÜL DENLİ",
        "grid_filename": "grid_1.png",
        "x": 2.064,
        "y": 0.04,
        "z": -19.53
    },
    {
        "personId": "00083609",
        "name": "ALPASLAN CEBE",
        "grid_filename": "grid_1.png",
        "x": -0.304,
        "y": 4.218,
        "z": 0.894
    },
    {
        "personId": "00054533",
        "name": "FARUK BİLİR",
        "grid_filename": "grid_1.png",
        "x": 2.985,
        "y": 1.534,
        "z": -7.813
    },
    {
        "personId": "00109385",
        "name": "ENES YILMAZ",
        "grid_filename": "grid_1.png",
        "x": 2.839,
        "y": 0.603,
        "z": -16.26
    },
    {
        "personId": "00064649",
        "name": "ENES SAİM ÖZYÜREK",
        "grid_filename": "grid_1.png",
        "x": 2.779,
        "y": 0.415,
        "z": -16.187
    },
    {
        "personId": "00048323",
        "name": "CEM TANBURACI",
        "grid_filename": "grid_1.png",
        "x": -1.146,
        "y": 4.051,
        "z": -0.416
    },
    {
        "personId": "00058832",
        "name": "ŞAFAK BAŞARAN",
        "grid_filename": "grid_1.png",
        "x": 2.233,
        "y": -0.145,
        "z": -17.785
    },
    {
        "personId": "00061461",
        "name": "İSMAİL SELİM ECİRLİ",
        "grid_filename": "grid_1.png",
        "x": 2.234,
        "y": 3.221,
        "z": -7.591
    },
    {
        "personId": "123456789",
        "name": "ARİF ALİ GEZMİŞOĞLU",
        "grid_filename": "grid_1.png",
        "x": 2.957,
        "y": 0.883,
        "z": -10.066
    },
    {
        "personId": "00020257",
        "name": "ÖZGÜL ÖZKAN YAVUZ",
        "grid_filename": "grid_1.png",
        "x": 2.998,
        "y": 1.069,
        "z": -10.283
    },
    {
        "personId": "00083341",
        "name": "YUNUS DOĞAN",
        "grid_filename": "grid_1.png",
        "x": -2.99,
        "y": 1.498,
        "z": -14.522
    },
    {
        "personId": "00067797",
        "name": "MEHMET ZAHİD ÖZEL",
        "grid_filename": "grid_1.png",
        "x": 3.014,
        "y": 1.352,
        "z": -10.72
    },
    {
        "personId": "00053407",
        "name": "RAFET ŞİŞMAN",
        "grid_filename": "grid_1.png",
        "x": 2.644,
        "y": -0.143,
        "z": -10.066
    },
    {
        "personId": "00069763",
        "name": "KENAN TURGUT",
        "grid_filename": "grid_1.png",
        "x": 2.903,
        "y": 0.881,
        "z": -15.316
    },
    {
        "personId": "00057988",
        "name": "HAKAN LOKMAN YÜKSEL",
        "grid_filename": "grid_1.png",
        "x": 2.772,
        "y": 0.325,
        "z": -10.718
    },
    {
        "personId": "00068205",
        "name": "AYŞE TOPÇU",
        "grid_filename": "grid_1.png",
        "x": -0.864,
        "y": 4.107,
        "z": -13.866
    },
    {
        "personId": "00066473",
        "name": "HASAN BEYAZÖRTÜ",
        "grid_filename": "grid_1.png",
        "x": 2.698,
        "y": 0.041,
        "z": -11.301
    },
    {
        "personId": "123456789",
        "name": "FATİH VURAL SAYIN",
        "grid_filename": "grid_1.png",
        "x": -2.919,
        "y": 0.938,
        "z": -14.156
    },
    {
        "personId": "00062095",
        "name": "CÜNEYT SEVIM",
        "grid_filename": "grid_1.png",
        "x": -2.717,
        "y": 2.528,
        "z": -11.756
    },
    {
        "personId": "00054283",
        "name": "SELAMET TURNA",
        "grid_filename": "grid_1.png",
        "x": 2.99,
        "y": 0.782,
        "z": -0.322
    },
    {
        "personId": "00049794",
        "name": "MEHMET AKAY",
        "grid_filename": "grid_1.png",
        "x": 2.681,
        "y": 0.043,
        "z": -13.045
    },
    {
        "personId": "00085211",
        "name": "ÖMER SEVBAN CEYLAN",
        "grid_filename": "grid_1.png",
        "x": -2.565,
        "y": 2.624,
        "z": -18.68
    },
    {
        "personId": "123456789",
        "name": "MUSTAFA ÖZGÜREL",
        "grid_filename": "grid_1.png",
        "x": 1.649,
        "y": 3.681,
        "z": -18.954
    },
    {
        "personId": "00054209",
        "name": "ORHAN GÜVEN",
        "grid_filename": "grid_1.png",
        "x": 3.01,
        "y": 1.259,
        "z": -13.481
    },
    {
        "personId": "00072805",
        "name": "SÜLEYMAN YASİR VERİMLİ",
        "grid_filename": "grid_1.png",
        "x": -1.152,
        "y": 4.051,
        "z": -3.178
    },
    {
        "personId": "123456789",
        "name": "MUSTAFA TALHA KARAHAN",
        "grid_filename": "grid_1.png",
        "x": 1.914,
        "y": -1.893,
        "z": 4.416
    },
    {
        "personId": "00057482",
        "name": "BİLAL DEMİÇ",
        "grid_filename": "grid_1.png",
        "x": 2.467,
        "y": -0.142,
        "z": -14.922
    },
    {
        "personId": "00050498",
        "name": "AKIN ÇARKÇI",
        "grid_filename": "grid_1.png",
        "x": 2.594,
        "y": -0.05,
        "z": -13.558
    },
    {
        "personId": "00072966",
        "name": "EBUZER TANHAN",
        "grid_filename": "grid_1.png",
        "x": 2.861,
        "y": 0.696,
        "z": -15.679
    },
    {
        "personId": "00047213",
        "name": "ERSEN ENGİN",
        "grid_filename": "grid_1.png",
        "x": 2.472,
        "y": 0.694,
        "z": -20.114
    },
    {
        "personId": "123456789",
        "name": "EMRE HARPUTLU",
        "grid_filename": "grid_1.png",
        "x": 2.963,
        "y": 0.883,
        "z": -9.845
    },
    {
        "personId": "00067464",
        "name": "BİLAL SEMİH ÖNEL",
        "grid_filename": "grid_1.png",
        "x": 3.124,
        "y": 0.098,
        "z": 0.708
    },
    {
        "personId": "00051344",
        "name": "SELÇUK ÇAPUK",
        "grid_filename": "grid_1.png",
        "x": 2.989,
        "y": 1.538,
        "z": -12.827
    },
    {
        "personId": "123456789",
        "name": "SEMİH AKBULUT",
        "grid_filename": "grid_1.png",
        "x": 3.001,
        "y": 1.435,
        "z": -10.352
    },
    {
        "personId": "00080829",
        "name": "MEHMET ARİF TATOĞLU",
        "grid_filename": "grid_1.png",
        "x": -2.426,
        "y": -0.183,
        "z": -14.922
    },
    {
        "personId": "00054140",
        "name": "NERMİNAZEM KIRAN",
        "grid_filename": "grid_1.png",
        "x": 2.971,
        "y": 1.628,
        "z": -8.319
    },
    {
        "personId": "00075011",
        "name": "ABDULLAH YILMAZ",
        "grid_filename": "grid_1.png",
        "x": -0.865,
        "y": 4.106,
        "z": -14.232
    },
    {
        "personId": "00068235",
        "name": "ADNAN KARAİSMAİLOĞLU",
        "grid_filename": "grid_1.png",
        "x": -1.238,
        "y": 4.009,
        "z": -8.122
    },
    {
        "personId": "00073957",
        "name": "MUSTAFA OĞULCAN BİLGİN",
        "grid_filename": "grid_1.png",
        "x": -1.374,
        "y": 3.72,
        "z": -21.589
    },
    {
        "personId": "00075124",
        "name": "MEHMET AŞIK",
        "grid_filename": "grid_1.png",
        "x": 1.8,
        "y": -0.053,
        "z": -20.551
    },
    {
        "personId": "00061901",
        "name": "LEVENT KESKİNGÖZ",
        "grid_filename": "grid_1.png",
        "x": 2.994,
        "y": 1.444,
        "z": -15.169
    },
    {
        "personId": "00062192",
        "name": "AHMET YILDIZ",
        "grid_filename": "grid_1.png",
        "x": 2.568,
        "y": -0.048,
        "z": -14.134
    },
    {
        "personId": "00073583",
        "name": "LOKMAN BALKAN",
        "grid_filename": "grid_1.png",
        "x": 2.473,
        "y": -1.746,
        "z": 3.69
    },
    {
        "personId": "00095386",
        "name": "HAKAN ÖZTÜRK",
        "grid_filename": "grid_1.png",
        "x": 2.771,
        "y": 0.325,
        "z": -10.573
    },
    {
        "personId": "00089119",
        "name": "CİHAD MUHAMMED YILDIZ",
        "grid_filename": "grid_1.png",
        "x": 2.516,
        "y": -0.051,
        "z": -15.099
    },
    {
        "personId": "00090381",
        "name": "GÜLÇİN GÜLKILIK",
        "grid_filename": "grid_1.png",
        "x": 2.799,
        "y": 0.418,
        "z": -11.301
    },
    {
        "personId": "00081737",
        "name": "ADEM KILIÇ",
        "grid_filename": "grid_1.png",
        "x": 2.075,
        "y": 0.133,
        "z": -19.896
    },
    {
        "personId": "00066157",
        "name": "ESRA KARAYAKA",
        "grid_filename": "grid_1.png",
        "x": 2.55,
        "y": -0.234,
        "z": -11.445
    },
    {
        "personId": "00053707",
        "name": "FATİH RÜŞTÜ ALTUNOK",
        "grid_filename": "grid_1.png",
        "x": 2.699,
        "y": 0.044,
        "z": -11.446
    },
    {
        "personId": "00071061",
        "name": "FADEN ÖZTÜRK",
        "grid_filename": "grid_1.png",
        "x": -2.446,
        "y": 0.376,
        "z": -18.68
    },
    {
        "personId": "00072747",
        "name": "MEHMET FATİH KORKMAZ",
        "grid_filename": "grid_1.png",
        "x": 2.637,
        "y": -0.048,
        "z": -12.753
    },
    {
        "personId": "00074152",
        "name": "İSLAM GÜRE",
        "grid_filename": "grid_1.png",
        "x": 2.97,
        "y": 1.535,
        "z": -16.041
    },
    {
        "personId": "00054292",
        "name": "İBRAHİM ÜMİT",
        "grid_filename": "grid_1.png",
        "x": 10.248,
        "y": -1.074,
        "z": 6.546
    },
    {
        "personId": "00065127",
        "name": "ALİ VAHAP NANE",
        "grid_filename": "grid_1.png",
        "x": -0.681,
        "y": 4.147,
        "z": -11.54
    },
    {
        "personId": "00049971",
        "name": "YAKUP GÜL",
        "grid_filename": "grid_1.png",
        "x": 2.948,
        "y": 0.978,
        "z": -11.011
    },
    {
        "personId": "00063316",
        "name": "YUSUF DİLBEROĞLU",
        "grid_filename": "grid_1.png",
        "x": 2.971,
        "y": 1.634,
        "z": -9.41
    },
    {
        "personId": "00083144",
        "name": "SERASER GİZEM BAŞAK",
        "grid_filename": "grid_1.png",
        "x": -1.809,
        "y": 3.648,
        "z": -14.084
    },
    {
        "personId": "00116828",
        "name": "MEHMET YEŞİLKAYA",
        "grid_filename": "grid_1.png",
        "x": 2.678,
        "y": 0.044,
        "z": -13.118
    },
    {
        "personId": "00068041",
        "name": "YASİN KAPANCI",
        "grid_filename": "grid_1.png",
        "x": 2.416,
        "y": 3.035,
        "z": -2.94
    },
    {
        "personId": "00072677",
        "name": "YUSUF GÖKSU",
        "grid_filename": "grid_1.png",
        "x": 3.0,
        "y": 1.44,
        "z": -9.773
    },
    {
        "personId": "00068973",
        "name": "FUAT FIRAT",
        "grid_filename": "grid_1.png",
        "x": 2.85,
        "y": 0.606,
        "z": -11.52
    },
    {
        "personId": "00101132",
        "name": "ZEYNEP GÜLEN",
        "grid_filename": "grid_1.png",
        "x": 2.923,
        "y": 0.88,
        "z": -11.958
    },
    {
        "personId": "00058406",
        "name": "NİGAR YILMAZ",
        "grid_filename": "grid_1.png",
        "x": 2.646,
        "y": 0.408,
        "z": -17.714
    },
    {
        "personId": "00073644",
        "name": "BAYRAM ERYILMAZ",
        "grid_filename": "grid_1.png",
        "x": 2.589,
        "y": 0.039,
        "z": -14.922
    },
    {
        "personId": "00098585",
        "name": "SİNAN UĞUR",
        "grid_filename": "grid_1.png",
        "x": 2.988,
        "y": 1.538,
        "z": -11.809
    },
    {
        "personId": "00075003",
        "name": "ALİ FUAT KAZANCI",
        "grid_filename": "grid_1.png",
        "x": 2.585,
        "y": -0.048,
        "z": -13.772
    },
    {
        "personId": "00047927",
        "name": "ÖMER DERE",
        "grid_filename": "grid_1.png",
        "x": 2.975,
        "y": 1.165,
        "z": -14.427
    },
    {
        "personId": "123456789",
        "name": "MEHMET ALİ GÜZEL",
        "grid_filename": "grid_1.png",
        "x": 2.801,
        "y": 0.416,
        "z": -13.118
    },
    {
        "personId": "00061468",
        "name": "ÖZGE ŞAHİN",
        "grid_filename": "grid_1.png",
        "x": 2.995,
        "y": 1.166,
        "z": -12.973
    },
    {
        "personId": "00058824",
        "name": "BİLAL ACAR",
        "grid_filename": "grid_1.png",
        "x": -2.911,
        "y": 0.845,
        "z": -11.249
    },
    {
        "personId": "00063987",
        "name": "UĞUR ŞAHİN",
        "grid_filename": "grid_1.png",
        "x": -0.955,
        "y": 4.076,
        "z": -16.135
    },
    {
        "personId": "123456789",
        "name": "MEHMET AYKUT TUTUCU",
        "grid_filename": "grid_1.png",
        "x": 2.776,
        "y": 0.321,
        "z": -12.173
    },
    {
        "personId": "00057076",
        "name": "MEHMET KADAİFÇİLER",
        "grid_filename": "grid_1.png",
        "x": 2.825,
        "y": 0.511,
        "z": -13.336
    },
    {
        "personId": "00055279",
        "name": "FATİH MATUK",
        "grid_filename": "grid_1.png",
        "x": 2.998,
        "y": 1.438,
        "z": -7.591
    },
    {
        "personId": "00050290",
        "name": "SERKAN YÜRÜMEZ",
        "grid_filename": "grid_1.png",
        "x": 2.968,
        "y": 1.069,
        "z": -13.337
    },
    {
        "personId": "00051880",
        "name": "ERTANALPAY",
        "grid_filename": "grid_1.png",
        "x": 2.055,
        "y": 0.321,
        "z": -20.695
    },
    {
        "personId": "00063969",
        "name": "AKIN ÖMERCİKOĞLU",
        "grid_filename": "grid_1.png",
        "x": 2.75,
        "y": 0.232,
        "z": -14.281
    },
    {
        "personId": "00073326",
        "name": "AHMET KÜRŞAT BALTACI",
        "grid_filename": "grid_1.png",
        "x": 2.752,
        "y": 0.231,
        "z": -13.483
    },
    {
        "personId": "00075918",
        "name": "GÜLDEHAN ERDOĞAN",
        "grid_filename": "grid_1.png",
        "x": 2.627,
        "y": -0.144,
        "z": -11.011
    },
    {
        "personId": "00120306",
        "name": "OKAN ÇETİNKAYA",
        "grid_filename": "grid_1.png",
        "x": 2.422,
        "y": 3.034,
        "z": -7.884
    },
    {
        "personId": "00121979",
        "name": "SEYDA NURZAT ERKAL",
        "grid_filename": "grid_1.png",
        "x": -2.81,
        "y": 0.468,
        "z": -12.118
    },
    {
        "personId": "00054361",
        "name": "GÖKAY KOCA",
        "grid_filename": "grid_1.png",
        "x": -3.031,
        "y": -0.843,
        "z": -7.106
    },
    {
        "personId": "00063501",
        "name": "İBRAHİM HÜNKAR HAN ÇELİKHATİBOĞLU",
        "grid_filename": "grid_1.png",
        "x": 0.92,
        "y": 4.096,
        "z": 0.04
    },
    {
        "personId": "00069138",
        "name": "ALİ FUAT CİCAVOĞLU",
        "grid_filename": "grid_1.png",
        "x": 2.64,
        "y": 0.044,
        "z": -13.918
    },
    {
        "personId": "00055927",
        "name": "MESUT ALAN",
        "grid_filename": "grid_1.png",
        "x": 0.376,
        "y": 4.082,
        "z": -20.82
    },
    {
        "personId": "00069337",
        "name": "FIRAT ÖZBAY",
        "grid_filename": "grid_1.png",
        "x": 2.8,
        "y": 0.418,
        "z": -11.52
    },
    {
        "personId": "00062347",
        "name": "MUSTAFA SANDIKÇI",
        "grid_filename": "grid_1.png",
        "x": 2.191,
        "y": 2.844,
        "z": -21.276
    },
    {
        "personId": "00068245",
        "name": "GÜLAY ERKAL",
        "grid_filename": "grid_1.png",
        "x": 2.772,
        "y": 0.324,
        "z": -10.862
    },
    {
        "personId": "00072940",
        "name": "MEHMET ERTUĞRUL AKTAN",
        "grid_filename": "grid_1.png",
        "x": 2.516,
        "y": 2.938,
        "z": -8.247
    },
    {
        "personId": "00071951",
        "name": "MURAT ŞAHİN",
        "grid_filename": "grid_1.png",
        "x": 2.949,
        "y": 1.072,
        "z": -14.79
    },
    {
        "personId": "123456789",
        "name": "ALİ EMRE YILDIRIM",
        "grid_filename": "grid_1.png",
        "x": 2.718,
        "y": 0.134,
        "z": -13.555
    },
    {
        "personId": "00048232",
        "name": "ADNAN SÖKER",
        "grid_filename": "grid_1.png",
        "x": 2.873,
        "y": 0.697,
        "z": -13.989
    },
    {
        "personId": "00060935",
        "name": "HANDE SÖYLER",
        "grid_filename": "grid_1.png",
        "x": -2.265,
        "y": 3.179,
        "z": 3.002
    },
    {
        "personId": "00075396",
        "name": "YUSUF İSLAM EGİCİ",
        "grid_filename": "grid_1.png",
        "x": -2.814,
        "y": 2.336,
        "z": -13.65
    },
    {
        "personId": "00063341",
        "name": "ÖMER TAYYİP ÇALIŞKAN",
        "grid_filename": "grid_1.png",
        "x": 1.029,
        "y": 4.031,
        "z": -18.292
    },
    {
        "personId": "00051125",
        "name": "YAVUZ AKKAYNAK",
        "grid_filename": "grid_1.png",
        "x": 3.001,
        "y": 1.44,
        "z": -11.229
    },
    {
        "personId": "00087734",
        "name": "HAYRULLAH CİHAT TUTCUOĞLU",
        "grid_filename": "grid_1.png",
        "x": -2.778,
        "y": 0.37,
        "z": -14.447
    },
    {
        "personId": "00061134",
        "name": "SERAP OKÇU",
        "grid_filename": "grid_1.png",
        "x": 3.015,
        "y": 1.355,
        "z": -13.264
    },
    {
        "personId": "00053385",
        "name": "AŞKIN CANTİMUR",
        "grid_filename": "grid_1.png",
        "x": 2.358,
        "y": 0.133,
        "z": -18.222
    },
    {
        "personId": "00114978",
        "name": "SİNAN OTAĞ",
        "grid_filename": "grid_1.png",
        "x": 2.924,
        "y": 0.881,
        "z": -11.736
    },
    {
        "personId": "00112961",
        "name": "MACİD BOYAR",
        "grid_filename": "grid_1.png",
        "x": 0.566,
        "y": 4.041,
        "z": -20.963
    },
    {
        "personId": "00094478",
        "name": "MEHMET ALİ SÖYLET",
        "grid_filename": "grid_1.png",
        "x": 2.874,
        "y": 0.699,
        "z": -12.608
    },
    {
        "personId": "00052196",
        "name": "SÜLEYMAN ERSİN ÖZTOPAL",
        "grid_filename": "grid_1.png",
        "x": 2.988,
        "y": 1.537,
        "z": -12.101
    },
    {
        "personId": "00073663",
        "name": "OSMANNURİ USTABAŞ",
        "grid_filename": "grid_1.png",
        "x": -2.912,
        "y": 2.058,
        "z": -12.63
    },
    {
        "personId": "00098302",
        "name": "CABİR KARANFİL",
        "grid_filename": "grid_1.png",
        "x": 2.656,
        "y": 0.137,
        "z": -14.922
    },
    {
        "personId": "00058862",
        "name": "HANIFE HILAL DEMIRTAS",
        "grid_filename": "grid_1.png",
        "x": 2.882,
        "y": 0.79,
        "z": -16.262
    },
    {
        "personId": "00052435",
        "name": "SERHAT TÜMER",
        "grid_filename": "grid_1.png",
        "x": 2.922,
        "y": 0.886,
        "z": -12.971
    },
    {
        "personId": "00054202",
        "name": "AHMET İSMAİL GÜLLE",
        "grid_filename": "grid_1.png",
        "x": 2.777,
        "y": 0.325,
        "z": -13.561
    },
    {
        "personId": "00074223",
        "name": "AHMET EREN",
        "grid_filename": "grid_1.png",
        "x": -2.713,
        "y": 1.684,
        "z": -19.917
    },
    {
        "personId": "00063185",
        "name": "RAMAZAN BİNGÜL",
        "grid_filename": "grid_1.png",
        "x": 2.909,
        "y": 0.699,
        "z": -9.992
    },
    {
        "personId": "00061687",
        "name": "OĞUZCAN YERLİ",
        "grid_filename": "grid_1.png",
        "x": 3.015,
        "y": 1.352,
        "z": -13.481
    },
    {
        "personId": "00054634",
        "name": "AYHAN TAN",
        "grid_filename": "grid_1.png",
        "x": 2.8,
        "y": 0.418,
        "z": -14.572
    },
    {
        "personId": "123456789",
        "name": "BURAK HASAN GÜLTEMİZ",
        "grid_filename": "grid_1.png",
        "x": 2.353,
        "y": -0.238,
        "z": -15.606
    },
    {
        "personId": "00053200",
        "name": "ALİ İHSAN DİKBAŞ",
        "grid_filename": "grid_1.png",
        "x": 2.626,
        "y": 0.043,
        "z": -14.208
    },
    {
        "personId": "00054926",
        "name": "EROL ŞENOL",
        "grid_filename": "grid_1.png",
        "x": 1.8,
        "y": -0.053,
        "z": -20.551
    },
    {
        "personId": "00053214",
        "name": "MEHMET EKŞİ",
        "grid_filename": "grid_1.png",
        "x": 2.966,
        "y": 0.781,
        "z": -7.373
    },
    {
        "personId": "00110385",
        "name": "RIDVAN MERT YÜZSEVER",
        "grid_filename": "grid_1.png",
        "x": 0.28,
        "y": 4.146,
        "z": -19.378
    },
    {
        "personId": "00074999",
        "name": "TUĞBA CERRAH",
        "grid_filename": "grid_1.png",
        "x": -3.01,
        "y": 1.217,
        "z": -11.904
    },
    {
        "personId": "00070352",
        "name": "YASİN BEKAROĞLU",
        "grid_filename": "grid_1.png",
        "x": 2.236,
        "y": 3.219,
        "z": -8.173
    },
    {
        "personId": "00068460",
        "name": "AHMET MİTHAT ÇELEBİ",
        "grid_filename": "grid_1.png",
        "x": 2.753,
        "y": 0.233,
        "z": -13.627
    },
    {
        "personId": "00083993",
        "name": "ERKAY DEGERLI",
        "grid_filename": "grid_1.png",
        "x": -0.401,
        "y": 4.2,
        "z": -2.38
    },
    {
        "personId": "00059940",
        "name": "BURAK YILDIZ",
        "grid_filename": "grid_1.png",
        "x": 2.588,
        "y": 0.04,
        "z": -14.952
    },
    {
        "personId": "00054223",
        "name": "HALİS CUMHUR KILINÇ",
        "grid_filename": "grid_1.png",
        "x": 2.572,
        "y": 0.04,
        "z": -15.169
    },
    {
        "personId": "00074780",
        "name": "LEVENT KODAKOĞLU",
        "grid_filename": "grid_1.png",
        "x": 2.997,
        "y": 1.348,
        "z": -15.457
    },
    {
        "personId": "00080374",
        "name": "MELİH ÖZTÜRK",
        "grid_filename": "grid_1.png",
        "x": -1.428,
        "y": 3.906,
        "z": -5.65
    },
    {
        "personId": "00049773",
        "name": "ÖZLEM ÖZYÖN",
        "grid_filename": "grid_1.png",
        "x": 2.988,
        "y": 1.54,
        "z": -13.19
    },
    {
        "personId": "00098941",
        "name": "SERCAN SERT",
        "grid_filename": "grid_1.png",
        "x": 2.987,
        "y": 1.54,
        "z": -13.409
    },
    {
        "personId": "00100616",
        "name": "OKANAKTAŞ",
        "grid_filename": "grid_1.png",
        "x": 2.984,
        "y": 1.165,
        "z": -13.771
    },
    {
        "personId": "00075457",
        "name": "AYŞE TUBA BERK",
        "grid_filename": "grid_1.png",
        "x": 2.398,
        "y": -0.245,
        "z": -14.922
    },
    {
        "personId": "00102882",
        "name": "İBRAHİM HALİL TUNÇ",
        "grid_filename": "grid_1.png",
        "x": -2.914,
        "y": -1.33,
        "z": 3.738
    },
    {
        "personId": "00080786",
        "name": "BUĞRAHAN KARADEMİR",
        "grid_filename": "grid_1.png",
        "x": 2.652,
        "y": 0.131,
        "z": -14.922
    },
    {
        "personId": "00063345",
        "name": "MUHAMMED ZİYA ÖZTÜRK",
        "grid_filename": "grid_1.png",
        "x": 2.657,
        "y": -1.536,
        "z": 4.271
    },
    {
        "personId": "00060616",
        "name": "OKAN ÖKSÜZ",
        "grid_filename": "grid_1.png",
        "x": 3.013,
        "y": 1.355,
        "z": -13.918
    },
    {
        "personId": "00065998",
        "name": "ESER KARAMAN",
        "grid_filename": "grid_1.png",
        "x": 2.144,
        "y": 3.31,
        "z": -7.519
    },
    {
        "personId": "00094875",
        "name": "SERKANAYDIN",
        "grid_filename": "grid_1.png",
        "x": 2.696,
        "y": 0.693,
        "z": -18.732
    },
    {
        "personId": "00068755",
        "name": "SABRİ KARAKAŞ",
        "grid_filename": "grid_1.png",
        "x": 2.757,
        "y": 0.231,
        "z": -9.701
    },
    {
        "personId": "00071214",
        "name": "MEHMET EMİN TUFAN",
        "grid_filename": "grid_1.png",
        "x": -0.305,
        "y": 4.218,
        "z": -13.577
    },
    {
        "personId": "00075614",
        "name": "SEMİH KARTALOĞLU",
        "grid_filename": "grid_1.png",
        "x": 1.86,
        "y": 3.593,
        "z": -7.52
    },
    {
        "personId": "00068051",
        "name": "İZZET EMRE GÖL",
        "grid_filename": "grid_1.png",
        "x": 2.121,
        "y": -0.582,
        "z": -15.613
    },
    {
        "personId": "123456789",
        "name": "MUHAMMED MAHMUT ER",
        "grid_filename": "grid_1.png",
        "x": 2.694,
        "y": 0.041,
        "z": -10.21
    },
    {
        "personId": "00046053",
        "name": "ATİLLA COŞKUN",
        "grid_filename": "grid_1.png",
        "x": 2.797,
        "y": 0.418,
        "z": -14.922
    },
    {
        "personId": "00054960",
        "name": "ABDULLAH AYDIN",
        "grid_filename": "grid_1.png",
        "x": 2.767,
        "y": -1.34,
        "z": -2.114
    },
    {
        "personId": "00056441",
        "name": "ARİF AYAZ",
        "grid_filename": "grid_1.png",
        "x": -3.001,
        "y": 0.561,
        "z": -4.996
    },
    {
        "personId": "00052413",
        "name": "İPEK GÜRBÜZ TOKLİCAN",
        "grid_filename": "grid_1.png",
        "x": 2.882,
        "y": 0.788,
        "z": -16.551
    },
    {
        "personId": "00090619",
        "name": "EYYÜP ÖZKAYMAK",
        "grid_filename": "grid_1.png",
        "x": -2.376,
        "y": 3.084,
        "z": -11.54
    },
    {
        "personId": "00052789",
        "name": "REŞAT GÜNDÜZ",
        "grid_filename": "grid_1.png",
        "x": 2.326,
        "y": 3.125,
        "z": -3.667
    },
    {
        "personId": "00069339",
        "name": "MUHAMMET TAHA ÖZKAN",
        "grid_filename": "grid_1.png",
        "x": 1.109,
        "y": 4.059,
        "z": -0.467
    },
    {
        "personId": "00068521",
        "name": "RESUL ÇAKMAK",
        "grid_filename": "grid_1.png",
        "x": 2.805,
        "y": 0.324,
        "z": -9.557
    },
    {
        "personId": "00069768",
        "name": "KORAY ÖZÖNER",
        "grid_filename": "grid_1.png",
        "x": 1.107,
        "y": 4.062,
        "z": -9.992
    },
    {
        "personId": "00063193",
        "name": "BİLAL ÇELİK",
        "grid_filename": "grid_1.png",
        "x": 2.466,
        "y": -0.144,
        "z": -14.922
    },
    {
        "personId": "00057605",
        "name": "ABDULLAH BİNBİR",
        "grid_filename": "grid_1.png",
        "x": -2.62,
        "y": 2.709,
        "z": -2.815
    },
    {
        "personId": "00053419",
        "name": "EMRE ÇELİK",
        "grid_filename": "grid_1.png",
        "x": 2.686,
        "y": 0.321,
        "z": -16.623
    },
    {
        "personId": "00055408",
        "name": "AHMET ULUDAĞ",
        "grid_filename": "grid_1.png",
        "x": 2.975,
        "y": 1.165,
        "z": -14.427
    },
    {
        "personId": "00065617",
        "name": "MUHAMMET ENSAR KARABULUT",
        "grid_filename": "grid_1.png",
        "x": 2.441,
        "y": 3.032,
        "z": -14.79
    },
    {
        "personId": "00073571",
        "name": "AHMET HALİD KUTLUOĞLU",
        "grid_filename": "grid_1.png",
        "x": 2.847,
        "y": 0.606,
        "z": -14.425
    },
    {
        "personId": "00060617",
        "name": "HATİCE GİRGİN",
        "grid_filename": "grid_1.png",
        "x": 2.87,
        "y": 0.694,
        "z": -10.501
    },
    {
        "personId": "00057501",
        "name": "ZEYNEP TARTAN GÜÇEL",
        "grid_filename": "grid_1.png",
        "x": 1.201,
        "y": 4.026,
        "z": -2.795
    },
    {
        "personId": "00063474",
        "name": "ÖMER FARUK GÖK",
        "grid_filename": "grid_1.png",
        "x": 3.0,
        "y": 1.437,
        "z": -14.136
    },
    {
        "personId": "00083565",
        "name": "BANUHAN BERBEROĞLU TAŞAR",
        "grid_filename": "grid_1.png",
        "x": 2.654,
        "y": 0.134,
        "z": -14.922
    },
    {
        "personId": "00063015",
        "name": "TARIK PARLAK",
        "grid_filename": "grid_1.png",
        "x": 29.725,
        "y": 2.248,
        "z": -10.716
    },
    {
        "personId": "00076889",
        "name": "ALİ ARTUN TELLİ",
        "grid_filename": "grid_1.png",
        "x": 2.651,
        "y": 0.044,
        "z": -13.702
    },
    {
        "personId": "00065161",
        "name": "MİKAİL AKBULUT",
        "grid_filename": "grid_1.png",
        "x": 2.142,
        "y": 3.312,
        "z": -7.738
    },
    {
        "personId": "00089852",
        "name": "MURAT ATEŞ",
        "grid_filename": "grid_1.png",
        "x": 1.759,
        "y": 3.687,
        "z": 2.152
    },
    {
        "personId": "00053332",
        "name": "FİKRET KOÇ",
        "grid_filename": "grid_1.png",
        "x": 2.953,
        "y": 0.697,
        "z": -7.52
    },
    {
        "personId": "123456789",
        "name": "SİNANAY",
        "grid_filename": "grid_1.png",
        "x": 2.974,
        "y": 1.632,
        "z": -11.664
    },
    {
        "personId": "123456789",
        "name": "MUHAMMED CAHİT ŞİRİN",
        "grid_filename": "grid_1.png",
        "x": 2.694,
        "y": 0.041,
        "z": -10.21
    },
    {
        "personId": "00093864",
        "name": "KÜBRA FİLİKCİ",
        "grid_filename": "grid_1.png",
        "x": -1.895,
        "y": 3.554,
        "z": -4.052
    },
    {
        "personId": "00102094",
        "name": "SELDA KOÇAK",
        "grid_filename": "grid_1.png",
        "x": 2.991,
        "y": 1.162,
        "z": -13.19
    },
    {
        "personId": "00059725",
        "name": "HALİT ANLATAN",
        "grid_filename": "grid_1.png",
        "x": -2.542,
        "y": -0.281,
        "z": -10.518
    },
    {
        "personId": "00098944",
        "name": "AHMET EMRE KAVAK",
        "grid_filename": "grid_1.png",
        "x": 2.85,
        "y": 0.608,
        "z": -13.627
    },
    {
        "personId": "00086500",
        "name": "TUBA DEMİRTAŞ",
        "grid_filename": "grid_1.png",
        "x": 3.013,
        "y": 1.166,
        "z": -10.429
    },
    {
        "personId": "00051364",
        "name": "EMRE ŞEN",
        "grid_filename": "grid_1.png",
        "x": 2.442,
        "y": -0.05,
        "z": -16.187
    },
    {
        "personId": "00067755",
        "name": "MEHMET KIZILTAN",
        "grid_filename": "grid_1.png",
        "x": 2.702,
        "y": 0.04,
        "z": -12.465
    },
    {
        "personId": "00057427",
        "name": "CELAL BAYKAL",
        "grid_filename": "grid_1.png",
        "x": 2.796,
        "y": 0.414,
        "z": -14.922
    },
    {
        "personId": "123456789",
        "name": "MURAT YUŞAN",
        "grid_filename": "grid_1.png",
        "x": 2.949,
        "y": 1.072,
        "z": -14.79
    },
    {
        "personId": "00067036",
        "name": "ABDULLAH AKAT",
        "grid_filename": "grid_1.png",
        "x": 2.173,
        "y": 0.228,
        "z": -19.749
    },
    {
        "personId": "00064434",
        "name": "SELÇUK ÇELEBI",
        "grid_filename": "grid_1.png",
        "x": 2.972,
        "y": 1.634,
        "z": -13.99
    },
    {
        "personId": "00048474",
        "name": "MEHMET BAYER",
        "grid_filename": "grid_1.png",
        "x": 2.478,
        "y": -0.235,
        "z": -13.409
    },
    {
        "personId": "00064254",
        "name": "AYNUR AŞKIN",
        "grid_filename": "grid_1.png",
        "x": 2.776,
        "y": 0.325,
        "z": -14.718
    },
    {
        "personId": "00052389",
        "name": "METIN BEKIL",
        "grid_filename": "grid_1.png",
        "x": -0.868,
        "y": 4.106,
        "z": 1.619
    },
    {
        "personId": "00069089",
        "name": "ABDULLAH ÖMER ÇELİK",
        "grid_filename": "grid_1.png",
        "x": -0.489,
        "y": 4.179,
        "z": -14.303
    },
    {
        "personId": "00074868",
        "name": "EKREM RODOPLU",
        "grid_filename": "grid_1.png",
        "x": 2.861,
        "y": 0.696,
        "z": -15.824
    },
    {
        "personId": "00057437",
        "name": "HASAN MALİK AYDINER",
        "grid_filename": "grid_1.png",
        "x": 2.846,
        "y": 0.605,
        "z": -10.646
    },
    {
        "personId": "00064656",
        "name": "ÖZER GÜLER",
        "grid_filename": "grid_1.png",
        "x": 2.331,
        "y": 3.125,
        "z": -8.245
    },
    {
        "personId": "00051126",
        "name": "AHMET KULA",
        "grid_filename": "grid_1.png",
        "x": 2.776,
        "y": 0.324,
        "z": -14.355
    },
    {
        "personId": "00054116",
        "name": "ENGİNAKBAŞ",
        "grid_filename": "grid_1.png",
        "x": 2.536,
        "y": 0.042,
        "z": -15.678
    },
    {
        "personId": "00069819",
        "name": "İBRAHİM HAKKI GÜNTAY",
        "grid_filename": "grid_1.png",
        "x": 2.849,
        "y": 0.605,
        "z": -11.373
    },
    {
        "personId": "00058255",
        "name": "SEDAT EŞGİ",
        "grid_filename": "grid_1.png",
        "x": 2.057,
        "y": 3.406,
        "z": -14.644
    },
    {
        "personId": "00066867",
        "name": "TARIK ZİYA GÜRLER",
        "grid_filename": "grid_1.png",
        "x": 3.022,
        "y": 1.259,
        "z": -11.59
    },
    {
        "personId": "00083143",
        "name": "GÖKHAN DÖRTKOL",
        "grid_filename": "grid_1.png",
        "x": 2.582,
        "y": -0.235,
        "z": -10.501
    },
    {
        "personId": "123456789",
        "name": "ENGİN KARACAN",
        "grid_filename": "grid_1.png",
        "x": -1.148,
        "y": 4.055,
        "z": -10.813
    },
    {
        "personId": "00105456",
        "name": "OKTAY ALTINDİŞ",
        "grid_filename": "grid_1.png",
        "x": -1.789,
        "y": 3.651,
        "z": -16.643
    },
    {
        "personId": "00100480",
        "name": "FATİH ŞİRİN",
        "grid_filename": "grid_1.png",
        "x": 2.749,
        "y": 0.231,
        "z": -11.448
    },
    {
        "personId": "00067375",
        "name": "DENİZ DAŞTAN",
        "grid_filename": "grid_1.png",
        "x": 2.552,
        "y": 0.042,
        "z": -15.46
    },
    {
        "personId": "00073477",
        "name": "ERSEL ÇAĞATAY SAVCI",
        "grid_filename": "grid_1.png",
        "x": 2.318,
        "y": 0.599,
        "z": -20.474
    },
    {
        "personId": "00087268",
        "name": "ANIL MERCAN",
        "grid_filename": "grid_1.png",
        "x": 2.722,
        "y": 0.231,
        "z": -14.864
    },
    {
        "personId": "00045416",
        "name": "EMEL BİRYILMAZ",
        "grid_filename": "grid_1.png",
        "x": 2.361,
        "y": -0.145,
        "z": -16.403
    },
    {
        "personId": "00057576",
        "name": "AHMET COSKUN",
        "grid_filename": "grid_1.png",
        "x": -2.875,
        "y": 2.067,
        "z": -17.082
    },
    {
        "personId": "00051436",
        "name": "TOLGAHANAKBAŞ",
        "grid_filename": "grid_1.png",
        "x": 2.948,
        "y": 0.98,
        "z": -12.318
    },
    {
        "personId": "00068246",
        "name": "MEHMET CAN TAŞCI",
        "grid_filename": "grid_1.png",
        "x": -0.77,
        "y": 4.129,
        "z": -7.542
    },
    {
        "personId": "00051609",
        "name": "IBRAHIM SEDQI",
        "grid_filename": "grid_1.png",
        "x": -1.048,
        "y": 4.053,
        "z": -16.935
    },
    {
        "personId": "00052294",
        "name": "SERHAT GÖK",
        "grid_filename": "grid_1.png",
        "x": 2.971,
        "y": 1.072,
        "z": -12.536
    },
    {
        "personId": "00060754",
        "name": "MEHMET DENİZ AYBEY",
        "grid_filename": "grid_1.png",
        "x": 2.826,
        "y": 0.511,
        "z": -12.608
    },
    {
        "personId": "00053712",
        "name": "GÖKHAN ÇİFCİ",
        "grid_filename": "grid_1.png",
        "x": -3.02,
        "y": 1.217,
        "z": -8.851
    },
    {
        "personId": "00045398",
        "name": "KAĞAN TARANCI",
        "grid_filename": "grid_1.png",
        "x": 2.883,
        "y": 0.791,
        "z": -15.46
    },
    {
        "personId": "00063143",
        "name": "ÖMER ÜNSAL OKÇU",
        "grid_filename": "grid_1.png",
        "x": 2.703,
        "y": 0.227,
        "z": -15.097
    },
    {
        "personId": "123456789",
        "name": "HÜSEYİN ÇELİK",
        "grid_filename": "grid_1.png",
        "x": 2.932,
        "y": 1.069,
        "z": -16.404
    },
    {
        "personId": "00085909",
        "name": "TÜLİN YILMAZ",
        "grid_filename": "grid_1.png",
        "x": 2.973,
        "y": 1.072,
        "z": -10.864
    },
    {
        "personId": "00069823",
        "name": "FATİH MEHMET KURŞUN",
        "grid_filename": "grid_1.png",
        "x": 2.826,
        "y": 0.509,
        "z": -12.392
    },
    {
        "personId": "00080837",
        "name": "ÖMER MESUT ÖZEN",
        "grid_filename": "grid_1.png",
        "x": 1.673,
        "y": 3.777,
        "z": -7.956
    },
    {
        "personId": "00060200",
        "name": "MEHMET EMİN İŞBİLEN",
        "grid_filename": "grid_1.png",
        "x": 2.8,
        "y": 0.415,
        "z": -13.409
    },
    {
        "personId": "00059982",
        "name": "SELAHATTİN EYÜP ÖZBAY",
        "grid_filename": "grid_1.png",
        "x": 1.764,
        "y": 3.684,
        "z": -1.123
    },
    {
        "personId": "00110404",
        "name": "KEMAL İBİŞ",
        "grid_filename": "grid_1.png",
        "x": 2.752,
        "y": 0.23,
        "z": -14.062
    },
    {
        "personId": "00058385",
        "name": "HÜSEYİN YÜKSEK",
        "grid_filename": "grid_1.png",
        "x": 2.946,
        "y": 1.066,
        "z": -15.75
    },
    {
        "personId": "00085337",
        "name": "NECMEDDİN ESAT BELEN",
        "grid_filename": "grid_1.png",
        "x": 2.861,
        "y": 0.696,
        "z": -15.679
    },
    {
        "personId": "00057224",
        "name": "DİLEK DANIŞMAN",
        "grid_filename": "grid_1.png",
        "x": 1.872,
        "y": 3.119,
        "z": -22.658
    },
    {
        "personId": "00046599",
        "name": "EMİNE BANU EKERİM",
        "grid_filename": "grid_1.png",
        "x": 2.958,
        "y": 1.721,
        "z": -8.758
    },
    {
        "personId": "00051089",
        "name": "HAYRULLAH TÜRHAN",
        "grid_filename": "grid_1.png",
        "x": -2.823,
        "y": 0.566,
        "z": -15.99
    },
    {
        "personId": "00085958",
        "name": "ZEKERİYA DEMİR",
        "grid_filename": "grid_1.png",
        "x": 3.013,
        "y": 1.352,
        "z": -9.554
    },
    {
        "personId": "00075466",
        "name": "TUBA NUR YAZICI",
        "grid_filename": "grid_1.png",
        "x": 2.969,
        "y": 0.98,
        "z": -10.499
    },
    {
        "personId": "00077578",
        "name": "HİLYE BANU DEĞERLİ",
        "grid_filename": "grid_1.png",
        "x": -2.768,
        "y": 2.433,
        "z": -14.812
    },
    {
        "personId": "00120293",
        "name": "MEHMET KARAKAŞ",
        "grid_filename": "grid_1.png",
        "x": 2.874,
        "y": 0.699,
        "z": -13.192
    },
    {
        "personId": "00113038",
        "name": "HAYRİ CAN DUYGUN",
        "grid_filename": "grid_1.png",
        "x": 2.882,
        "y": 0.788,
        "z": -15.825
    },
    {
        "personId": "00064874",
        "name": "SAMİ AYDOGAN",
        "grid_filename": "grid_1.png",
        "x": 3.022,
        "y": 1.259,
        "z": -6.21
    },
    {
        "personId": "00069450",
        "name": "FATİH BOZKURT",
        "grid_filename": "grid_1.png",
        "x": 2.531,
        "y": -0.236,
        "z": -11.955
    },
    {
        "personId": "00051940",
        "name": "EDA OCAK",
        "grid_filename": "grid_1.png",
        "x": 1.947,
        "y": 3.501,
        "z": -1.848
    },
    {
        "personId": "00068981",
        "name": "ALİ ÇOLAK",
        "grid_filename": "grid_1.png",
        "x": -3.037,
        "y": 0.388,
        "z": 3.175
    },
    {
        "personId": "00058831",
        "name": "ŞEVKİ BAŞ",
        "grid_filename": "grid_1.png",
        "x": -2.839,
        "y": 2.251,
        "z": -2.231
    },
    {
        "personId": "00074864",
        "name": "RAMAZAN YAŞA",
        "grid_filename": "grid_1.png",
        "x": 2.901,
        "y": 0.606,
        "z": -9.557
    },
    {
        "personId": "00104636",
        "name": "FİLİZ SEMERCİ",
        "grid_filename": "grid_1.png",
        "x": 2.851,
        "y": 0.605,
        "z": -12.174
    },
    {
        "personId": "00074202",
        "name": "SELÇUK İBRAHİMOĞLU",
        "grid_filename": "grid_1.png",
        "x": 3.016,
        "y": 1.261,
        "z": -13.046
    },
    {
        "personId": "00101062",
        "name": "ALI IHSAN ÖZEK",
        "grid_filename": "grid_1.png",
        "x": 2.798,
        "y": 0.418,
        "z": -14.79
    },
    {
        "personId": "00068652",
        "name": "YUSUF ZİYA İSKENDER",
        "grid_filename": "grid_1.png",
        "x": 2.985,
        "y": 1.543,
        "z": -9.627
    },
    {
        "personId": "00064972",
        "name": "AHMET NUMAN CEBECİ",
        "grid_filename": "grid_1.png",
        "x": -2.921,
        "y": 1.964,
        "z": -7.034
    },
    {
        "personId": "00061123",
        "name": "MUHAMMET BURAK ÖZTÜRK",
        "grid_filename": "grid_1.png",
        "x": 2.454,
        "y": -0.144,
        "z": -15.096
    },
    {
        "personId": "00058926",
        "name": "MUSTAFA ABACI",
        "grid_filename": "grid_1.png",
        "x": 2.927,
        "y": 0.978,
        "z": -14.864
    },
    {
        "personId": "00049845",
        "name": "KAZIM ÜNLÜ",
        "grid_filename": "grid_1.png",
        "x": -2.812,
        "y": 2.337,
        "z": -13.212
    },
    {
        "personId": "00057990",
        "name": "AHMET ESAT HIZIR",
        "grid_filename": "grid_1.png",
        "x": -2.995,
        "y": 1.029,
        "z": 2.202
    },
    {
        "personId": "00080838",
        "name": "AYTEKİN SERBEST",
        "grid_filename": "grid_1.png",
        "x": 2.547,
        "y": -0.048,
        "z": -14.572
    },
    {
        "personId": "00065587",
        "name": "AYŞEGÜL AYDINLIK",
        "grid_filename": "grid_1.png",
        "x": 2.515,
        "y": 2.747,
        "z": -18.514
    },
    {
        "personId": "00073493",
        "name": "RIZA ÖNER",
        "grid_filename": "grid_1.png",
        "x": 2.984,
        "y": 0.883,
        "z": -2.865
    },
    {
        "personId": "00063320",
        "name": "ÖMER ASLAN",
        "grid_filename": "grid_1.png",
        "x": 2.332,
        "y": 3.123,
        "z": -7.809
    },
    {
        "personId": "00057668",
        "name": "MEHMET MELİK KARAKAŞ",
        "grid_filename": "grid_1.png",
        "x": 0.641,
        "y": 4.154,
        "z": -7.52
    },
    {
        "personId": "00070062",
        "name": "MUHAMMET YAZICI",
        "grid_filename": "grid_1.png",
        "x": -1.237,
        "y": 4.008,
        "z": -7.106
    },
    {
        "personId": "00054126",
        "name": "BERNA SALİHOĞLU",
        "grid_filename": "grid_1.png",
        "x": 2.739,
        "y": 0.231,
        "z": -14.5
    },
    {
        "personId": "00065802",
        "name": "ÖMER FARUK ALİER",
        "grid_filename": "grid_1.png",
        "x": -2.361,
        "y": 3.09,
        "z": -3.834
    },
    {
        "personId": "00063147",
        "name": "FATİH GÜVER",
        "grid_filename": "grid_1.png",
        "x": 2.728,
        "y": 0.14,
        "z": -12.173
    },
    {
        "personId": "00053408",
        "name": "FERDİ ÖZBÜYÜKYÖRÜK",
        "grid_filename": "grid_1.png",
        "x": 2.538,
        "y": -0.236,
        "z": -11.737
    },
    {
        "personId": "00068515",
        "name": "ŞEFİKA ARSLAN BOZ",
        "grid_filename": "grid_1.png",
        "x": 2.97,
        "y": 1.071,
        "z": -13.192
    },
    {
        "personId": "00067251",
        "name": "ARİFE ÖZTÜRK",
        "grid_filename": "grid_1.png",
        "x": 2.803,
        "y": 0.691,
        "z": -17.86
    },
    {
        "personId": "00087332",
        "name": "MEHMET SADIK KARAKUŞ",
        "grid_filename": "grid_1.png",
        "x": 2.85,
        "y": 0.606,
        "z": -13.264
    },
    {
        "personId": "00077469",
        "name": "MUSTAFA ÇALIŞKAN",
        "grid_filename": "grid_1.png",
        "x": 2.362,
        "y": -0.614,
        "z": -10.063
    },
    {
        "personId": "00063318",
        "name": "NEVZAT ERDEMİR",
        "grid_filename": "grid_1.png",
        "x": 2.989,
        "y": 0.783,
        "z": -1.557
    },
    {
        "personId": "00058563",
        "name": "KAMİL GÖKAL",
        "grid_filename": "grid_1.png",
        "x": 2.904,
        "y": 0.884,
        "z": -15.096
    },
    {
        "personId": "00063985",
        "name": "ÖMER FARUK ULU",
        "grid_filename": "grid_1.png",
        "x": 2.986,
        "y": 1.54,
        "z": -13.699
    },
    {
        "personId": "00083636",
        "name": "EMRE DEMİRHAN",
        "grid_filename": "grid_1.png",
        "x": 2.704,
        "y": 0.324,
        "z": -16.334
    },
    {
        "personId": "00069771",
        "name": "BETÜL AKDOĞAN",
        "grid_filename": "grid_1.png",
        "x": 2.48,
        "y": -0.142,
        "z": -14.646
    },
    {
        "personId": "00054246",
        "name": "ELİF ÖZSOY",
        "grid_filename": "grid_1.png",
        "x": 2.528,
        "y": 0.042,
        "z": -15.822
    },
    {
        "personId": "00065731",
        "name": "NUMAN ÇİZMECİOĞLU",
        "grid_filename": "grid_1.png",
        "x": 2.964,
        "y": 1.075,
        "z": -13.772
    },
    {
        "personId": "00053722",
        "name": "YAVUZ BARBAROS ULUSOY",
        "grid_filename": "grid_1.png",
        "x": 2.998,
        "y": 1.166,
        "z": -11.083
    },
    {
        "personId": "00063738",
        "name": "ÖMER ÖNDER HABERDAR",
        "grid_filename": "grid_1.png",
        "x": 2.959,
        "y": 1.726,
        "z": -13.627
    },
    {
        "personId": "00047077",
        "name": "MUSTAFA KARAKAŞ",
        "grid_filename": "grid_1.png",
        "x": 2.983,
        "y": 1.535,
        "z": -14.922
    },
    {
        "personId": "00121428",
        "name": "ÖZLEM İNANÇ",
        "grid_filename": "grid_1.png",
        "x": 0.172,
        "y": 4.245,
        "z": -1.632
    },
    {
        "personId": "00079845",
        "name": "GÖKHAN ÖZBEY",
        "grid_filename": "grid_1.png",
        "x": 1.482,
        "y": 3.877,
        "z": -4.177
    },
    {
        "personId": "00069084",
        "name": "OĞUZHAN CERRAH",
        "grid_filename": "grid_1.png",
        "x": 2.973,
        "y": 1.632,
        "z": -13.481
    },
    {
        "personId": "00064886",
        "name": "ALİ TİPİ",
        "grid_filename": "grid_1.png",
        "x": 2.839,
        "y": 0.602,
        "z": -14.922
    },
    {
        "personId": "00063570",
        "name": "NASRULLAH ERULUSOY",
        "grid_filename": "grid_1.png",
        "x": 2.289,
        "y": -1.8,
        "z": 4.051
    },
    {
        "personId": "00059382",
        "name": "MURAT GÜR",
        "grid_filename": "grid_1.png",
        "x": 2.567,
        "y": -1.625,
        "z": 4.053
    },
    {
        "personId": "00048765",
        "name": "RASİM KUZGUNLU",
        "grid_filename": "grid_1.png",
        "x": 2.836,
        "y": 0.421,
        "z": -9.629
    },
    {
        "personId": "00042015",
        "name": "ABDULAZIZ SALIM ABDULLAH BA MOHAMMED",
        "grid_filename": "grid_1.png",
        "x": -2.988,
        "y": 1.49,
        "z": -4.193
    },
    {
        "personId": "00020138",
        "name": "ŞEKİB AVDAGİÇ",
        "grid_filename": "grid_1.png",
        "x": 2.99,
        "y": 1.168,
        "z": -13.408
    },
    {
        "personId": "00069927",
        "name": "KENAN İNCE",
        "grid_filename": "grid_1.png",
        "x": 2.903,
        "y": 0.881,
        "z": -15.462
    },
    {
        "personId": "00073302",
        "name": "TUĞBA KOÇ",
        "grid_filename": "grid_1.png",
        "x": -2.996,
        "y": 1.03,
        "z": 0.094
    },
    {
        "personId": "00073329",
        "name": "MEHMED EKREM ERGİN",
        "grid_filename": "grid_1.png",
        "x": 2.697,
        "y": 0.046,
        "z": -12.753
    },
    {
        "personId": "00067695",
        "name": "MUHAMMED OSMAN BAYRAK",
        "grid_filename": "grid_1.png",
        "x": -1.934,
        "y": 0.004,
        "z": -20.135
    },
    {
        "personId": "00068250",
        "name": "ERHAN ŞENEL",
        "grid_filename": "grid_1.png",
        "x": 2.645,
        "y": 0.225,
        "z": -16.113
    },
    {
        "personId": "00053225",
        "name": "CENGİZ İNCEOSMAN",
        "grid_filename": "grid_1.png",
        "x": 2.945,
        "y": 0.509,
        "z": -6.649
    },
    {
        "personId": "123456789",
        "name": "TAHA AKÇAKAYA",
        "grid_filename": "grid_1.png",
        "x": 2.668,
        "y": 1.626,
        "z": -20.33
    },
    {
        "personId": "00051365",
        "name": "ERSİN DEMİR",
        "grid_filename": "grid_1.png",
        "x": 2.408,
        "y": 0.696,
        "z": -20.404
    },
    {
        "personId": "00046557",
        "name": "VEDAT ÖZSABUNCU",
        "grid_filename": "grid_1.png",
        "x": 1.95,
        "y": 3.502,
        "z": -5.847
    },
    {
        "personId": "00066599",
        "name": "EMİNE AHMETOĞLU HAKBİLEN",
        "grid_filename": "grid_1.png",
        "x": 2.86,
        "y": 0.694,
        "z": -16.116
    },
    {
        "personId": "00047828",
        "name": "YELİZ DUYURAN",
        "grid_filename": "grid_1.png",
        "x": 2.948,
        "y": 1.534,
        "z": -17.423
    },
    {
        "personId": "00110382",
        "name": "İSMAİL BENLİ",
        "grid_filename": "grid_1.png",
        "x": 0.36,
        "y": 4.21,
        "z": -12.753
    },
    {
        "personId": "123456789",
        "name": "EMRE ÇEVİK",
        "grid_filename": "grid_1.png",
        "x": 2.627,
        "y": 0.228,
        "z": -16.479
    },
    {
        "personId": "00074311",
        "name": "İREM KUYAN",
        "grid_filename": "grid_1.png",
        "x": 10.536,
        "y": -0.163,
        "z": 0.963
    },
    {
        "personId": "00068052",
        "name": "CEMİL ÇİLOĞLU",
        "grid_filename": "grid_1.png",
        "x": -2.23,
        "y": 3.185,
        "z": -18.1
    },
    {
        "personId": "00053159",
        "name": "LEVENT KONUKCU",
        "grid_filename": "grid_1.png",
        "x": 2.967,
        "y": 1.16,
        "z": -15.532
    },
    {
        "personId": "00120870",
        "name": "CEMAL KAYA",
        "grid_filename": "grid_1.png",
        "x": 2.529,
        "y": -0.051,
        "z": -14.922
    },
    {
        "personId": "00051906",
        "name": "MEHMET YILDIRIM",
        "grid_filename": "grid_1.png",
        "x": -2.734,
        "y": 0.191,
        "z": -12.922
    },
    {
        "personId": "00062098",
        "name": "BİRSEL DÖRTELMA",
        "grid_filename": "grid_1.png",
        "x": 10.777,
        "y": -2.041,
        "z": 7.854
    },
    {
        "personId": "00098829",
        "name": "HÜSEYİN KÜÇÜK",
        "grid_filename": "grid_1.png",
        "x": -0.893,
        "y": 4.011,
        "z": -20.198
    },
    {
        "personId": "00063044",
        "name": "DİNÇER EROĞLU",
        "grid_filename": "grid_1.png",
        "x": 2.94,
        "y": 0.602,
        "z": -7.229
    },
    {
        "personId": "00059350",
        "name": "SERKAN KANDEMİR",
        "grid_filename": "grid_1.png",
        "x": -0.956,
        "y": 4.092,
        "z": -7.978
    },
    {
        "personId": "00052883",
        "name": "BANU KURT",
        "grid_filename": "grid_1.png",
        "x": 2.718,
        "y": 0.23,
        "z": -14.922
    },
    {
        "personId": "00065126",
        "name": "BİLAL ARPACI",
        "grid_filename": "grid_1.png",
        "x": 2.613,
        "y": 0.044,
        "z": -14.5
    },
    {
        "personId": "00067771",
        "name": "ALİ TÜRK",
        "grid_filename": "grid_1.png",
        "x": -1.511,
        "y": 3.846,
        "z": -17.298
    },
    {
        "personId": "00056393",
        "name": "TAHİR UYANIR",
        "grid_filename": "grid_1.png",
        "x": -2.84,
        "y": 2.246,
        "z": -1.434
    },
    {
        "personId": "00700023",
        "name": "ERCAN DEMİRTAŞ",
        "grid_filename": "grid_1.png",
        "x": 2.315,
        "y": 0.039,
        "z": -18.079
    },
    {
        "personId": "00055187",
        "name": "MEHMET FATİH AYGÜNER",
        "grid_filename": "grid_1.png",
        "x": 2.777,
        "y": 0.324,
        "z": -12.755
    },
    {
        "personId": "00086839",
        "name": "İBRAHİM TUNÇ",
        "grid_filename": "grid_1.png",
        "x": 2.332,
        "y": 3.123,
        "z": -8.028
    },
    {
        "personId": "00076885",
        "name": "ERTAN TENGİZ",
        "grid_filename": "grid_1.png",
        "x": 2.953,
        "y": 0.508,
        "z": -6.431
    },
    {
        "personId": "00068462",
        "name": "TAHA SELMAN YEĞENLER",
        "grid_filename": "grid_1.png",
        "x": -2.85,
        "y": 2.239,
        "z": -7.614
    },
    {
        "personId": "00069377",
        "name": "ARİF ŞENGÖR",
        "grid_filename": "grid_1.png",
        "x": 1.573,
        "y": 3.826,
        "z": -0.322
    },
    {
        "personId": "00088095",
        "name": "SELİM YUMURTACI",
        "grid_filename": "grid_1.png",
        "x": 1.387,
        "y": 3.928,
        "z": -5.338
    },
    {
        "personId": "00061462",
        "name": "EMİR ALİ GÖZE",
        "grid_filename": "grid_1.png",
        "x": 2.987,
        "y": 0.974,
        "z": -9.629
    },
    {
        "personId": "00106852",
        "name": "ISMET EVREN KARATEPE",
        "grid_filename": "grid_1.png",
        "x": 2.972,
        "y": 1.535,
        "z": -15.896
    },
    {
        "personId": "00047091",
        "name": "FİLİZ TUĞÇAY",
        "grid_filename": "grid_1.png",
        "x": 3.011,
        "y": 1.35,
        "z": -7.664
    },
    {
        "personId": "00061823",
        "name": "MEHMET KEREM KIZILTUNÇ",
        "grid_filename": "grid_1.png",
        "x": 2.925,
        "y": 0.974,
        "z": -15.169
    },
    {
        "personId": "00067658",
        "name": "NİHAT ÇEVİK",
        "grid_filename": "grid_1.png",
        "x": 2.608,
        "y": 0.408,
        "z": -17.932
    },
    {
        "personId": "00105313",
        "name": "AHMET KORAY ERGÜN",
        "grid_filename": "grid_1.png",
        "x": 2.562,
        "y": 2.845,
        "z": -10.357
    },
    {
        "personId": "123456789",
        "name": "TAHA ÇAKMAK",
        "grid_filename": "grid_1.png",
        "x": 2.742,
        "y": 0.225,
        "z": -10.066
    },
    {
        "personId": "00060945",
        "name": "HASAN SERKAN BİNYAR",
        "grid_filename": "grid_1.png",
        "x": 3.003,
        "y": 1.438,
        "z": -12.903
    },
    {
        "personId": "00072760",
        "name": "ECE BAŞ",
        "grid_filename": "grid_1.png",
        "x": 2.995,
        "y": 0.974,
        "z": -6.212
    },
    {
        "personId": "00072998",
        "name": "MUSTAFA KEMAL ÖZAHİ",
        "grid_filename": "grid_1.png",
        "x": 2.997,
        "y": 1.44,
        "z": -14.922
    },
    {
        "personId": "00088447",
        "name": "BURHAN GÜNGÖR",
        "grid_filename": "grid_1.png",
        "x": 2.776,
        "y": 2.378,
        "z": 0.042
    },
    {
        "personId": "00063740",
        "name": "UBEYDULLAH CAN",
        "grid_filename": "grid_1.png",
        "x": 2.561,
        "y": 2.844,
        "z": -8.028
    },
    {
        "personId": "00053161",
        "name": "EROL KURU",
        "grid_filename": "grid_1.png",
        "x": 2.976,
        "y": 0.883,
        "z": -8.829
    },
    {
        "personId": "00080793",
        "name": "GÖKHAN TAŞAR",
        "grid_filename": "grid_1.png",
        "x": 2.637,
        "y": -0.144,
        "z": -10.717
    },
    {
        "personId": "00092099",
        "name": "ERSİN DENİZ",
        "grid_filename": "grid_1.png",
        "x": -2.579,
        "y": 1.499,
        "z": -20.789
    },
    {
        "personId": "00083474",
        "name": "MEHMET YANMAZ",
        "grid_filename": "grid_1.png",
        "x": -0.212,
        "y": 4.237,
        "z": 0.893
    },
    {
        "personId": "00063338",
        "name": "GÖKHAN ÇETİN",
        "grid_filename": "grid_1.png",
        "x": 2.422,
        "y": 3.034,
        "z": -7.884
    },
    {
        "personId": "00075881",
        "name": "BİLAL KARAMAN",
        "grid_filename": "grid_1.png",
        "x": 2.403,
        "y": -0.238,
        "z": -14.922
    },
    {
        "personId": "00074946",
        "name": "İBRAHİM ORHANLI",
        "grid_filename": "grid_1.png",
        "x": 2.951,
        "y": 1.162,
        "z": -16.187
    },
    {
        "personId": "00046043",
        "name": "ŞULE YILMAZ",
        "grid_filename": "grid_1.png",
        "x": 2.995,
        "y": 1.164,
        "z": -12.318
    },
    {
        "personId": "00122169",
        "name": "YUNUS YILDIZ",
        "grid_filename": "grid_1.png",
        "x": 2.653,
        "y": 0.133,
        "z": -14.922
    },
    {
        "personId": "123456789",
        "name": "UĞUR UYAN",
        "grid_filename": "grid_1.png",
        "x": 2.838,
        "y": 0.512,
        "z": -9.991
    },
    {
        "personId": "00098698",
        "name": "GÖKHAN KARAHAN",
        "grid_filename": "grid_1.png",
        "x": 2.67,
        "y": -0.051,
        "z": -10.646
    },
    {
        "personId": "00064974",
        "name": "KEMAL AKIN ÖZYAKA",
        "grid_filename": "grid_1.png",
        "x": 2.424,
        "y": 3.032,
        "z": -8.319
    },
    {
        "personId": "00066531",
        "name": "AYŞE ALTAN",
        "grid_filename": "grid_1.png",
        "x": 2.465,
        "y": -0.145,
        "z": -14.922
    },
    {
        "personId": "00069802",
        "name": "AHMET FARUK ŞAHİNER",
        "grid_filename": "grid_1.png",
        "x": 2.994,
        "y": 1.35,
        "z": -15.604
    },
    {
        "personId": "00089609",
        "name": "YÜCEL DEMİRCİ",
        "grid_filename": "grid_1.png",
        "x": 3.014,
        "y": 1.355,
        "z": -11.083
    },
    {
        "personId": "00061125",
        "name": "HİLMİ BURCU",
        "grid_filename": "grid_1.png",
        "x": 2.516,
        "y": 2.938,
        "z": -7.52
    },
    {
        "personId": "00058221",
        "name": "ÖMER FARUK KILIÇ",
        "grid_filename": "grid_1.png",
        "x": 2.01,
        "y": -0.242,
        "z": -18.658
    },
    {
        "personId": "00075370",
        "name": "ESRA FINDIK",
        "grid_filename": "grid_1.png",
        "x": 2.216,
        "y": 0.509,
        "z": -20.623
    },
    {
        "personId": "00072085",
        "name": "SEYFULLAH İLYAS",
        "grid_filename": "grid_1.png",
        "x": -1.996,
        "y": 3.464,
        "z": -12.048
    },
    {
        "personId": "00073646",
        "name": "CİHANGİR GÜN",
        "grid_filename": "grid_1.png",
        "x": 1.763,
        "y": 3.689,
        "z": -7.447
    },
    {
        "personId": "00044442",
        "name": "SERKAN ÖZBÜYÜKYÖRÜK",
        "grid_filename": "grid_1.png",
        "x": 2.946,
        "y": 0.978,
        "z": -12.828
    },
    {
        "personId": "00053723",
        "name": "İSMAİL USTAOĞLU",
        "grid_filename": "grid_1.png",
        "x": 2.973,
        "y": 1.537,
        "z": -15.75
    },
    {
        "personId": "00064261",
        "name": "ÖMER SAKA",
        "grid_filename": "grid_1.png",
        "x": -1.425,
        "y": 3.732,
        "z": -21.006
    },
    {
        "personId": "00063750",
        "name": "EMRAH ÇAĞLAR DELEN",
        "grid_filename": "grid_1.png",
        "x": 2.601,
        "y": 0.137,
        "z": -15.751
    },
    {
        "personId": "00079896",
        "name": "ABDULKERİM ÇAY",
        "grid_filename": "grid_1.png",
        "x": 2.304,
        "y": 0.415,
        "z": -19.823
    },
    {
        "personId": "00069898",
        "name": "BERKANT KOLCU",
        "grid_filename": "grid_1.png",
        "x": 2.528,
        "y": -0.052,
        "z": -14.922
    },
    {
        "personId": "00051183",
        "name": "TANER ERİM",
        "grid_filename": "grid_1.png",
        "x": -2.658,
        "y": 0.566,
        "z": -18.244
    },
    {
        "personId": "00054158",
        "name": "UĞUR CANTİMUR",
        "grid_filename": "grid_1.png",
        "x": 2.875,
        "y": 1.441,
        "z": -18.223
    },
    {
        "personId": "00075459",
        "name": "ÖMER KEREM BEKTEŞ",
        "grid_filename": "grid_1.png",
        "x": 2.971,
        "y": 1.634,
        "z": -14.283
    },
    {
        "personId": "00051672",
        "name": "FIRAT KİRİŞ",
        "grid_filename": "grid_1.png",
        "x": 2.802,
        "y": 0.416,
        "z": -12.392
    },
    {
        "personId": "00104825",
        "name": "ÖZEN ÖZER",
        "grid_filename": "grid_1.png",
        "x": 2.969,
        "y": 1.068,
        "z": -12.903
    },
    {
        "personId": "00082725",
        "name": "MÜNİR BEYAZAL",
        "grid_filename": "grid_1.png",
        "x": 2.005,
        "y": -1.87,
        "z": 4.269
    },
    {
        "personId": "00080216",
        "name": "MUHAMMED ALİ YAPAR",
        "grid_filename": "grid_1.png",
        "x": 2.572,
        "y": -1.635,
        "z": 3.835
    },
    {
        "personId": "00051092",
        "name": "YÜCEL BAŞYİĞİT",
        "grid_filename": "grid_1.png",
        "x": 2.986,
        "y": 1.543,
        "z": -10.501
    },
    {
        "personId": "00070369",
        "name": "AHMET AKBULUT",
        "grid_filename": "grid_1.png",
        "x": 3.129,
        "y": 0.081,
        "z": 0.608
    },
    {
        "personId": "00069246",
        "name": "MUTTALİP İLHAN",
        "grid_filename": "grid_1.png",
        "x": 2.143,
        "y": 3.312,
        "z": -7.953
    },
    {
        "personId": "00057757",
        "name": "MEHMET CÜNEYD DOĞRUER",
        "grid_filename": "grid_1.png",
        "x": 2.631,
        "y": 0.136,
        "z": -15.243
    },
    {
        "personId": "00112933",
        "name": "AYDIN KOZANOĞLU",
        "grid_filename": "grid_1.png",
        "x": 2.839,
        "y": 0.603,
        "z": -14.922
    },
    {
        "personId": "00068745",
        "name": "ÇAĞATAY CAN",
        "grid_filename": "grid_1.png",
        "x": -2.907,
        "y": 2.059,
        "z": -7.467
    },
    {
        "personId": "00053382",
        "name": "KAMİL ÖNDER NERGİZ",
        "grid_filename": "grid_1.png",
        "x": 2.982,
        "y": 0.884,
        "z": 0.552
    },
    {
        "personId": "00063646",
        "name": "EMRE AKMAN",
        "grid_filename": "grid_1.png",
        "x": -2.299,
        "y": -1.801,
        "z": 3.959
    },
    {
        "personId": "00057494",
        "name": "HÜSEYIN OZAN PENEKLIOGLU",
        "grid_filename": "grid_1.png",
        "x": -0.584,
        "y": 4.165,
        "z": -6.596
    },
    {
        "personId": "00085400",
        "name": "NECMİ BİRİNCİ",
        "grid_filename": "grid_1.png",
        "x": 2.895,
        "y": 0.784,
        "z": -13.627
    },
    {
        "personId": "00064253",
        "name": "ORHAN DOĞAN",
        "grid_filename": "grid_1.png",
        "x": 2.56,
        "y": 2.845,
        "z": -8.175
    },
    {
        "personId": "00073080",
        "name": "NURAN ERDAĞ HABERDAR",
        "grid_filename": "grid_1.png",
        "x": 2.916,
        "y": 0.884,
        "z": -14.059
    },
    {
        "personId": "00068383",
        "name": "ZEKERİYA KURUÇAM",
        "grid_filename": "grid_1.png",
        "x": 2.986,
        "y": 1.54,
        "z": -9.991
    },
    {
        "personId": "00062292",
        "name": "ÖMER FARUK YILMAZ",
        "grid_filename": "grid_1.png",
        "x": 3.014,
        "y": 1.35,
        "z": -13.699
    },
    {
        "personId": "00074319",
        "name": "YÜCEL ÇINAR",
        "grid_filename": "grid_1.png",
        "x": 3.014,
        "y": 1.355,
        "z": -10.865
    },
    {
        "personId": "00057852",
        "name": "MÜCAHİT BIÇAKÇI",
        "grid_filename": "grid_1.png",
        "x": 2.007,
        "y": -1.889,
        "z": 3.835
    },
    {
        "personId": "123456789",
        "name": "YUSUF EMİN ZEREN",
        "grid_filename": "grid_1.png",
        "x": 3.0,
        "y": 1.44,
        "z": -9.991
    },
    {
        "personId": "00069103",
        "name": "AYDINAKGÜL",
        "grid_filename": "grid_1.png",
        "x": -2.994,
        "y": 1.495,
        "z": -11.831
    },
    {
        "personId": "00057996",
        "name": "MUSTAFA PEHLİVAN",
        "grid_filename": "grid_1.png",
        "x": 3.011,
        "y": 1.353,
        "z": -14.646
    },
    {
        "personId": "00075176",
        "name": "HALİM YILMAZ",
        "grid_filename": "grid_1.png",
        "x": 2.747,
        "y": 0.231,
        "z": -10.862
    },
    {
        "personId": "00053144",
        "name": "SAVAŞ MUSA DURSUN",
        "grid_filename": "grid_1.png",
        "x": -1.414,
        "y": 3.902,
        "z": -16.498
    },
    {
        "personId": "00054023",
        "name": "ERSEN KUZU",
        "grid_filename": "grid_1.png",
        "x": 1.769,
        "y": 3.687,
        "z": -13.844
    },
    {
        "personId": "00083039",
        "name": "OSMAN YURTTADUR",
        "grid_filename": "grid_1.png",
        "x": 2.947,
        "y": 0.981,
        "z": -12.681
    },
    {
        "personId": "00049302",
        "name": "TURGUT KARADEDE",
        "grid_filename": "grid_1.png",
        "x": 2.95,
        "y": 0.98,
        "z": -10.72
    },
    {
        "personId": "00056457",
        "name": "ÖZLEM ÇERİ",
        "grid_filename": "grid_1.png",
        "x": -0.958,
        "y": 4.091,
        "z": -7.106
    },
    {
        "personId": "00062033",
        "name": "EMIN SELÇUK",
        "grid_filename": "grid_1.png",
        "x": 3.014,
        "y": 1.352,
        "z": -10.72
    },
    {
        "personId": "00064387",
        "name": "MUSTAFA ASIM SUBAŞI",
        "grid_filename": "grid_1.png",
        "x": 3.01,
        "y": 1.354,
        "z": -14.922
    },
    {
        "personId": "00051245",
        "name": "MEHMET GÜRHANARSLAN",
        "grid_filename": "grid_1.png",
        "x": 2.752,
        "y": 0.23,
        "z": -13.408
    },
    {
        "personId": "00061975",
        "name": "ELİF DEĞİRMENCİ",
        "grid_filename": "grid_1.png",
        "x": -2.62,
        "y": 2.712,
        "z": -4.122
    },
    {
        "personId": "00045552",
        "name": "SERKAN BAŞAR",
        "grid_filename": "grid_1.png",
        "x": -2.911,
        "y": 0.846,
        "z": -11.102
    },
    {
        "personId": "00054224",
        "name": "MUSTAFA KEMAL KIZILAY",
        "grid_filename": "grid_1.png",
        "x": -3.076,
        "y": 0.279,
        "z": -1.724
    },
    {
        "personId": "00054150",
        "name": "RESUL BAŞ",
        "grid_filename": "grid_1.png",
        "x": -3.024,
        "y": 0.563,
        "z": -3.106
    },
    {
        "personId": "00079643",
        "name": "AHMET ENES ADALI",
        "grid_filename": "grid_1.png",
        "x": 2.135,
        "y": 3.311,
        "z": 0.624
    },
    {
        "personId": "00926816",
        "name": "ÖMER FARUK ŞAFAK",
        "grid_filename": "grid_1.png",
        "x": 2.972,
        "y": 1.632,
        "z": -13.772
    },
    {
        "personId": "00102493",
        "name": "OSMAN NAHIT YILMAZ",
        "grid_filename": "grid_1.png",
        "x": 2.975,
        "y": 1.63,
        "z": -12.903
    },
    {
        "personId": "00070169",
        "name": "MEHMET NURETTİN KAYGISIZ",
        "grid_filename": "grid_1.png",
        "x": 2.143,
        "y": 3.312,
        "z": -8.1
    },
    {
        "personId": "00077571",
        "name": "SILA ADİLOĞLU YETİK",
        "grid_filename": "grid_1.png",
        "x": 2.924,
        "y": 0.883,
        "z": -11.59
    },
    {
        "personId": "00090420",
        "name": "GÖZDE ŞEN",
        "grid_filename": "grid_1.png",
        "x": 1.953,
        "y": 3.5,
        "z": -8.103
    },
    {
        "personId": "00066593",
        "name": "MUHAMMED NURULLAH HEPER",
        "grid_filename": "grid_1.png",
        "x": 1.572,
        "y": 3.826,
        "z": 0.331
    },
    {
        "personId": "00058984",
        "name": "AHMET TİKVEŞ",
        "grid_filename": "grid_1.png",
        "x": 2.768,
        "y": 1.625,
        "z": -19.385
    },
    {
        "personId": "00053104",
        "name": "BİLAL EKŞİ",
        "grid_filename": "grid_1.png",
        "x": 2.648,
        "y": 0.125,
        "z": -14.922
    },
    {
        "personId": "00064993",
        "name": "MUHAMMET BAYRAM TOPCU",
        "grid_filename": "grid_1.png",
        "x": 1.953,
        "y": 3.5,
        "z": -7.373
    },
    {
        "personId": "00054307",
        "name": "MURAT SAMİ YÜZBAŞI",
        "grid_filename": "grid_1.png",
        "x": 2.06,
        "y": -0.244,
        "z": -18.369
    },
    {
        "personId": "00050148",
        "name": "UFUK ÜNAL",
        "grid_filename": "grid_1.png",
        "x": -2.381,
        "y": 3.086,
        "z": -13.356
    },
    {
        "personId": "00048801",
        "name": "ALPASLANAĞDAŞ",
        "grid_filename": "grid_1.png",
        "x": 2.98,
        "y": 0.882,
        "z": -7.666
    },
    {
        "personId": "123456789",
        "name": "ATTİLA TURGUT DOĞUDAN",
        "grid_filename": "grid_1.png",
        "x": 3.024,
        "y": 1.258,
        "z": -9.41
    },
    {
        "personId": "00062357",
        "name": "ALPER KAŞIKÇI",
        "grid_filename": "grid_1.png",
        "x": 2.775,
        "y": 0.324,
        "z": -14.574
    },
    {
        "personId": "00926814",
        "name": "TALHA ÖZCAN",
        "grid_filename": "grid_1.png",
        "x": 2.679,
        "y": 0.228,
        "z": -15.532
    },
    {
        "personId": "00063000",
        "name": "İBRAHİM SARIKAYA",
        "grid_filename": "grid_1.png",
        "x": 0.922,
        "y": 4.097,
        "z": -3.884
    },
    {
        "personId": "00063735",
        "name": "VEYSEL UZUN",
        "grid_filename": "grid_1.png",
        "x": -0.864,
        "y": 4.109,
        "z": -4.997
    },
    {
        "personId": "00081435",
        "name": "GONCA GÜL EREN PINAR",
        "grid_filename": "grid_1.png",
        "x": 2.795,
        "y": 0.415,
        "z": -10.645
    },
    {
        "personId": "00051103",
        "name": "MEHMET İLKER BAŞARAN",
        "grid_filename": "grid_1.png",
        "x": 2.825,
        "y": 0.512,
        "z": -12.903
    },
    {
        "personId": "00063163",
        "name": "UMUT GÜRŞEN",
        "grid_filename": "grid_1.png",
        "x": 2.949,
        "y": 0.98,
        "z": -11.373
    },
    {
        "personId": "00700010",
        "name": "MUSTAFA EKMEN",
        "grid_filename": "grid_1.png",
        "x": 3.024,
        "y": 1.258,
        "z": -9.629
    },
    {
        "personId": "00079587",
        "name": "MELİK TAHA KİRAZ",
        "grid_filename": "grid_1.png",
        "x": 2.566,
        "y": -1.646,
        "z": 3.762
    },
    {
        "personId": "00069818",
        "name": "OSMAN KERİM AVANAŞ",
        "grid_filename": "grid_1.png",
        "x": 2.994,
        "y": 1.35,
        "z": -15.604
    },
    {
        "personId": "123456789",
        "name": "BURAK ŞAKACI",
        "grid_filename": "grid_1.png",
        "x": -2.979,
        "y": 1.59,
        "z": -10.885
    },
    {
        "personId": "00064810",
        "name": "RAFET FATİH ÖZGÜR",
        "grid_filename": "grid_1.png",
        "x": 2.796,
        "y": 0.418,
        "z": -10.064
    },
    {
        "personId": "00075131",
        "name": "BAYRAM BURAK KARALİ",
        "grid_filename": "grid_1.png",
        "x": -2.614,
        "y": 2.711,
        "z": 3.938
    },
    {
        "personId": "00074199",
        "name": "HAMZA ALTUNDAĞ",
        "grid_filename": "grid_1.png",
        "x": 1.869,
        "y": 3.587,
        "z": -14.952
    },
    {
        "personId": "00095286",
        "name": "KADİR BOZKURT",
        "grid_filename": "grid_1.png",
        "x": 2.985,
        "y": 1.441,
        "z": -15.968
    },
    {
        "personId": "00060961",
        "name": "YAHYA ZAHİD ŞENSOY",
        "grid_filename": "grid_1.png",
        "x": 2.987,
        "y": 1.538,
        "z": -10.718
    },
    {
        "personId": "00067264",
        "name": "ORHAN ÖNAL",
        "grid_filename": "grid_1.png",
        "x": 3.0,
        "y": 1.44,
        "z": -13.99
    },
    {
        "personId": "00074315",
        "name": "FATİH İNAN",
        "grid_filename": "grid_1.png",
        "x": 1.673,
        "y": 3.777,
        "z": -7.519
    },
    {
        "personId": "00058132",
        "name": "ALİ ÖZDEMİR",
        "grid_filename": "grid_1.png",
        "x": 2.817,
        "y": 0.508,
        "z": -14.922
    },
    {
        "personId": "00049186",
        "name": "HASAN SAVAŞ ERDEN",
        "grid_filename": "grid_1.png",
        "x": 2.821,
        "y": 0.512,
        "z": -10.571
    },
    {
        "personId": "00067259",
        "name": "MUSTAFA DEMİRCİ",
        "grid_filename": "grid_1.png",
        "x": 2.1,
        "y": -1.856,
        "z": 3.979
    },
    {
        "personId": "00089904",
        "name": "FATİH TAYYAR",
        "grid_filename": "grid_1.png",
        "x": 0.826,
        "y": 4.114,
        "z": 2.729
    },
    {
        "personId": "00057538",
        "name": "KADİR BURÇİN YILMAZ",
        "grid_filename": "grid_1.png",
        "x": 2.981,
        "y": 1.446,
        "z": -16.26
    },
    {
        "personId": "00054245",
        "name": "SERDAR ÖZKAN",
        "grid_filename": "grid_1.png",
        "x": -2.619,
        "y": 2.711,
        "z": -1.943
    },
    {
        "personId": "00080784",
        "name": "ŞÜKÜR ERKUT",
        "grid_filename": "grid_1.png",
        "x": -3.097,
        "y": 0.188,
        "z": -0.272
    },
    {
        "personId": "00114980",
        "name": "MEHMET ERKUL",
        "grid_filename": "grid_1.png",
        "x": 2.093,
        "y": 0.974,
        "z": -22.656
    },
    {
        "personId": "00049854",
        "name": "ARİF EKEN",
        "grid_filename": "grid_1.png",
        "x": 2.999,
        "y": 1.437,
        "z": -7.81
    },
    {
        "personId": "00067693",
        "name": "VEYSEL SERDAR",
        "grid_filename": "grid_1.png",
        "x": 2.961,
        "y": 0.778,
        "z": -8.831
    },
    {
        "personId": "00081640",
        "name": "HATİCE ÜRKAN",
        "grid_filename": "grid_1.png",
        "x": 2.719,
        "y": 0.127,
        "z": -10.79
    },
    {
        "personId": "00083959",
        "name": "SAMİ ARVAS",
        "grid_filename": "grid_1.png",
        "x": -2.286,
        "y": 3.179,
        "z": -12.995
    },
    {
        "personId": "123456789",
        "name": "MUZAFFER KUZUBAŞOĞLU",
        "grid_filename": "grid_1.png",
        "x": 2.279,
        "y": -0.61,
        "z": -12.755
    },
    {
        "personId": "00093388",
        "name": "BİLAL OKUR",
        "grid_filename": "grid_1.png",
        "x": 2.589,
        "y": 0.039,
        "z": -14.922
    },
    {
        "personId": "00061887",
        "name": "MUHAMMED HAMZA ARSLAN",
        "grid_filename": "grid_1.png",
        "x": -2.888,
        "y": 2.149,
        "z": -2.671
    },
    {
        "personId": "00057456",
        "name": "AHMET MENNAN MÜFTÜOĞLU",
        "grid_filename": "grid_1.png",
        "x": 2.777,
        "y": 2.376,
        "z": -0.321
    },
    {
        "personId": "123456789",
        "name": "SERDAR GÜLER",
        "grid_filename": "grid_1.png",
        "x": 3.013,
        "y": 1.35,
        "z": -9.773
    },
    {
        "personId": "00067458",
        "name": "BARBAROS KURTUL",
        "grid_filename": "grid_1.png",
        "x": -2.912,
        "y": 1.964,
        "z": 3.793
    },
    {
        "personId": "00063245",
        "name": "ALİ ENSAR KILIÇOĞLU",
        "grid_filename": "grid_1.png",
        "x": 2.513,
        "y": -0.145,
        "z": -13.917
    },
    {
        "personId": "00073699",
        "name": "HAKANANKARA",
        "grid_filename": "grid_1.png",
        "x": 2.773,
        "y": 0.321,
        "z": -11.299
    },
    {
        "personId": "00042581",
        "name": "BÜLENT ÜNALAN",
        "grid_filename": "grid_1.png",
        "x": 2.432,
        "y": -0.144,
        "z": -15.388
    },
    {
        "personId": "123456789",
        "name": "HAYRİ ÖZTURAN",
        "grid_filename": "grid_1.png",
        "x": 2.903,
        "y": 0.881,
        "z": -15.896
    },
    {
        "personId": "00062899",
        "name": "EMRE İSMAİLOĞLU",
        "grid_filename": "grid_1.png",
        "x": 2.319,
        "y": -0.241,
        "z": -16.043
    },
    {
        "personId": "00093317",
        "name": "MUHAMMED FURKAN BULUT",
        "grid_filename": "grid_1.png",
        "x": 2.143,
        "y": -0.147,
        "z": -18.297
    },
    {
        "personId": "00062147",
        "name": "YILMAZ GORALI",
        "grid_filename": "grid_1.png",
        "x": -2.995,
        "y": 0.75,
        "z": 1.547
    },
    {
        "personId": "00062358",
        "name": "ENGİN DURMAZ",
        "grid_filename": "grid_1.png",
        "x": 2.768,
        "y": 0.416,
        "z": -16.404
    },
    {
        "personId": "00051680",
        "name": "İRFAN KELER",
        "grid_filename": "grid_1.png",
        "x": 2.962,
        "y": 1.347,
        "z": -16.841
    },
    {
        "personId": "00074014",
        "name": "EMRE ARPA",
        "grid_filename": "grid_1.png",
        "x": 2.861,
        "y": 0.696,
        "z": -16.404
    },
    {
        "personId": "00053784",
        "name": "GÖKHAN EMİR",
        "grid_filename": "grid_1.png",
        "x": 2.722,
        "y": 0.14,
        "z": -10.645
    },
    {
        "personId": "00054287",
        "name": "HİKMET MESUT TÜRKSEVEN",
        "grid_filename": "grid_1.png",
        "x": 2.882,
        "y": 0.788,
        "z": -16.043
    },
    {
        "personId": "00062761",
        "name": "FATİH AYDIN",
        "grid_filename": "grid_1.png",
        "x": 2.523,
        "y": -0.235,
        "z": -12.392
    },
    {
        "personId": "00062029",
        "name": "HAKAN SÖGÜT",
        "grid_filename": "grid_1.png",
        "x": 2.696,
        "y": 0.044,
        "z": -10.718
    },
    {
        "personId": "123456789",
        "name": "AYHAN TOP",
        "grid_filename": "grid_1.png",
        "x": -2.97,
        "y": -0.279,
        "z": -6.596
    },
    {
        "personId": "00058062",
        "name": "FATİH KARAMAN",
        "grid_filename": "grid_1.png",
        "x": 2.752,
        "y": 0.228,
        "z": -12.246
    },
    {
        "personId": "00020128",
        "name": "MELİH ŞÜKRÜ ECERTAŞ",
        "grid_filename": "grid_1.png",
        "x": 2.775,
        "y": 0.318,
        "z": -13.264
    },
    {
        "personId": "00065352",
        "name": "MUSA DENİZ PERÇİNKAYA",
        "grid_filename": "grid_1.png",
        "x": 2.97,
        "y": 1.166,
        "z": -14.862
    },
    {
        "personId": "00071887",
        "name": "MEHMET YELTEKİN",
        "grid_filename": "grid_1.png",
        "x": 2.719,
        "y": 0.125,
        "z": -13.409
    },
    {
        "personId": "00077418",
        "name": "FATİH ONUL",
        "grid_filename": "grid_1.png",
        "x": 2.875,
        "y": 0.699,
        "z": -12.318
    },
    {
        "personId": "00069094",
        "name": "NURSİBEL AYDIN",
        "grid_filename": "grid_1.png",
        "x": 1.999,
        "y": -0.241,
        "z": -18.732
    },
    {
        "personId": "00059310",
        "name": "TURGUT KENDİRCİ",
        "grid_filename": "grid_1.png",
        "x": -0.503,
        "y": 4.119,
        "z": -18.748
    },
    {
        "personId": "00053044",
        "name": "BEKİR ALPER YILDIRIM",
        "grid_filename": "grid_1.png",
        "x": -3.017,
        "y": 1.218,
        "z": -10.957
    },
    {
        "personId": "00063916",
        "name": "HASAN ÖZGÜL",
        "grid_filename": "grid_1.png",
        "x": 0.92,
        "y": 4.098,
        "z": -5.702
    },
    {
        "personId": "00117545",
        "name": "ÖZCAN BAŞOĞLU",
        "grid_filename": "grid_1.png",
        "x": -3.012,
        "y": 1.218,
        "z": -11.176
    },
    {
        "personId": "00112215",
        "name": "HAMZA DİNÇ",
        "grid_filename": "grid_1.png",
        "x": -2.382,
        "y": 3.087,
        "z": -13.939
    },
    {
        "personId": "00071314",
        "name": "OSMAN TÜZER",
        "grid_filename": "grid_1.png",
        "x": -2.465,
        "y": 2.992,
        "z": -8.56
    },
    {
        "personId": "00048017",
        "name": "UTKU YAZAN",
        "grid_filename": "grid_1.png",
        "x": 2.998,
        "y": 1.163,
        "z": -11.373
    },
    {
        "personId": "00045705",
        "name": "SERKAN CEVDET TANSU",
        "grid_filename": "grid_1.png",
        "x": -2.617,
        "y": 2.715,
        "z": -2.524
    },
    {
        "personId": "00020256",
        "name": "GÜLDEN NACAR",
        "grid_filename": "grid_1.png",
        "x": 3.024,
        "y": 1.253,
        "z": -9.917
    },
    {
        "personId": "00055075",
        "name": "KADİR KÖK",
        "grid_filename": "grid_1.png",
        "x": 2.882,
        "y": 0.788,
        "z": -14.95
    },
    {
        "personId": "00069803",
        "name": "İBRAHİM BAHADIR KORKMAZ",
        "grid_filename": "grid_1.png",
        "x": -2.994,
        "y": 0.745,
        "z": -3.831
    },
    {
        "personId": "00053412",
        "name": "YUSUF GÜRDAL YILMAZ",
        "grid_filename": "grid_1.png",
        "x": 3.013,
        "y": 1.159,
        "z": -7.447
    },
    {
        "personId": "00068340",
        "name": "NEŞE AY",
        "grid_filename": "grid_1.png",
        "x": 3.012,
        "y": 1.349,
        "z": -14.427
    },
    {
        "personId": "00069439",
        "name": "ERHAN BALABAN",
        "grid_filename": "grid_1.png",
        "x": 2.662,
        "y": 0.227,
        "z": -15.824
    },
    {
        "personId": "00054306",
        "name": "ABDULLAH YORMAZ",
        "grid_filename": "grid_1.png",
        "x": 1.921,
        "y": 0.042,
        "z": -20.332
    },
    {
        "personId": "00055013",
        "name": "RAİF ASANA",
        "grid_filename": "grid_1.png",
        "x": 2.587,
        "y": -0.235,
        "z": -10.355
    },
    {
        "personId": "123456789",
        "name": "NESRİN ŞAHİN",
        "grid_filename": "grid_1.png",
        "x": 2.987,
        "y": 1.54,
        "z": -11.664
    },
    {
        "personId": "00058890",
        "name": "İSMET MİNDAŞ",
        "grid_filename": "grid_1.png",
        "x": -1.994,
        "y": 3.46,
        "z": -7.686
    },
    {
        "personId": "00048736",
        "name": "ÜMİT DEVELİ",
        "grid_filename": "grid_1.png",
        "x": 3.024,
        "y": 1.256,
        "z": -10.501
    },
    {
        "personId": "00070047",
        "name": "EMRAH KARACA",
        "grid_filename": "grid_1.png",
        "x": 2.299,
        "y": 0.224,
        "z": -18.954
    },
    {
        "personId": "00085084",
        "name": "İLKER HOLOĞLU",
        "grid_filename": "grid_1.png",
        "x": -3.008,
        "y": 1.405,
        "z": -13.139
    },
    {
        "personId": "00110386",
        "name": "OĞUZHAN HORASANLI",
        "grid_filename": "grid_1.png",
        "x": -2.931,
        "y": 1.867,
        "z": -2.742
    },
    {
        "personId": "00081708",
        "name": "MUHAMMET SELMAN ŞENKAL",
        "grid_filename": "grid_1.png",
        "x": 0.923,
        "y": 4.087,
        "z": -15.387
    },
    {
        "personId": "00067690",
        "name": "MAHMUD ÜSAME GÜNGÖR",
        "grid_filename": "grid_1.png",
        "x": 2.519,
        "y": -0.239,
        "z": -12.536
    },
    {
        "personId": "00070363",
        "name": "FEYYAZ ENES AKBEN",
        "grid_filename": "grid_1.png",
        "x": 2.61,
        "y": -0.142,
        "z": -11.518
    },
    {
        "personId": "123456789",
        "name": "NECMEDDİN SİNAN ÇITLAK",
        "grid_filename": "grid_1.png",
        "x": 2.959,
        "y": 1.068,
        "z": -13.99
    },
    {
        "personId": "00070175",
        "name": "ÇAĞKAN TORUNLAR",
        "grid_filename": "grid_1.png",
        "x": 2.69,
        "y": 0.227,
        "z": -15.315
    },
    {
        "personId": "00060615",
        "name": "ABDULLAH BAHADIR BÜYÜKKAYMAZ",
        "grid_filename": "grid_1.png",
        "x": 1.944,
        "y": 3.5,
        "z": 1.059
    },
    {
        "personId": "00066840",
        "name": "ÖMER FARUK SÖNMEZ",
        "grid_filename": "grid_1.png",
        "x": -2.845,
        "y": 2.248,
        "z": -6.597
    },
    {
        "personId": "00117299",
        "name": "SERDAR GÜRBÜZ",
        "grid_filename": "grid_1.png",
        "x": 2.973,
        "y": 1.632,
        "z": -13.409
    },
    {
        "personId": "00066788",
        "name": "ENES DEMİRÖZ",
        "grid_filename": "grid_1.png",
        "x": 2.818,
        "y": 0.511,
        "z": -16.113
    },
    {
        "personId": "00076851",
        "name": "MUHARREM BİLAL GURBETCİ",
        "grid_filename": "grid_1.png",
        "x": 2.744,
        "y": -1.469,
        "z": 4.269
    },
    {
        "personId": "00063586",
        "name": "KADİR YILDIZ",
        "grid_filename": "grid_1.png",
        "x": 2.18,
        "y": -0.148,
        "z": -18.078
    },
    {
        "personId": "00069988",
        "name": "SİNAN DİLEK",
        "grid_filename": "grid_1.png",
        "x": 2.397,
        "y": 0.319,
        "z": -18.805
    },
    {
        "personId": "00100421",
        "name": "FATİH ÜNALAN",
        "grid_filename": "grid_1.png",
        "x": -2.919,
        "y": 0.938,
        "z": -14.156
    },
    {
        "personId": "00926811",
        "name": "EMRAH SONUMUT",
        "grid_filename": "grid_1.png",
        "x": 2.875,
        "y": 2.188,
        "z": -15.678
    },
    {
        "personId": "00103956",
        "name": "MURAT YILMAZ",
        "grid_filename": "grid_1.png",
        "x": 3.011,
        "y": 1.353,
        "z": -14.79
    },
    {
        "personId": "00069778",
        "name": "FATİH KARAKOÇ",
        "grid_filename": "grid_1.png",
        "x": 2.826,
        "y": 0.509,
        "z": -12.174
    },
    {
        "personId": "00064470",
        "name": "MELTEM KARAN",
        "grid_filename": "grid_1.png",
        "x": -3.095,
        "y": 0.189,
        "z": -0.053
    },
    {
        "personId": "00061467",
        "name": "MUSTAFA DÖKMETAŞ",
        "grid_filename": "grid_1.png",
        "x": 2.379,
        "y": -1.771,
        "z": 4.125
    },
    {
        "personId": "00090410",
        "name": "EMRE MEMİŞ",
        "grid_filename": "grid_1.png",
        "x": 2.817,
        "y": 0.508,
        "z": -15.824
    },
    {
        "personId": "00090245",
        "name": "EMRE ERMUT",
        "grid_filename": "grid_1.png",
        "x": 2.839,
        "y": 0.602,
        "z": -15.678
    },
    {
        "personId": "00062791",
        "name": "MEHMET SAMİ İKİNCİ",
        "grid_filename": "grid_1.png",
        "x": 2.665,
        "y": 0.044,
        "z": -13.409
    },
    {
        "personId": "00075046",
        "name": "SERPİL ÇEKMEN KAYA",
        "grid_filename": "grid_1.png",
        "x": 1.293,
        "y": 3.976,
        "z": -2.499
    },
    {
        "personId": "123456789",
        "name": "HAKAN BABİLA",
        "grid_filename": "grid_1.png",
        "x": -2.717,
        "y": 2.528,
        "z": -11.756
    },
    {
        "personId": "00069354",
        "name": "YAVUZ ULUSOY",
        "grid_filename": "grid_1.png",
        "x": 2.971,
        "y": 0.978,
        "z": -10.429
    },
    {
        "personId": "00073273",
        "name": "HAMİD ELDELEKLİOĞLU",
        "grid_filename": "grid_1.png",
        "x": 2.673,
        "y": -0.05,
        "z": -11.083
    },
    {
        "personId": "00050400",
        "name": "AYŞEGÜL KARPUZOĞLU",
        "grid_filename": "grid_1.png",
        "x": 2.956,
        "y": 1.724,
        "z": -7.372
    },
    {
        "personId": "00114706",
        "name": "KENAN ŞAHAN",
        "grid_filename": "grid_1.png",
        "x": 2.655,
        "y": -1.572,
        "z": 3.689
    },
    {
        "personId": "00082453",
        "name": "SEFA KARAKELLE",
        "grid_filename": "grid_1.png",
        "x": 2.961,
        "y": 1.722,
        "z": -12.973
    },
    {
        "personId": "00066043",
        "name": "SİBEL EMRE",
        "grid_filename": "grid_1.png",
        "x": -1.709,
        "y": 3.739,
        "z": -1.579
    },
    {
        "personId": "00051933",
        "name": "OSMAN HACIMAHMUTOĞLU",
        "grid_filename": "grid_1.png",
        "x": -0.89,
        "y": 4.026,
        "z": -19.618
    },
    {
        "personId": "00054309",
        "name": "ÖMER ÇAPOĞLU",
        "grid_filename": "grid_1.png",
        "x": 2.984,
        "y": 1.54,
        "z": -14.427
    },
    {
        "personId": "00098299",
        "name": "BABÜR KAAN ŞENER",
        "grid_filename": "grid_1.png",
        "x": 2.592,
        "y": 0.043,
        "z": -14.922
    },
    {
        "personId": "00069289",
        "name": "YAVUZ AYMELEK",
        "grid_filename": "grid_1.png",
        "x": 3.023,
        "y": 1.259,
        "z": -11.299
    },
    {
        "personId": "00079316",
        "name": "MUSTAFA DEMİRAK",
        "grid_filename": "grid_1.png",
        "x": 2.656,
        "y": 0.137,
        "z": -14.922
    },
    {
        "personId": "00060464",
        "name": "MURAT GEZERAVCI",
        "grid_filename": "grid_1.png",
        "x": 2.192,
        "y": -1.827,
        "z": 4.051
    },
    {
        "personId": "00101447",
        "name": "TÜLAY YALÇINKAYA",
        "grid_filename": "grid_1.png",
        "x": 3.001,
        "y": 1.163,
        "z": -10.939
    },
    {
        "personId": "00043963",
        "name": "BÜLENT ECVET DENİZ",
        "grid_filename": "grid_1.png",
        "x": 2.498,
        "y": -0.054,
        "z": -15.315
    },
    {
        "personId": "00099793",
        "name": "KAYA KARAYEL",
        "grid_filename": "grid_1.png",
        "x": -2.93,
        "y": 1.868,
        "z": -0.924
    },
    {
        "personId": "00086779",
        "name": "MUSTAFA TUNCER",
        "grid_filename": "grid_1.png",
        "x": 3.023,
        "y": 1.256,
        "z": -8.539
    },
    {
        "personId": "123456789",
        "name": "HAKAN ÖZTÜRK",
        "grid_filename": "grid_1.png",
        "x": 2.771,
        "y": 0.325,
        "z": -10.573
    },
    {
        "personId": "00112952",
        "name": "MUHAMMET EMİN OKUR",
        "grid_filename": "grid_1.png",
        "x": 2.909,
        "y": 0.881,
        "z": -14.5
    },
    {
        "personId": "00075289",
        "name": "MÜBAREK BAYRAM",
        "grid_filename": "grid_1.png",
        "x": -2.722,
        "y": 2.526,
        "z": -14.886
    },
    {
        "personId": "00063507",
        "name": "BETÜL ÇOLAK",
        "grid_filename": "grid_1.png",
        "x": -3.028,
        "y": 0.421,
        "z": 3.53
    },
    {
        "personId": "00049410",
        "name": "SİNAN KÜNTAY",
        "grid_filename": "grid_1.png",
        "x": 2.974,
        "y": 1.632,
        "z": -11.664
    },
    {
        "personId": "00046743",
        "name": "ALPER ATALAY",
        "grid_filename": "grid_1.png",
        "x": 2.795,
        "y": 0.412,
        "z": -14.922
    },
    {
        "personId": "00068077",
        "name": "MUHAMMED İBRAHİM KAVRANOĞLU",
        "grid_filename": "grid_1.png",
        "x": -1.995,
        "y": 3.465,
        "z": -15.046
    },
    {
        "personId": "00020112",
        "name": "MECİT EŞ",
        "grid_filename": "grid_1.png",
        "x": 2.777,
        "y": 0.322,
        "z": -12.536
    },
    {
        "personId": "00088092",
        "name": "ENSAR AKDAĞ",
        "grid_filename": "grid_1.png",
        "x": -2.894,
        "y": -0.47,
        "z": -8.05
    },
    {
        "personId": "00110384",
        "name": "NAZLI CEYLAN MOLLAOĞLU",
        "grid_filename": "grid_1.png",
        "x": 2.868,
        "y": 1.44,
        "z": -18.297
    },
    {
        "personId": "00081647",
        "name": "MUHAMMED MASUM AYDIN",
        "grid_filename": "grid_1.png",
        "x": -2.54,
        "y": 2.899,
        "z": -14.303
    },
    {
        "personId": "00074856",
        "name": "MİTHAT SAMED YAZICI",
        "grid_filename": "grid_1.png",
        "x": 1.759,
        "y": 3.688,
        "z": -0.758
    },
    {
        "personId": "00073218",
        "name": "YASİN BİRİNCİ",
        "grid_filename": "grid_1.png",
        "x": -2.676,
        "y": 2.618,
        "z": -12.777
    },
    {
        "personId": "00068347",
        "name": "MURAT YALÇIN KIRCA",
        "grid_filename": "grid_1.png",
        "x": 2.997,
        "y": 1.348,
        "z": -15.457
    },
    {
        "personId": "00060497",
        "name": "CENKER EVREN TEZEL",
        "grid_filename": "grid_1.png",
        "x": 2.703,
        "y": 0.227,
        "z": -15.097
    },
    {
        "personId": "00086841",
        "name": "OSMAN ŞAFAK",
        "grid_filename": "grid_1.png",
        "x": -2.845,
        "y": 0.648,
        "z": -14.665
    },
    {
        "personId": "00058578",
        "name": "BİLAL İSMAİL YALMANBAŞ",
        "grid_filename": "grid_1.png",
        "x": 2.529,
        "y": -0.051,
        "z": -14.922
    },
    {
        "personId": "00085234",
        "name": "MEHMET ÇİÇEK",
        "grid_filename": "grid_1.png",
        "x": -1.989,
        "y": 3.461,
        "z": -4.197
    },
    {
        "personId": "00063761",
        "name": "ABDULLAH KOSİF",
        "grid_filename": "grid_1.png",
        "x": -2.668,
        "y": -0.28,
        "z": -9.067
    },
    {
        "personId": "00051483",
        "name": "CENGİZ TUNCEL",
        "grid_filename": "grid_1.png",
        "x": 2.768,
        "y": 0.322,
        "z": -15.168
    },
    {
        "personId": "00054161",
        "name": "FATİH CIĞAL",
        "grid_filename": "grid_1.png",
        "x": -2.276,
        "y": 3.182,
        "z": -10.23
    },
    {
        "personId": "00058137",
        "name": "DEMET TÜRKEL",
        "grid_filename": "grid_1.png",
        "x": 2.965,
        "y": 0.783,
        "z": -7.812
    },
    {
        "personId": "00062769",
        "name": "ÖZNUR AKSU",
        "grid_filename": "grid_1.png",
        "x": 1.762,
        "y": 3.687,
        "z": -3.665
    },
    {
        "personId": "00049778",
        "name": "GÜREL TÜMER",
        "grid_filename": "grid_1.png",
        "x": -2.804,
        "y": 2.339,
        "z": -9.796
    },
    {
        "personId": "00045975",
        "name": "ALİ BULUT",
        "grid_filename": "grid_1.png",
        "x": -2.967,
        "y": 1.686,
        "z": -12.921
    },
    {
        "personId": "00069380",
        "name": "MUSTAFA ERDOĞAN",
        "grid_filename": "grid_1.png",
        "x": 2.09,
        "y": -0.706,
        "z": -14.862
    },
    {
        "personId": "00079581",
        "name": "ÜLKER ŞULE AKSOY",
        "grid_filename": "grid_1.png",
        "x": 3.007,
        "y": 1.166,
        "z": -10.865
    },
    {
        "personId": "00063161",
        "name": "ADEM EKMEKCİ",
        "grid_filename": "grid_1.png",
        "x": 2.412,
        "y": 0.602,
        "z": -20.04
    },
    {
        "personId": "00047034",
        "name": "ÜMİT ALBAYRAK",
        "grid_filename": "grid_1.png",
        "x": 3.022,
        "y": 1.256,
        "z": -7.447
    },
    {
        "personId": "00065598",
        "name": "MUHAMMED BİLAL DÖNER",
        "grid_filename": "grid_1.png",
        "x": -0.771,
        "y": 4.129,
        "z": -12.631
    },
    {
        "personId": "00072638",
        "name": "ABDULLAH AHMET TUĞCU",
        "grid_filename": "grid_1.png",
        "x": 2.028,
        "y": 0.04,
        "z": -19.749
    },
    {
        "personId": "00070343",
        "name": "MUSTAFA İSMAİL MÜCAHİTOĞLU",
        "grid_filename": "grid_1.png",
        "x": -1.941,
        "y": 0.376,
        "z": -21.37
    },
    {
        "personId": "00069759",
        "name": "GAMZE UÇAR",
        "grid_filename": "grid_1.png",
        "x": 2.594,
        "y": -0.144,
        "z": -11.955
    },
    {
        "personId": "00054217",
        "name": "CİHAN KAN",
        "grid_filename": "grid_1.png",
        "x": 1.77,
        "y": 3.688,
        "z": -12.464
    },
    {
        "personId": "00057595",
        "name": "SAİT ARSLAN",
        "grid_filename": "grid_1.png",
        "x": -2.757,
        "y": 1.59,
        "z": -19.554
    },
    {
        "personId": "00064346",
        "name": "FİGEN BAYER",
        "grid_filename": "grid_1.png",
        "x": -2.722,
        "y": 0.092,
        "z": -9.504
    },
    {
        "personId": "00062214",
        "name": "KADİR COŞKUN",
        "grid_filename": "grid_1.png",
        "x": 2.099,
        "y": -1.87,
        "z": 3.688
    },
    {
        "personId": "123456789",
        "name": "ALİ KESKİN",
        "grid_filename": "grid_1.png",
        "x": 2.823,
        "y": 0.512,
        "z": -14.572
    },
    {
        "personId": "00042726",
        "name": "ABDULLAH TUNCER KEÇECİ",
        "grid_filename": "grid_1.png",
        "x": 2.786,
        "y": -1.334,
        "z": -1.62
    },
    {
        "personId": "00068412",
        "name": "SALİH DÖĞENCİ",
        "grid_filename": "grid_1.png",
        "x": 2.896,
        "y": 0.699,
        "z": -10.136
    },
    {
        "personId": "00057088",
        "name": "ERTUĞRUL SEVİMLİ",
        "grid_filename": "grid_1.png",
        "x": 2.342,
        "y": 0.694,
        "z": -20.693
    },
    {
        "personId": "00074921",
        "name": "MESUT AYBAKAN",
        "grid_filename": "grid_1.png",
        "x": -2.97,
        "y": 1.592,
        "z": -0.271
    },
    {
        "personId": "00064809",
        "name": "İSMAİL ÖZTÜRK",
        "grid_filename": "grid_1.png",
        "x": 2.956,
        "y": 1.631,
        "z": -15.969
    },
    {
        "personId": "00049610",
        "name": "SERKAN SÖNMEZ",
        "grid_filename": "grid_1.png",
        "x": 3.011,
        "y": 1.259,
        "z": -13.408
    },
    {
        "personId": "00073501",
        "name": "SALİH AHZEM TOPAL",
        "grid_filename": "grid_1.png",
        "x": 3.084,
        "y": -0.336,
        "z": -5.63
    },
    {
        "personId": "00074597",
        "name": "VELİ İBRAHİM UĞUR",
        "grid_filename": "grid_1.png",
        "x": -2.472,
        "y": 0.658,
        "z": -19.845
    },
    {
        "personId": "00926817",
        "name": "EMRE MENEVŞE",
        "grid_filename": "grid_1.png",
        "x": 2.256,
        "y": 0.413,
        "z": -20.112
    },
    {
        "personId": "00066282",
        "name": "SERTAN YÜCE",
        "grid_filename": "grid_1.png",
        "x": 3.002,
        "y": 1.44,
        "z": -11.445
    },
    {
        "personId": "00061175",
        "name": "BORA AKSOYLU",
        "grid_filename": "grid_1.png",
        "x": 2.465,
        "y": -0.145,
        "z": -14.922
    },
    {
        "personId": "00070864",
        "name": "HUZEYFE AKHAN",
        "grid_filename": "grid_1.png",
        "x": 2.903,
        "y": 0.881,
        "z": -16.187
    },
    {
        "personId": "00052348",
        "name": "AHMET OLMUŞTUR",
        "grid_filename": "grid_1.png",
        "x": 2.801,
        "y": 0.419,
        "z": -13.553
    },
    {
        "personId": "00083573",
        "name": "ABDULLAH ARİF UYSAL",
        "grid_filename": "grid_1.png",
        "x": -3.009,
        "y": 1.215,
        "z": -12.052
    },
    {
        "personId": "00054573",
        "name": "VURAL URSAVAŞ",
        "grid_filename": "grid_1.png",
        "x": 3.012,
        "y": 1.168,
        "z": -10.646
    },
    {
        "personId": "00062877",
        "name": "AHMET MAHIR TUZCU",
        "grid_filename": "grid_1.png",
        "x": -2.925,
        "y": 1.873,
        "z": -15.554
    },
    {
        "personId": "00062807",
        "name": "selim türk",
        "grid_filename": "grid_1.png",
        "x": -2.777,
        "y": 1.870,
        "z": -18.826
    },
    {
        "personId": "00926815",
        "name": "MUHAMMED KADRİ GÖZTOK",
        "grid_filename": "grid_1.png",
        "x": 2.774,
        "y": 0.319,
        "z": -14.922
    },
    {
        "personId": "00057452",
        "name": "AHMET ACAR",
        "grid_filename": "grid_1.png",
        "x": 2.152,
        "y": -0.239,
        "z": -17.859
    },
    {
        "personId": "00051342",
        "name": "ONUR ALPAN",
        "grid_filename": "grid_1.png",
        "x": 3.012,
        "y": 1.353,
        "z": -14.208
    },
    {
        "personId": "00049600",
        "name": "BERRAK DAMLA YILDIRIM",
        "grid_filename": "grid_1.png",
        "x": 2.414,
        "y": -0.235,
        "z": -14.72
    },
    {
        "personId": "00073370",
        "name": "HÜSEYİNAVNİ GÜMRÜKÇÜOĞLU",
        "grid_filename": "grid_1.png",
        "x": 2.904,
        "y": 0.882,
        "z": -16.404
    },
    {
        "personId": "00052186",
        "name": "AHMET METİN ÖLMEZ",
        "grid_filename": "grid_1.png",
        "x": 2.752,
        "y": 0.233,
        "z": -13.846
    },
    {
        "personId": "00063194",
        "name": "SEDAT ORMAN",
        "grid_filename": "grid_1.png",
        "x": 2.995,
        "y": 1.166,
        "z": -12.681
    },
    {
        "personId": "00061279",
        "name": "AHMET TURSUN",
        "grid_filename": "grid_1.png",
        "x": 2.777,
        "y": 0.327,
        "z": -13.772
    },
    {
        "personId": "00070365",
        "name": "ŞERAFETTİN EKİCİ",
        "grid_filename": "grid_1.png",
        "x": 2.97,
        "y": 1.071,
        "z": -13.046
    },
    {
        "personId": "00051606",
        "name": "AHMET SERHAT SARI",
        "grid_filename": "grid_1.png",
        "x": -2.892,
        "y": 0.848,
        "z": -14.972
    },
    {
        "personId": "00049834",
        "name": "EROL FAKİ",
        "grid_filename": "grid_1.png",
        "x": 1.76,
        "y": 3.688,
        "z": -2.502
    },
    {
        "personId": "00091365",
        "name": "GÖKHAN TELLİ",
        "grid_filename": "grid_1.png",
        "x": 2.574,
        "y": -0.232,
        "z": -10.79
    },
    {
        "personId": "00053149",
        "name": "MUSTAFA İÇELOĞLU",
        "grid_filename": "grid_1.png",
        "x": -2.156,
        "y": -0.653,
        "z": -14.303
    },
    {
        "personId": "00020159",
        "name": "RAMAZAN SARI",
        "grid_filename": "grid_1.png",
        "x": 2.887,
        "y": 0.608,
        "z": -9.848
    },
    {
        "personId": "00052500",
        "name": "HASAN DEMİR",
        "grid_filename": "grid_1.png",
        "x": 2.617,
        "y": -0.144,
        "z": -11.299
    },
    {
        "personId": "00080270",
        "name": "GİZEM ERCAN",
        "grid_filename": "grid_1.png",
        "x": 2.851,
        "y": 0.605,
        "z": -11.884
    },
    {
        "personId": "00068037",
        "name": "TUĞBA YAŞAROĞLU YAVUZ",
        "grid_filename": "grid_1.png",
        "x": -2.681,
        "y": -0.001,
        "z": -10.885
    },
    {
        "personId": "00070061",
        "name": "MELEK BİLİCİ",
        "grid_filename": "grid_1.png",
        "x": 2.521,
        "y": 2.938,
        "z": -12.173
    },
    {
        "personId": "00068792",
        "name": "HUZEYFE BİRKAN",
        "grid_filename": "grid_1.png",
        "x": -2.702,
        "y": 1.498,
        "z": -19.989
    },
    {
        "personId": "123456789",
        "name": "OSMAN ERHAN",
        "grid_filename": "grid_1.png",
        "x": -2.465,
        "y": 2.992,
        "z": -8.56
    },
    {
        "personId": "00054183",
        "name": "ÇETİN DURUGÖL",
        "grid_filename": "grid_1.png",
        "x": 2.752,
        "y": 0.322,
        "z": -15.46
    },
    {
        "personId": "00072774",
        "name": "MUKADDES SERT",
        "grid_filename": "grid_1.png",
        "x": -0.513,
        "y": -2.18,
        "z": 4.2
    },
    {
        "personId": "00089878",
        "name": "LAÇİN REYYAN GÜNDEN",
        "grid_filename": "grid_1.png",
        "x": -0.492,
        "y": 4.182,
        "z": -13.358
    },
    {
        "personId": "123456789",
        "name": "BERK YILDIZ",
        "grid_filename": "grid_1.png",
        "x": 2.517,
        "y": 2.936,
        "z": -7.81
    },
    {
        "personId": "00098768",
        "name": "MUSTAFA SÖZEN",
        "grid_filename": "grid_1.png",
        "x": 2.289,
        "y": -1.789,
        "z": 4.27
    },
    {
        "personId": "00044357",
        "name": "ŞEVKİ ERKAN ERDOĞAN",
        "grid_filename": "grid_1.png",
        "x": 3.02,
        "y": 1.259,
        "z": -12.246
    },
    {
        "personId": "00053185",
        "name": "MÜJDAT ULUDAĞ",
        "grid_filename": "grid_1.png",
        "x": 2.968,
        "y": 1.634,
        "z": -14.922
    },
    {
        "personId": "00072617",
        "name": "İBRAHİM KÜÇÜK",
        "grid_filename": "grid_1.png",
        "x": 2.967,
        "y": 1.257,
        "z": -16.115
    },
    {
        "personId": "00069822",
        "name": "ABDULLAH SEYMEN",
        "grid_filename": "grid_1.png",
        "x": 2.849,
        "y": 0.605,
        "z": -11.373
    },
    {
        "personId": "00062774",
        "name": "EMRAH TEKİNDEMİR",
        "grid_filename": "grid_1.png",
        "x": 2.562,
        "y": 0.133,
        "z": -16.404
    },
    {
        "personId": "00080075",
        "name": "MÜMİNALADAĞ",
        "grid_filename": "grid_1.png",
        "x": 2.954,
        "y": 1.728,
        "z": -14.79
    },
    {
        "personId": "00069934",
        "name": "HÜSEYİN ÖZBEK",
        "grid_filename": "grid_1.png",
        "x": 2.944,
        "y": 1.066,
        "z": -15.894
    },
    {
        "personId": "00078081",
        "name": "ÇAĞRI ALPAK",
        "grid_filename": "grid_1.png",
        "x": -2.981,
        "y": 1.592,
        "z": -12.703
    },
    {
        "personId": "00067991",
        "name": "SEDA LEBLEBİCİ",
        "grid_filename": "grid_1.png",
        "x": 1.953,
        "y": 3.5,
        "z": -7.666
    },
    {
        "personId": "00074328",
        "name": "ENSAR AKÇAY",
        "grid_filename": "grid_1.png",
        "x": -3.01,
        "y": 1.121,
        "z": -8.269
    },
    {
        "personId": "00087324",
        "name": "METİN GÜLŞEN",
        "grid_filename": "grid_1.png",
        "x": -2.915,
        "y": 1.958,
        "z": 0.893
    },
    {
        "personId": "00054299",
        "name": "MAHMUT YAYLA",
        "grid_filename": "grid_1.png",
        "x": 2.562,
        "y": 2.845,
        "z": -10.357
    },
    {
        "personId": "00083057",
        "name": "SELÇUK İNCE",
        "grid_filename": "grid_1.png",
        "x": 1.773,
        "y": 3.68,
        "z": -7.882
    },
    {
        "personId": "00114369",
        "name": "NURETTIN ERDEM GÜNDOGDU",
        "grid_filename": "grid_1.png",
        "x": 2.954,
        "y": 1.069,
        "z": -14.355
    },
    {
        "personId": "00074037",
        "name": "ALPER ÖZYILMAZ",
        "grid_filename": "grid_1.png",
        "x": 2.818,
        "y": 0.509,
        "z": -14.922
    },
    {
        "personId": "00700015",
        "name": "ZAHİD ÖZDOĞAN",
        "grid_filename": "grid_1.png",
        "x": 2.95,
        "y": 1.069,
        "z": -14.645
    },
    {
        "personId": "00088400",
        "name": "HABİBE ESRA ER",
        "grid_filename": "grid_1.png",
        "x": 2.775,
        "y": 2.379,
        "z": 0.405
    },
    {
        "personId": "00054291",
        "name": "MUSTAFA EMRE UZUNHÜSEYİNOĞLU",
        "grid_filename": "grid_1.png",
        "x": 2.743,
        "y": -1.483,
        "z": 4.05
    },
    {
        "personId": "00049945",
        "name": "ERCAN LAÇİN",
        "grid_filename": "grid_1.png",
        "x": 2.405,
        "y": -0.145,
        "z": -15.751
    },
    {
        "personId": "00078680",
        "name": "İBRAHİM DÜNDARAN",
        "grid_filename": "grid_1.png",
        "x": 2.987,
        "y": 1.35,
        "z": -15.896
    },
    {
        "personId": "00074662",
        "name": "AYBİKE BAŞÇİVİ",
        "grid_filename": "grid_1.png",
        "x": 2.717,
        "y": 0.228,
        "z": -14.922
    },
    {
        "personId": "00043858",
        "name": "ERKAN İNCE",
        "grid_filename": "grid_1.png",
        "x": 2.194,
        "y": 0.418,
        "z": -20.404
    },
    {
        "personId": "00062870",
        "name": "DOĞAN CEBECİ",
        "grid_filename": "grid_1.png",
        "x": 2.817,
        "y": 0.508,
        "z": -15.243
    },
    {
        "personId": "00112266",
        "name": "ERGÜNALTIYAPRAK",
        "grid_filename": "grid_1.png",
        "x": 2.989,
        "y": 0.783,
        "z": -1.051
    },
    {
        "personId": "00073673",
        "name": "EREN SÜRÜCÜ",
        "grid_filename": "grid_1.png",
        "x": -2.925,
        "y": 1.967,
        "z": -11.904
    },
    {
        "personId": "00046198",
        "name": "FATİH ATACAN TEMEL",
        "grid_filename": "grid_1.png",
        "x": 2.824,
        "y": 0.511,
        "z": -11.446
    },
    {
        "personId": "00051669",
        "name": "MUZAFFER RİFAİOĞLU",
        "grid_filename": "grid_1.png",
        "x": 2.983,
        "y": 1.541,
        "z": -14.72
    },
    {
        "personId": "00062830",
        "name": "MUHAMMED İKBAL ABAY",
        "grid_filename": "grid_1.png",
        "x": 2.978,
        "y": 1.54,
        "z": -15.315
    },
    {
        "personId": "00110195",
        "name": "KEREM SARP",
        "grid_filename": "grid_1.png",
        "x": 2.961,
        "y": 1.629,
        "z": -15.604
    },
    {
        "personId": "00060083",
        "name": "FATİH HARAS",
        "grid_filename": "grid_1.png",
        "x": 2.7,
        "y": 0.043,
        "z": -11.809
    },
    {
        "personId": "00066749",
        "name": "MUHAMMED EMRECAN İNANÇER",
        "grid_filename": "grid_1.png",
        "x": 2.995,
        "y": 1.438,
        "z": -3.884
    },
    {
        "personId": "00053411",
        "name": "İSMAİL HAKKI KILIÇ",
        "grid_filename": "grid_1.png",
        "x": -2.702,
        "y": 1.498,
        "z": -19.989
    },
    {
        "personId": "00099705",
        "name": "İBRAHİM ZEKİ AKYURT",
        "grid_filename": "grid_1.png",
        "x": 1.766,
        "y": 3.687,
        "z": -8.173
    },
    {
        "personId": "00068047",
        "name": "MERVE ORUÇ",
        "grid_filename": "grid_1.png",
        "x": -2.581,
        "y": 2.8,
        "z": -7.466
    },
    {
        "personId": "123456789",
        "name": "MEHMET ZAHİD UZUNLAR",
        "grid_filename": "grid_1.png",
        "x": 2.801,
        "y": 0.418,
        "z": -12.756
    },
    {
        "personId": "00058381",
        "name": "MEHMET ALAGÖZ",
        "grid_filename": "grid_1.png",
        "x": 2.728,
        "y": 0.137,
        "z": -13.12
    },
    {
        "personId": "123456789",
        "name": "HALİT ERKAN CENGİZ",
        "grid_filename": "grid_1.png",
        "x": 2.845,
        "y": 0.6,
        "z": -10.792
    },
    {
        "personId": "00051458",
        "name": "YİĞİT NELİK",
        "grid_filename": "grid_1.png",
        "x": 3.014,
        "y": 1.352,
        "z": -10.72
    },
    {
        "personId": "00061470",
        "name": "SÜLEYMAN SERDAR YAĞCI",
        "grid_filename": "grid_1.png",
        "x": 2.424,
        "y": 3.032,
        "z": -7.664
    },
    {
        "personId": "00049109",
        "name": "ESRA KAV",
        "grid_filename": "grid_1.png",
        "x": 3.005,
        "y": 1.071,
        "z": -7.663
    },
    {
        "personId": "00058167",
        "name": "GÖKHAN ÇERİ",
        "grid_filename": "grid_1.png",
        "x": 1.563,
        "y": 3.796,
        "z": -18.004
    },
    {
        "personId": "00052426",
        "name": "LATİF CEMRE OKTAR",
        "grid_filename": "grid_1.png",
        "x": 1.374,
        "y": -1.159,
        "z": -15.691
    },
    {
        "personId": "00054115",
        "name": "MEHMET AKALIN",
        "grid_filename": "grid_1.png",
        "x": 2.513,
        "y": -0.236,
        "z": -12.827
    },
    {
        "personId": "00067757",
        "name": "OZAN BELGE",
        "grid_filename": "grid_1.png",
        "x": 2.012,
        "y": 3.31,
        "z": -19.46
    },
    {
        "personId": "00085088",
        "name": "ÖZKAN ELBAN",
        "grid_filename": "grid_1.png",
        "x": 0.28,
        "y": 4.139,
        "z": -19.668
    },
    {
        "personId": "00058565",
        "name": "AHMET KAYA",
        "grid_filename": "grid_1.png",
        "x": 2.1,
        "y": -1.856,
        "z": 3.979
    },
    {
        "personId": "00057801",
        "name": "FAİK DENİZ",
        "grid_filename": "grid_1.png",
        "x": 2.958,
        "y": 1.716,
        "z": -8.176
    },
    {
        "personId": "00063649",
        "name": "DURMUŞ TARIK KARADAĞ",
        "grid_filename": "grid_1.png",
        "x": 3.061,
        "y": -0.894,
        "z": -7.01
    },
    {
        "personId": "00054136",
        "name": "MUHAMMED SONER AYDIN",
        "grid_filename": "grid_1.png",
        "x": 2.1,
        "y": -1.856,
        "z": 3.979
    },
    {
        "personId": "00074400",
        "name": "ABDULKADİR KARAMAN",
        "grid_filename": "grid_1.png",
        "x": 1.946,
        "y": -0.051,
        "z": -19.821
    },
    {
        "personId": "00110381",
        "name": "HADİCE MERYEM OKUMUŞ",
        "grid_filename": "grid_1.png",
        "x": 2.797,
        "y": 0.416,
        "z": -11.083
    },
    {
        "personId": "00065363",
        "name": "OSMAN ŞAFAK KÜÇÜKÇOLAK",
        "grid_filename": "grid_1.png",
        "x": 1.951,
        "y": 3.5,
        "z": -5.703
    },
    {
        "personId": "00067411",
        "name": "YUNUS ÖZLEYEN",
        "grid_filename": "grid_1.png",
        "x": 2.973,
        "y": 1.632,
        "z": -10.502
    },
    {
        "personId": "00110383",
        "name": "TANER ŞAHİN",
        "grid_filename": "grid_1.png",
        "x": 2.987,
        "y": 1.54,
        "z": -11.664
    },
    {
        "personId": "00053157",
        "name": "HALİD KOCA",
        "grid_filename": "grid_1.png",
        "x": 2.697,
        "y": 0.046,
        "z": -10.865
    },
    {
        "personId": "00112269",
        "name": "OKAN CAN KARAKAN",
        "grid_filename": "grid_1.png",
        "x": 8.666,
        "y": 0.752,
        "z": 5.193
    },
    {
        "personId": "00048529",
        "name": "BURÇAK KAYACAN",
        "grid_filename": "grid_1.png",
        "x": 2.379,
        "y": -0.239,
        "z": -15.241
    },
    {
        "personId": "00059111",
        "name": "OSMAN DİNÇER SAYICI",
        "grid_filename": "grid_1.png",
        "x": 2.989,
        "y": 1.54,
        "z": -12.681
    },
    {
        "personId": "00073678",
        "name": "AHMET FARUK TUNA",
        "grid_filename": "grid_1.png",
        "x": 2.825,
        "y": 0.512,
        "z": -13.481
    },
    {
        "personId": "00059707",
        "name": "DENİZ DEMİROĞLU",
        "grid_filename": "grid_1.png",
        "x": 2.612,
        "y": 0.136,
        "z": -15.534
    },
    {
        "personId": "00117237",
        "name": "HASAN DOĞAN",
        "grid_filename": "grid_1.png",
        "x": 2.723,
        "y": 0.138,
        "z": -11.082
    },
    {
        "personId": "00072609",
        "name": "HÜSEYİN GÜZEL",
        "grid_filename": "grid_1.png",
        "x": 2.98,
        "y": 1.443,
        "z": -16.406
    },
    {
        "personId": "00063983",
        "name": "NECMİ BARIŞ ÜLGAY",
        "grid_filename": "grid_1.png",
        "x": -0.677,
        "y": 4.115,
        "z": -17.518
    },
    {
        "personId": "00051524",
        "name": "ÖZLEM ÖNCEL",
        "grid_filename": "grid_1.png",
        "x": -2.996,
        "y": 0.752,
        "z": 0.749
    },
    {
        "personId": "00061465",
        "name": "MEHMET FARUK GURULKAN",
        "grid_filename": "grid_1.png",
        "x": 2.874,
        "y": 0.699,
        "z": -12.905
    },
    {
        "personId": "00073938",
        "name": "ALİ BATTAL",
        "grid_filename": "grid_1.png",
        "x": 2.66,
        "y": 0.043,
        "z": -13.481
    },
    {
        "personId": "00067014",
        "name": "FATİH TUNEL",
        "grid_filename": "grid_1.png",
        "x": 2.048,
        "y": 3.406,
        "z": -7.592
    },
    {
        "personId": "00063566",
        "name": "MUHARREM REÇBER",
        "grid_filename": "grid_1.png",
        "x": 2.288,
        "y": -1.782,
        "z": 4.416
    },
    {
        "personId": "00054925",
        "name": "SELİM KAHRAMAN",
        "grid_filename": "grid_1.png",
        "x": 2.986,
        "y": 1.53,
        "z": -8.245
    },
    {
        "personId": "00069386",
        "name": "HİLMİ HAKAN KAHRAMAN",
        "grid_filename": "grid_1.png",
        "x": 2.047,
        "y": 3.408,
        "z": -8.029
    },
    {
        "personId": "00053817",
        "name": "SELİM KAHRIMAN",
        "grid_filename": "grid_1.png",
        "x": -2.915,
        "y": 1.958,
        "z": 0.893
    },
    {
        "personId": "00054196",
        "name": "FEDAİ SAİT EŞ",
        "grid_filename": "grid_1.png",
        "x": -2.888,
        "y": 2.148,
        "z": -1.726
    },
    {
        "personId": "00089802",
        "name": "ÖMER YUSUF KARAOĞLU",
        "grid_filename": "grid_1.png",
        "x": 1.661,
        "y": 3.774,
        "z": -16.406
    },
    {
        "personId": "00067657",
        "name": "ABDURRAHİM DÜZCAN",
        "grid_filename": "grid_1.png",
        "x": 2.706,
        "y": 0.506,
        "z": -17.786
    },
    {
        "personId": "00051478",
        "name": "ÖZGÜR KOCABAY",
        "grid_filename": "grid_1.png",
        "x": 2.974,
        "y": 1.634,
        "z": -13.12
    },
    {
        "personId": "00047026",
        "name": "SERKAN MURAT AKHARMAN",
        "grid_filename": "grid_1.png",
        "x": 2.41,
        "y": 2.842,
        "z": -19.314
    },
    {
        "personId": "123456789",
        "name": "MUSTAFA AKIN TERZİOĞLU",
        "grid_filename": "grid_1.png",
        "x": -2.156,
        "y": -0.653,
        "z": -14.303
    },
    {
        "personId": "00088016",
        "name": "KAZIM APALI",
        "grid_filename": "grid_1.png",
        "x": 3.247,
        "y": -0.879,
        "z": -5.702
    },
    {
        "personId": "00123820",
        "name": "HAMDİ CEM KARADAŞ",
        "grid_filename": "grid_1.png",
        "x": 0.661,
        "y": 4.052,
        "z": -20.247
    },
    {
        "personId": "00108618",
        "name": "ALI KORHAN USTUNER",
        "grid_filename": "grid_1.png",
        "x": -1.996,
        "y": 3.464,
        "z": -12.048
    },
    {
        "personId": "00045021",
        "name": "BÜNYAMİNAKYILDIZ",
        "grid_filename": "grid_1.png",
        "x": 2.922,
        "y": 0.88,
        "z": -12.389
    },
    {
        "personId": "00020134",
        "name": "MURAT ŞEKER",
        "grid_filename": "grid_1.png",
        "x": 2.775,
        "y": 0.318,
        "z": -12.973
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
