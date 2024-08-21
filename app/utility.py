import math
from datetime import timedelta
from constants import PAGINATION_LIMIT, NUMBER_OF_NEWS_ARTICLES_PER_REQUEST
from random import randint

from bson import ObjectId

# used
def to_ObjectId(input_id: str) -> ObjectId:
    return ObjectId(input_id)


def generate_code(digits=6):
    range_start = 10 ** (digits - 1)
    range_end = (10**digits) - 1
    return randint(range_start, range_end)


def paginate_query(query, total_count, page_number=1):
    skip_count = (page_number - 1) * PAGINATION_LIMIT
    number_of_pages = get_pages_number(total_count)
    results = list(query.skip(skip_count).limit(PAGINATION_LIMIT))
    for item in results:
        if item.get("_id"):
            item["_id"] = str(item["_id"])

    return {"results": list(results), "number_of_pages": number_of_pages}


def get_pages_number(total_count):
    return math.ceil(total_count / PAGINATION_LIMIT)


def months_to_timedelta(months):
    days = months * 30  # Approximate a month as 30 days
    return timedelta(days=days)


def build_proxy_for_news_engine(task):
    if task.get("proxy"):
        return {
            "proxyUrl": task.get("proxy").get("proxy_url"),
            "proxyPublic_ip": task.get("proxy").get("proxy_ip"),
            "proxyUsername": task.get("proxy").get("proxy_username"),
            "proxyPassword": task.get("proxy").get("proxy_password"),
        }


def build_task_details_for_news_engine(task):
    task_details = {
        "query": task.get("keyword"),
        "numberOfPosts": NUMBER_OF_NEWS_ARTICLES_PER_REQUEST,
        "interaction_depth": 1,
        "numberOfPages": 1,
        "fetchFullArticle": True,
    }
    if task.get("country"):
        task_details["country"] = task.get("country")

    if task.get("language"):
        task_details["language"] = task.get("language")

    if task.get("topic") or task.get("is_topic"):
        task_details["searchType"] = "Topic"

    return task_details


def build_task_for_news_engine(task):
    engine_task = {
        "_id": str(task.get("_id")),
        "id": str(task.get("_id")),
        "majorType": task.get("major_type"),
        "status": task.get("status"),
        "feedback": task.get("feedback"),
        "attacker": {
            "_id": "",
            "username": "",
            "password": "",
            "proxy": build_proxy_for_news_engine(task),
        },
        "target": "news",
        "type": task.get("orchestrator_key"),
        "createdAt": task.get("created_at"),
        "updatedAt": task.get("updated_at"),
        "details": build_task_details_for_news_engine(task),
    }
    return [engine_task]
