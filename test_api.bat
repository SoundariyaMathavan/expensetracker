@echo off
echo Testing API endpoints...

echo.
echo Testing /api/summary with no category filter...
curl -s http://localhost:5000/api/summary | python -m json.tool

echo.
echo Testing /api/summary with category=Food...
curl -s http://localhost:5000/api/summary?category=Food | python -m json.tool

echo.
echo Testing /api/expenses with no category filter...
curl -s http://localhost:5000/api/expenses?period=monthly | python -m json.tool

echo.
echo Testing /api/expenses with category=Food...
curl -s http://localhost:5000/api/expenses?period=monthly^&category=Food | python -m json.tool

echo.
echo Testing complete.
pause