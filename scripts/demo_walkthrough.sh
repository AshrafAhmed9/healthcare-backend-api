#!/bin/sh
# Runs a full walkthrough against the live Healthcare Backend API:
# register -> create doctor/patient -> assign -> query -> security checks.
set -e

BASE="${BASE_URL:-https://healthcare-backend-api-0y2l.onrender.com/api}"
EMAIL="${1:-demo.$(date +%s)@test.com}"
PASSWORD="StrongPass123!"

echo "== Using $BASE =="
echo

echo "--- 1. Register ($EMAIL) ---"
REGISTER=$(curl -s -X POST "$BASE/auth/register/" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$EMAIL\",\"name\":\"Demo User\",\"password\":\"$PASSWORD\"}")
echo "$REGISTER"
echo

TOKEN=$(echo "$REGISTER" | python3 -c "import json,sys; print(json.load(sys.stdin)['access'])")
AUTH="Authorization: Bearer $TOKEN"

echo "--- 2. Create doctor ---"
DOCTOR=$(curl -s -X POST "$BASE/doctors/" -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"name":"Dr Jane Doe","specialization":"CARDIOLOGY","email":"jane.doe.'"$(date +%s)"'@test.com","years_of_experience":7}')
echo "$DOCTOR"
echo
DOCTOR_ID=$(echo "$DOCTOR" | python3 -c "import json,sys; print(json.load(sys.stdin)['id'])")

echo "--- 3. Create patient ---"
PATIENT=$(curl -s -X POST "$BASE/patients/" -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"name":"Sam Patient","date_of_birth":"1992-06-15","gender":"M"}')
echo "$PATIENT"
echo
PATIENT_ID=$(echo "$PATIENT" | python3 -c "import json,sys; print(json.load(sys.stdin)['id'])")

echo "--- 4. Assign doctor $DOCTOR_ID to patient $PATIENT_ID ---"
curl -s -X POST "$BASE/mappings/" -H "$AUTH" -H "Content-Type: application/json" \
  -d "{\"patient\":$PATIENT_ID,\"doctor\":$DOCTOR_ID}"
echo
echo

echo "--- 5. Doctors assigned to patient $PATIENT_ID ---"
curl -s "$BASE/mappings/$PATIENT_ID/" -H "$AUTH"
echo
echo

echo "--- 6. List your patients ---"
curl -s "$BASE/patients/" -H "$AUTH"
echo
echo

echo "--- 7. Security check: no token -> expect 401 ---"
curl -s -o /dev/null -w "status: %{http_code}\n" "$BASE/patients/"
echo

echo "--- 8. Security check: register a second user, try to view patient $PATIENT_ID -> expect 404 ---"
OTHER_EMAIL="demo.other.$(date +%s)@test.com"
OTHER_REGISTER=$(curl -s -X POST "$BASE/auth/register/" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$OTHER_EMAIL\",\"name\":\"Other User\",\"password\":\"$PASSWORD\"}")
OTHER_TOKEN=$(echo "$OTHER_REGISTER" | python3 -c "import json,sys; print(json.load(sys.stdin)['access'])")
curl -s -o /dev/null -w "status: %{http_code}\n" "$BASE/patients/$PATIENT_ID/" -H "Authorization: Bearer $OTHER_TOKEN"

echo
echo "--- 9. Security check: second user tries to assign a doctor to patient $PATIENT_ID -> expect 400 ---"
curl -s -X POST "$BASE/mappings/" -H "Authorization: Bearer $OTHER_TOKEN" -H "Content-Type: application/json" \
  -d "{\"patient\":$PATIENT_ID,\"doctor\":$DOCTOR_ID}"
echo

echo
echo "== Done =="
