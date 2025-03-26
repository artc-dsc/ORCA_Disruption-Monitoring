from fastapi import APIRouter, HTTPException, Request, Query
from typing import Optional, List, Dict
import app.utils as utils
import app.models.models as mod
from bson import ObjectId
from datetime import datetime
from fastapi.responses import FileResponse
import os
import pickle 
import pyLDAvis

router = APIRouter()

@router.get("/",
    summary="Default",
    description="Default",
    response_description="Empty response",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "message": "Default Page: Please specify route for relevant output"
                    }
                }
            },
        },
    },)
def root():
    return {"message": "Default Page: Please specify route for relevant output"}

@router.get("/data/all",
    summary="Finds all data from database",
    description="All data from database. You can input limit=integer to show only documents up to limit. If not specified, all documents will show.",
    response_description="List of data from database",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "_id": "67628aa0422c93410a6a1314",
                        "url": "https://securityaffairs.com/172059/security/u-s-cisa-adds-microsoft-windows-kernel-mode-driver-and-adobe-coldfusion-flaws-to-its-known-exploited-vulnerabilities-catalog.html",
                        "disruptionType": "Political",
                        "imageUrl": "https://securityaffairs.com/wp-content/uploads/2020/07/CISA.jpeg",
                        "isdeleted": "false",
                        "lat": 38.7945952,
                        "lng": -106.5348379,
                        "location": "United States",
                        "publishedDate": "2024-12-17T08:23:49Z",
                        "radius": 11134.1553838169,
                        "raw_text": "U.S. CISA adds Microsoft Windows Kernel-Mode Driver and Adobe ColdFusion flaws to its Known Exploited Vulnerabilities catalog\r\n | ConnectOnCall data breach impacted over 900,000 individuals\r\n | Repor… [+124062 chars]",
                        "severity": "High",
                        "text": "The U.S. Cybersecurity and Infrastructure Security Agency (CISA) has included vulnerabilities in the Microsoft Windows Kernel-Mode Driver and Adobe ColdFusion to its Known Exploited Vulnerabilities catalog, highlighting their potential risks. Additionally, a data breach at ConnectOnCall has affected over 900,000 individuals, raising concerns about data security. These developments underscore the ongoing threats posed by software vulnerabilities and data breaches in the digital landscape.",
                        "title": "U.S. CISA adds Microsoft Windows Kernel-Mode Driver and Adobe ColdFusion flaws to its Known Exploited Vulnerabilities catalog",
                        "actual_text": "U.S. CISA adds Microsoft Windows Kernel-Mode Driver and Adobe ColdFusion flaws to its Known Exploited Vulnerabilities catalog\n\nPierluigi Paganini December 17, 2024 December 17, 2024\n\nU.S. Cybersecurity and Infrastructure Security Agency (CISA) adds Microsoft Windows Kernel-Mode Driver and Adobe ColdFusion flaws to its Known Exploited Vulnerabilities catalog...",
                        "sentiment": "null",
                        "wordcloud": "null"
                    }
                }
            },
        },
        404: {
            "description": "Invalid query specified",
            "content": {
                "application/json": {
                    "example": {"message": "Unexpected query parameter"}
                }
            },
        },
    },
)
async def get_alldata(request: Request, limits: Optional[int] = Query(None, ge=int(1)))-> List[mod.news]:
    allowed_params = ["limits"]
    extra_params = [key for key in request.query_params if key not in allowed_params]

    if extra_params:
        raise HTTPException(status_code=404, detail="Unexpected query parameter")
    
    db = request.app.news

    if limits is None:
        response = list(db.find({}))

    else:
        response = list(db.find({}).limit(limits))
    documents = []
    for item in response:
        item["_id"] = str(item.get("_id"))
        if item.get("imageUrl") == "No Image" or item.get("imageUrl") == "":
            item["imageUrl"] = None

        documents.append(mod.news(**item))
    return documents

