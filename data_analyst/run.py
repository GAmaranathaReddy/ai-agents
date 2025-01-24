import os
import sys

def main():
    os.system("streamlit run data_analyst/ai_data_analyst.py --server.port=8501 --server.address=0.0.0.0")

if __name__ == "__main__":
    sys.exit(main())
