import pandas as pd
from fastapi import APIRouter
from fastapi import Query, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Annotated

router = APIRouter(prefix="/demo")


@router.get("/pandas")
def demo_pandas():
    data = {
        "name": ["Alice", "Bob", "Charlie"],
        "age": [25, 30, 35],
        "city": ["New York", "Los Angeles", "Chicago"],
    }
    df = pd.DataFrame(data)
    return {
        "message": "Pandas DataFrame created successfully!",
        "data": df.to_dict(orient="records"),
    }


@router.get("/data-frame-test")
def demo_data_frame_test():
    df = pd.DataFrame({"Name": ["John", "John", "Amy", "Amy"]})
    return {
        "message": "DataFrame example",
        "data": df.to_dict(orient="records"),
    }


@router.get("/data-frame-group-by")
def demo_data_frame_group_by():
    df = pd.DataFrame(
        {
            "Name": ["John", "John", "Amy", "Amy"],
            "State": ["NY", "NY", "CA", "CA"],
            "Category": ["A", "B", "A", "B"],
            "Sales": [100, 200, 300, 400],
            "Profit": [10, 20, 30, 40],
        }
    )

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    result_all = df.groupby(["Name", "State"]).sum().reset_index()
    result_numeric = df.groupby(["Name", "State"])[numeric_cols].sum().reset_index()
    return {
        "result_all": result_all.to_dict(orient="records"),
        "result_numeric": result_numeric.to_dict(orient="records"),
    }


@router.get("/query")
def demo_query(
    name: str = Query(
        default="John", min_length=1, max_length=50, description="Name of the person"
    ),
    age: int = Query(default=30, ge=0, le=120, description="Age of the person"),
):
    return {
        "message": "Query parameters received successfully!",
        "name": name,
        "age": age,
    }


@router.get("/validation")
def demo_validation(
    name: str = Query(
        default="John", min_length=1, max_length=50, description="Name of the person"
    ),
    age: int = Query(default=30, ge=0, le=120, description="Age of the person"),
):
    return {
        "message": "Validation successful!",
        "name": name,
        "age": age,
    }


@router.get("/error")
def demo_error():
    raise HTTPException(status_code=400, detail="This is a demo error")


class CreateItem(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Name of the item")
    price: float = Field(..., gt=0, description="Price of the item")


@router.post("/items")
def create_item(item: CreateItem):
    return {
        "message": "Item created successfully!",
        "item": item.model_dump(),
    }


@router.post("/items/validation")
def create_item_validation(item: CreateItem):
    return {
        "message": "Item created successfully with validation!",
        "item": item.model_dump(),
    }


@router.get("/skills")
def list_skills():
    return [
        {
            "name": "Python",
            "description": "A versatile programming language.",
            "demand": "high",
            "founded": 1991,
        },
        {
            "name": "JavaScript",
            "description": "The language of the web.",
            "demand": "high",
            "founded": 1995,
        },
        {
            "name": "Java",
            "description": "A widely-used programming language.",
            "demand": "medium",
            "founded": 1995,
        },
        {
            "name": "C#",
            "description": "A language developed by Microsoft.",
            "demand": "medium",
            "founded": 2000,
        },
        {
            "name": "Go",
            "description": "A statically typed language from Google.",
            "demand": "rising",
            "founded": 2009,
        },
    ]


@router.get("/skills/search")
def search_skills(
    name: str = Query(default=None, description="Name of the skill to search for"),
    demand: str = Query(
        default=None, description="Filter by demand level (e.g., high, medium, low)"
    ),
    order: str = Query(
        default="asc", description="Order by founded year (asc or desc)"
    ),
    limit: int = Query(
        default=10, ge=1, description="Maximum number of results to return"
    ),
    offset: int = Query(
        default=0, ge=0, description="Number of results to skip before returning"
    ),
):
    skills = list_skills()

    if name:
        needle = name.strip().lower()
        skills = [s for s in skills if needle in s.get("name", "").lower()]
        if not skills:
            raise HTTPException(
                status_code=404, detail=f"No skill found matching name={name}"
            )

    if demand is not None:
        skills = [s for s in skills if s.get("demand") == demand]

    order_lower = (order or "").lower()
    if order_lower not in ("asc", "desc"):
        raise HTTPException(
            status_code=400, detail=f"Invalid order={order}. Must be 'asc' or 'desc'."
        )

    skills = sorted(
        skills, key=lambda s: s.get("founded", 0), reverse=(order_lower == "desc")
    )
    skills = skills[offset : offset + limit]

    return {
        "total": len(skills),
        "skills": skills,
        "order": order_lower,
        "demand": demand,
        "name": name,
        "offset": offset,
        "limit": limit,
    }


@router.get("/read-csv")
def read_csv():
    """
    Reads two CSV files (csv/1.csv and csv/2.csv) and returns:
    - result1: first row of csv/1.csv
    - result2: first row of csv/2.csv
    - has_difference: whether the first rows differ
    - difference_in_1_2: columns in csv/1.csv but not in csv/2.csv
    - difference_in_2_1: columns in csv/2.csv but not in csv/1.csv

    Expected output:
    {
        "result1": [{"Name": "Alice", "ID": 101, "Age": 25, "Score": 88.5, "State": "NY"}],
        "result2": [{"Name": "Alice", "Age": 25, "Score": 88.5}],
        "has_difference": true,
        "difference_in_1_2": ["ID", "State"],
        "difference_in_2_1": []
    }
    """
    df1 = pd.read_csv("csv/1.csv")
    df2 = pd.read_csv("csv/2.csv")

    return {
        "result1": df1.head(1).to_dict(orient="records"),
        "result2": df2.head(1).to_dict(orient="records"),
        "has_difference": df1.head(1).to_dict(orient="records")
        != df2.head(1).to_dict(orient="records"),
        "difference_in_1_2": df1.columns.difference(df2.columns).tolist(),
        "difference_in_2_1": df2.columns.difference(df1.columns).tolist(),
    }
