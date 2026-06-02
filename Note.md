
# fastapi run main.py
# uvicorn main:app --reload reload only in dev not prod
# alembic revision --autogenerate -m "message"
# alembic upgrade head
# pip freeze > ./requirements.txt
# pip install 'pwdlib[argon2]'
# pip install pyjwt
# pip install psycopg[binary]
# pip install 'pydantic[email]'
# pip install shutils
# pip install -r requirements.txt
# pip install python-multipart

# #!/bin/bash
# source myenv/bin/activate
# Your commands here
# deactivate

# alias activate='source myenv/bin/activate'
# alias deactivate='deactivate'

# The groupby().sum() returns a pandas DataFrame, which isn't JSON serializable. The fix calls .to_dict() on the result to make it serializable.
# Problem: df.groupby(["Name", "State"]).sum() returns a pandas DataFrame with a MultiIndex.
# FastAPI uses the jsonable_encoder to serialize responses,
# but pandas DataFrames aren't natively handled — the response fails because FastAPI can't convert a DataFrame to JSON

# numneric_only="True" → selects numeric columns explicitly with select_dtypes (avoids the deprecated/broken numeric_only parameter)
# result_numeric (raw DataFrame) → .to_dict(orient="records") so JSON serialization works
`
{
  "result_all": [
    {
      "Name": "Amy",
      "State": "CA",
      "Category": "AB",
      "Sales": 700,
      "Profit": 70
    },
    {
      "Name": "John",
      "State": "NY",
      "Category": "AB",
      "Sales": 300,
      "Profit": 30
    }
  ],
  "result_numeric": [
    {
      "Name": "Amy",
      "State": "CA",
      "Sales": 700,
      "Profit": 70
    },
    {
      "Name": "John",
      "State": "NY",
      "Sales": 300,
      "Profit": 30
    }
  ]
}`