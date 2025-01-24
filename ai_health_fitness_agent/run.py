import os
import sys

def main():
    os.system("streamlit run ai_health_fitness_agent/helath_fitness_agent.py  --server.port=8501 --server.address=0.0.0.0")

if __name__ == "__main__":
    sys.exit(main())
