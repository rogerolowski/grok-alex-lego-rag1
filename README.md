# Grok-Alex-LEGO-RAG1

This repository contains a Retrieval-Augmented Generation (RAG) system for LEGO data, integrating APIs from Rebrickable, Brickset, and BrickOwl. The application uses LangChain with OpenAI GPT-4, ChromaDB for vector storage, and SQLite for persistence, with a Streamlit UI for querying. Deployed on Gitpod for easy development and testing.

## Launch on Gitpod

Click the button below to launch this project in Gitpod:

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/rogerolowski/grok-alex-lego-rag1)

## Prerequisites
- Gitpod account (free tier available at [gitpod.io](https://gitpod.io))
- API keys for:
  - OpenAI[](https://platform.openai.com/api-keys)
  - Rebrickable[](https://rebrickable.com/api/)
  - Brickset (https://brickset.com - request via registration)
  - BrickOwl (https://www.brickowl.com - account settings)

## Setup
1. Clone or open this repository in Gitpod using the launch link above.
2. Configure API keys in the `.env` file or Gitpod environment variables.
3. Run `python preload_db.py` to populate the database and build the ChromaDB index (may take time on first run).
4. The Streamlit app will automatically launch on port 8080 via `.gitpod.yml`.

## Usage
- Use the Streamlit UI to query LEGO set data from the integrated APIs.
- Debug output is available in the Gitpod terminal.

## Notes
- Initial database preload may take longer due to API fetches and ChromaDB indexing. Subsequent runs use persisted data.
- Monitor API rate limits (e.g., BrickOwl: 600 requests/min, Brickset: daily limit).
- Back up `lego_data.db` and `chroma_db` to avoid data loss on Gitpod's free tier.

## Files
- `app.py`: Main Streamlit application with RAG logic.
- `preload_db.py`: Script to preload database and ChromaDB.
- `.gitpod.yml`: Gitpod configuration.
- `.gitpod.Dockerfile`: Custom Docker image for Python 3.10.
- `requirements.txt`: Project dependencies.
- `.env`: API key configuration (add to `.gitignore`).
- `.gitignore`: Excludes temporary and sensitive files.

## Contributing
Feel free to fork and submit pull requests. Report issues via GitHub Issues.

## License
[MIT License](LICENSE) (add a `LICENSE` file if desired)