@router.get("/data",
    summary="Finds data from database based on column and specified value",
    description="Finds data from database based on column and specified value. Specify column with column=, and specify value with value= . If value not specified, all data is shown. Search query is case insensitive.",
    response_description="List of data from database",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "_id": "67628aa0422c93410a6a1314",
                        "url": "https://securityaffairs.com/172059/security/u-s-cisa-adds-microsoft-windows-kernel-mode-driver-and-adobe-coldfusion-flaws-to-its-known-exploited-vulnerabilities-catalog.html",
                        "disruptionType": "Political",
                        "imageUrl": "https://securityaffairs.com/wp-content/uploads/2020/07/CISA.jpeg",
                        "isdeleted": "false",
                        "lat": 38.7945952,
                        "lng": -106.5348379,
                        "location": "United States",
                        "publishedDate": "2024-12-17T08:23:49Z",
                        "radius": 11134.1553838169,
                        "raw_text": "U.S. CISA adds Microsoft Windows Kernel-Mode Driver and Adobe ColdFusion flaws to its Known Exploited Vulnerabilities catalog\r\n | ConnectOnCall data breach impacted over 900,000 individuals\r\n | Repor… [+124062 chars]",
                        "severity": "High",
                        "text": "The U.S. Cybersecurity and Infrastructure Security Agency (CISA) has included vulnerabilities in the Microsoft Windows Kernel-Mode Driver and Adobe ColdFusion to its Known Exploited Vulnerabilities catalog, highlighting their potential risks. Additionally, a data breach at ConnectOnCall has affected over 900,000 individuals, raising concerns about data security. These developments underscore the ongoing threats posed by software vulnerabilities and data breaches in the digital landscape.",
                        "title": "U.S. CISA adds Microsoft Windows Kernel-Mode Driver and Adobe ColdFusion flaws to its Known Exploited Vulnerabilities catalog",
                        "actual_text": "U.S. CISA adds Microsoft Windows Kernel-Mode Driver and Adobe ColdFusion flaws to its Known Exploited Vulnerabilities catalog\n\nPierluigi Paganini December 17, 2024 December 17, 2024\n\nU.S. Cybersecurity and Infrastructure Security Agency (CISA) adds Microsoft Windows Kernel-Mode Driver and Adobe ColdFusion flaws to its Known Exploited Vulnerabilities catalog...",
                        "sentiment": "null",
                        "wordcloud": "null"
                    }
                }
            },
        },
        400: {
            "description": "Invalid column specified",
            "content": {
                "application/json": {
                    "example": {"message": "Invalid column specified"}
                }
            },
        },
        404: {
            "description": "Invalid query specified",
            "content": {
                "application/json": {
                    "example": {"message": "Unexpected query parameter"}
                }
            },
        },
    },
)
async def get_filtereddata(request: Request, column: str, value: str = "") -> List[mod.news]:
    allowed_params = ["column", "value"]
    extra_params = [key for key in request.query_params if key not in allowed_params]

    if extra_params:
        raise HTTPException(status_code=404, detail="Unexpected query parameter")
    
    valid_columns = ["_id", "url", "disruptionType", "imageUrl", "isdeleted", "lat", "lng", "location", "publishedDate", "radius", "raw_text", "severity", "text", "title", "actual_text"]
    if column not in valid_columns:
        raise HTTPException(status_code=400, detail="Invalid column specified")

    db = request.app.news
    if value == "":
        response = list(db.find({}))
    else: 
        if column == "_id":
            response = list(db.find({column: ObjectId(value)}))
        else:
            regex = {'$regex': value, '$options': 'i'}
            response = list(db.find({column: regex}))

    documents = []
    for item in response:
        item["_id"] = str(item.get("_id"))
        if item.get("imageUrl") == "No Image" or item.get("imageUrl") == "":
            item["imageUrl"] = None

        documents.append(mod.news(**item))

    return documents

