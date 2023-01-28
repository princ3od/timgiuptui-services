from firebase_admin import credentials, firestore, initialize_app
from google.cloud.firestore import Client

firebase_credentials = credentials.Certificate("platform/crec.json")
initialize_app(firebase_credentials)
firestore_db: Client = firestore.client()

sources = {
    "nld": {
        "business": {
            "url": "https://nld.com.vn/kinh-te.rss",
        },
        "entertainment": {
            "url": "https://nld.com.vn/giai-tri.rss",
        },
        "news": {
            "url": "https://nld.com.vn/thoi-su.rss",
        },
        "sport": {
            "url": "https://nld.com.vn/the-thao.rss",
        },
        "technology": {
            "url": "https://nld.com.vn/cong-nghe.rss",
        },
        "travel": {
            "url": "https://nld.com.vn/du-lich-xanh.rss",
        },
    },
    "vnexpress": {
        "business": {
            "url": "https://vnexpress.net/rss/kinh-doanh.rss",
        },
        "entertainment": {
            "url": "https://vnexpress.net/rss/giai-tri.rss",
        },
        "news": {
            "url": "https://vnexpress.net/rss/thoi-su.rss",
        },
        "sport": {
            "url": "https://vnexpress.net/rss/the-thao.rss",
        },
        "technology": {
            "url": "https://vnexpress.net/rss/so-hoa.rss",
        },
        "travel": {
            "url": "https://vnexpress.net/rss/du-lich.rss",
        },
    },
    "tuoitre": {
        "business": {
            "url": "https://tuoitre.vn/rss/kinh-doanh.rss",
        },
        "entertainment": {
            "url": "https://tuoitre.vn/rss/giai-tri.rss",
        },
        "news": {
            "url": "https://tuoitre.vn/rss/thoi-su.rss",
        },
        "sport": {
            "url": "https://tuoitre.vn/rss/the-thao.rss",
        },
        "technology": {
            "url": "https://tuoitre.vn/rss/nhip-song-so.rss",
        },
        "travel": {
            "url": "https://tuoitre.vn/rss/du-lich.rss",
        },
    },
}

editors = {
    "nld": {
        "logo": "",
        "name": "Người Lao Động",
        "url": "https://nld.com.vn",
        "slogan": "",
    },
    "vnexpress": {
        "logo": "https://s1.vnecdn.net/vnexpress/restruct/i/v75/v2_2019/pc/graphics/logo.svg",
        "name": "VnExpress",
        "url": "https://vnexpress.net",
        "slogan": "",
    },
    "tuoitre": {
        "logo": "https://static.mediacdn.vn/tuoitre/web_images/logottonew_tet_2023.png",
        "name": "Tuổi Trẻ",
        "url": "https://tuoitre.vn",
        "slogan": "",
    },
}

topics = {
    "news": {
        "name": "Tin tức",
        "ordinal": 1,
    },
    "business": {
        "name": "Kinh doanh",
        "ordinal": 2,
    },
    "entertainment": {
        "name": "Giải trí",
        "ordinal": 3,
    },
    "sport": {
        "name": "Thể thao",
        "ordinal": 4,
    },
    "technology": {
        "name": "Công nghệ",
        "ordinal": 5,
    },
    "travel": {
        "name": "Du lịch",
        "ordinal": 6,
    },
}

# firestore_db.collection("sources").document("content").set(sources)

# firestore_db.collection("editors").document("content").set(editors)

firestore_db.collection("topics").document("content").set(topics)
