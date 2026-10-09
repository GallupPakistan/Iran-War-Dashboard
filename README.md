# Iran War Poll 2026 - Dashboard

Gallup Pakistan Digital Analytics. Iran War Poll 2026: 17 countries, 14,853 respondents.

This folder is self-contained. It needs no HuggingFace download and no token.

## Files
- `Survey_Overview.py` - main page (set this as the main file)
- `pages/` - 10 analysis pages
- `Iran_Snap_Poll_2026_-_Merged_Data_Working_File__17_Countries_.xlsx` - data (Armenia Q2 corrected, 9 Oct 2026)
- `EOY_IRAN_CODE_BOOK_APR26.csv` - codebook
- `GDAP_LOGO.png`, `GIA.png` - logos
- `requirements.txt` - Python libraries

## Run locally
```
pip install -r requirements.txt
streamlit run Survey_Overview.py
```

## Deploy on Streamlit Community Cloud
1. Upload everything in this folder to a GitHub repo, keeping the same structure.
2. On share.streamlit.io, create a new app, pick the repo, and set the main file to `Survey_Overview.py`.
3. Replace the dashboard link on the website with the new app link.

## Updating the data
Replace the Excel file with a new one of the same name, then reboot the app.

## Change log
- 9 Oct 2026: Armenia Q2 (side supported) answers were reversed. "Iran" and "USA-Israel coalition" were swapped back. Armenia now shows Iran 57.9% and USA-Israel 3.3%.
