# Mutual Fund Facts Assistant

Facts-only FAQ chatbot for selected INDMoney mutual fund scheme pages.

## Scope
- Platform: INDMoney
- Data source type: Public INDMoney mutual fund scheme pages
- Included schemes: 6 direct growth schemes (including ELSS)
- Assistant behavior: factual scheme lookups only (no advice/recommendations)

## Project Files
- `app.py`: Streamlit UI
- `rag.py`: retrieval and response logic
- `prompts.py`: policy and keyword rules
- `data/funds.json`: structured source facts
- `data/funds.csv`: tabular source facts
- `sources.md`: list of URLs used
- `sample_qa.md`: sample questions and outputs

## Setup
1. Create and activate a virtual environment (optional but recommended).
2. Install dependencies:
   ```bash
   pip install streamlit
   ```
3. Run the app:
   ```bash
   streamlit run app.py
   ```

## Deploy on Render
1. Push this repository to GitHub (already done).
2. In Render Dashboard, create a new Blueprint and select this repo.
3. Render will detect `render.yaml` and create one web service.
4. Deploy and open the generated service URL.

## Architecture
1. **Data layer** (`data/funds.json`, `data/funds.csv`)
   - Stores factual fields per scheme:
     - fund name
     - AMC
     - category
     - expense ratio
     - exit load
     - minimum SIP
     - minimum lump sum
     - lock-in period
     - riskometer
     - benchmark index
     - last updated date
     - source URL
2. **Retrieval layer** (`rag.py`)
   - Keyword-based field detection.
   - Fund matching via aliases and token overlap.
   - Refuses investment advice/recommendation intents.
   - Handles mutual fund statement-download intent with one official INDMoney source.
3. **UI layer** (`app.py`)
   - Minimal Streamlit interface.
   - Displays answer text, exactly one source link, and last updated note.

## Guardrails
- No portfolio recommendations
- No buy/sell calls
- No return/performance comparisons
- No third-party sources
- No personal data collection

## Known Limitations
- Dataset is intentionally small and static (6 schemes).
- Facts are limited to what was extracted from listed INDMoney pages in March 2026.
- Name matching is rule-based and may miss unusual fund name variants.
- Statement-download response points to an official INDMoney educational page, not an in-app workflow.
