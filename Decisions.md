## V1 vs V2 — Evolution Log

### V1 (expense-tracker)
- **Database:** SQLite (file-based, built into Python)
- **Hosting:** Streamlit Cloud
- **Data isolation:** None — all users shared same database
- **Persistence:** Data lost on Streamlit Cloud restarts
- **Repo:** https://github.com/RahulMatai/expense-tracker

### V2 (expense-tracker-v2) — Current Submission
- **Database:** Supabase (PostgreSQL) — free tier
- **Hosting:** Streamlit Cloud
- **Data isolation:** Session-based UUID in URL — each user gets private data
- **Persistence:** Data persists forever via Supabase
- **Repo:** https://github.com/RahulMatai/expenses-tracker-v2

### Why V2 is better
- Real database — no data loss on restarts
- User isolation — sharing the app doesn't expose your data
- PostgreSQL — production ready, scalable
- Session ID in URL — bookmark and return to your data anytime

### What we would do with more time
- User authentication (login/signup)
- Edit expense feature
- CSV export
- Charts and spending trends
- Mobile responsive UI
- Pagination for large datasets