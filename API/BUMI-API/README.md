
# Recommender API

API for recommending videos based on watch history of a user

## API Reference

### Get Recommendation Based on Watch History

#### Route
```http
  POST /api/v1/inference
```
#### Request Example
```json
{
  "user_request": ["string"],
  "ids": [21,22,23,25,25,26,27,28,29,210]
}
```
#### Response Example
```json
[
  {
    "description": "Hallo temen2 buat yang mau bisa import kuy merapat jangan lupa tonton videonya sampe abis ya �?� Buat yang mau daftar ...",
    "genre": "Kuliner|Homecare|Healthcare|Tutorial",
    "id": "rhA8KSyXAgQ",
    "noID": 109,
    "thumbnail": "https://i.ytimg.com/vi/rhA8KSyXAgQ/mqdefault.jpg",
    "title": "CARA IMPORT BARANG DARI CHINA KE INDONESIA UNTUK PEMULA DIJAMIN AUTO BISA IMPORT ! (2021)"
  },
  {
    "description": "Assalamualaikum Hay semuanyaaaa apa kabar nih tmn tmn semoga sehat terus yaaa, jasmani dan ruhaninya ?? aamiin ...",
    "genre": "Kuliner|Tutorial",
    "id": "MEdw7g01kMQ",
    "noID": 8,
    "thumbnail": "https://i.ytimg.com/vi/MEdw7g01kMQ/mqdefault.jpg",
    "title": "IDE BISNIS FROZEN FOOD !! HEKENG PALING PREMIUM ALA WAIS ALQORNI �?�??�?Ǭ�� DIJAMIN LARIS MANIS (2021)"
  },
  ...
]
```

### Get Recommendation Based on Genre

#### Route
```http
  POST /api/v1/genre
```
#### Request Example
```json
{
  "genre": "Healthcare"
}
```
#### Response Example
```json
[
    {
        "description": "selamat datang di channel top produk masker beneran full face nih Produk unik #SHORTS #tiktok #unik #gadgets #china ...",
        "genre": "Healthcare|Review",
        "id": "4F1Bz-Jr9ec",
        "noID": 129,
        "thumbnail": "https://i.ytimg.com/vi/4F1Bz-Jr9ec/mqdefault.jpg",
        "title": "masker beneran full face nih Produk unik #SHORTS #tiktok #unik #gadgets #china (2021)"
    },
    {
        "description": "dropshipper #suppliertanganpertama #caramencarisupplier #bisnisonline #shopee #ideusaha #dropship #reseller #carajualan ...",
        "genre": "Kuliner|Homecare|Healthcare|Tutorial|Ecommerce",
        "id": "1iFTX5l7KYU",
        "noID": 195,
        "thumbnail": "https://i.ytimg.com/vi/1iFTX5l7KYU/mqdefault.jpg",
        "title": "Cara Mencari Supplier Tangan Pertama Di Shopee 2022 - Bisnis Modal Kecil Untung Besar - Ide Usaha (2021)"
    },
  ...
]
```