#SENTIMENTS
@router.put("/update/sentiments",
    summary="Updates sentiment for doc specified.",
    description="Finds data from database based on _id and updates sentiment value. Specify doc id with _id. If _id not specified or invalid, it will not go through. This a PUT operation, refer to example on GitHub README on how to pull the info",
    response_description="Confirmation that Doc is updated with Sentiment Score, along with id and sentiment",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "update": "True",
                        "_id": "67628aa0422c93410a6a1314",
                        "sentiment": 0.997,
                    }
                }
            },
        },
        400: {
            "description": "Invalid _id specified",
            "content": {
                "application/json": {
                    "example": {"message": "Invalid _id specified"}
                }
            },
        }
    },
)
async def update_sentiment(request: Request, _id: str = Query(..., alias="_id")):
    allowed_params = ["id", "_id"]
    extra_params = [key for key in request.query_params if key not in allowed_params]

    if extra_params:
        raise HTTPException(status_code=404, detail="Unexpected query parameter")
    
    db = request.app.news
    try:
        object_id = ObjectId(_id)
        document = db.find_one({"_id": object_id})
        text = document.get("actual_text", "None")
        score = utils.input_sentiments_vader(text)
        result = db.update_one(
            {"_id": object_id},
            {"$set": {"sentiment": score}}
        )
        if result.modified_count == 0:
            if not document:
                raise HTTPException(status_code=404, detail="Document not found")
            else:
                raise HTTPException(status_code=404, detail="Field unchanged")
        else:
            update_doc = db.find_one({"_id": object_id})
            return {"update": True, "id": str(update_doc["_id"]), "sentiment": update_doc.get("sentiment", None)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/update/sentiments/all",
    summary="Updates sentiment for all docs without sentiments",
    description="Finds data from database where sentiment has not been updated. The sentiment scores are then calculated and added. When completed, output will return True. If all data has sentiments, update will return False. refer to example on GitHub README on how to pull the info",
    response_description="Confirmation that all docs is updated with Sentiment Score, or that update is not required as all data has sentiment scores",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "update": "True"
                    }
                }
            },
        },
        404: {
            "description": "Invalid query specified",
            "content": {
                "application/json": {
                    "example": {"message": "Unexpected query parameter"}
                }
            },
        },
        500: {
            "description": "Invalid _id specified",
            "content": {
                "application/json": {
                    "example": {"message": "10/100 sentiment unchanged"}
                }
            },
        }
    },
)
async def update_all_sentiment(request: Request):
    db = request.app.news
    allowed_params = []
    extra_params = [key for key in request.query_params if key not in allowed_params]

    if extra_params:
        raise HTTPException(status_code=404, detail="Unexpected query parameter")
    try:
        document = db.find({"sentiment": {"$exists": False}}) 
        to_modify= db.count_documents({"sentiment": {"$exists": False}})
        modified = 0
        if to_modify==0:
            return {'update': False}
        for doc in document:
            text = doc.get("actual_text", "None")
            score = utils.input_sentiments_vader(text)
            result = db.update_one(
                {"_id": doc.get("_id")},
                {"$set": {"sentiment": score}}
            )
            if result.modified_count != 0:
                modified += 1

        if modified/to_modify <= 0:
            raise HTTPException(status_code=500, detail=f"{to_modify-modified}/{to_modify} sentiment unchanged")
        else:
            return {"update": True}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/get_sentiment",
    response_model=mod.TimeSeriesData, 
    summary="Provides sentiment by date",
    description="""Provides sentiment by date. Sentiment score is aggregated based on specification. 
    Please input either sum/average/positive_count/negative_count/total_count using query: aggregate= . 
    Specify date_only=True so that the aggregation is by date and not the exact time.
    Specify filter_column= and filter_value= to filter data by, ensure that column is written in proper casing. Value is not case sensitive""",
    response_description="Provides sentiment by date given type of aggregation",
    responses={
        200: {
            "content": {
                "application/json": {
                    "data": {
                        "2024-12-17T00:00:00": 2, 
                        "2024-12-18T00:00:00": 1,
                    }
                }
            },
        },
        400: {
            "description": "Invalid aggregation method specified",
            "content": {
                "application/json": {
                    "example": {"message": "Invalid aggregation method specified"}
                }
            },
        },
        404: {
            "description": "Invalid query specified",
            "content": {
                "application/json": {
                    "example": {"message": "Unexpected query parameter"}
                }
            },
        },
        422: {
            "description": "Filter value not specified",
            "content": {
                "application/json": {
                    "example": {"message": "Filter value not specified"}
                }
            },
        },
    },
)
async def get_sentiment(request: Request, aggregate: str, date_only: bool = False, filter_column:str = None , filter_value:str = None) -> mod.TimeSeriesData:
    allowed_params = ["aggregate", "date_only", "filter_column", "filter_value"]
    extra_params = [key for key in request.query_params if key not in allowed_params]

    if extra_params:
        raise HTTPException(status_code=404, detail="Unexpected query parameter")
    
    valid_methods = ["sum", "average", "positive_count", "negative_count", "total_count"]
    if aggregate not in valid_methods:
        raise HTTPException(status_code=400, detail="Invalid aggregation method specified")

    if filter_column != None:
        if filter_value == None:
            raise HTTPException(status_code=422, detail="Filter value not specified")

    db = request.app.news
    if filter_column == None:
        documents = db.find({"sentiment": {"$exists": True}})
    else:
        regex = {'$regex': filter_value, '$options': 'i'}
        documents = db.find({
            "ner": {"$exists": True},
            filter_column: regex
        })
    tracker_averaging = {}
    sentiment_per_date = {}
    for doc in documents:
        if date_only == True:
            date = str(doc.get("publishedDate"))[:10]
        else:
            date = str(doc.get("publishedDate"))
        sentiment = doc.get("sentiment")
        if aggregate == "sum":
            if date not in sentiment_per_date:
                sentiment_per_date[date] = sentiment
            else:
                sentiment_per_date[date] = sentiment_per_date.get(date) + sentiment
        elif aggregate == "average":
            if date not in sentiment_per_date:
                tracker_averaging[date] = {
                    "sum": sentiment,
                    "count": 1,
                }
            else:
                tracker_averaging[date]["sum"] = (tracker_averaging.get(date)).get("sum") + sentiment
                tracker_averaging[date]["count"] = (tracker_averaging.get(date)).get("count") + 1
        else:
            if aggregate == "positive_count":
                if sentiment > 0:
                    if date not in sentiment_per_date:
                        sentiment_per_date[date] = 1
                    else:
                        sentiment_per_date[date] = sentiment_per_date.get(date) + 1
            elif aggregate == "negative_count":
                if sentiment < 0:
                    if date not in sentiment_per_date:
                        sentiment_per_date[date] = 1
                    else:
                        sentiment_per_date[date] = sentiment_per_date.get(date) + 1
            else:
                if date not in sentiment_per_date:
                    sentiment_per_date[date] = 1
                else:
                    sentiment_per_date[date] = sentiment_per_date.get(date) + 1
    
    if aggregate == "average":
        for key, value in tracker_averaging.items():
            sentiment_per_date[key] = value.get("sum")/value.get("count")
    return {"data": sentiment_per_date}

