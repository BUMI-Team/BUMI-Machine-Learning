
# BUMI Recommender API

# 1) Video Recommender
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
    "description": "FROZEN FOOD MODAL KECIL! OWNERNYA MASIH KECIL OMSET 130JUTA PERBULAN ...",
    "genre": "Kuliner|Review",
    "id": "reeDm_UdZPY",
    "thumbnail": "https://i.ytimg.com/vi/reeDm_UdZPY/mqdefault.jpg",
    "title": "FROZEN FOOD MODAL KECIL! OWNERNYA IMUT, OMSETNYA130JUTA PERBULAN (2021)"
  },
  {
    "description": "Bisnis yang lagi hits dimasa pandemi frozen food nuget ekonomis dari 1/4 daging ayam jadi 7 pack isi 10 pcs dengan modal ...",
    "genre": "Kuliner|Tutorial|Review",
    "id": "xOJiNBjx8zg",
    "thumbnail": "https://i.ytimg.com/vi/xOJiNBjx8zg/mqdefault.jpg",
    "title": "Ide bisnis frozen food ekonomis modal 20K jual 70K bisnis (2021)"
  },
  ...
]
```

# 2) Business Recommender
API for recommending business reference for new user which have not business yet

## API Reference

### Get Recommendation Based on Collaborative Filtering between users

#### Route
```http
  POST /api/v1/bRecommendation
```
#### Request Example
```json
{
  "user_id": "ycfqjQk3TvVCkXkhzi2jPNvdGZF2"
}
```
#### Response Example
```json
{
  "jenis_usaha": "Usaha Menengah",
  "rekomendasi": [
    "Gilbert Medical",
    "Toko Alat Kesehatan Bandung",
    "Toko Alat Kesehatan Tokopedia"
  ],
  "bidang_usaha": [
    "rumah tangga",
    "kesehatan"
  ]
}
```