#NER
@router.put("/update/ner",
    summary="Updates NER for doc specified.",
    description="Finds data from database based on _id and updates NERs detected. Specify doc id with _id=. If value not specified, operation will not go through. This a PUT operation, refer to example on GitHub README on how to pull the info",
    response_description="Confirmation that Doc is updated with NER outputs, along with id and NER values",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "update": "True",
                        "_id": "67628aa0422c93410a6a1314",
                        "ner": {
                            "country": ["U.S."],
                            "organisation": ["CISA","U.S. Cybersecurity and Infrastructure Security Agency","FCEB agencies","federal agencies"],"person": ["Pierluigi Paganini"]
                        },
                    }
                }
            },
        },
        400: {
            "description": "Invalid _id specified",
            "content": {
                "application/json": {
                    "example": {"message": "Invalid column specified"}
                }
            },
        }
    },
)
async def update_ner(request: Request, _id: str = Query(..., alias="_id")):
    allowed_params = ["id", "_id"]
    extra_params = [key for key in request.query_params if key not in allowed_params]

    if extra_params:
        raise HTTPException(status_code=404, detail="Unexpected query parameter")
    
    db = request.app.news
    try:
        object_id = ObjectId(_id)
        document = db.find_one({"_id": object_id})
        text = document.get("actual_text")
        if text == "":
            text = document.get("text")
            if text == "":
                text = document.get("title", "")
        ner_dict = utils.gliner_ner(text)
        print(ner_dict)

        result = db.update_one(
            {"_id": object_id},
            {"$set": {"ner": ner_dict}}
        )
        if result.modified_count == 0:
            if not document:
                raise HTTPException(status_code=404, detail="Document not found")
            else:
                raise HTTPException(status_code=404, detail="Field unchanged")
        else:
            update_doc = db.find_one({"_id": object_id})
            return {"update": True, "id": str(update_doc["_id"]), "ner": update_doc.get("ner", None)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/update/ner/all",
    summary="Updates NER for all docs without NER",
    description="Finds data from database where NER has not been updated. The NER values are then calculated and added. When completed, output will return True. If all data has NER, update will return False. refer to example on GitHub README on how to pull the info",
    response_description="Confirmation that all docs is updated with NER, or that update is not required as all data has NER values",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "update": "True"
                    }
                }
            },
        },
        404: {
            "description": "Invalid query specified",
            "content": {
                "application/json": {
                    "example": {"message": "Unexpected query parameter"}
                }
            },
        },
        500: {
            "description": "Invalid _id specified",
            "content": {
                "application/json": {
                    "example": {"message": "10/100 sentiment unchanged"}
                }
            },
        }
    },
)
async def update_all_ner(request: Request):
    db = request.app.news
    allowed_params = []
    extra_params = [key for key in request.query_params if key not in allowed_params]

    if extra_params:
        raise HTTPException(status_code=404, detail="Unexpected query parameter")
    try:
        document = db.find({"ner": {"$exists": True}}) 
        to_modify= db.count_documents({"ner": {"$exists": True}})
        modified = 0
        if to_modify==0:
            return {'update': False}
        document = db.find()
        for doc in document:
            text = doc.get("actual_text")
            if text == "":
                text = doc.get("text")
                if text == "":
                    text = doc.get("title")
            ner_dict = utils.gliner_ner(text)
            result = db.update_one(
                {"_id": doc.get("_id")},
                {"$set": {"ner": ner_dict}}
            )
            if result.modified_count != 0:
                modified += 1

        if modified/to_modify <= 0:
            raise HTTPException(status_code=500, detail=f"{to_modify-modified}/{to_modify} NER unchanged")
        else:
            return {"update": True}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/get_ner",
    response_model=mod.TimeSeriesData_Dict, 
    summary="Provides sentiment by date",
    description="""Provides sentiment by date. Sentiment score is aggregated based on specification. 
    Specify date_only=True so that the aggregation is by date and not the exact time.
    Specify filter_column= and filter_value= to filter data by, ensure that column is written in proper casing. Value is not case sensitive""",
    response_description="Provides sentiment by date given type of aggregation",
    responses={
        200: {
            "content": {
                "application/json": {
                    "data": {
                        "2024-12-17T00:00:00": 2, 
                        "2024-12-18T00:00:00": 1,
                    }
                }
            },
        },
        404: {
            "description": "Invalid query specified",
            "content": {
                "application/json": {
                    "example": {"message": "Unexpected query parameter"}
                }
            },
        },
        422: {
            "description": "Filter value not specified",
            "content": {
                "application/json": {
                    "example": {"message": "Filter value not specified"}
                }
            },
        },
    },
)
async def get_ner(request: Request, date_only: bool = False, filter_column:str = None , filter_value:str = None) -> mod.TimeSeriesData_Dict:
    allowed_params = ["date_only", "filter_column", "filter_value"]
    extra_params = [key for key in request.query_params if key not in allowed_params]

    if extra_params:
        raise HTTPException(status_code=404, detail="Unexpected query parameter")

    if filter_column != None:
        if filter_value == None:
            raise HTTPException(status_code=422, detail="Filter value not specified")

    db = request.app.news
    if filter_column == None:
        documents = db.find({"ner": {"$exists": True}})
    else:
        regex = {'$regex': filter_value, '$options': 'i'}
        documents = db.find({
            "ner": {"$exists": True},
            filter_column: regex
        })

    ner_per_date: Dict[str, Dict[str, list]] = {}
    for doc in documents:
        date = str(doc.get("publishedDate"))
        if date_only == True:
            date = date[:10]
        date_obj = datetime.fromisoformat(date.replace("Z", ""))
        date_key = str(date_obj.isoformat())
        if date_key not in ner_per_date:
            ner_per_date[date_key] = {}
        ner_dict = doc.get("ner")
        if not ner_dict: 
            continue
        else:
            for key, value in ner_dict.items():
                if key not in ner_per_date[date_key]:
                    ner_per_date[date_key][key] = []
                for val in value:
                    ner_per_date[date_key][key].append(val)

    return mod.TimeSeriesData_Dict(data=ner_per_date)


@router.get("/get_topic_model_pyLDAvis",
    response_model=mod.Topic_Modelling_pyLDAvis, 
    summary="Provides topic modelling data from pyLDAvis",
    description="""Provides the top few relevant terms associated with each grouped topic. Provide number of topics to group be with num_topics= , provide number of relevant terms to include with relevant_terms= (Default is 10)""",
    response_description="Provides the relevant terms associated with each grouped topic",
    responses={
        200: {
            "content": {
                "application/json": {
                    "data": {
                        "2024-12-17T00:00:00": 2, 
                        "2024-12-18T00:00:00": 1,
                    }
                }
            },
        },
        404: {
            "description": "Invalid query specified",
            "content": {
                "application/json": {
                    "example": {"message": "Unexpected query parameter"}
                }
            },
        },
        422: {
            "description": "Filter value not specified",
            "content": {
                "application/json": {
                    "example": {"message": "Filter value not specified"}
                }
            },
        },
    },
)
async def get_pyLDAvis_data(request: Request, num_topics: int = None, relevant_terms: int = 10) -> mod.Topic_Modelling_pyLDAvis:
    allowed_params = ["num_topics", "relevant_terms"]
    extra_params = [key for key in request.query_params if key not in allowed_params]

    if extra_params:
        raise HTTPException(status_code=404, detail="Unexpected query parameter")

    if num_topics == None:
        raise HTTPException(status_code=422, detail="Number of topics value not specified")

    db = request.app.news
    documents = db.find()

    topics_data: Dict[str, str] = {}
    text = []
    for doc in documents:
        text.append(doc.get("actual_text"))
    score_data, topics_data = utils.generate_pyLDAvis_topics(text, num_topics, relevant_terms)
        
    return mod.Topic_Modelling_pyLDAvis(score= score_data, data=topics_data)


@router.get("/get_topic_model_pyLDAvis/visual",
    summary="Provides topic modelling graphics",
    description="""Provides the pyLDAvis visualisations as a downloadable file. Provide path to download if a volume is mounted with docker container (Otherwise default downloaded to download file)""",
    response_description="NA",
    responses={
        404: {
            "description": "Invalid query specified",
            "content": {
                "application/json": {
                    "example": {"message": "Unexpected query parameter"}
                }
            },
        },
        422: {
            "description": "Filter value not specified",
            "content": {
                "application/json": {
                    "example": {"message": "Filter value not specified"}
                }
            },
        },
    },
)
async def get_pyLDAvis_visual(request: Request, download_path:str = None,  num_topics: int = None) -> mod.Topic_Modelling_pyLDAvis:
    allowed_params = ["download_path", "num_topics"]
    extra_params = [key for key in request.query_params if key not in allowed_params]

    if extra_params:
        raise HTTPException(status_code=404, detail="Unexpected query parameter")
    
    if num_topics == None:
        raise HTTPException(status_code=422, detail="Number of topics value not specified")

    LDAvis_data_filepath = os.path.join('./LDA_visual_Latest/ldavis_prepared_'+str(num_topics))

    with open(LDAvis_data_filepath, 'rb') as f:
        vis_data = pickle.load(f)
    
    html_path = "lda_vis.html"
    pyLDAvis.save_html(vis_data, html_path)
    
    return FileResponse(html_path, media_type='text/html', filename="lda_vis.html")

